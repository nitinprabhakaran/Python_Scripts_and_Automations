---
- name: Copy tags from root EBS drive to newly attached EBS volume
  hosts: localhost
  gather_facts: false
  vars:
    instance_id: "i-xxxxxxxxxxxxxxxxx" # Replace with your EC2 instance ID
    new_volume_size: 5  # Size of the new EBS volume in GB
    region: "us-west-2"  # Replace with your AWS region

  tasks:
    - name: Gather information about the instance
      ec2_instance_info:
        region: "{{ region }}"
        instance_ids:
          - "{{ instance_id }}"
      register: instance_info

    - name: Ensure instance information was retrieved
      fail:
        msg: "Failed to retrieve instance information."
      when: instance_info.instances | length == 0

    - name: Get the root EBS volume ID
      set_fact:
        root_volume_id: "{{ instance_info.instances[0].block_device_mapping | selectattr('device_name', '==', instance_info.instances[0].root_device_name) | map(attribute='ebs.volume_id') | first }}"

    - name: Gather tags from the root EBS volume
      ec2_tag_info:
        region: "{{ region }}"
        filters:
          resource-id: "{{ root_volume_id }}"
      register: root_volume_tags

    - name: Create a new EBS volume
      ec2_vol:
        region: "{{ region }}"
        size: "{{ new_volume_size }}"
        availability_zone: "{{ instance_info.instances[0].placement.availability_zone }}"
        state: present
      register: new_volume

    - name: Attach the new EBS volume to the instance
      ec2_vol:
        region: "{{ region }}"
        volume_id: "{{ new_volume.volume_id }}"
        instance: "{{ instance_id }}"
        device_name: "/dev/sdf"  # You might need to adjust this based on your instance type and OS

    - name: Apply tags from the root EBS volume to the new EBS volume
      ec2_tag:
        region: "{{ region }}"
        resource: "{{ new_volume.volume_id }}"
        state: present
        tags: "{{ root_volume_tags.tags }}"



---
- name: Dynamically generate variable names in Ansible
  hosts: localhost
  gather_facts: false
  vars:
    items:
      - name: item1
        value: "This is the first item"
      - name: item2
        value: "This is the second item"
      - name: item3
        value: "This is the third item"

  tasks:
    - name: Process each item
      loop: "{{ items }}"
      vars:
        dynamic_var_name: "result_{{ item.name }}"
      block:
        - name: Simulate a task and register the result
          command: "echo {{ item.value }}"
          register: task_result

        - name: Set dynamic fact
          set_fact:
            "{{ dynamic_var_name }}": "{{ task_result.stdout }}"

    - name: Debug dynamic variables
      debug:
        msg: "Result for {{ item.name }} is: {{ hostvars[inventory_hostname][dynamic_var_name] }}"
      loop: "{{ items }}"
      vars:
        dynamic_var_name: "result_{{ item.name }}"