import re
from collections import defaultdict

# Variables
host_name = ""
OS = ""
date = ""

Disk_VG = {}
LV_Disk = {}
LV_Size = {}
LV_Identifier = {}

Disk_Status = {}
Disk_Tier = {}
Disk_ID = {}
Disk_Stat = {}
Disk_Size = {}
Disk_Used_Size = {}
VG_Identifier = {}
VG_Size = {}

Unassigned_Disks = {}
Lun_Id = {}

Dark_Lun_ID = {}
Dark_Lun_Size = {}
Dark_Lun_DG = {}
Dark_Lun_Utilization = {}

Veritas_Lun = {}
Veritas_Disk = {}
Veritas_Disk_Size = {}
Veritas_VG = {}

LV_PV = defaultdict(list)
MP = {}
MP_Size = {}

nas_volumes = []

Veritas_Vols = []

# Functions
def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("Filename:"):
            continue
        elif line.startswith("Part 1"):
            continue
        elif line.startswith("Part 2"):
            continue
        elif line.startswith("Part 3"):
            continue
        elif line.startswith("HostName"):
            host_name, OS, date = line.split("\t")
        elif line.startswith("Disk(s) without any VG tagged"):
            process_unassigned_disks(lines)
        elif line.startswith("HostName\tDisk"):
            process_disk_vg_lines(lines)
        elif line.startswith("NAS Volumes under"):
            process_nas_volume_lines(lines)
        elif line.startswith("Veritas Volume Report"):
            process_veritas_volume_lines(lines)
        elif line.startswith("PhysicalVolume"):
            process_logical_volume_lines(lines)

def process_unassigned_disks(lines):
    for line in lines:
        line = line.strip()
        
        if line.startswith("Disk(s) without any VG tagged"):
            continue
        elif line == "":
            break
        
        disk, size = line.split(": ")
        Unassigned_Disks[disk] = size

def process_disk_vg_lines(lines):
    for line in lines:
        line = line.strip()
        
        if line.startswith("HostName\tDisk"):
            continue
        elif line == "":
            break
        
        fields = line.split("\t")
        disk = fields[1]
        vg = fields[9]
        Disk_VG[disk] = vg

def process_nas_volume_lines(lines):
    for line in lines:
        line = line.strip()
        
        if line.startswith("NAS Volumes under"):
            continue
        elif line == "":
            break
        
        vol, size, used_size, avail_size, _, mount_point = line.split("\t")
        nas_volumes.append((vol, size, used_size, avail_size, mount_point))

def process_veritas_volume_lines(lines):
    for line in lines:
        line = line.strip()
        
        if line.startswith("Veritas Volume Report"):
            continue
        elif line == "":
            break
        
        vol = line.split("\t")[0]
        Veritas_Vols.append(vol)

def process_logical_volume_lines(lines):
    for line in lines:
        line = line.strip()
        
        if line.startswith("HostName\tVG_Identifier"):
            continue
        elif line == "":
            break
        
        fields = line.split("\t")
        vg_identifier = fields[1]
        disk = fields[2]
        lv = fields[4]
        lv_identifier = fields[5]
        lv_size = fields[6]
        mp = fields[9]
        mp_size = fields[10]
        
        LV_Disk[lv] = disk
        LV_Size[lv] = lv_size
        LV_Identifier[lv] = lv_identifier
        VG_Identifier[lv] = vg_identifier
        LV_PV[lv].append(disk)
        MP[mp] = lv
        MP_Size[mp] = mp_size

