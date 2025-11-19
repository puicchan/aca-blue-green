@description('Environment name')
param environmentName string

@description('Primary location for all resources')
param location string

@description('Container registry name')
param containerRegistryName string

@description('Container Apps environment name')
param containerAppsEnvironmentName string

@description('Container image name')
param imageName string

@description('User-assigned managed identity resource ID')
param identityId string

@description('CommitId for blue revision')
param blueCommitId string

@description('CommitId for green revision')
param greenCommitId string = ''

@description('CommitId for the latest deployed revision')
param latestCommitId string = ''

@allowed(['blue', 'green'])
@description('Name of the label that gets 100% of the traffic')
param productionLabel string = 'blue'

// Use service name for container app name
var containerAppName = 'web'

// Calculate current commit ID and sanitize for revision names
var currentCommitId = !empty(latestCommitId) ? latestCommitId : blueCommitId
var sanitizedBlueCommitId = replace(replace(toLower(blueCommitId), '.', ''), '_', '-')
var sanitizedGreenCommitId = !empty(greenCommitId) ? replace(replace(toLower(greenCommitId), '.', ''), '_', '-') : ''

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' existing = {
  name: containerRegistryName
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2022-03-01' existing = {
  name: containerAppsEnvironmentName
}

resource webApp 'Microsoft.App/containerApps@2025-02-02-preview' = {
  name: containerAppName
  location: location
  tags: {
    'azd-env-name': environmentName
    'azd-service-name': 'web'
    blueCommitId: blueCommitId
    greenCommitId: greenCommitId
    latestCommitId: currentCommitId
    productionLabel: productionLabel
  }
  properties: {
    environmentId: containerAppsEnvironment.id
    configuration: {
      maxInactiveRevisions: 10
      ingress: {
        external: true
        targetPort: 8000
        transport: 'http'
        traffic: !empty(greenCommitId) ? [
          {
            revisionName: '${containerAppName}--${sanitizedBlueCommitId}'
            weight: productionLabel == 'blue' ? 100 : 0
            label: 'blue'
          }
          {
            revisionName: '${containerAppName}--${sanitizedGreenCommitId}'
            weight: productionLabel == 'green' ? 100 : 0
            label: 'green'
          }
        ] : [
          {
            latestRevision: true
            weight: 100
            label: 'blue'
          }
        ]
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: identityId
        }
      ]
      activeRevisionsMode: 'Multiple'
    }
    template: {
      revisionSuffix: replace(replace(replace(toLower(currentCommitId), '.', ''), '_', '-'), '/', '-')
      containers: [
        {
          image: imageName
          name: 'ai-chatbot'
          env: concat([
            {
              name: 'COMMIT_ID'
              value: currentCommitId
            }
            {
              name: 'BLUE_COMMIT_ID'
              value: blueCommitId
            }
            {
              name: 'PRODUCTION_LABEL'
              value: productionLabel
            }
          ], !empty(greenCommitId) ? [
            {
              name: 'GREEN_COMMIT_ID'
              value: greenCommitId
            }
          ] : [])
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
      }
    }
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identityId}': {}
    }
  }
}

// Required outputs for azd Container Apps integration
output SERVICE_WEB_NAME string = webApp.name
output SERVICE_WEB_URI string = 'https://${webApp.properties.configuration.ingress.fqdn}'
output containerAppName string = webApp.name
