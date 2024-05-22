Param
(
  [Parameter (Mandatory= $true)]
  [string] $identity,

  [Parameter (Mandatory= $true)]
  [string] $subscription
)

# $subscription = "MOON-NM-DIG-DEV"
# $identity = "af3790d3-869e-4582-b72a-fe020311d392"
$AzureContext = (Connect-AzAccount -Identity -AccountId $identity).context
$connectionResult = Set-AzContext -Subscription $subscription -DefaultProfile $AzureContext

$policyAssignmentIdArray="queuepolicy2","tablepolicy2","blobpolicy2","filepolicy2"

for ($var = 0; $var -le 4; $var++) {
    $policyAssignmentId="/subscriptions/a273b4fb-6a3d-4804-a047-5d293da8811d/providers/microsoft.authorization/policyassignments/"+$policyAssignmentIdArray[$var]
    try {
        $name = "remediation"+$var
        Start-AzPolicyRemediation -PolicyAssignmentId $policyAssignmentId -Name $name 
        Write-Output "Remediation task started successfully."
    } catch {
        Write-Error "Failed to start remediation task: $_"
    }
}
