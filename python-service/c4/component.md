---
title: 'Components Diagram'
weight: 5
tags: ['c4', 'container']
image: 'index.png'
draft: false
---
# Components Diagram

* [Introduction](#introduction)
* [Backend (Application Component)](#backend-application-component)
* [List Files (Application Interface)](#list-files-application-interface)
* [Update File Extension (Application Interface)](#update-file-extension-application-interface)
* [Download File (Application Interface)](#download-file-application-interface)
* [File Process (Application Component)](#file-process-application-component)
* [Process File (Application Interface)](#process-file-application-interface)
* [Auth Google (Application Interface)](#auth-google-application-interface)
* [Google Identity (Application Component)](#google-identity-application-component)
* [Google Drive (Application Component)](#google-drive-application-component)
* [Push File (Application Interface)](#push-file-application-interface)
* [Github (Application Component)](#github-application-component)
* [Frontend (Application Component)](#frontend-application-component)
* [Drive Component (Application Function)](#drive-component-application-function)
* [Static Website (Application Component)](#static-website-application-component)
* [ADR (Application Function)](#adr-application-function)
* [File Publish (Application Component)](#file-publish-application-component)
* [Google Gemini (Application Component)](#google-gemini-application-component)
* [Pusher (Application Component)](#pusher-application-component)

## Introduction

![Components Diagram][embedView]

Backend for Frontend (BFF) architecture that facilitates secure access to Google Drive and integrates with GitHub for file management. The BFF handles user authentication via Google Identity to interact with Google Drive APIs for listing, updating, and downloading files. A File Process Microservice asynchronously processes Markdown files using a Pub/Sub mechanism and pushes the processed files to GitHub for version control. The architecture ensures separation of concerns, secure access, and scalability for file processing and artifact storage.

## Backend (Application Component)

**Properties**

|Stereotype|Github|
|---|---|
|Container|https://github.com/mickael-royer/unicorn-express-server|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Backend|Aggregation Relationship|[List Files (Application Interface)](#list-files-application-interface)|||
|Backend|Aggregation Relationship|[Update File Extension (Application Interface)](#update-file-extension-application-interface)|||
|Backend|Aggregation Relationship|[Download File (Application Interface)](#download-file-application-interface)|||
|Backend|Composition Relationship|[Auth Google (Application Interface)](#auth-google-application-interface)|||

Backend for Frontend (BFF) to support Google Drive acces.

## List Files (Application Interface)

**Properties**

|Stereotype|Protocole|
|---|---|
|API|REST|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|List Files|Flow Relationship|[Google Drive (Application Component)](#google-drive-application-component)|list||

## Update File Extension (Application Interface)

**Properties**

|Stereotype|Protocole|
|---|---|
|API|REST|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Update File Extension|Flow Relationship|[Google Drive (Application Component)](#google-drive-application-component)|update||

Iterate through fileIds and update each file

## Download File (Application Interface)

**Properties**

|Stereotype|Protocole|
|---|---|
|API|REST|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Download File|Flow Relationship|[Process File (Application Interface)](#process-file-application-interface)|Pub/Sub||
|Download File|Flow Relationship|[Google Drive (Application Component)](#google-drive-application-component)|get||

## File Process (Application Component)

**Properties**

|Stereotype|
|---|
|Container|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|File Process|Aggregation Relationship|[Process File (Application Interface)](#process-file-application-interface)|||

Microservice to process and enhance Markdown file

## Process File (Application Interface)

**Properties**

|Stereotype|Protocole|
|---|---|
|API|REST|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Process File|Triggering Relationship|[Push File (Application Interface)](#push-file-application-interface)|State store|https://docs.dapr.io/developing-applications/building-blocks/state-management/howto-get-save-state/|
|Process File|Flow Relationship|[Google Gemini (Application Component)](#google-gemini-application-component)|prompt||
|Process File|Flow Relationship|[Pusher (Application Component)](#pusher-application-component)|notification||

Retrieve the message sent by the publisher
Extract the data field, which contains the file information
Extract the file content (base64 encoded) and other info
If content is base64 encoded, decode it first

## Auth Google (Application Interface)

**Properties**

|Stereotype|Protocole|
|---|---|
|API|REST|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Auth Google|Flow Relationship|[Google Identity (Application Component)](#google-identity-application-component)|getToken ||

## Google Identity (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Google|https://developers.google.com/identity|

## Google Drive (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Google|https://drive.google.com|

Stores files for further processing, with secure access through Google AuthN.

## Push File (Application Interface)

**Properties**

|Stereotype|Protocole|
|---|---|
|API|REST|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Push File|Flow Relationship|[Github (Application Component)](#github-application-component)|push|https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pushes/create?view=azure-devops-rest-7.1&tabs=HTTP|

## Github (Application Component)

**Properties**

|Stereotype|URL|Registry|
|---|---|---|
|System Software|https://github.com/mickael-royer|https://github.com/mickael-royer?tab=packages|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Github|Triggering Relationship|[ADR (Application Function)](#adr-application-function)|update||

Code and Artefact repository with version control.


## Frontend (Application Component)

**Properties**

|Stereotype|Github|
|---|---|
|Container|https://github.com/mickael-royer/unicorn-ionic|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Frontend|Assignment Relationship|[Drive Component (Application Function)](#drive-component-application-function)|||

Frontend based on Ionic and Auth0 authentication

## Drive Component (Application Function)

**Properties**

|Stereotype|
|---|
|Component|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Drive Component|Flow Relationship|[Backend (Application Component)](#backend-application-component)|fetch||

## Static Website (Application Component)

**Properties**

|Stereotype|Github|
|---|---|
|Container|https://github.com/mickael-royer/unicorn-hugo-website|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Static Website|Assignment Relationship|[ADR (Application Function)](#adr-application-function)|||

Website to support Project Documentation, Archimate and Architecture Decision Record repositories

## ADR (Application Function)

**Properties**

|Stereotype|
|---|
|Component|

## File Publish (Application Component)

**Properties**

|Stereotype|
|---|
|Container|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|File Publish|Aggregation Relationship|[Push File (Application Interface)](#push-file-application-interface)|||

Microservice to publish Markdown file

## Google Gemini (Application Component)

**Properties**

|Stereotype|URL|
|---|---|
|System Software|https://aistudio.google.com/|

LLM


## Pusher (Application Component)

**Properties**

|Stereotype|URL|
|---|---|
|System Software|https://dashboard.pusher.com/apps/1920401|

Cross-platform API for native programmatic push notifications.
