![microsoft](images/microsoft.png)

# Purview Stuff

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![dk](https://img.shields.io/badge/lang-dk-red.svg)](README-da.md)
[![de](https://img.shields.io/badge/lang-de-yellow.svg)](README-de.md)
[![main](https://img.shields.io/badge/main-document-green.svg)](README.md)

<div style="text-align: center"><img src="images/tiger.jpg" width="400" /></div>

## Einleitung

Dieses Repository enthält Informationen, die ich im Laufe der Jahre aus Purview‑Kundenprojekten gesammelt habe.

## Powerpoint's

In der aktuellen Liste finden Sie die PowerPoints und ihren Status.

Die Farbkennzeichnung ist wie folgt: :green_circle: – Inhalt ist bereit, :yellow_circle: – in Bearbeitung und :red_circle: – noch nicht begonnen.

>[!Note]
>Diese Informationen ersetzen nicht die offizielle Microsoft Purview Data >Governance‑Dokumentation.  
>Sie werden aktualisiert, sobald ich Zeit dafür habe.  
>Alle Folien sind auf Englisch.  

### Purview-übersicht ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :green_circle:[Ûbersicht](Presentations/1-Intro/Purview-overview.PPTX) Eine Menge verschiedener Dinge - Inhalt ist einsatzbereit, aber nicht besonders gut organisiert. :smile:
2. :green_circle:[Retention](Presentations/1-Intro/Purview-retention-policies.PPTX) Retentionstechniken für sowohl M365 als auch Azure.
3. :green_circle:[Preismodell](Presentations/1-Intro/Purview-pricing.PPTX) Preismodell für Purview Data Governance.
4. :green_circle:[Scanning](Presentations/1-Intro/Purview-scaning.pptx) Scanning – quellen übersicht.

### Getting started ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :green_circle:[Demo-case](Presentations/2-Getting%20Started/Purview-democase.pptx) Beschreibung des in den Screenshots verwendeten Demofalls.
2. :green_circle:[Setup](Presentations/2-Getting%20Started/Purview-1-setup.pptx) Ersteinrichtung – wie man Purview Data Governance für die Nutzung bereit macht.
3. :green_circle:[Data Map](Presentations/2-Getting%20Started/Purview-2-datamap.pptx) Data Map – wie man Domänen, Sammlungen und Data Assets mithilfe von Scans erstellt.
4. :yellow_circle:[Unified catalog](Presentations/2-Getting%20Started/Purview-3-unified-catalog.pptx) Unified Catalog – Aufbau von Governance-Domänen, Datenprodukten und zusätzlichem Inhalt.
5. :red_circle:[Data Quality](Presentations/2-Getting%20Started/Purview-4-data-quality.pptx) Data Quality – wie man sie erstellt, verwendet und ausführt.

### Advanced ![Powerpoint](images/PowerPoint_48x48.jpeg)

1. :red_circle:[Advanced](Presentations/3-Advanced/Purview-1-advanced.pptx) Fortgeschrittene Themen
2. :yellow_circle:[APIs](Presentations/3-Advanced/Purview-2-APIs.pptx) APIs – was man damit machen kann und wie man sie verwendet.

## Scripts

Einige kleine Skripte, die für verschiedene kleine, praktische Aufgaben verwendet werden können.  
Bitte passen Sie sie an Ihre spezifischen Anforderungen an.  

1. Assets in einer angegebenen Collection löschen [Delete collection](Scripts/delete_collection.sh).  
   Bitte beachten Sie, dass dieses Skript je nach Verwendung unter Linux oder macOS angepasst werden muss.  
   Suchen Sie beispielsweise nach dem Text ‚MacOS‘
2. Ein Purview-Skript-Setup zum Laden von Metadaten: https://github.com/jcordtz/load_script  

## Zugehörige GitHub‑Repositories (meine eigenen :smile:)

1. A modern data platform: https://github.com/jcordtz/a_data_platform  
2. Ein Purview-Skript-Setup zum Laden von Metadaten: https://github.com/jcordtz/load_script  

# Eine Sammlung nützlicher Purview‑Links, die hilfreich sein können

Datenquellen und wie man sie verbindet: https://learn.microsoft.com/en-us/purview/data-map-data-sources  

Roadmap: https://learn.microsoft.com/en-us/purview/whats-new  

PyApacheAtlas (Python SDK): https://github.com/wjohnson/pyapacheatlas  
Azure Purview CLI: https://github.com/tayganr/purviewcli  

Apache Atlas v2 documentation: https://atlas.apache.org/api/v2/index.html  
Azure Purview API deep-dive video: (ttps://www.youtube.com/watch?v=4qzjnMf1GN4  

Training #1: https://learn.microsoft.com/en-us/purview/  
Training #2: https://learn.microsoft.com/en-us/training/purview/  
Training #3: https://learn.microsoft.com/en-us/training/paths/describe-capabilities-of-microsoft-compliance-solutions/  
Training #4: https://learn.microsoft.com/en-us/training/modules/describe-purview-data-governance/  
Training #5: https://github.com/tayganr/purviewlab   

Purview StarterKit: https://techcommunity.microsoft.com/t5/azure-purview/getting-started-with-azure-purview-using-purview-starter-kit-cli/m-p/2645574  
Anleitung zur Erstellung benutzerdefinierter Lineage: https://piethein.medium.com/use-azure-purviews-rest-apis-for-creating-custom-lineage-ad8efacc6230  
Anleitung zur scanning Delta Lake: https://www.youtube.com/watch?v=pk0Gx_HHY4A  
Community: https://techcommunity.microsoft.com/category/microsoft-purview  

### In Purview integrierte 3rd Party tools

MDM - Cluedin : https://www.cluedin.com/product/microsoft-purview-mdm-integration  
MDM - Profisee: https://profisee.com/solutions/microsoft-enterprise/  
MDM - Reltio: https://learn.reltio.com/reltio-integration-for-microsoft-purview  
MDM - Semarchy: https://www.semarchy.com/doc/semarchy-xdm/xdm/latest/Install/azure/purview/integrate-xdm-with-purview.html  

Lineage – Solidatus: https://www.solidatus.com/partners/microsoft-purview-partnership/  

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![dk](https://img.shields.io/badge/lang-da-red.svg)](README-da.md)
[![de](https://img.shields.io/badge/lang-de-yellow.svg)](README-de.md)
[![main](https://img.shields.io/badge/main-document-green.svg)](README.md)