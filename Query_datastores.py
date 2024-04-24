# Import necessary modules
Install-Module -Name AWS.Tools.Installer -Force -Scope CurrentUser
Install-AWSToolsModule aws.ssm -Force -Scope CurrentUser

# Set AWS credentials
Set-AWSCredential -AccessKey "your-access-key" -SecretKey "your-secret-key" -StoreAs "MyCredentials"

# AWS SSM Parameter Store details
$parameterName = "YourParameterName"
$region = "your-aws-region"

# Ansible Tower API details
$ansibleTowerUrl = "https://your-ansible-tower-url/api/v2/job_templates/your-template-id/launch/"
$ansibleTowerUsername = "your-ansible-tower-username"
$ansibleTowerPassword = "your-ansible-tower-password"

# Get parameter value from AWS SSM
$parameterValue = (Get-SSMParameter -Name $parameterName -Region $region).Value

# Create JSON body for Ansible Tower API request
$body = @{
    "extra_vars" = @{
        "your_variable_name" = $parameterValue
    }
} | ConvertTo-Json

# Encode credentials for Basic Authentication
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $ansibleTowerUsername, $ansibleTowerPassword)))

# Make HTTP POST request to Ansible Tower API with Basic Authentication
$response = Invoke-RestMethod -Uri $ansibleTowerUrl -Method Post -Headers @{ "Authorization" = "Basic $base64AuthInfo" } -Body $body -ContentType "application/json"

# Print response
$response