---
title: 'Infrastructure Diagram'
weight: 1
tags: ['c4', 'deployement']
image: 'index.png'
draft: false
---
# Infrastructure Diagram

![image](index.png)

* [Introduction](#introduction)
* [Container Instance (Node)](#container-instance-node)
* [Cosmos DB (Node)](#cosmos-db-node)
* [Storage Account (Node)](#storage-account-node)
* [Bicep (Application Function)](#bicep-application-function)
* [Managed Environment (Node)](#managed-environment-node)
  * [App Insight (Technology Service)](#app-insight-technology-service)
  * [Log Analytics Workspace (Technology Service)](#log-analytics-workspace-technology-service)
* [Static Web App (Node)](#static-web-app-node)
* [Github (Application Component)](#github-application-component)
* [Sonar Cloud (Application Component)](#sonar-cloud-application-component)
* [Dependabot (Application Component)](#dependabot-application-component)

## Introduction

Infrastructure diagram with an emphasis on infrastructure as code (IaC), automation, and quality assurance. 

> - Bicep (IaC Component)
Automates the provisioning of infrastructure (Container Instances, Cosmos DB, Storage Account) within a Managed Environment. It ensures repeatability and consistency.
> - Managed Environment
Provides observability through App Insights and Log Analytics Workspace, addressing monitoring and operational concerns.
> - GitHub
Acts as the source code repository and orchestrates triggers for creating deployment nodes (e.g., Static Web App) and integrating automated quality and security checks.

DevSecOps Integrations:

> - Dependabot
Performs dependency analysis to identify outdated or vulnerable libraries.
> - SonarCloud
Conducts software quality analysis, ensuring code adheres to security and quality standards.

This architecture enforces secure, automated deployment practices while maintaining visibility, ensuring infrastructure consistency, and embedding security checks early in the CI/CD pipeline.

## Container Instance (Node)

**Properties**

|Stereotype|
|---|
|Deployment Node|

## Cosmos DB (Node)

**Properties**

|Stereotype|
|---|
|Deployment Node|

## Storage Account (Node)

**Properties**

|Stereotype|
|---|
|Deployment Node|

## Bicep (Application Function)

**Properties**

|Stereotype|
|---|
|Component|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Bicep|Triggering Relationship|[App Insight (Technology Service)](#app-insight-technology-service)|Setup||
|Bicep|Triggering Relationship|[Log Analytics Workspace (Technology Service)](#log-analytics-workspace-technology-service)|Setup||
|Bicep|Triggering Relationship|[Container Instance (Node)](#container-instance-node)|Create||
|Bicep|Triggering Relationship|[Cosmos DB (Node)](#cosmos-db-node)|Create||
|Bicep|Triggering Relationship|[Storage Account (Node)](#storage-account-node)|Create||

Infrastructure as Code (IaC)

https://github.com/Azure-Samples/container-apps-store-api-microservice/blob/main/deploy/main.bicep

## Managed Environment (Node)

**Properties**

|Stereotype|
|---|
|Deployment Node|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Managed Environment|Assignment Relationship|[App Insight (Technology Service)](#app-insight-technology-service)|||
|Managed Environment|Assignment Relationship|[Log Analytics Workspace (Technology Service)](#log-analytics-workspace-technology-service)|||

Managed environments are primarily designed for hosting Azure Functions, Web Apps, and other Azure App Services in a more controlled, secure, and scalable way.

### App Insight (Technology Service)

### Log Analytics Workspace (Technology Service)

## Static Web App (Node)

**Properties**

|Stereotype|
|---|
|Deployment Node|

Managed platform for building and deploying static web applications.

## Github (Application Component)

**Properties**

|Stereotype|URL|Registry|
|---|---|---|
|System Software|https://github.com/mickael-royer|https://github.com/mickael-royer?tab=packages|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Github|Triggering Relationship|[Sonar Cloud (Application Component)](#sonar-cloud-application-component)|||
|Github|Triggering Relationship|[Dependabot (Application Component)](#dependabot-application-component)|||
|Github|Triggering Relationship|[Bicep (Application Function)](#bicep-application-function)|Trigger||
|Github|Triggering Relationship|[Static Web App (Node)](#static-web-app-node)|Create||

Code and Artefact repository with version control.


## Sonar Cloud (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Sonarsource|https://sonarcloud.io/|

Software Quality Analysis

## Dependabot (Application Component)

**Properties**

|Stereotype|
|---|
|System Software|

Dependency Analysis
