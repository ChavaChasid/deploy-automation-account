
from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.resource.policy.models import PolicyAssignment, Identity
from azure.identity import AzureCliCredential


subId = "a173eef2-33d7-4d55-b0b5-18b271f8d42b"
assignmentLocation = "East US"
credential = AzureCliCredential()
policyClient = PolicyClient(credential, subId, base_url="https://management.azure.com/")

policyAssignmentIdentity = Identity(type="UserAssigned",user_assigned_identities={"/subscriptions/a173eef2-33d7-4d55-b0b5-18b271f8d42b/resourcegroups/AKS/providers/Microsoft.ManagedIdentity/userAssignedIdentities/userAssigned":{}})

workspace_id = "/subscriptions/a173eef2-33d7-4d55-b0b5-18b271f8d42b/resourcegroups/DefaultResourceGroup-EUS/providers/microsoft.operationalinsights/workspaces/DefaultWorkspace-a173eef2-33d7-4d55-b0b5-18b271f8d42b-EUS"
parameters = {
    "logAnalytics": {
        "value": workspace_id
    }
}

assignments_name=["queuepolicybycodenorg","tablepolicybycodenorg","blobpolicybycodenorg","filepolicybycodenorg"]
definitions_id=["7bd000e3-37c7-4928-9f31-86c4b77c5c45","2fb86bf3-d221-43d1-96d1-2434af34eaa0","7bd000e3-37c7-4928-9f31-86c4b77c5c45","25a70cc8-2bd4-47f1-90b6-1478e4662c96"]
for i in range(0,4):
    policyAssignmentDetails1 = PolicyAssignment(display_name=assignments_name[i],
                                               policy_definition_id=f"/providers/Microsoft.Authorization/policyDefinitions/{definitions_id[i]}",
                                                description="Updating log analytics",
                                                identity=policyAssignmentIdentity,
                                                location=assignmentLocation,
                                                parameters=parameters)

    policyAssignment = policyClient.policy_assignments.create("/subscriptions/a173eef2-33d7-4d55-b0b5-18b271f8d42b",
                                                              assignments_name[i],
                                                              policyAssignmentDetails1)
    print(policyAssignment)

