function Get-ORGAccountList {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$false)]
        [string]$ApiUrl,  # The URL of your internal API

        [Parameter(Mandatory=$false)]
        [hashtable]$Headers  # Optional headers for the API request
    )

    try {
        # Call the internal API to get the list of AWS Organization accounts
        $response = Invoke-RestMethod -Uri $ApiUrl -Headers $Headers -Method Get

        # Assuming the JSON response is a list of accounts
        $accounts = $response | ConvertFrom-Json

        # Format the output similar to Get-ORGAccountList
        $output = foreach ($account in $accounts) {
            [PSCustomObject]@{
                AccountId      = $account.AccountId
                AccountName    = $account.AccountName
                Email          = $account.Email
                Status         = $account.Status
                JoinedTimestamp = $account.JoinedTimestamp
            }
        }

        return $output
    }
    catch {
        Write-Error "An error occurred while fetching the account list: $_"
    }
}