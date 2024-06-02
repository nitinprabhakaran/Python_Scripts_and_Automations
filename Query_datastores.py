---
- name: Check disk space and manage fstab
  hosts: all
  become: true
  gather_facts: true
  vars:
    threshold: 80
    mountpoints_to_hash: 
      - "/mnt/data1"
      - "/mnt/data2"

  tasks:
    - name: Get disk usage information
      command: df -h --output=pcent,target
      register: disk_usage
      changed_when: false

    - name: Parse disk usage information
      set_fact:
        defaulters: "{{ defaulters | default([]) + [item.split()[1]] }}"
      when: item.split()[0] | regex_replace('%','') | int > threshold
      loop: "{{ disk_usage.stdout_lines[1:] }}"

    - name: Display defaulters
      debug:
        msg: "Mount points exceeding {{ threshold }}% usage: {{ defaulters }}"

    - name: Backup /etc/fstab
      copy:
        src: /etc/fstab
        dest: /etc/fstab.bak
        remote_src: yes

    - name: Comment out specified mount points in /etc/fstab
      lineinfile:
        path: /etc/fstab
        regexp: "^(.*{{ item }}.*)"
        line: "# \\1"
        state: present
        backrefs: yes
      loop: "{{ mountpoints_to_hash }}"
      notify: Restart NFS if needed

  handlers:
    - name: Restart NFS if needed
      service:
        name: nfs
        state: restarted
      when: mountpoints_to_hash | length > 0