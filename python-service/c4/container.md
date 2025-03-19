---
title: 'Container Diagram'
weight: 7
tags: ['c4', 'container']
image: 'index.png'
draft: false
---
# Container Diagram

* [Introduction](#introduction)
* [Unicorn (Application Component)](#unicorn-application-component)
  * [Components Diagram (Archimate Diagram Model)](#components-diagram-archimate-diagram-model)
  * [Frontend (Application Component)](#frontend-application-component)
    * [React (Application Function)](#react-application-function)
    * [Ionic (Application Function)](#ionic-application-function)
  * [Backend (Application Component)](#backend-application-component)
    * [Express (Application Function)](#express-application-function)
  * [Static Website (Application Component)](#static-website-application-component)
    * [Hugo (Application Function)](#hugo-application-function)
  * [File Process (Application Component)](#file-process-application-component)
    * [FastAPI (Application Function)](#fastapi-application-function)
  * [File Publish (Application Component)](#file-publish-application-component)
    * [Gorilla Mux (Application Function)](#gorilla-mux-application-function)
* [Google Drive (Application Component)](#google-drive-application-component)
* [Google Identity (Application Component)](#google-identity-application-component)
* [Auth0 (Application Component)](#auth0-application-component)
* [MADR Tools (Application Function)](#madr-tools-application-function)
* [Ionos (Application Component)](#ionos-application-component)
* [Github (Application Component)](#github-application-component)
* [Google Gemini (Application Component)](#google-gemini-application-component)
* [Pusher (Application Component)](#pusher-application-component)

## Introduction

![Container Diagram][embedView]

System architecture for the Unicorn project, which follows a Frontend/Backend pattern. The Frontend uses an Ionic framework with React (cf. ADR 0013-frontend-framework) and integrates Auth0 for secure user authentication via Authorization Code Flow with PKCE. It connects to Google Identity to obtain access tokens, enabling access to Google Drive for file storage and management.

The Backend consists of:A Backend for Frontend (BFF) implemented using Express (cf. ADR 0015-backend-framework) to interact with Google Drive via APIs.
A File Process microservice, implemented with FastAPI, to process Markdown files.
The system also supports a Static Website, built with Hugo, to display project documentation, Archimate diagrams, and Architecture Decision Records (ADRs). Processed Markdown files are pushed to a GitHub repository via API, ensuring version control. MADR Tools facilitate the creation and management of ADRs.

## Unicorn (Application Component)

**Properties**

|Stereotype|
|---|
|System Software|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Unicorn|Composition Relationship|[Frontend (Application Component)](#frontend-application-component)|||
|Unicorn|Composition Relationship|[Backend (Application Component)](#backend-application-component)|||
|Unicorn|Composition Relationship|[Static Website (Application Component)](#static-website-application-component)|||
|Unicorn|Composition Relationship|[File Process (Application Component)](#file-process-application-component)|||
|Unicorn|Composition Relationship|[File Publish (Application Component)](#file-publish-application-component)|||

Handles the import, conversion, and publication of architecture artifacts.

### Components Diagram (Archimate Diagram Model)

Backend for Frontend (BFF) architecture that facilitates secure access to Google Drive and integrates with GitHub for file management. The BFF handles user authentication via Google Identity to interact with Google Drive APIs for listing, updating, and downloading files. A File Process Microservice asynchronously processes Markdown files using a Pub/Sub mechanism and pushes the processed files to GitHub for version control. The architecture ensures separation of concerns, secure access, and scalability for file processing and artifact storage.

### Frontend (Application Component)

**Properties**

|Stereotype|Github|
|---|---|
|Container|https://github.com/mickael-royer/unicorn-ionic|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Frontend|Assignment Relationship|[React (Application Function)](#react-application-function)|||
|Frontend|Assignment Relationship|[Ionic (Application Function)](#ionic-application-function)|||
|Frontend|Triggering Relationship|[Auth0 (Application Component)](#auth0-application-component)|OIDC|Authorization Code Flow with PKCE https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce|
|Frontend|Triggering Relationship|[Backend (Application Component)](#backend-application-component)|List Drive||

Frontend based on Ionic and Auth0 authentication

#### React (Application Function)

**Properties**

|Stereotype|
|---|
|Component|

#### Ionic (Application Function)

**Properties**

|Stereotype|
|---|
|Component|

### Backend (Application Component)

**Properties**

|Stereotype|Github|
|---|---|
|Container|https://github.com/mickael-royer/unicorn-express-server|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Backend|Assignment Relationship|[Express (Application Function)](#express-application-function)|||
|Backend|Triggering Relationship|[Google Drive (Application Component)](#google-drive-application-component)|REST API|Access Google Drive via API|
|Backend|Triggering Relationship|[Google Identity (Application Component)](#google-identity-application-component)|REST API|Get Access Token via API|
|Backend|Flow Relationship|[File Process (Application Component)](#file-process-application-component)|||

Backend for Frontend (BFF) to support Google Drive acces.

#### Express (Application Function)

**Properties**

|Stereotype|URL|
|---|---|
|Component|https://expressjs.com|

Express is a fast, unopinionated, minimalist web framework for Node.js, providing a robust set of features for web and mobile applications.

### Static Website (Application Component)

**Properties**

|Stereotype|Github|
|---|---|
|Container|https://github.com/mickael-royer/unicorn-hugo-website|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Static Website|Assignment Relationship|[Hugo (Application Function)](#hugo-application-function)|||

Website to support Project Documentation, Archimate and Architecture Decision Record repositories

#### Hugo (Application Function)

**Properties**

|Stereotype|URL|
|---|---|
|Component|https://gohugo.io/|

### File Process (Application Component)

**Properties**

|Stereotype|
|---|
|Container|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|File Process|Assignment Relationship|[FastAPI (Application Function)](#fastapi-application-function)|||
|File Process|Triggering Relationship|[File Publish (Application Component)](#file-publish-application-component)|||
|File Process|Triggering Relationship|[Pusher (Application Component)](#pusher-application-component)|REST API||

Microservice to process and enhance Markdown file

#### FastAPI (Application Function)

**Properties**

|Stereotype|URL|
|---|---|
|Component|https://fastapi.tiangolo.com/|

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

### File Publish (Application Component)

**Properties**

|Stereotype|
|---|
|Container|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|File Publish|Assignment Relationship|[Gorilla Mux (Application Function)](#gorilla-mux-application-function)|||
|File Publish|Triggering Relationship|[Github (Application Component)](#github-application-component)|Push|Push change to repository via API|
|File Publish|Triggering Relationship|[Google Gemini (Application Component)](#google-gemini-application-component)|Prompt|Generate ADR Synthesis|

Microservice to publish Markdown file

#### Gorilla Mux (Application Function)

**Properties**

|Stereotype|URL|
|---|---|
|Component|https://github.com/gorilla/mux|

Package gorilla/mux implements a request router and dispatcher for matching incoming requests to their respective handler.

## Google Drive (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Google|https://drive.google.com|

Stores files for further processing, with secure access through Google AuthN.

## Google Identity (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Google|https://developers.google.com/identity|

## Auth0 (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Okta|https://auth0.com/|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Auth0|Triggering Relationship|[Google Identity (Application Component)](#google-identity-application-component)|AuthN||

Manages secure user authentication and access control.

## MADR Tools (Application Function)

**Properties**

|Stereotype|Github|
|---|---|
|Component|https://github.com/butonic/adr-tools|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|MADR Tools|Triggering Relationship|[Static Website (Application Component)](#static-website-application-component)|Push MADR||

Markdown Architecture Decision Record Tools

## Ionos (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Ionos|https://www.ionos.fr/|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Ionos|Flow Relationship|[Frontend (Application Component)](#frontend-application-component)|||

DNS domain and SSL Provider

## Github (Application Component)

**Properties**

|Stereotype|URL|Registry|
|---|---|---|
|System Software|https://github.com/mickael-royer|https://github.com/mickael-royer?tab=packages|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Github|Triggering Relationship|[Static Website (Application Component)](#static-website-application-component)|Deploy|Deploy Hugo Website to Static Web App|

Code and Artefact repository with version control.


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

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Pusher|Triggering Relationship|[Frontend (Application Component)](#frontend-application-component)|Webb Socket||

Cross-platform API for native programmatic push notifications.
