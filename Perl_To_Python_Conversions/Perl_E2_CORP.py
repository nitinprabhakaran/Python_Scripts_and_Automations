import re

# Part 1: Reading the TXT file and extracting relevant data

filename = "sample.txt"
host_name = ""
OS = ""
date = ""

Disk_VG = {}
LV_Disk = {}
LV_Size = {}
LV_Identifier = {}
Disk_Status = {}
Disk_Tier = {}

with open(filename, 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("HostName"):
            host_name = line.split(":")[1].strip()
        elif line.startswith("OS"):
            OS = line.split(":")[1].strip()
        elif line.startswith("Date"):
            date = line.split(":")[1].strip()
        elif re.match(r"\w+:\s*\w+", line):
            key, value = line.split(":")
            Disk_VG[key.strip()] = value.strip()

        # Part 2: Processing the data and storing relevant information

        if line.startswith("VG-"):
            vg_info = line.split(",")
            vg_identifier = vg_info[0].split(":")[1].strip()
            vg_name = vg_info[1].strip()
            vg_total_space = vg_info[2].strip()
            vg_used_space = vg_info[3].strip()
            vg_status = vg_info[4].strip()
            vg_tier = vg_info[5].strip()
            vg_mount_point = vg_info[6].strip()
            LVs = vg_info[7:]

            for lv in LVs:
                lv_info = lv.split(",")
                lv_name = lv_info[0].strip()
                lv_identifier = lv_info[1].strip()
                lv_size = lv_info[2].strip()
                lv_disk = lv_info[3].strip()

                LV_Disk[lv_name] = lv_disk
                LV_Size[lv_identifier] = lv_size
                LV_Identifier[lv_name] = lv_identifier

                if lv_disk not in Disk_Status:
                    Disk_Status[lv_disk] = vg_status

                if lv_disk not in Disk_Tier:
                    Disk_Tier[lv_disk] = vg_tier

        # Part 3: Generating the CSV output

        unassigned_disks = {}
        lun_id = {}
        dark_lun_size = {}
        dark_lun_utilization = {}
        veritas_lun = {}

        for key in Disk_VG:
            if Disk_VG[key] == "Unassigned":
                unassigned_disks[key] = Disk_VG[key]

            if key in LV_Disk:
                lun_id[key] = LV_Disk[key]

            if key in dark_lun_size:
                for df_line in lines:
                    if re.search(dark_lun_dg[key], df_line):
                        match = re.search(r"(\d*\.*\d*[TGMK])\s+(\d*\.*\d*[TGMK])\s+\d*\.*\d*[TGMK]\s+\d*%\s+(.*)", df_line)
                        if match:
                            utilization = match.group(2)
                            if re.match(r"\d*\.*\d*\s*T.*", utilization):
                                utilization = float(utilization) * 1024 * 1024
                                dark_lun_utilization[key] += utilization
                            elif re.match(r"\d*\.*\d*\s*G.*", utilization):
                                utilization = float(utilization) * 1024
                                dark_lun_utilization[key] += utilization
                            elif re.match(r"\d*\.*\d*\s*M.*", utilization):
                                utilization = float(utilization)
                                dark_lun_utilization[key] += utilization

        # Write the output to a CSV file
        with open('output.csv', 'w') as csv_file:
            csv_file.write("HostName,VG_Identifier,Disk,VG,LV,LV_Identifier,PP_Size,Size,Tier,MountPoint,Date\n")
            for lv_name in LV_Identifier:
                vg_identifier = Disk_VG[LV_Disk[lv_name]]
                disk = lv_name.split("_")[0]
                vg = Disk_VG[LV_Disk[lv_name]]
                lv = lv_name.split("_")[1]
                lv_identifier = LV_Identifier[lv_name]
                pp_size = "N/A"
                size = LV_Size[lv_identifier]
                tier = Disk_Tier[LV_Disk[lv_name]]
                mount_point = vg_mount_point if lv == "lvroot" else "N/A"
                csv_file.write(f"{host_name},{vg_identifier},{disk},{vg},{lv},{lv_identifier},{pp_size},{size},{tier},{mount_point},{date}\n")
            for disk in unassigned_disks:
                csv_file.write(f"{host_name},N/A,{disk},N/A,N/A,N/A,N/A,N/A,{Disk_Status[disk]},N/A,{date}\n")
            for dark_lun in dark_lun_size:
                csv_file.write(f"{host_name},N/A,{dark_lun},N/A,N/A,N/A,{dark_lun_size[dark_lun]},N/A,{Disk_Tier[dark_lun]},N/A,{date}\n")
            for veritas_vol in veritas_lun:
                csv_file.write(f"{host_name},N/A,{veritas_vol},N/A,N/A,N/A,N/A,N/A,N/A,N/A,{date}\n")
