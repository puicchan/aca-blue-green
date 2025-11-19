targetScope = 'subscription'

// Parameters
@description('Location for all resources')
param location string

@description('Environment name for resource naming')
param environmentName string

// Naming conventions
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var prefix = '${environmentName}-${resourceToken}'

// Create resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: {
    'azd-env-name': environmentName
  }
}

// Resource names
var containerRegistryName = 'cr${take(replace(resourceToken, '-', ''), 20)}'
var logAnalyticsWorkspaceName = '${prefix}-logs'
var containerAppsEnvironmentName = '${prefix}-env'

// Abbreviations for resource naming
var abbrs = {
  managedIdentityUserAssignedIdentities: 'id-'
}
var tags = {
  'azd-env-name': environmentName
}

// User-assigned managed identity for Container Apps
module webIdentity 'br/public:avm/res/managed-identity/user-assigned-identity:0.4.1' = {
  name: 'webIdentity'
  scope: rg
  params: {
    name: '${abbrs.managedIdentityUserAssignedIdentities}web-${resourceToken}'
    location: location
    tags: tags
  }
}

// Deploy Log Analytics Workspace using AVM
module logAnalyticsWorkspace 'br/public:avm/res/operational-insights/workspace:0.12.0' = {
  name: 'log-analytics-deployment'
  scope: rg
  params: {
    name: logAnalyticsWorkspaceName
    location: location
    skuName: 'PerGB2018'
    dataRetention: 30
    tags: {
      'azd-env-name': environmentName
    }
  }
}

// Deploy Container Registry using AVM
module containerRegistry 'br/public:avm/res/container-registry/registry:0.9.3' = {
  name: 'container-registry-deployment'
  scope: rg
  params: {
    name: containerRegistryName
    location: location
    acrSku: 'Premium'
    acrAdminUserEnabled: true
    publicNetworkAccess: 'Enabled'
    networkRuleBypassOptions: 'AzureServices'
    exportPolicyStatus: 'enabled'  // Required when publicNetworkAccess is Enabled
    retentionPolicyStatus: 'enabled'
    retentionPolicyDays: 7
    zoneRedundancy: 'Disabled'
    roleAssignments: [
      {
        principalId: webIdentity.outputs.principalId
        principalType: 'ServicePrincipal'
        roleDefinitionIdOrName: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
      }
    ]
    tags: {
      'azd-env-name': environmentName
    }
  }
}

// Deploy Container Apps Environment directly (not using AVM due to public access issue)
module containerAppsEnvironment './modules/container-apps-environment.bicep' = {
  name: 'container-apps-environment-deployment'
  scope: rg
  params: {
    name: containerAppsEnvironmentName
    location: location
    logAnalyticsWorkspaceId: logAnalyticsWorkspace.outputs.resourceId
    tags: tags
  }
}

// Note: Container App will be created by azd during deploy phase
// This follows the revision-based deployment strategy where azd manages the container app

// Outputs for azd conventions
@description('The Container Registry endpoint for azd')
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.outputs.loginServer

@description('The Container Registry name for azd')
output AZURE_CONTAINER_REGISTRY_NAME string = containerRegistry.outputs.name

@description('The Container Apps Environment ID for azd')
output AZURE_CONTAINER_APPS_ENVIRONMENT_ID string = containerAppsEnvironment.outputs.resourceId

@description('The Container Apps Environment name for deployment')
output AZURE_CONTAINER_APPS_ENVIRONMENT_NAME string = containerAppsEnvironmentName

@description('The user-assigned managed identity resource ID for web service')
output SERVICE_WEB_IDENTITY_ID string = webIdentity.outputs.resourceId

@description('The Container Registry resource ID for azd')
output AZURE_CONTAINER_REGISTRY_RESOURCE_ID string = containerRegistry.outputs.resourceId

@description('The web service container app name')
output SERVICE_WEB_NAME string = 'web'
