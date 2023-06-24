import pexpect

def execute_expect_script(hostname, user, password):
    # SSH to the remote host
    ssh_command = f"ssh -o StrictHostKeyChecking=no {user}@{hostname}"
    ssh_session = pexpect.spawn(ssh_command)

    # Set the timeout and prompt pattern
    ssh_session.timeout = 200
    prompt_pattern = r".*[#|%|>|$|:].*"

    # Match password prompt and send password
    ssh_session.expect("assword")
    ssh_session.sendline(password)

    # Create the StorageReport directory
    ssh_session.expect(prompt_pattern)
    ssh_session.sendline("rm -rf /tmp/StorageReport/")
    ssh_session.expect(prompt_pattern)
    ssh_session.sendline("mkdir /tmp/StorageReport/")
    ssh_session.expect(prompt_pattern)

    # Identify the OS
    ssh_session.sendline("uname")
    index = ssh_session.expect(["AIX", "Aix", "Linux", "LINUX"])
    os_flag = 0 if index < 2 else 1

    # Common functions
    def send_command_and_wait(command):
        ssh_session.sendline(command)
        ssh_session.expect(prompt_pattern)

    def append_to_report(content):
        send_command_and_wait(f'echo "{content}" >> /tmp/StorageReport/{hostname}.txt')

    # Execute commands based on the OS
    if os_flag == 0:  # AIX
        append_to_report(hostname)
        append_to_report("OS:AIX")
        send_command_and_wait("df -g")
        send_command_and_wait("for hdisk in `lsdev -c disk | grep 'Available' | awk '{print $1}'`; do printf '%-10s %-12s %-15s\\n' $hdisk `getconf DISK_SIZE /dev/$hdisk` `lspv | grep \"^$hdisk \" | awk '{print $3}'`; done | awk '{total+=$2} {print} END{print \"------------------\\nTotal:     \" total-49152 \" MB (\" total/1024-48 \" GB)'}'")
        send_command_and_wait("lspv")
        send_command_and_wait("lsdev -c disk")
        send_command_and_wait("lspv | awk '{print $1}'")
        lspv_det = ssh_session.before.decode()
        for line in lspv_det.splitlines():
            line = line.strip()
            if line.startswith("hdisk"):
                send_command_and_wait(f"echo lspv {line}")
                send_command_and_wait(f"lspv {line}")
                send_command_and_wait(f"echo lspv -l {line}")
                send_command_and_wait(f"lspv -l {line}")
                send_command_and_wait(f"echo lscfg -vpl {line} with egrep hdisk pipe Serial")
                send_command_and_wait(f"lscfg -vpl {line} | egrep 'hdisk|Serial'")
        send_command_and_wait("lsvg")
        lsvg_det = ssh_session.before.decode()
        for line1 in lsvg_det.splitlines():
            line1 = line1.strip()
            if line1.isalnum():
                send_command_and_wait(f"echo lscfg {line1}")
                send_command_and_wait(f"lsvg {line1}")
                send_command_and_wait(f"echo lsvg -l {line1} | awk '{{print}}' | tail -n 3")
                send_command_and_wait(f"lsvg -l {line1} | awk '{{print $7}}' | tail -n 3")

    elif os_flag == 1:  # Linux
        append_to_report(hostname)
        append_to_report("OS:Linux")
        send_command_and_wait("df -Bm")
        send_command_and_wait("multipathd -k show status")
        send_command_and_wait("ls -l /dev/sd*")
        send_command_and_wait("ls -l /dev/disk/by-id/")
        send_command_and_wait("ls -l /dev/disk/by-path/")
        send_command_and_wait("fdisk -l")
        send_command_and_wait("ls -l /dev/mapper/*")
        send_command_and_wait("ls -l /dev/mapper/mpath*")

    # Veritas Cluster Server (VCS) configuration
    send_command_and_wait("hastatus")
    send_command_and_wait("vxdisk list")
    send_command_and_wait("vxprint -ht")
    send_command_and_wait("vxprint -ght")

    # Logout from the SSH session
    ssh_session.sendline("exit")
    ssh_session.close()


# Example usage
hostname = "remote.example.com"
user = "username"
password = "password"

execute_expect_script(hostname, user, password)
