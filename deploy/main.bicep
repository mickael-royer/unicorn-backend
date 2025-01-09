param location string = resourceGroup().location
param environmentName string = 'env-unicorn-dev'

param minReplicas int = 1

param nodeImage string
param nodePort int = 3001

param pythonImage string
param pythonPort int = 5001

param goImage string
param goPort int = 8050

param isPrivateRegistry bool = true

param containerRegistry string = 'ghcr.io'
param containerRegistryUsername string = 'mickael-royer'
@secure()
param containerRegistryPassword string = ''
param registryPassword string = 'registry-password'

@secure()
param pubsubAccesskey string = ''

@secure()
param statestoreMasterkey string = ''

var nodeServiceAppName = 'unicorn-bff'
var pythonServiceAppName = 'unicorn-process'
var goServiceAppName = 'unicorn-publish'


// Container Apps Environment 
module environment 'environment.bicep' = {
  name: '${deployment().name}--environment'
  params: {
    environmentName: environmentName
    location: location
    appInsightsName: '${environmentName}-ai'
    logAnalyticsWorkspaceName: '${environmentName}-la'
  }
}

// Python App
module pythonService 'container-http.bicep' = {
  name: '${deployment().name}--${pythonServiceAppName}'
  dependsOn: [
    environment
  ]
  params: {
    enableIngress: true
    isExternalIngress: false
    location: location
    environmentName: environmentName
    containerAppName: pythonServiceAppName
    containerImage: pythonImage
    containerPort: pythonPort
    isPrivateRegistry: isPrivateRegistry 
    minReplicas: minReplicas
    containerRegistry: containerRegistry
    registryPassword: registryPassword
    containerRegistryUsername: containerRegistryUsername
    revisionMode: 'Single'
    secrets: [
      {
        name: registryPassword
        value: containerRegistryPassword
      }
    ]
  }
}

// Go App
module goService 'container-http.bicep' = {
  name: '${deployment().name}--${goServiceAppName}'
  dependsOn: [
    environment
  ]
  params: {
    enableIngress: true
    isExternalIngress: false
    location: location
    environmentName: environmentName
    containerAppName: goServiceAppName
    containerImage: goImage
    containerPort: goPort
    isPrivateRegistry: isPrivateRegistry
    minReplicas: minReplicas
    containerRegistry: containerRegistry
    registryPassword: registryPassword
    containerRegistryUsername: containerRegistryUsername
    revisionMode: 'Single'
    secrets: isPrivateRegistry ? [
      {
        name: registryPassword
        value: containerRegistryPassword
      }
    ] : []
  }
}

// Node App
module nodeService 'container-http.bicep' = {
  name: '${deployment().name}--${nodeServiceAppName}'
  dependsOn: [
    environment
  ]
  params: {
    enableIngress: true 
    isExternalIngress: true
    location: location
    environmentName: environmentName
    containerAppName: nodeServiceAppName
    containerImage: nodeImage
    containerPort: nodePort
    minReplicas: minReplicas
    isPrivateRegistry: isPrivateRegistry 
    containerRegistry: containerRegistry
    registryPassword: registryPassword
    containerRegistryUsername: containerRegistryUsername
    revisionMode: 'Single'
    secrets: [
      {
        name: registryPassword
        value: containerRegistryPassword
      }
    ]
  }
}

// Dapr Component for Azure Event Bus PubSub
resource pubsubDaprComponent 'Microsoft.App/managedEnvironments/daprComponents@2024-03-01' = {
  name: '${environmentName}/files'
  dependsOn: [
    environment
  ]
  properties: {
    componentType: 'pubsub.azure.servicebus.queues'
    version: 'v1'
    metadata: [
      {
        name: 'connectionString'
        value: 'Endpoint=sb://royerm.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=${pubsubAccesskey}'
      }
    ]
    scopes: [
      nodeServiceAppName
      pythonServiceAppName
    ]
  }
}

// Dapr Component for CosmosDB StateStore
resource stateDaprComponent 'Microsoft.App/managedEnvironments/daprComponents@2024-03-01' = {
  name: '${environmentName}/filestore'
  dependsOn: [
    environment
  ]
  properties: {
    componentType: 'state.azure.cosmosdb'
    version: 'v1'
    secrets: [
      {
        name: 'masterkey'
        value: statestoreMasterkey
      }
    ]
    metadata: [
      {
        name: 'url'
        value: 'https://account-cosmodb-westeurope.documents.azure.com:443/'
      }
      {
        name: 'database'
        value: 'filesDB'
      }
      {
        name: 'collection'
        value: 'files'
      }
      {
        name: 'masterkey'
        secretRef: 'masterkey'
      }
      {
        name: 'keyPrefix'
        value: 'none'
      }
    ]
    scopes: [
      pythonServiceAppName
      goServiceAppName
    ]
  }
}

output nodeFqdn string = nodeService.outputs.fqdn
output pythonFqdn string = pythonService.outputs.fqdn
output goFqdn string = goService.outputs.fqdn
