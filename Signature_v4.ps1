function Get-AWSSignatureV4 {
    param (
        [string]$AccessKeyId,
        [string]$SecretAccessKey,
        [string]$Region,
        [string]$Service,
        [string]$HttpMethod,
        [string]$UriPath,
        [string]$Payload = "",
        [hashtable]$Headers
    )

    # Get the current time and date in UTC
    $amzDate = (Get-Date -Format "yyyyMMddTHHmmssZ").ToUpper()
    $dateStamp = (Get-Date -Format "yyyyMMdd").ToUpper()

    # Create the canonical request
    $canonicalUri = $UriPath
    $canonicalQuerystring = ""
    $signedHeaders = ($Headers.GetEnumerator() | Sort-Object Name | ForEach-Object { $_.Name.ToLower() }) -join ";"
    $canonicalHeaders = ($Headers.GetEnumerator() | Sort-Object Name | ForEach-Object { "$($_.Name.ToLower()):$($_.Value.Trim())`n" }) -join ""
    $payloadHash = [System.BitConverter]::ToString((New-Object -TypeName System.Security.Cryptography.SHA256Managed).ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Payload))).Replace("-", "").ToLower()

    $canonicalRequest = "$HttpMethod`n$canonicalUri`n$canonicalQuerystring`n$canonicalHeaders`n$signedHeaders`n$payloadHash"

    # Create the string to sign
    $algorithm = "AWS4-HMAC-SHA256"
    $credentialScope = "$dateStamp/$Region/$Service/aws4_request"
    $stringToSign = "$algorithm`n$amzDate`n$credentialScope`n" + [System.BitConverter]::ToString((New-Object -TypeName System.Security.Cryptography.SHA256Managed).ComputeHash([System.Text.Encoding]::UTF8.GetBytes($canonicalRequest))).Replace("-", "").ToLower()

    # Create the signing key
    function HMAC-SHA256 ($key, $data) {
        $hmacsha256 = New-Object System.Security.Cryptography.HMACSHA256
        $hmacsha256.Key = [Text.Encoding]::UTF8.GetBytes($key)
        $hmacsha256.ComputeHash([Text.Encoding]::UTF8.GetBytes($data))
    }

    $kSecret = "AWS4" + $SecretAccessKey
    $kDate = HMAC-SHA256 $kSecret $dateStamp
    $kRegion = HMAC-SHA256 $kDate $Region
    $kService = HMAC-SHA256 $kRegion $Service
    $kSigning = HMAC-SHA256 $kService "aws4_request"

    # Calculate the signature
    $signature = [System.BitConverter]::ToString((HMAC-SHA256 $kSigning $stringToSign)).Replace("-", "").ToLower()

    # Create the authorization header
    $authorizationHeader = "$algorithm Credential=$AccessKeyId/$credentialScope, SignedHeaders=$signedHeaders, Signature=$signature"

    # Return headers including the authorization header
    $Headers.Add("Authorization", $authorizationHeader)
    $Headers.Add("x-amz-date", $amzDate)
    return $Headers
}

# Example usage
$accessKeyId = "your_access_key_id"
$secretAccessKey = "your_secret_access_key"
$region = "us-east-1"
$service = "execute-api"
$httpMethod = "GET"
$uriPath = "/your/api/path"
$payload = ""
$headers = @{
    "host" = "example.amazonaws.com"
    "x-amz-content-sha256" = "UNSIGNED-PAYLOAD"
}

$signedHeaders = Get-AWSSignatureV4 -AccessKeyId $accessKeyId -SecretAccessKey $secretAccessKey -Region $region -Service $service -HttpMethod $httpMethod -UriPath $uriPath -Payload $payload -Headers $headers

# Now you can use $signedHeaders in your Invoke-RestMethod or Invoke-WebRequest