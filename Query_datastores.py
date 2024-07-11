#!/bin/bash

# Run the yum repolist all command and capture its output
output=$(yum repolist all 2>/dev/null)

# Print the header
echo -e "Repo ID\t\t\tRepo Name\t\t\t\t\tStatus"

# Parse the output and print the required information
echo "$output" | awk '
BEGIN {found=0}
/^repo id/ {found=1; next}
found {
    # Split the line into an array of fields
    split($0, fields)
    repo_id = fields[1]
    # Status is the last field
    status = fields[length(fields)]
    # Repository name is everything between the repo_id and status
    repo_name_start = index($0, repo_id) + length(repo_id) + 1
    repo_name_end = length($0) - length(status) - 1
    repo_name = substr($0, repo_name_start, repo_name_end - repo_name_start + 1)
    # Check if repo_name contains "Red Hat" or "RHUI"
    if (index(repo_name, "Red Hat") == 0 && index(repo_name, "RHUI") == 0) {
        printf "%-20s%-50s%s\n", repo_id, repo_name, status
    }
}'