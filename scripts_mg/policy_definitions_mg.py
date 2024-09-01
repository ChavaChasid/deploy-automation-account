
from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.resource.policy.models import PolicyAssignment, Identity
from azure.identity import AzureCliCredential, DefaultAzureCredential   

import os
from dotenv import load_dotenv
load_dotenv()


subscription_id = os.getenv("SUBSCRIPTION_ID")
workspace_id = os.getenv("WORKSPACE_ID")
resource_group = os.getenv("RESOURCE_GROUP")
assignment_location = os.getenv("ASSIGNMENT_LOCATION")
management_group = os.getenv("MANAGEMENT_GROUP")
managed_identity_name = os.getenv("MANAGED_IDENTITY_NAME")

# subscription_id = '0552f1af-c9b7-43a3-8d3a-3a069a790bdc'
# workspace_id = '/subscriptions/0552f1af-c9b7-43a3-8d3a-3a069a790bdc/resourcegroups/rg-storages/providers/microsoft.operationalinsights/workspaces/storages-log-analytics'
# resource_group = 'rg-storages'
# assignment_location = 'Israel Central'
# management_group = 'group-moon'
# managed_identity_name = 'policy-prod'

credential = DefaultAzureCredential()
policyClient = PolicyClient(credential, subscription_id, base_url="https://management.azure.com/")

