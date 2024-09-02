Param
(
  [Parameter (Mandatory= $true)]
  [string] $managementGroup
)

Connect-AzAccount -Identity

$policyAssignmentIdArray="policy-la-queue-custom","policy-la-table-custom","policy-la-blob-custom","policy-la-file-custom"

for ($var = 0; $var -le 4; $var++) {
    $policyAssignmentId="/providers/microsoft.management/managementgroups/"+$managementGroup+"/providers/microsoft.authorization/policyassignments/"+$policyAssignmentIdArray[$var]
    try {
        $name = "remediation"+$var
        Start-AzPolicyRemediation -ManagementGroupName $managementGroup -PolicyAssignmentId $policyAssignmentId -Name $name 
        Write-Output "Remediation task started successfully."
    } catch {
        Write-Error "Failed to start remediation task: $_"
    }
}

