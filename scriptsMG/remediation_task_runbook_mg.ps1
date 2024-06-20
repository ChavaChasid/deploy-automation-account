Connect-AzAccount -Identity 
# queueMG, tableMG
$policyAssignmentIdArray="56c19d7a200a4b75bc4e4c18","f4dada8f0f504d7cb030fa20"

for ($var = 0; $var -le 2; $var++) {

    $policyAssignmentId='/providers/microsoft.management/managementgroups/moon-test/providers/microsoft.authorization/policyassignments/'+$policyAssignmentIdArray[$var]
    try {
        $name = "remediation"+$var
        Start-AzPolicyRemediation -PolicyAssignmentId $policyAssignmentId -Name $name 
        Write-Output "Remediation task started successfully."
    } catch {
        Write-Error "Failed to start remediation task: $_"
    }
}
