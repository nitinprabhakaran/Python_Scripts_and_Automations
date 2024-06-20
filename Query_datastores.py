---
- name: Ensure EC2 instance is stopped, attach the specified security group, and remove EBS volumes
  hosts: localhost
  gather_facts: false
  vars:
    instance_id: "i-0abcd1234efgh5678"  # Replace with your instance ID
    region: "us-east-1"  # Replace with your AWS region
    aws_access_key: "YOUR_AWS_ACCESS_KEY"  # Replace with your AWS access key
    aws_secret_key: "YOUR_AWS_SECRET_KEY"  # Replace with your AWS secret key
    security_group_name: "my-security-group"  # Replace with your security group name tag

  tasks:
    - name: Check the current state of the EC2 instance
      ec2_instance_info:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: "{{ region }}"
        instance_ids:
          - "{{ instance_id }}"
      register: ec2_info

    - name: Set instance_state variable
      set_fact:
        instance_state: "{{ ec2_info.instances[0].state.name }}"
        instance_ebs_volumes: "{{ ec2_info.instances[0].block_device_mapping | map(attribute='ebs.volume_id') | list }}"

    - name: Stop the EC2 instance if it is not stopped
      ec2:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: "{{ region }}"
        instance_ids:
          - "{{ instance_id }}"
        state: stopped
      when: instance_state != "stopped"

    - name: Wait for the instance to stop
      ec2_instance:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: "{{ region }}"
        instance_id: "{{ instance_id }}"
        state: stopped
        wait: yes

    - name: Get all security groups
      ec2_group_facts:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: "{{ region }}"
      register: security_groups

    - name: Find the security group ID by name tag
      set_fact:
        security_group_id: "{{ item.group_id }}"
      loop: "{{ security_groups.security_groups }}"
      when: item.tags.Name == security_group_name
      register: matched_security_group

    - name: Ensure the instance has the specified security group attached
      ec2_instance:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: "{{ region }}"
        instance_id: "{{ instance_id }}"
        groups: "{{ instance_security_groups | map(attribute='group_id') | list + [security_group_id] }}"
      when: matched_security_group is defined

    - name: Debug the result
      debug:
        msg: "Security group '{{ security_group_name }}' (ID: {{ security_group_id }}) is attached to the instance {{ instance_id }}."

    - name: Detach and delete EBS volumes attached to the instance
      block:
        - name: Detach EBS volumes
          ec2_vol:
            aws_access_key: "{{ aws_access_key }}"
            aws_secret_key: "{{ aws_secret_key }}"
            region: "{{ region }}"
            volume_id: "{{ item }}"
            state: absent
            instance: "{{ instance_id }}"
            wait: yes
          loop: "{{ instance_ebs_volumes }}"
          register: detach_results

        - name: Delete EBS volumes
          ec2_vol:
            aws_access_key: "{{ aws_access_key }}"
            aws_secret_key: "{{ aws_secret_key }}"
            region: "{{ region }}"
            volume_id: "{{ item }}"
            state: absent
            delete_on_termination: yes
            wait: yes
          loop: "{{ instance_ebs_volumes }}"
          when: item in detach_results.results | map(attribute='volume_id') | list
          
  vars:
    instance_security_groups: "{{ ec2_info.instances[0].security_groups }}"