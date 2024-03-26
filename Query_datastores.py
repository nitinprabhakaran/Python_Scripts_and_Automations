import boto3

def get_ssm_execution_info(region):
    ssm_client = boto3.client('ssm', region_name=region)

    # Get maintenance windows
    maintenance_windows = ssm_client.describe_maintenance_windows()

    # Create a dictionary to store the correlation
    execution_info = {}

    for window in maintenance_windows['WindowIdentities']:
        window_id = window['WindowId']
        execution_info[window_id] = []

        # Get window executions
        window_executions = ssm_client.describe_maintenance_window_executions(WindowId=window_id)

        for execution in window_executions['WindowExecutions']:
            execution_id = execution['WindowExecutionId']
            execution_info[window_id].append({
                'WindowExecutionId': execution_id,
                'TaskExecutions': []
            })

            # Get task executions
            task_executions = ssm_client.describe_maintenance_window_execution_task_invocations(
                WindowExecutionId=execution_id,
                WindowId=window_id
            )

            for task_execution in task_executions['WindowExecutionTaskInvocationIdentities']:
                task_execution_id = task_execution['WindowExecutionId']
                command_id = task_execution['CommandId']
                execution_info[window_id][-1]['TaskExecutions'].append({
                    'TaskExecutionId': task_execution_id,
                    'CommandId': command_id
                })

    return execution_info

# Replace 'your-region' with your desired AWS region
execution_info = get_ssm_execution_info('your-region')
print(execution_info)