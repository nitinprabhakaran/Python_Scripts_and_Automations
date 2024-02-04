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

def get_datastore_info(datastore):
    summary = datastore.summary
    return {
        'Name': summary.name,
        'VMs': [vm.summary.config.name for vm in datastore.vm],
        'FreeSpaceGB': summary.freeSpace / (1024 ** 3),
        'CapacityGB': summary.capacity / (1024 ** 3),
        'UncommittedGB': (summary.capacity - summary.freeSpace) / (1024 ** 3)
    }

def main():
    vcenter_host = 'your_vcenter_host'
    vcenter_user = 'your_username'
    vcenter_password = 'your_password'

    content = connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password)

    datastores = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.Datastore], True
    ).view

    datastore_info_list = [get_datastore_info(ds) for ds in datastores]

    with open('datastore_report.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'VMs', 'FreeSpaceGB', 'CapacityGB', 'UncommittedGB']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for datastore_info in datastore_info_list:
            writer.writerow(datastore_info)

if __name__ == "__main__":
    main()