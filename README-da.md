<div style="text-align: center"><img src="images/tiger.jpg" width="700" /></div>

# Purview *Stuff*

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![dk](https://img.shields.io/badge/lang-dk-red.svg)](README-da.md)
[![de](https://img.shields.io/badge/lang-de-yellow.svg)](README-de.md)
[![main](https://img.shields.io/badge/main-document-green.svg)](README-da.md)

## Introduktion

Dette repository indholder information jeg har samlet over årene i forbindelse med de Purview projekter jeg har haft hos kunder.

## Powerpoint's

Følgende liste viser de tilgængelige Powerpoint samt deres status.

>[!Note]
>Dette indholder erstatter ikke den officielle Purview dokumentation.  
>Opdateringer sker I det omfang jeg har tid.  
>Alle slides er på engelsk.

### Purview-oversigt ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :green_circle:[Oversigt](Presentations/1-Intro/Purview-overview.PPTX) En masse forskellige ting, dog ikke særlig velorganiseret :smile:
2. :green_circle:[Retention](Presentations/1-Intro/Purview-retention-policies.PPTX) Retention teknikker for både M365 og Azure.brug
3. :green_circle:[Prissætning](Presentations/1-Intro/Purview-pricing.PPTX) Pris model for Purview Data Governance.
4. :green_circle:[Scanning](Presentations/1-Intro/Purview-scaning.pptx) Scanning – kilde oversigt

### Getting started ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :green_circle:[Democase](Presentations/2-Getting%20Started/Purview-democase.pptx) Demo case der bruges i de screen shots der i præsentationerne
2. :green_circle:[Opsætning](Presentations/2-Getting%20Started/Purview-1-setup.pptx) Opsætning af Purview til første gangs brug
3. :green_circle:[Datamap](Presentations/2-Getting%20Started/Purview-2-datamap.pptx) Data Map - opsætning af domæner, collections og data assets ved brug af scanning
4. :yellow_circle:[Unified-catalog](Presentations/2-Getting%20Started/Purview-3-unified-catalog.pptx) Unified catalog - etablering af governance domæner, data produkter samt yderligere information
5. :red_circle:[Data-quality](Presentations/2-Getting%20Started/Purview-4-data-quality.pptx) Data Quality - opsætning, håndtering og rapportering

### Advanced ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :red_circle:[Advanceret](Presentations/3-Advanced/Purview-1-advanced.pptx) Advanceret indhold
2. :yellow_circle:[APIs](Presentations/3-Advanced/Purview-2-APIs.pptx) API's, hvad man kan bruge dem til og hvorledes dette gøres

## Scripts

Nogle små scripts til forskellige praktiske opgaver. Tilpas dem efter egne behov.

>[!Note]
> **Disse scripts stilles til rådighed "as is" uden nogen garanti for at de ville virke i "hvilket som helst" miljø.**.  
> **De *skal* altså justeres og sikres at de vil virke i jeres eget miljø.**


1. Slet assets hørende til en given collection [Delete collection](Scripts/delete_collection.sh).  
   **Bemærk** at dette script skal ændres om man bruger det på Linux eller MacOS. Søg f.eks. efter teksten "MacOS".
2. Python script for update data assets: [Python update](Scripts/update_assets.py)
4. Python script to test the connection to Purview: [Connection](Scripts/purview_connect.py)
3. Et Purview script setup til at indsætte metadata:[Load script](<https://github.com/jcordtz/load_script>)

## Andre relaterede GitHub repositories (mine egne :smile:)

1. En moderne data platform: <https://github.com/jcordtz/a_data_platform>

## Smarte værktøjer til forskellige opgaver

1. Data masking baseret på Python: <https://microsoft.github.io/presidio/>  
2. Dannelse af syntetiske data: <https://github.com/sdv-dev/SDV/blob/main/README.md> (både Open Source og licens)  

## Purview reporting/analytics

1. Purview self-serve analytics: <https://learn.microsoft.com/en-us/purview/unified-catalog-self-serve-analytics>

## En liste af Purview links, som kan vise sig brugbare

Data kilder og hvorledes man forbinder til disse: <https://learn.microsoft.com/en-us/purview/data-map-data-sources>  

Roadmap: <https://learn.microsoft.com/en-us/purview/whats-new>  

PyApacheAtlas (Python SDK): <https://github.com/wjohnson/pyapacheatlas>  
Azure Purview CLI: <https://github.com/tayganr/purviewcli>  

Purview Rest API's: <https://learn.microsoft.com/en-us/rest/api/purview/>
Purview Python SDK's: <https://azure.github.io/azure-sdk-for-python/purview.html>
Purview og Open Source tools: <https://learn.microsoft.com/en-us/purview/legacy/tutorial-azure-purview-tools>
Apache Atlas v2 documentation: <https://atlas.apache.org/api/v2/index.html>  
Azure Purview API deep-dive video: <https://www.youtube.com/watch?v=4qzjnMf1GN4>  

Træning #1: <https://learn.microsoft.com/en-us/purview/>  
Træning #2: <https://learn.microsoft.com/en-us/training/purview/>  
Træning #3: <https://learn.microsoft.com/en-us/training/paths/describe-capabilities-of-microsoft-compliance-solutions/>  
Træning #4: <https://learn.microsoft.com/en-us/training/modules/describe-purview-data-governance/>  
Træning #5: <https://github.com/tayganr/purviewlab>  

Purview StarterKit: <https://techcommunity.microsoft.com/t5/azure-purview/getting-started-with-azure-purview-using-purview-starter-kit-cli/m-p/2645574>  
Tutorial for creating custom lineage: <https://piethein.medium.com/use-azure-purviews-rest-apis-for-creating-custom-lineage-ad8efacc6230>  
Tutorial for scanning Delta Lake: <https://www.youtube.com/watch?v=pk0Gx_HHY4A>  
Community: <https://techcommunity.microsoft.com/category/microsoft-purview>  

### 3. parts tools som er integreret med Purview

MDM - Cluedin : <https://www.cluedin.com/product/microsoft-purview-mdm-integration>  
MDM - Profisee: <https://profisee.com/solutions/microsoft-enterprise/>  
MDM - Reltio: <https://learn.reltio.com/reltio-integration-for-microsoft-purview>  
MDM - Semarchy: <https://www.semarchy.com/doc/semarchy-xdm/xdm/latest/Install/azure/purview/integrate-xdm-with-purview.html>  

Lineage – Solidatus: <https://www.solidatus.com/partners/microsoft-purview-partnership/>  

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![dk](https://img.shields.io/badge/lang-da-red.svg)](README-da.md)
[![de](https://img.shields.io/badge/lang-de-yellow.svg)](README-de.md)
[![main](https://img.shields.io/badge/main-document-green.svg)](README-da.md)