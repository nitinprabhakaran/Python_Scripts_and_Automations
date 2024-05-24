---
- name: Attach and configure new EBS volume
  hosts: localhost
  gather_facts: false
  vars:
    ec2_instance_id: "i-xxxxxxxxxxxxxx"  # Replace with your EC2 instance ID
    aws_region: "us-west-2"  # Replace with your AWS region
    ebs_volume_size: 5  # Size in GB
    device_name: "/dev/xvdf"  # The device name where the EBS volume will be attached

  tasks:
    - name: Create a new EBS volume
      ec2_vol:
        region: "{{ aws_region }}"
        instance: "{{ ec2_instance_id }}"
        volume_size: "{{ ebs_volume_size }}"
        device_name: "{{ device_name }}"
      register: ebs_volume

    - name: Wait for the volume to become available
      ec2_vol:
        region: "{{ aws_region }}"
        volume_id: "{{ ebs_volume.volume_id }}"
        state: present
        wait: yes
        wait_timeout: 600

- name: Configure new EBS volume on the EC2 instance
  hosts: your_ec2_instance  # Replace with your actual EC2 instance hostname or IP
  become: true
  tasks:
    - name: Rescan the SCSI bus
      shell: echo "- - -" > /sys/class/scsi_host/host0/scan

    - name: Wait for the new disk to be available
      wait_for:
        path: "{{ device_name }}"
        state: present
        timeout: 300

    - name: Create a physical volume on the new disk
      lvg:
        vg: vg01
        pvs: "{{ device_name }}"

    - name: Get the root volume group name
      command: vgs --noheadings -o vg_name
      register: vg_name_output

    - name: Set the root volume group name
      set_fact:
        root_vg_name: "{{ vg_name_output.stdout | trim }}"

    - name: Extend the root volume group with the new physical volume
      command: vgextend {{ root_vg_name }} {{ device_name }}

    - name: Create a logical volume of 5 GB
      lvol:
        vg: "{{ root_vg_name }}"
        lv: lv_home
        size: 5g

    - name: Format the new logical volume with xfs
      filesystem:
        fstype: xfs
        dev: "/dev/{{ root_vg_name }}/lv_home"

    - name: Create /home directory if it doesn't exist
      file:
        path: /home
        state: directory

    - name: Mount the new logical volume to /home
      mount:
        path: /home
        src: "/dev/{{ root_vg_name }}/lv_home"
        fstype: xfs
        state: mounted

    - name: Ensure the new logical volume is mounted at boot
      mount:
        path: /home
        src: "/dev/{{ root_vg_name }}/lv_home"
        fstype: xfs
        opts: defaults
        state: present