import re

# Variable declarations
LV_Size = {}
LV_Identifier = {}
Disk_VG = {}
LV_Disk = {}
Unassigned_Disks = {}
Lun_Id = {}
Disk_Status = {}
Disk_Tier = {}
Disk_Stat = {}
VG_Identifier = {}
Disk_Size = {}
Disk_Used_Size = {}
Disk_ID = {}
Disk_Size_GB = {}
Disk_Used_Size_GB = {}
Disk_Free_Size_GB = {}
Dark_Lun_Size = {}
Dark_Lun_Utilization = {}
Dark_Lun_DG = {}
Dark_Lun_ID = {}
Veritas_Lun = {}
Veritas_Disk = {}
Veritas_Disk_Size = {}
Veritas_VG = {}
MP = {}
MP_Size = {}

# Initialize variables
host_name = ""
count = 1
Unallocated_Disk_Size = 0
Total_VG_Size = 0
dark_lun_flag = 0
nas_volumes = []
df_arr = []

# Open input files
with open('input_file.txt', 'r') as input_file:
    input_lines = input_file.readlines()

# Process input file
for line in input_lines:
    line = line.strip()
    if line.startswith("Filesystem"):
        df_arr.append(line)
    elif line.startswith("Logical"):
        # Extract LV_Size and LV_Identifier
        match = re.match(r"Logical Volume ([\w]+) size: (\d+\.*\d*) (\w+)", line)
        if match:
            lv = match.group(1)
            size = float(match.group(2))
            unit = match.group(3)
            if unit == "G":
                size *= 1024
            elif unit == "M":
                size /= 1024
            LV_Size[LV_Identifier[lv]] = size
    elif line.startswith("Physical"):
        # Extract LV_Identifier and LV_Disk
        match = re.match(r"Physical volume ([\w]+) \(([\w]+)\) status: (\w+)", line)
        if match:
            lv = match.group(1)
            identifier = match.group(2)
            disk = match.group(3)
            LV_Identifier[lv] = identifier
            LV_Disk[LV_Identifier[lv]] = disk
    elif line.startswith("Disk"):
        # Extract disk details
        match = re.match(r"Disk ([\w]+) \(([\w]+)\), (\d+\.*\d*[TGMK]), (\d+\.*\d*[TGMK]), (\d+\.*\d*[TGMK])", line)
        if match:
            disk = match.group(1)
            scsi_controller = match.group(2)
            scsi_target = match.group(3)
            size = match.group(4)
            used_size = match.group(5)
            Disk_VG[disk] = ""
            Disk_Status[disk] = ""
            Disk_Tier[disk] = ""
            Disk_Stat[disk] = ""
            Disk_Size[disk] = size
            Disk_Used_Size[disk] = used_size
            Disk_Size_GB[disk] = ""
            Disk_Used_Size_GB[disk] = ""
            Disk_Free_Size_GB[disk] = ""

# Open output files
with open('disk_output.csv', 'w') as disk_output_file, \
     open('pp_output.csv', 'w') as pp_output_file, \
     open('vg_output.csv', 'w') as vg_output_file, \
     open('nas_output.csv', 'w') as nas_output_file:

    # Write disk header
    disk_output_file.write("HostName,Disk,VG,Size,Used,Free,Status,Tier,Stat\n")

    # Process disk information
    for disk, size in Disk_Size.items():
        used_size = Disk_Used_Size[disk]
        disk_output_file.write(f"{host_name},{disk},{Disk_VG[disk]},{size},{used_size},,{Disk_Status[disk]},{Disk_Tier[disk]},{Disk_Stat[disk]}\n")

    # Write pp header
    pp_output_file.write("HostName,PP,Size,Used,Free\n")

    # Process pp information
    for disk, size in Disk_Size.items():
        used_size = Disk_Used_Size[disk]
        free_size = float(size) - float(used_size)
        pp_output_file.write(f"{host_name},{disk},{size},{used_size},{free_size}\n")

    # Write vg header
    vg_output_file.write("HostName,VG,Size,Used,Free\n")

    # Process vg information
    for disk, size in Disk_Size.items():
        used_size = Disk_Used_Size[disk]
        vg_output_file.write(f"{host_name},{Disk_VG[disk]},{size},{used_size},\n")

    # Write nas header
    nas_output_file.write("HostName,NAS,Size,Used,Free\n")

    # Process nas information
    for nas_volume in nas_volumes:
        nas_output_file.write(f"{host_name},{nas_volume},{MP_Size[nas_volume]},,,\n")
