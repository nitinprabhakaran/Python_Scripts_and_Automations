---
- name: Check EBS volume status
  hosts: localhost
  gather_facts: false
  vars:
    aws_region: "us-west-2"  # Replace with your AWS region
    ebs_volume_id: "vol-xxxxxxxxxxxxxxxxx"  # Replace with your EBS volume ID

  tasks:
    - name: Check EBS volume state and attachment
      ec2_vol_info:
        region: "{{ aws_region }}"
        volume_ids: "{{ ebs_volume_id }}"
      register: volume_info

    - name: Ensure the volume information was retrieved
      fail:
        msg: "Failed to retrieve volume information."
      when: volume_info.volumes | length == 0

    - name: Check if the volume is attached
      set_fact:
        is_attached: "{{ volume_info.volumes[0].attachments | length > 0 }}"

    - name: Check if the volume is available
      set_fact:
        is_available: "{{ volume_info.volumes[0].state == 'available' }}"

    - name: Print volume status
      debug:
        msg: >
          Volume {{ ebs_volume_id }} is
          {% if is_attached %}
            attached
          {% else %}
            not attached
          {% endif %}
          and is
          {% if is_available %}
            available
          {% else %}
            not available
          {% endif %}.