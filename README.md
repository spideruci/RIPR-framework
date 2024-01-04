# RIPR-framework
This is an artifact package for the ICSE 2024 paper "Ripples of a Mutation — An Empirical Study of Propagation Effects in Mutation Testing"

# Purpose
- This is an open-source artifact that provides: (1) a functional and scalable implementation of the RIPR (Reachability, Infection, Propagation, and Reveal)  analysis framework for mutants; (2) designated subject projects for RIPR analysis, as discussed in this paper; and (3) the pertinent dataset.
- We aim to earn available and reusable badges. This framework is not only applicable to subject projects in the paper but may potentially apply to a broader range of subject projects and also holds significant value for other mutant-based downstream research endeavors.

# Provenance 
This artifact and the related paper can be obtained through Zenodo link XXXXXXXXXXXXX

# Data
The data supporting the findings of this paper are organized under the 'data' directory, where two compressed (zip) files contain the CSV datasets for 10 subject projects. For page-limitation, the fields within these CSV datasets are thoroughly explained in the accompanying Zenodo artifact package.

# Setup
Executing RIPR analysis for each subject project present in the paper can span from several hours to up to 4-5 days, depending on project size as this process necessitates ten supplementary non-mutation test runs for each mutation test run, together with additional probes that synchronize two test runs with and without mutation execution, check state infection, and propagation. Moreover, storage requirements for memory data range up to 300 GB per subject project.

As such, we configured dual Docker containers to accommodate both Intel and ARM architectures, thereby illustrating the pipelines and configuration of our experimental setup for running RIPR (and mutation) analyses locally pertinent to a production class and a test class from our Apache commons-text subject program. Furthermore, we provide guidance on tailoring the RIPR analysis beyond the Docker environment, with the possibility of modifying the code to pave the way for future research endeavors.

Requirements:
For Docker tutorial example: Must have the latest version of Docker installed.
General Requirments on Subject Projects: 1) Subject projects should utilize the Junit5 framework. 2) Maven must be used as the build system. 3) Compatibility with Pitest is required. 4) Each test class should include methods annotated with @BeforeAll and @AfterAll.

# Usage
## Basic Usage through Docker Examples:

### For ARM-based laptops:

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

**hashResult.csv:** contains CSV-formatted processed data. 
**0snakey.png:** demonstrates an example of localized RIPR analysis for a specific production class and test class for the Apache commons-text subject program. 
**everything directory:** This directory houses the raw data organization structure. Each compressed (zip) file within this directory encapsulates data pertaining to a specific mutation. More explanation is in the artifact package.

## Major Result Illustration from the CSVs

The Docker image provided facilitates the translation of CSV data into Sankey diagrams, as exemplified in Figure 3 of the paper. These diagrams constitute the core results presented in our study.

### For Arm-based machines, run
``` 
docker pull qinfendeheichi/getsankey:latest
docker run --name sannkey qinfendeheichi/getsankey
```

then get individual Sankey diagrams 
```
docker cp sankey:commons-textsankey.png . 
```
### For Amd-based machines, run
``` 
docker pull qinfendeheichi/getsankeyamd:latest
docker run --name sannkeyamd qinfendeheichi/getsankeyamd
docker cp sankeyamd:commons-textsankey.png . 
```

Replace cdk-data with commons-cli/commons-codec/commons-validator/cdk-data/dyn4j/jfreechart/jline-reader/joda-money/spotify-web-api for sankey diagrams from other projects.


## Beyond Docker
We also provide additional information that facilitates the reuse of the artifact in the Zenodo artifact's Readme file.
