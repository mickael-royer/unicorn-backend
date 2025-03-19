---
title: 'System Context Diagram'
weight: 9
tags: ['c4', 'system context']
image: 'index.png'
draft: false
---
# System Context Diagram

* [Introduction](#introduction)
* [Container Diagram (Archimate Diagram Model)](#container-diagram-archimate-diagram-model)
* [Architects (Business Actor)](#architects-business-actor)
* [Unicorn (Application Component)](#unicorn-application-component)
* [Google Drive (Application Component)](#google-drive-application-component)
* [Google Mail  (Application Component)](#google-mail--application-component)
* [Zappier (Application Component)](#zappier-application-component)
* [Auth0 (Application Component)](#auth0-application-component)
* [Google Identity (Application Component)](#google-identity-application-component)
* [Kindle Scribe (Device)](#kindle-scribe-device)

## Introduction

The Unicorn project is designed to streamline the documentation and sharing of architecture artifacts created on a Kindle Scribe. Its primary objective is to enable users to export diagrams and Architecture Decision Records (ADRs) from Kindle Scribe, convert them into Markdown format, and host them on a secure, static website for easy access and collaboration.

## Container Diagram (Archimate Diagram Model)

## Architects (Business Actor)

**Properties**

|Stereotype|
|---|
|Person|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Architects|Triggering Relationship|[Unicorn (Application Component)](#unicorn-application-component)|Consult Architecture Diagrams and Decision Records||
|Architects|Triggering Relationship|[Auth0 (Application Component)](#auth0-application-component)|AuthN||
|Architects|Triggering Relationship|[Kindle Scribe (Device)](#kindle-scribe-device)|Create Architecture Diagrams and Decision Records ||

Use Kindle Scribe to document diagrams and ADRs.

## Unicorn (Application Component)

**Properties**

|Stereotype|
|---|
|System Software|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Unicorn|Triggering Relationship|[Google Drive (Application Component)](#google-drive-application-component)|Import documents||
|Unicorn|Triggering Relationship|[Google Identity (Application Component)](#google-identity-application-component)|AuthN||

Handles the import, conversion, and publication of architecture artifacts.

## Google Drive (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Google|https://drive.google.com|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|

Stores files for further processing, with secure access through Google AuthN.

> Google Drive is used as file storage account
> cf. ADR 0008-file-storage

## Google Mail  (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Google|https://mail.google.com|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Google Mail |Triggering Relationship|[Zappier (Application Component)](#zappier-application-component)|Triger on mail reception||

Sends exported files as email attachments to a designated Gmail account.

## Zappier (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Zapier|https://zapier.com/|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Zappier|Triggering Relationship|[Google Drive (Application Component)](#google-drive-application-component)|Export mail attachment to Drive||

Automates the process of moving email attachments from Gmail to a Google Drive folder, eliminating manual steps in the export process.

> Zapier is used to automate export process
> cf. ADR 0007-automate-action

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

> Auth0 and Google Identity serve IAM purpose
> cf. 0014-identity-and-access-management

## Google Identity (Application Component)

**Properties**

|Stereotype|Provider|URL|
|---|---|---|
|System Software|Google|https://developers.google.com/identity|

> Auth0 and Google Identity serve IAM purpose
> cf. 0014-identity-and-access-management

## Kindle Scribe (Device)

**Properties**

|Stereotype|Provider|URL|Email|
|---|---|---|---|
|Device|Amazon|https://www.amazon.fr/gp/help/customer/display.html?nodeId=T4sq0EZZFwu9vvH3Fx|royerm_V64O4A@kindle.com|

**Relationships**

|From|Relationship|To|Name/Label|Description|
|---|---|---|---|---|
|Kindle Scribe|Triggering Relationship|[Google Mail  (Application Component)](#google-mail--application-component)|Export Notebooks||

Facilitates export of documents and diagrams.

> Kindle Scribe is used as a Personal Device
> cf. ADR 0006-scribe-personal-device
