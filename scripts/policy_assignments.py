
from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.resource.policy.models import PolicyAssignment, Identity
from azure.identity import AzureCliCredential

import os
from dotenv import load_dotenv

load_dotenv()


subscription_id = os.getenv("SUBSCRIPTION_ID")
workspace_id = os.getenv("WORKSPACE_ID")
resource_group = os.getenv("RESOURCE_GROUP")
assignment_location = os.getenv("ASSIGNMENT_LOCATION")
managed_identity_name = os.getenv("MANAGED_IDENTITY")

credential = AzureCliCredential()
policyClient = PolicyClient(credential, subscription_id, base_url="https://management.azure.com/")


policy_assignment_identity = Identity(type="UserAssigned",user_assigned_identities={f"/subscriptions/{subscription_id}/resourcegroups/{resource_group}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/policy":{}})

parameters = {
    "logAnalytics": {
        "value": workspace_id
    }
}

assignments_name=["queuepolicy","tablepolicy","blobpolicy","filepolicy"]
definitions_id=["7bd000e3-37c7-4928-9f31-86c4b77c5c45","2fb86bf3-d221-43d1-96d1-2434af34eaa0","7bd000e3-37c7-4928-9f31-86c4b77c5c45","25a70cc8-2bd4-47f1-90b6-1478e4662c96"]
for i in range(0,4):
    policy_assignment_details = PolicyAssignment(display_name=assignments_name[i],
                                               policy_definition_id=f"/providers/Microsoft.Authorization/policyDefinitions/{definitions_id[i]}",
                                                description="Updating log analytics",
                                                identity=policy_assignment_identity,
                                                location=assignment_location,
                                                parameters=parameters)

    policy_assignment = policyClient.policy_assignments.create(f"/subscriptions/{subscription_id}",
                                                              assignments_name[i],
                                                              policy_assignment_details)
    print(policy_assignment)

