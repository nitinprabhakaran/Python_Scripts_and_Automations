#!/usr/bin/env python3

import pexpect

hostname = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
os_flag = 0
multiprompt = r'.*[#|%|>|$|:].*'

child = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {user}@{hostname}.ampf.com')
child.timeout = 100
child.expect("assword")
child.sendline(password)
child.expect(multiprompt)
child.sendline("rm -rf /tmp/StorageReport/")
child.expect(multiprompt)
child.sendline("mkdir /tmp/StorageReport")
child.expect(multiprompt)

# Identify the OS
child.sendline("uname")
index = child.expect(["AIX", "Aix", "Linux", "LINUX"])
if index == 0 or index == 1:
    os_flag = 0
elif index == 2 or index == 3:
    os_flag = 1

child.sendline(f"rm -f /tmp/StorageReport/{hostname}.txt")
index = child.expect([".*"])
if index == 0:
    print("Removed the output file from host")

if os_flag == 0:
    child.sendline(f"echo {hostname} >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo OS:AIX >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo df -g >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline("df -g >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo for hdisk in command >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline("for hdisk in `lsdev -c disk | grep \"Available\" | awk '{print $1}'`; do printf \"%-10s %-12s %-15s\n\" $hdisk `getconf DISK_SIZE /dev/$hdisk` `lspv | grep \"^$hdisk \" | awk '{print $3}'`; done | awk '{total+=$2} {print} END{print \"------------------\\nTotal:     \" total-49152 \" MB (\" total/1024-48 \" GB)'}>>/tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo Running DB names command >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline("for dir in `ls /db | awk '{print $NF}'`; do echo Dir:$dir; for subdir in `sudo ls /db/$dir | grep -v 'lost+found' | grep -v 'log'`; do echo SubDir:/db/$dir/$subdir; echo Running df on /db/$dir/$subdir; df -m /db/$dir/$subdir; for dbname in `sudo ls /db/$dir/$subdir | awk '{print $NF}' | grep -v 'lost+found' | grep -v 'log'`; do echo DBName:$dbname; echo DBPath:/db/$dir/$subdir/$dbname; echo Running du on /db/$dir/$subdir/$dbname; sudo du -sm /db/$dir/$subdir/$dbname; done; done; done>>/tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo Running DB2 get db cfg command >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline("for dir in `ls /db | awk '{print $NF}'`; do echo Dir:$dir; for subdir in `sudo ls /db/$dir | grep -v 'lost+found' | grep -v 'log'`; do echo SubDir:/db/$dir/$subdir; echo Running DB2 get db cfg on /db/$dir/$subdir; sudo -u db2inst1 db2 list db directory | grep 'Database alias' | awk '{print $NF}' | xargs -I {} db2 get db cfg for {} | grep 'Database name\|Current storage path\|Log file path\|First active log file' | awk '{print}' ORS='\\n'; done; done>>/tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)

elif os_flag == 1:
    child.sendline(f"echo {hostname} >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo OS:Linux >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo df -h >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline("df -h >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo lvs --units g >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline("lvs --units g >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo Running DB names command >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline("for dir in `ls /db`; do echo Dir:$dir; for subdir in `sudo ls /db/$dir | grep -v 'lost+found' | grep -v 'log'`; do echo SubDir:/db/$dir/$subdir; echo Running df on /db/$dir/$subdir; df -h /db/$dir/$subdir; for dbname in `sudo ls /db/$dir/$subdir | awk '{print $NF}' | grep -v 'lost+found' | grep -v 'log'`; do echo DBName:$dbname; echo DBPath:/db/$dir/$subdir/$dbname; echo Running du on /db/$dir/$subdir/$dbname; sudo du -sh /db/$dir/$subdir/$dbname; done; done; done>>/tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline(f"echo Running MySQL DB names command >> /tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)
    child.sendline("for dir in `ls /var/lib/mysql`; do echo Dir:$dir; for subdir in `sudo ls /var/lib/mysql/$dir | grep -v 'lost+found' | grep -v 'log'`; do echo SubDir:/var/lib/mysql/$dir/$subdir; echo Running du on /var/lib/mysql/$dir/$subdir; sudo du -sh /var/lib/mysql/$dir/$subdir; done; done>>/tmp/StorageReport/{hostname}.txt")
    child.expect(multiprompt)

child.sendline("exit")
child.close()
