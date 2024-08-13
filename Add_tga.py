import boto3
from botocore.exceptions import ClientError

def get_latest_patch(instance_id):
    ssm_client = boto3.client('ssm')
    
    try:
        # Initialize variables for latest patch information
        latest_patch_time = None
        latest_patch_name = None
        
        # Paginate through patch compliance details
        paginator = ssm_client.get_paginator('describe_instance_patches')
        response_iterator = paginator.paginate(
            InstanceId=instance_id,
            Filters=[
                {
                    'Key': 'State',
                    'Values': ['INSTALLED']
                }
            ]
        )
        
        # Loop through paginated results to find the latest patch
        for response in response_iterator:
            for patch in response['Patches']:
                # Compare patch installation times to find the latest one
                if latest_patch_time is None or patch['InstalledTime'] > latest_patch_time:
                    latest_patch_time = patch['InstalledTime']
                    latest_patch_name = patch['Title']
        
        if latest_patch_name:
            print(f"Latest patch installed on {instance_id}: {latest_patch_name} at {latest_patch_time}")
        else:
            print(f"No patches found for instance {instance_id}.")
    
    except ClientError as e:
        print(f"Error retrieving patch information: {e}")

def main():
    instance_id = 'i-0abcd1234efgh5678'  # Replace with your EC2 or managed instance ID
    get_latest_patch(instance_id)

if __name__ == "__main__":
    main()