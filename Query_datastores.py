#!/bin/bash

# Function to increment IP address
increment_ip() {
    local IFS=.
    local ip=($1)
    ip[3]=$((ip[3]+2))

    for i in {3..0}; do
        if [ ${ip[i]} -ge 256 ]; then
            ip[i]=0
            if [ $i -gt 0 ]; then
                ip[$((i-1))]=$((ip[$((i-1))]+1))
            fi
        fi
    done

    echo "${ip[0]}.${ip[1]}.${ip[2]}.${ip[3]}"
}

# Check if an IP address is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <IP_ADDRESS>"
    exit 1
fi

# Increment the provided IP address
new_ip=$(increment_ip $1)

# Output the new IP address
echo "New IP Address: $new_ip"

# Check if the new IP is reachable on port 53
if nc -z -w 3 "$new_ip" 53; then
    echo "$new_ip is reachable on port 53."

    # Backup the original /etc/resolv.conf
    sudo cp /etc/resolv.conf /etc/resolv.conf.bak

    # Replace nameserver in /etc/resolv.conf with the new IP
    sudo sed -i '/^nameserver /d' /etc/resolv.conf
    echo "nameserver $new_ip" | sudo tee -a /etc/resolv.conf

    echo "Updated /etc/resolv.conf with new nameserver $new_ip."
else
    echo "$new_ip is not reachable on port 53."
fi