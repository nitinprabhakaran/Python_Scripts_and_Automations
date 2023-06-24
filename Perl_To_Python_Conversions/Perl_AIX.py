import re

# Initialize variables
Disk_Size = {}
Disk_VG = {}
LV_Disk = {}
Disk_ID = {}
VG_Total_Size = {}
VG_Used_Size = {}
VG_Identifier = {}
Disk_Status = {}
Disk_Stat = {}
Disk_Tier = {}
Disk_Used_Size = {}
Disk_Free_Size = {}
Disk_Used_Size_GB = {}
Disk_Free_Size_GB = {}
Disk_Size_GB = {}
Lun_Id = {}
MP = {}

# Read the file
with open('New_collect2.pl', 'r') as file:
    lines = file.readlines()

# Helper functions
def extract_value(line, pattern):
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    return None

def extract_disk_name(disk_vg):
    for key, value in Disk_VG.items():
        if value == disk_vg:
            return key
    return None

def process_disk(line):
    disk = extract_value(line, r'PV Name\s+(.*)')
    if disk:
        disk_name = extract_disk_name(disk)
        if disk_name:
            Disk_VG[disk_name] = extract_value(line, r'VG Name\s+(.*)')
            PP_Size[disk_name] = extract_value(line, r'PE Size\s+(\d+\.\d+)\s+MiB')
            total_pe = int(extract_value(line, r'Total PE\s+(\d+)'))
            Disk_Size[disk_name] = total_pe * float(PP_Size[disk_name])
            Disk_Size_GB[disk_name] = Disk_Size[disk_name] / 1024
            Disk_Free_Size[disk_name] = int(extract_value(line, r'Free PE\s+(\d+)')) * float(PP_Size[disk_name])
            Disk_Used_Size[disk_name] = Disk_Size[disk_name] - Disk_Free_Size[disk_name]
            Disk_Used_Size_GB[disk_name] = Disk_Used_Size[disk_name] / 1024
            Disk_Free_Size_GB[disk_name] = Disk_Free_Size[disk_name] / 1024
            Disk_ID[disk_name] = extract_value(line, r'PV UUID\s+(.*)')

def process_volume_group(line):
    vg_name = extract_value(line, r'VG Name\s+(.*)')
    if vg_name:
        VG_Total_Size[vg_name] = extract_value(line, r'VG Size\s+(.*)')
        VG_Used_Size[vg_name] = extract_value(line, r'Alloc PE \/ Size\s+\d+\/\s+(.*)')
        VG_Identifier[vg_name] = extract_value(line, r'VG UUID\s+(.*)')

def process_logical_volume(line):
    lv_name = extract_value(line, r'LV Name\s+(.*)')
    if lv_name:
        disk_name = extract_disk_name(extract_value(line, r'VG Name\s+(.*)'))
        if disk_name:
            LV_Disk[lv_name] = disk_name
            if lv_name not in MP:
                MP[lv_name] = lv_name
            LV_Identifier[lv_name] = extract_value(line, r'LV UUID\s+(.*)')
            LV_Size = extract_value(line, r'LV Size\s+(.*)')
            if LV_Size:
                if re.match(r'\d*\.*\d*\s*T.*', LV_Size):
                    LV_Size = float(re.search(r'(\d*\.*\d*)\s*T.*', LV_Size).group(1)) * 1024
                elif re.match(r'\d*\.*\d*\s*G.*', LV_Size):
                    LV_Size = float(re.search(r'(\d*\.*\d*)\s*G.*', LV_Size).group(1))
                elif re.match(r'\d*\.*\d*\s*M.*', LV_Size):
                    LV_Size = float(re.search(r'(\d*\.*\d*)\s*M.*', LV_Size).group(1)) / 1024
                LV_Size_GB[lv_name] = LV_Size

# Process each line in the file
for line in lines:
    line = line.strip()
    if line.startswith('Disk /dev'):
        process_disk(line)
    elif line.startswith('VG Name'):
        process_volume_group(line)
    elif line.startswith('LV Name'):
        process_logical_volume(line)

# Print the collected information
print("Disk Information:")
print("--------------------------------------------------------------")
print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
    "Disk Name", "Size (GB)", "Used (GB)", "Free (GB)", "VG", "Disk ID", "Disk Status", "Disk Tier"))
print("--------------------------------------------------------------")
for disk in Disk_VG:
    print("{:<15} {:<15.2f} {:<15.2f} {:<15.2f} {:<15} {:<15} {:<15} {:<15}".format(
        disk, Disk_Size_GB[disk], Disk_Used_Size_GB[disk], Disk_Free_Size_GB[disk], Disk_VG[disk], Disk_ID[disk],
        Disk_Status[disk], Disk_Tier[disk]))

print("\nPV Information:")
print("--------------------------------------------------------------")
print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
    "Disk Name", "Size (GB)", "Used (GB)", "Free (GB)", "Disk ID", "LUN ID"))
print("--------------------------------------------------------------")
for disk in Disk_VG:
    print("{:<15} {:<15.2f} {:<15.2f} {:<15.2f} {:<15} {:<15}".format(
        disk, Disk_Size_GB[disk], Disk_Used_Size_GB[disk], Disk_Free_Size_GB[disk], Disk_ID[disk], Lun_Id[disk]))

print("\nVG Information:")
print("--------------------------------------------------------------")
print("{:<15} {:<15} {:<15} {:<15}".format("VG Name", "Total Size", "Used Size", "VG Identifier"))
print("--------------------------------------------------------------")
for vg in VG_Total_Size:
    print("{:<15} {:<15} {:<15} {:<15}".format(vg, VG_Total_Size[vg], VG_Used_Size[vg], VG_Identifier[vg]))

print("\nLV Information:")
print("--------------------------------------------------------------")
print("{:<15} {:<15} {:<15} {:<15} {:<15}".format("LV Name", "Size (GB)", "Disk Name", "LV Identifier", "Mount Point"))
print("--------------------------------------------------------------")
for lv in LV_Size_GB:
    print("{:<15} {:<15.2f} {:<15} {:<15} {:<15}".format(
        lv, LV_Size_GB[lv], LV_Disk[lv], LV_Identifier[lv], MP.get(lv, "")))
