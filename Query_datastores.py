---
- name: Modify GRUB_CMDLINE_LINUX in /etc/default/grub
  hosts: your_server
  become: true
  vars:
    grub_options: "your_new_options"  # Specify the options you want to add or modify
  tasks:
    - name: Backup /etc/default/grub file
      copy:
        src: /etc/default/grub
        dest: /etc/default/grub.bak
        remote_src: yes

    - name: Ensure GRUB_CMDLINE_LINUX is present in /etc/default/grub
      lineinfile:
        path: /etc/default/grub
        insertafter: EOF
        line: 'GRUB_CMDLINE_LINUX=""'
      when: '"GRUB_CMDLINE_LINUX" not in lookup("file", "/etc/default/grub")'

    - name: Modify GRUB_CMDLINE_LINUX entry
      lineinfile:
        path: /etc/default/grub
        regexp: '^GRUB_CMDLINE_LINUX="(.*)"'
        line: 'GRUB_CMDLINE_LINUX="\1 {{ grub_options }}"'
        backrefs: yes

    - name: Update grub configuration
      command: grub2-mkconfig -o /boot/grub2/grub.cfg
      when: ansible_facts['distribution'] in ['CentOS', 'RedHat', 'Amazon']

    - name: Update grub configuration for Debian-based systems
      command: update-grub
      when: ansible_facts['distribution'] in ['Debian', 'Ubuntu']