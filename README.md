<div style="text-align: center"><img src="images/tiger.jpg" width="700" /></div>

# Purview *Stuff*

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![dk](https://img.shields.io/badge/lang-dk-red.svg)](README-da.md)
[![de](https://img.shields.io/badge/lang-de-yellow.svg)](README-de.md)
[![main](https://img.shields.io/badge/main-document-green.svg)](README.md)

## Introduction

This repository contains info I have gathered through Purview customer projects over the years.

## Powerpoint's

In the current list you will find PowerPoint's and there status. 

The color code is as follows :green_circle: - content is ready, :yellow_circle: - working on it and :red_circle: - not started yet.

>[!Note]
>This information does not replace official Microsoft Purview Data Governance documentation.  
>It is kept up-to-date as I have time to do so.  
>All slides are in english

### Purview overview ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :green_circle:[Stuff](Presentations/1-Intro/Purview-overview.PPTX) A lot of different stuff: Content is ready to use but not that well organized :smile:
2. :green_circle:[Retention](Presentations/1-Intro/Purview-retention-policies.PPTX) Retention technics for both M365 and Azure
3. :green_circle:[Pricing](Presentations/1-Intro/Purview-pricing.PPTX) Pricing model for Purview Data Governance.
4. :green_circle:[Scanning](Presentations/1-Intro/Purview-scaning.pptx) Scanning – source overview

### Getting started ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :green_circle:[Demo-case](Presentations/2-Getting%20Started/Purview-democase.pptx) Description of the demo case used in the screen shots.
2. :green_circle:[Setup](Presentations/2-Getting%20Started/Purview-1-setup.pptx) Inital setup, how to get Purview Data Governance ready for use.
3. :green_circle:[Data Map](Presentations/2-Getting%20Started/Purview-2-datamap.pptx) Data Map, how to create domains, collections and data assets using scanning.
4. :yellow_circle:[Unified catalog](Presentations/2-Getting%20Started/Purview-3-unified-catalog.pptx) Unified catalog, establish governance domains, data products and added content
5. :red_circle:[Data Quality](Presentations/2-Getting%20Started/Purview-4-data-quality.pptx) Data Quality, how to create, use and run.

### Advanced ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :red_circle:[Advanced](Presentations/3-Advanced/Purview-1-advanced.pptx) Advanced stuff
2. :yellow_circle:[APIs](Presentations/3-Advanced/Purview-2-APIs.pptx) API's, what can be done with them and how to use them.

## Scripts

Some small scripts that can be used for different small handy tasks. Please adjust to your specific needs.

>![Note]
> These scripts are provided as is and hence with no guarentee they will work in "any" environment.
> So, you must adjust and ensure they will work in your environment.

1. Delete assets in a given collection [Delete collection](Scripts/delete_collection.sh).  
   **Note** that this script must be modified depending on whether it is used on Linux or macOS.  
   For example, search for the text ‘MacOS’.
2. Python script for update data assets: [Python update](Scripts/update_assets.py)
3. A Purview script setup for loading metadata: https://github.com/jcordtz/load_script  

## Related GitHub repositories (of mine :smile:)

1. A modern data platform: https://github.com/jcordtz/a_data_platform  

## Handy tools for different tasks

Data masking based on Python: https://microsoft.github.io/presidio/
Synthetic Data creation: https://github.com/sdv-dev/SDV/blob/main/README.md (both Open Source and licensable)

## Purview reporting/analytics

Purview self-serve analytics: https://learn.microsoft.com/en-us/purview/unified-catalog-self-serve-analytics

## A list of Purview useful links, that can come in handy

Data sources and howto connect: https://learn.microsoft.com/en-us/purview/data-map-data-sources  

Roadmap: https://learn.microsoft.com/en-us/purview/whats-new  

Purview Rest API's: https://learn.microsoft.com/en-us/rest/api/purview/
Purview Python SDK's: https://azure.github.io/azure-sdk-for-python/purview.html
Purview and Open Source tools: https://learn.microsoft.com/en-us/purview/legacy/tutorial-azure-purview-tools
PyApacheAtlas (Python SDK): https://github.com/wjohnson/pyapacheatlas  
Azure Purview CLI: https://github.com/tayganr/purviewcli  

Apache Atlas v2 documentation: https://atlas.apache.org/api/v2/index.html  
Azure Purview API deep-dive video: https://www.youtube.com/watch?v=4qzjnMf1GN4  

Training #1: https://learn.microsoft.com/en-us/purview/  
Training #2: https://learn.microsoft.com/en-us/training/purview/  
Training #3: https://learn.microsoft.com/en-us/training/paths/describe-capabilities-of-microsoft-compliance-solutions/  
Training #4: https://learn.microsoft.com/en-us/training/modules/describe-purview-data-governance/  
Training #5: https://github.com/tayganr/purviewlab  

Purview StarterKit: https://techcommunity.microsoft.com/t5/azure-purview/getting-started-with-azure-purview-using-purview-starter-kit-cli/m-p/2645574  
Tutorial for creating custom lineage: https://piethein.medium.com/use-azure-purviews-rest-apis-for-creating-custom-lineage-ad8efacc6230  
Tutorial for scanning Delta Lake: https://www.youtube.com/watch?v=pk0Gx_HHY4A  
Community: https://techcommunity.microsoft.com/category/microsoft-purview  

### 3rd Party tools integrated with Purview

MDM - Cluedin : https://www.cluedin.com/product/microsoft-purview-mdm-integration  
MDM - Profisee: https://profisee.com/solutions/microsoft-enterprise/  
MDM - Reltio: https://learn.reltio.com/reltio-integration-for-microsoft-purview  
MDM - Semarchy: https://www.semarchy.com/doc/semarchy-xdm/xdm/latest/Install/azure/purview/integrate-xdm-with-purview.html  

Lineage – Solidatus: https://www.solidatus.com/partners/microsoft-purview-partnership/  

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![dk](https://img.shields.io/badge/lang-da-red.svg)](README-da.md)
[![de](https://img.shields.io/badge/lang-de-yellow.svg)](README-de.md)
[![main](https://img.shields.io/badge/main-document-green.svg)](README.md)