from pyVim import connect
from pyVmomi import vim
import csv

def connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password):
    service_instance = connect.SmartConnectNoSSL(
        host=vcenter_host,
        user=vcenter_user,
        pwd=vcenter_password,
        port=443
    )
    return service_instance.RetrieveContent()

def get_vm_info(vm):
    vm_info = {
        'VirtualMachine': vm.name,
        'Datacenter': vm.datacenter.name,
        'Cluster': vm.resourcePool.name
    }
    datastores = vm.datastore
    for datastore in datastores:
        summary = datastore.summary
        provisioned_space_gb = (summary.capacity - summary.freeSpace + summary.uncommitted) / (1024 ** 3)
        vm_info[f'{summary.name}_FreeSpaceGB'] = summary.freeSpace / (1024 ** 3)
        vm_info[f'{summary.name}_ConsumedSpaceGB'] = (summary.capacity - summary.freeSpace) / (1024 ** 3)
        vm_info[f'{summary.name}_UncommittedSpaceGB'] = summary.uncommitted / (1024 ** 3)
        vm_info[f'{summary.name}_ProvisionedSpaceGB'] = provisioned_space_gb if provisioned_space_gb > 0 else 0
    return vm_info

def main():
    vcenter_host = 'your_vcenter_host'
    vcenter_user = 'your_username'
    vcenter_password = 'your_password'

    content = connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password)

    vm_container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )

    vm_info_list = [get_vm_info(vm) for vm in vm_container.view]

    with open('vm_datastore_report.csv', 'w', newline='') as csvfile:
        fieldnames = ['VirtualMachine', 'Datacenter', 'Cluster']
        for vm_info in vm_info_list:
            for key in vm_info.keys():
                if key not in ['VirtualMachine', 'Datacenter', 'Cluster']:
                    fieldnames.append(key)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for vm_info in vm_info_list:
            writer.writerow(vm_info)

    connect.Disconnect(content)

if __name__ == "__main__":
    main()