---
description: "Search for an AMI by name, launch an instance with a specified ENI, and attach a security group"
schemaVersion: '0.3'
assumeRole: "{{ AutomationAssumeRole }}"
parameters:
  AmiName:
    type: String
    description: "Name of the AMI to search for"
  SubnetId:
    type: String
    description: "The subnet ID where the instance will be launched"
  EnclaveSecurityGroupId:
    type: String
    description: "The ID of the security group to attach to the instance"
  InstanceType:
    type: String
    description: "The instance type to use for the new instance"
    default: "t2.micro"
  EnclaveElasticNetworkInterfaceId:
    type: String
    description: "The ENI ID to attach to the instance"

mainSteps:
  - name: searchAMI
    action: aws:executeAwsApi
    inputs:
      Service: ec2
      Api: DescribeImages
      Filters:
        - Name: "name"
          Values: ["{{ AmiName }}"]
    outputs:
      - Name: ImageId
        Selector: "$.Images[0].ImageId"
        Type: String

  - name: launchInstance
    action: aws:runInstances
    maxAttempts: 3
    timeoutSeconds: 1200
    inputs:
      ImageId: "{{ searchAMI.ImageId }}"
      InstanceType: "{{ InstanceType }}"
      NetworkInterfaces:
        - DeviceIndex: 0
          NetworkInterfaceId: "{{ EnclaveElasticNetworkInterfaceId }}"
      SubnetId: "{{ SubnetId }}"
      MinCount: 1
      MaxCount: 1
      SecurityGroupIds:
        - "{{ EnclaveSecurityGroupId }}"

  - name: attachSecurityGroup
    action: aws:executeAwsApi
    inputs:
      Service: ec2
      Api: ModifyNetworkInterfaceAttribute
      NetworkInterfaceId: "{{ EnclaveElasticNetworkInterfaceId }}"
      Groups:
        - "{{ EnclaveSecurityGroupId }}"
      
  - name: verifyInstance
    action: aws:assertAwsResourceProperty
    inputs:
      Service: ec2
      Api: DescribeInstances
      InstanceIds:
        - "{{ launchInstance.InstanceIds[0] }}"
      PropertySelector: "$.Reservations[0].Instances[0].State.Name"
      DesiredValues:
        - "running"