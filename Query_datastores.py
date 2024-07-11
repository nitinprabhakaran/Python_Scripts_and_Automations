---
- name: Check if a given mountpoint is mounted and retrieve mount options
  hosts: all
  become: yes
  vars:
    mountpoint: "/your/mountpoint"  # Specify the mountpoint to check

  tasks:
    - name: Gather facts
      setup:
        gather_subset:
          - hardware
          - network
          - mounts

    - name: Check if the mountpoint is mounted
      set_fact:
        is_mounted: "{{ ansible_mounts | selectattr('mount', 'equalto', mountpoint) | list | length > 0 }}"

    - name: Extract mount options if mounted
      set_fact:
        mount_options: "{{ (ansible_mounts | selectattr('mount', 'equalto', mountpoint) | list)[0].options }}"
      when: is_mounted

    - name: Print mount status
      debug:
        msg: "Mountpoint {{ mountpoint }} is mounted: {{ is_mounted }}"

    - name: Print mount options
      debug:
        msg: "Mount options for {{ mountpoint }}: {{ mount_options }}"
      when: is_mounted