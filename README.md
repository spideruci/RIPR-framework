# RIPR-framework
This is an artifact package for the ICSE 2024 paper "Ripples of a Mutation — An Empirical Study of Propagation Effects in Mutation Testing"

# Purpose
- This is an open-source artifact that provides: (1) a functional and scalable implementation of the RIPR (Reachability, Infection, Propagation, and Reveal)  analysis framework for mutants; (2) designated subject projects for RIPR analysis, as discussed in this paper; and (3) the pertinent dataset.
- We aim to earn available and reusable badges as our artifact provides a practical framework for RIPR analysis in mutation testing which may be applicable to more subject projects and may be valuable to other mutant-based downstream research. 

# Provenance 
This artifact and the related paper can be obtained through link XXXXXXXXXXXXX

# Data
The data presented in the paper are under the data directory where two zip files contain the CSV dataset for 10 subject projects. For simplicity, the fields of the CSV dataset are explained in the Zenodo artifact package

# Setup
Executing RIPR analysis for each subject project present in the paper can span from several hours to up to 4-5 days, depending on project size as this process necessitates ten supplementary non-mutation test runs for each mutation test run, together with additional probes that synchronize two test runs with and without mutation execution, check state infection, and propagation. Moreover, storage requirements for memory data range up to 300 GB per subject project.

As such, we configured dual Docker containers to accommodate both Intel and ARM architectures, thereby illustrating the pipelines and configuration of our experimental setup for running RIPR (and mutation) analyses locally pertinent to a production class and a test class from our Apache commons-text subject program. Furthermore, we provide guidance on tailoring the RIPR analysis beyond the Docker environment, with the possibility of modifying the code to pave the way for future research endeavors.

Requirements:
Docker tutorial example: Latest Version of Docker installed. 
Beyond Docker: For customized experiments for projects outside of the paper, subject projects shall use the Junit5 framework, using maven as built system, support running with Pitest, each test class shall have methods with @BeforeAll and @AfterAll methods. 

# Usage
## Basic Usage through Docker Examples:

### For Arm-based laptops:

pull the image and run the container
``` 
docker pull qinfendeheichi/text-arm:latest
docker run --name arm qinfendeheichi/text-arm
```
Copy Docker Configuration
This Dockerfile demonstrates a minimal example that contains configuration for Apache commons-text subject program
```
docker cp arm:/commons-text/project/Dockerfile .
```

Copy Core Output
```
docker cp arm:/commons-text/project/hashResult.csv .
docker cp arm:/commons-text/project/0sankey.png .
docker cp arm:/commons-text/project/target/everything/ .
```

### For AMD-based laptops:

pull the image and run the container
``` 
docker pull qinfendeheichi/text-amd:latest
docker run --name amd qinfendeheichi/text-amd
```
Copy Docker Configuration
```
docker cp amd:/commons-text/project/Dockerfile .
```

Copy Core Output
```
docker cp amd:/commons-text/project/hashResult.csv .
docker cp and:/commons-text/project/0sankey.png .
docker cp amd:/commons-text/project/target/everything/ .
```

**hashResult.csv** contains formatted processed data. 
**0snakey.png** demonstrates an example of localized RIPR analysis for a production class and test class for the Apache commons-text subject program. 
**everything directory** contains the raw data organization structure where each zip file contains data for one mutation
For Intel-based laptops

## Raw Data Explanation

Under **everything directory**, each zip file represents data related to one mutation. More information related to the organization of raw data is explained in the Zenodo artfiact's Readme file.

## Major Result Illustration from the CSVs

The following docker image translates the CSV data into Sankey diagrams as presented in Figure 3 in the paper, which are the major results in the paper.

Run
``` 
docker pull qinfendeheichi/getsankey:latest
docker run --name sannkey qinfendeheichi/getsankey
```

then get individual Sankey diagrams 
```
docker cp getsankey:commons-textsankey.png . 
```
Replace cdk-data with commons-cli/commons-codec/commons-validator/cdk-data/dyn4j/jfreechart/jline-reader/joda-money/spotify-web-api for all other sankey diagrams.

## Beyond Docker
We also provide additional information on the reuse of the artifact in the Zenodo artifact's Readme file.
