import pexpect

def generate_storage_report(hostname, username, password):
    os_flag = 0

    # Spawn SSH session
    ssh_command = f"ssh -o StrictHostKeyChecking=no {username}@{hostname}"
    ssh_session = pexpect.spawn(ssh_command)

    ssh_session.expect("assword")
    ssh_session.sendline(password)

    # Check OS type
    index = ssh_session.expect(["AIX", "Aix", "Linux", "LINUX"])
    if index in [0, 1]:
        os_flag = 0
    elif index in [2, 3]:
        os_flag = 1

    # Send commands based on OS type
    if os_flag == 0:  # AIX
        ssh_session.sendline(f"echo {hostname} >> /tmp/StorageReport/{hostname}.txt")
        ssh_session.expect("#|%|>|$|:")

        ssh_session.sendline("echo OS:AIX >> /tmp/StorageReport/{hostname}.txt")
        ssh_session.expect("#|%|>|$|:")

        ssh_session.sendline("echo df -g >> /tmp/StorageReport/{hostname}.txt")
        ssh_session.expect("#|%|>|$|:")

        ssh_session.sendline("df -g >> /tmp/StorageReport/{hostname}.txt")
        ssh_session.expect("#|%|>|$|:")
        
        # ... continue with the rest of the commands for AIX

    else:  # Linux
        ssh_session.sendline(f"echo {hostname} >> /tmp/StorageReport/{hostname}.txt")
        ssh_session.expect("#|%|>|$|:")

        ssh_session.sendline("echo OS:LINUX >> /tmp/StorageReport/{hostname}.txt")
        ssh_session.expect("#|%|>|$|:")

        ssh_session.sendline("echo df -Bm >> /tmp/StorageReport/{hostname}.txt")
        ssh_session.expect("#|%|>|$|:")

        ssh_session.sendline("df -Bm | grep -v /amp/tools >> /tmp/StorageReport/{hostname}.txt")
        ssh_session.expect("#|%|>|$|:")

        # ... continue with the rest of the commands for Linux

    ssh_session.sendline("exit")
    ssh_session.expect(pexpect.EOF)

    # Close the SSH session
    ssh_session.close()

# Example usage
hostname = "example.com"
username = "your_username"
password = "your_password"

generate_storage_report(hostname, username, password)
