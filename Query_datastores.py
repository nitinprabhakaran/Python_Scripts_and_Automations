from pyVim import connect
from pyVmomi import vim

def connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password):
    service_instance = connect.SmartConnectNoSSL(
        host=vcenter_host,
        user=vcenter_user,
        pwd=vcenter_password,
        port=443
    )
    return service_instance.RetrieveContent()

def list_disk_partitions(vm):
    partitions = {}
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualDisk):
            partitions[device.deviceInfo.label] = []
            for disk_partition in device.layout.partition:
                partitions[device.deviceInfo.label].append({
                    "Partition": disk_partition.partition,
                    "Start": disk_partition.startSector,
                    "End": disk_partition.endSector,
                    "CapacityMB": disk_partition.length / (1024 ** 2)
                })
    return partitions

def main():
    vcenter_host = 'your_vcenter_host'
    vcenter_user = 'your_username'
    vcenter_password = 'your_password'

    content = connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password)

    vm_container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )

    for vm in vm_container.view:
        partitions = list_disk_partitions(vm)
        if partitions:
            print(f"VM: {vm.name}")
            for disk, disk_partitions in partitions.items():
                print(f"Disk: {disk}")
                for partition in disk_partitions:
                    print(f"  Partition: {partition['Partition']}, Start: {partition['Start']}, End: {partition['End']}, Capacity: {partition['CapacityMB']} MB")
            print()

    connect.Disconnect(content)

if __name__ == "__main__":
    main()