policy_assignment_identity = Identity(type="UserAssigned",user_assigned_identities={f"/subscriptions/{subscription_id}/resourcegroups/{resource_group}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{managed_identity_name}":{}})
parameters = {
    "logAnalytics": {
        "value": workspace_id
    }
}
def getDefinition(type):
    definition = {
      "properties": {
        "displayName": f"Configure diagnostic settings for {type} Services to Log Analytics workspace",
        "policyType": "Custom",
        "mode": "All",
        "description": f"Deploys the diagnostic settings for {type} Services to stream resource logs to a Log Analytics workspace when any {type} Service which is missing this diagnostic settings is created or updated.",
        "metadata": {
          "category": "Storage",
          "version": "4.0.0"
        },
        "version": "4.0.0",
        "parameters": {
          "effect": {
            "type": "String",
            "metadata": {
              "displayName": "Effect",
              "description": "Enable or disable the execution of the policy"
            },
            "allowedValues": [
              "DeployIfNotExists",
              "AuditIfNotExists",
              "Disabled"
            ],
            "defaultValue": "DeployIfNotExists"
          },
          "profileName": {
            "type": "String",
            "metadata": {
              "displayName": "Profile name",
              "description": "The diagnostic settings profile name"
            },
            "defaultValue": f"{type}ServicesDiagnosticsLogsToWorkspace"
          },
          "logAnalytics": {
            "type": "String",
            "metadata": {
              "displayName": "Log Analytics workspace",
              "description": "Select Log Analytics workspace from dropdown list. If this workspace is outside of the scope of the assignment you must manually grant 'Log Analytics Contributor' permissions (or similar) to the policy assignment's principal ID.",
              "strongType": "omsWorkspace",
              "assignPermissions": True
            }
          },
          "metricsEnabled": {
            "type": "Boolean",
            "metadata": {
              "displayName": "Enable metrics",
              "description": "Whether to enable metrics stream to the Log Analytics workspace - True or False"
            },
            "allowedValues": [
              True,
              False
            ],
            "defaultValue": True
          },
          "logsEnabled": {
            "type": "Boolean",
            "metadata": {
              "displayName": "Enable logs",
              "description": "Whether to enable logs stream to the Log Analytics workspace - True or False"
            },
            "allowedValues": [
              True,
              False
            ],
            "defaultValue": True
          }
        },
        "policyRule": {
          "if": {
            "field": "type",
            "equals": f"Microsoft.Storage/storageAccounts/{type}Services"
          },
          "then": {
            "effect": "[parameters('effect')]",
            "details": {
              "type": "Microsoft.Insights/diagnosticSettings",
              "name": "[parameters('profileName')]",
              "existenceCondition": {
                "allOf": [
                  {
                    "field": "Microsoft.Insights/diagnosticSettings/logs.enabled",
                    "equals": "[parameters('logsEnabled')]"
                  },
                  {
                    "field": "Microsoft.Insights/diagnosticSettings/metrics.enabled",
                    "equals": "[parameters('metricsEnabled')]"
                  },
                  {
                    "field": "Microsoft.Insights/diagnosticSettings/workspaceId",
                    "equals": "[parameters('logAnalytics')]"
                  }
                ]
              },
              "roleDefinitionIds": [
                "/providers/microsoft.authorization/roleDefinitions/749f88d5-cbae-40b8-bcfc-e573ddc772fa",
                "/providers/microsoft.authorization/roleDefinitions/92aaf0da-9dab-42b6-94a3-d43ce8d16293"
              ],
              "deployment": {
                "properties": {
                  "mode": "incremental",
                  "template": {
                    "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                    "contentVersion": "1.0.0.0",
                    "parameters": {
                      "resourceName": {
                        "type": "string"
                      },
                      "location": {
                        "type": "string"
                      },
                      "logAnalytics": {
                        "type": "string"
                      },
                      "metricsEnabled": {
                        "type": "bool"
                      },
                      "logsEnabled": {
                        "type": "bool"
                      },
                      "profileName": {
                        "type": "string"
                      }
                    },
                    "variables": {},
                    "resources": [
                      {
                        "type": f"Microsoft.Storage/storageAccounts/{type}Services/providers/diagnosticSettings",
                        "apiVersion": "2021-05-01-preview",
                        "name": "[concat(parameters('resourceName'), '/', 'Microsoft.Insights/', parameters('profileName'))]",
                        "location": "[parameters('location')]",
                        "dependsOn": [],
                        "properties": {
                          "workspaceId": "[parameters('logAnalytics')]",
                          "metrics": [
                            {
                              "category": "AllMetrics",
                              "enabled": "[parameters('metricsEnabled')]"
                            }
                          ],
                          "logs": [
                            {
                              "category": "StorageRead",
                              "enabled": "[parameters('logsEnabled')]"
                            }
                          ]
                        }
                      }
                    ],
                    "outputs": {}
                  },
                  "parameters": {
                    "location": {
                      "value": "[field('location')]"
                    },
                    "resourceName": {
                      "value": "[field('fullName')]"
                    },
                    "logAnalytics": {
                      "value": "[parameters('logAnalytics')]"
                    },
                    "metricsEnabled": {
                      "value": "[parameters('metricsEnabled')]"
                    },
                    "logsEnabled": {
                      "value": "[parameters('logsEnabled')]"
                    },
                    "profileName": {
                      "value": "[parameters('profileName')]"
                    }
                  }
                }
              }
            }
          }
        }
      },
      "id": "/providers/Microsoft.Authorization/policyDefinitions/b4fe1a3b-0715-4c6c-a5ea-ffc33cf823cb/versions/4.0.0",
      "type": "Microsoft.Authorization/policyDefinitions/versions",
      "name": "4.0.0"
    }
    return definition

storages_type=['blob','file','queue','table']
policy_name=["policy-la-blob-custom","policy-la-file-custom","policy-la-queue-custom","policy-la-table-custom",]
# definitions_id=["7bd000e3-37c7-4928-9f31-86c4b77c5c45","2fb86bf3-d221-43d1-96d1-2434af34eaa0","b4fe1a3b-0715-4c6c-a5ea-ffc33cf823cb","25a70cc8-2bd4-47f1-90b6-1478e4662c96"]

for i in range(0,4):
    policyClient.policy_definitions.create_or_update_at_management_group(policy_name[i], management_group, getDefinition(storages_type[i]))

    policy_assignment_details = PolicyAssignment(display_name=policy_name[i],
                                               policy_definition_id=f"/providers/Microsoft.Management/managementGroups/{management_group}/providers/Microsoft.Authorization/policyDefinitions/{policy_name[i]}",
                                                description="Updating log analytics",
                                                identity=policy_assignment_identity,
                                                location=assignment_location,
                                                parameters=parameters)

    policy_assignment = policyClient.policy_assignments.create(f"/providers/Microsoft.Management/managementGroups/{management_group}",
                                                              policy_name[i],
                                                              policy_assignment_details)
    
