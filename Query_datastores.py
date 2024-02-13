from pyVim import connect
from pyVmomi import vim
import ssl

def connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE
    service_instance = connect.SmartConnect(host=vcenter_host,
                                            user=vcenter_user,
                                            pwd=vcenter_password,
                                            sslContext=context)
    return service_instance.RetrieveContent()

def get_vm_disk_partition_info(vm):
    disk_partitions = {}
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualDisk):
            disk_label = device.deviceInfo.label
            disk_partitions[disk_label] = []
            for disk_partition in device.layout.partition:
                partition_info = {
                    "Partition": disk_partition.partition,
                    "Start": disk_partition.startSector,
                    "End": disk_partition.endSector,
                    "CapacityMB": disk_partition.length / (1024 ** 2)
                }
                disk_partitions[disk_label].append(partition_info)
    return disk_partitions

def main():
    vcenter_host = 'your_vcenter_host'
    vcenter_user = 'your_username'
    vcenter_password = 'your_password'
    vm_name = 'your_vm_name'

    content = connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password)

    vm_view = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    vm = None
    for managed_object_ref in vm_view.view:
        if managed_object_ref.name == vm_name:
            vm = managed_object_ref
            break

    if vm:
        disk_partitions = get_vm_disk_partition_info(vm)
        print("Disk Layout and Partition Details for VM:", vm_name)
        for disk, partitions in disk_partitions.items():
            print("Disk:", disk)
            for partition in partitions:
                print("  Partition:", partition["Partition"])
                print("    Start:", partition["Start"])
                print("    End:", partition["End"])
                print("    Capacity (MB):", partition["CapacityMB"])
    else:
        print("Virtual Machine", vm_name, "not found.")

    connect.Disconnect(content)

if __name__ == "__main__":
    main()