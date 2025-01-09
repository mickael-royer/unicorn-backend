param redisName string = 'redis-pubsub'
param redisSku string = 'Basic' // You can change to Standard or Premium as needed
param redisCapacity int = 1 // Redis memory capacity in GB
param location string

resource redisCache 'Microsoft.Cache/Redis@2023-03-01' = {
  name: redisName
  location: location
  properties: {
    sku: {
      name: redisSku
      family: 'C'
      capacity: redisCapacity
    }
    enableNonSslPort: false
    redisVersion: '6'
  }
}

output redisHostName string = redisCache.properties.hostName
output redisPort int = redisCache.properties.sslPort
