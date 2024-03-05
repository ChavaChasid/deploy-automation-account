
$subscription = "Moon- azure camp"
$identity = "3e455f37-1e8b-4dd6-bff0-26d3859e7d37"
$AzureContext = (Connect-AzAccount -Identity -AccountId $identity).context
$connectionResult = Set-AzContext -Subscription $subscription -DefaultProfile $AzureContext

$policyAssignmentIdArray="tablepolicybycodenorg","queuepolicybycodenorg","filepolicybycodenorg","blobpolicybycodenorg"

for ($var = 0; $var -le 4; $var++) {
    $policyAssignmentId="/subscriptions/a173eef2-33d7-4d55-b0b5-18b271f8d42b/providers/microsoft.authorization/policyassignments/"+$policyAssignmentIdArray[$var]
    try {
        $name = "remediation"+$var
        Start-AzPolicyRemediation -PolicyAssignmentId $policyAssignmentId -Name $name 
        Write-Output "Remediation task started successfully."
    } catch {
        Write-Error "Failed to start remediation task: $_"
    }
}
