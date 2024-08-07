import boto3

def update_patch_group_tag(instance_id):
    ssm_client = boto3.client('ssm')
    
    # Fetch the current tags for the SSM managed instance
    response = ssm_client.list_tags_for_resource(
        ResourceType='ManagedInstance',
        ResourceId=instance_id
    )
    
    tags = response.get('TagList', [])
    
    # Check if 'Patch Group' tag is present
    has_patch_group_tag = any(tag['Key'] == 'Patch Group' for tag in tags)
    
    if not has_patch_group_tag:
        # Add the 'Patch Group' tag with the value 'NA'
        ssm_client.add_tags_to_resource(
            ResourceType='ManagedInstance',
            ResourceId=instance_id,
            Tags=[
                {
                    'Key': 'Patch Group',
                    'Value': 'NA'
                }
            ]
        )
        print(f"Added 'Patch Group' tag with value 'NA' to instance {instance_id}")
    else:
        print(f"'Patch Group' tag already exists on instance {instance_id}")

def main():
    instance_id = 'i-0abcd1234efgh5678'  # Replace with your managed instance ID
    
    update_patch_group_tag(instance_id)

if __name__ == "__main__":
    main()