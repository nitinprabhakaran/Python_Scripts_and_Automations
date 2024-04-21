---
- name: Group instances by account number and region
  hosts: localhost
  gather_facts: false
  vars:
    csv_file_path: "/path/to/your/csv/file.csv"
  tasks:
    - name: Read CSV file
      read_csv:
        path: "{{ csv_file_path }}"
      register: csv_data

    - name: Initialize dictionary for grouped instances
      set_fact:
        instances_grouped_by_account_and_region: {}

    - name: Loop through CSV data and group instances
      set_fact:
        instances_grouped_by_account_and_region: "{{ instances_grouped_by_account_and_region | combine({ item.0.account_number: (instances_grouped_by_account_and_region[item.0.account_number] | default({})) | combine({ item.0.region: (instances_grouped_by_account_and_region[item.0.account_number][item.0.region] | default([]) + [item.0]) }) }) }}"
      loop: "{{ csv_data.list }}"