def process_disk_status(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DiskStatus DiskName"):
            continue
        elif line.startswith("DiskStatus"):
            continue
        elif line == "":
            break
        
        disk, status = line.split("\t")
        Disk_Status[disk] = status

def process_disk_tier(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DiskTier DiskName"):
            continue
        elif line.startswith("DiskTier"):
            continue
        elif line == "":
            break
        
        disk, tier = line.split("\t")
        Disk_Tier[disk] = tier

def process_disk_id(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DiskID DiskName"):
            continue
        elif line.startswith("DiskID"):
            continue
        elif line == "":
            break
        
        disk, disk_id = line.split("\t")
        Disk_ID[disk] = disk_id

def process_disk_stat(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DiskStat DiskName"):
            continue
        elif line.startswith("DiskStat"):
            continue
        elif line == "":
            break
        
        disk, stat = line.split("\t")
        Disk_Stat[disk] = stat

def process_disk_size(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DiskSize DiskName"):
            continue
        elif line.startswith("DiskSize"):
            continue
        elif line == "":
            break
        
        disk, size = line.split("\t")
        Disk_Size[disk] = size

def process_disk_used_size(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DiskUsedSize DiskName"):
            continue
        elif line.startswith("DiskUsedSize"):
            continue
        elif line == "":
            break
        
        disk, used_size = line.split("\t")
        Disk_Used_Size[disk] = used_size

def process_vg_size(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("VGSize VG_Identifier"):
            continue
        elif line.startswith("VGSize"):
            continue
        elif line == "":
            break
        
        vg, size = line.split("\t")
        VG_Size[vg] = size

def process_lun_id(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("LunID DiskName"):
            continue
        elif line.startswith("LunID"):
            continue
        elif line == "":
            break
        
        disk, lun_id = line.split("\t")
        Lun_Id[disk] = lun_id

def process_dark_lun_id(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DarkLunID DarkLun"):
            continue
        elif line.startswith("DarkLunID"):
            continue
        elif line == "":
            break
        
        dark_lun, lun_id = line.split("\t")
        Dark_Lun_ID[dark_lun] = lun_id

def process_dark_lun_size(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DarkLunSize DarkLun"):
            continue
        elif line.startswith("DarkLunSize"):
            continue
        elif line == "":
            break
        
        dark_lun, size = line.split("\t")
        Dark_Lun_Size[dark_lun] = size

def process_dark_lun_dg(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DarkLunDG DarkLun"):
            continue
        elif line.startswith("DarkLunDG"):
            continue
        elif line == "":
            break
        
        dark_lun, dg = line.split("\t")
        Dark_Lun_DG[dark_lun] = dg

def process_dark_lun_utilization(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DarkLunUtilization DarkLun"):
            continue
        elif line.startswith("DarkLunUtilization"):
            continue
        elif line == "":
            break
        
        dark_lun, utilization = line.split("\t")
        Dark_Lun_Utilization[dark_lun] = utilization

def process_veritas_disk(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        
        if not line.startswith("Disk") or line.startswith("Disk DiskName"):
            continue
        elif line == "":
            break
        
        fields = line.split("\t")
        disk = fields[1]
        veritas_disk = fields[2]
        veritas_disk_size = fields[3]
        veritas_vg = fields[6]
        
        Veritas_Disk[disk] = veritas_disk
        Veritas_Disk_Size[disk] = veritas_disk_size
        Veritas_VG[disk] = veritas_vg

def optimize_data_structures():
    global Unassigned_Disks, nas_volumes, Veritas_Vols
    
    Unassigned_Disks = dict(sorted(Unassigned_Disks.items()))
    nas_volumes.sort(key=lambda x: x[0])
    Veritas_Vols.sort()

def main():
    # File paths
    file_path = "input.txt"
    disk_status_path = "diskstatus.txt"
    disk_tier_path = "disktier.txt"
    disk_id_path = "diskid.txt"
    disk_stat_path = "diskstat.txt"
    disk_size_path = "disksize.txt"
    disk_used_size_path = "diskusedsize.txt"
    vg_size_path = "vgsize.txt"
    lun_id_path = "lunid.txt"
    dark_lun_id_path = "darklunid.txt"
    dark_lun_size_path = "darklunsize.txt"
    dark_lun_dg_path = "darklundg.txt"
    dark_lun_utilization_path = "darklunutilization.txt"
    veritas_disk_path = "veritasdisk.txt"

    # Parse data files
    parse_file(file_path)
    process_disk_status(disk_status_path)
    process_disk_tier(disk_tier_path)
    process_disk_id(disk_id_path)
    process_disk_stat(disk_stat_path)
    process_disk_size(disk_size_path)
    process_disk_used_size(disk_used_size_path)
    process_vg_size(vg_size_path)
    process_lun_id(lun_id_path)
    process_dark_lun_id(dark_lun_id_path)
    process_dark_lun_size(dark_lun_size_path)
    process_dark_lun_dg(dark_lun_dg_path)
    process_dark_lun_utilization(dark_lun_utilization_path)
    process_veritas_disk(veritas_disk_path)

    # Optimize data structures
    optimize_data_structures()

    # Print results
    print("HostName:", host_name)
    print("OS:", OS)
    print("Date:", date)
    print("Unassigned Disks:")
    for disk, size in Unassigned_Disks.items():
        print(f"\t{disk}: {size}")
    print("NAS Volumes:")
    for vol, size, used_size, avail_size, mount_point in nas_volumes:
        print(f"\tVolume: {vol}")
        print(f"\t\tSize: {size}")
        print(f"\t\tUsed Size: {used_size}")
        print(f"\t\tAvailable Size: {avail_size}")
        print(f"\t\tMount Point: {mount_point}")
    print("Veritas Volumes:")
    for vol in Veritas_Vols:
        print(f"\t{vol}")
    print("Logical Volumes:")
    for lv, disk in LV_Disk.items():
        print(f"\tLV: {lv}")
        print(f"\t\tDisk: {disk}")
        print(f"\t\tSize: {LV_Size[lv]}")
        print(f"\t\tIdentifier: {LV_Identifier[lv]}")
        print(f"\t\tVG Identifier: {VG_Identifier[lv]}")
        print(f"\t\tPVs: {', '.join(LV_PV[lv])}")
    print("Mount Points:")
    for mp, lv in MP.items():
        print(f"\tMount Point: {mp}")
        print(f"\t\tLV: {lv}")
        print(f"\t\tSize: {MP_Size[mp]}")

if __name__ == "__main__":
    main()
