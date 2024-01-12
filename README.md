# RIPR-framework
This is an artifact package for the ICSE 2024 paper "Ripples of a Mutation — An Empirical Study of Propagation Effects in Mutation Testing"

# Purpose
- This is an open-source artifact that provides: (1) a functional and scalable implementation of the RIPR (Reachability, Infection, Propagation, and Reveal)  analysis framework for mutants; (2) designated subject projects for RIPR analysis, as discussed in this paper; and (3) the pertinent dataset.
- We aim to earn available and reusable badges. This framework is not only applicable to subject projects in the paper but may potentially apply to a broader range of subject projects and also holds significant value for other mutant-based downstream research endeavors.

# Provenance 
This artifact and the related paper can be obtained through Zenodo link https://zenodo.org/records/10460085.

# Data
The data supporting the findings of this paper are organized under the 'data' directory, where two compressed (zip) files contain the CSV datasets for 10 subject projects. Due to the page limit, the fields within these CSV datasets are thoroughly explained in the accompanying Zenodo artifact package.

# Setup
Executing RIPR analysis for each subject project present in the paper can span from several hours to up to 4&ndash;5 days, depending on project size as this process necessitates ten supplementary non-mutation test runs for each mutation test run, together with additional probes that synchronize two test runs with and without mutation execution, check state infection, and propagation. Moreover, storage requirements for memory data range up to 300 GB per subject project.

As such, we configured dual Docker containers to accommodate both Intel/AMD and ARM architectures, thereby illustrating the pipelines and configuration of our experimental setup for running RIPR (and mutation) analyses locally pertinent to a production class and a test class from our Apache commons-text subject program. Furthermore, we provide guidance on tailoring the RIPR analysis beyond the Docker environment, with the possibility of modifying the code to pave the way for future research endeavors.

Requirements:
For Docker tutorial example: Must have the latest version of Docker installed.
General Requirments on Subject Projects: 1) Subject projects should utilize the JUnit5 framework. 2) Maven must be used as the build system. 3) Compatibility with PITest is required. 4) Each test class should include methods annotated with @BeforeAll and @AfterAll.

# Usage
## Basic Usage through Docker Examples:

### For ARM-based laptops:

pull the image and run the container
``` 
docker pull qinfendeheichi/text-arm:v1
docker run --name arm qinfendeheichi/text-arm
```

To monitor the progress of our analysis, the console will display the count of processed outputs at intervals of every 100 mutants (starting from 0).

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

### For Intel/AMD-based laptops:

pull the image and run the container
``` 
docker pull qinfendeheichi/text-amd:v1
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
**0sankey.png:** demonstrates an example of localized RIPR analysis for a specific production class and test class for the Apache commons-text subject program. 
**everything directory:** This directory houses the raw data organization structure. Each compressed (zip) file within this directory encapsulates data pertaining to a specific mutation. More explanation is in the artifact package.

In this scenario, we engage with 7 mutants, encompassing 12 passing and 11 failing mutation test runs. All mutants are killed, achieving an infection and propagation rate of 100%. The data can be reasoned through the Sankey diagram and corresponding CSV files.

## Major Result Illustration from the CSVs

The following Docker image is equipped with scripts and configuration settings necessary for generating key findings related to research questions RQ1 through RQ4. Execution of the container typically requires approximately two minutes.

### For ARM-based machines, run
``` 
docker pull qinfendeheichi/getsankey:v1
docker run --name sankeyarm qinfendeheichi/getsankey
```

### For Intel/AMD-based machines, run
``` 
docker pull qinfendeheichi/getsankeyamd:v1
docker run --name sankeyamd qinfendeheichi/getsankeyamd

```

If using an Intel/AMD-based machine, modify the following instructions by replacing "arm" with "and" as needed. To retrieve the Docker configuration file, execute the following command:
``` 
docker cp sankeyarm:Dockerfile .
```

Scripts designated for processing RQ1 to RQ4 are titled getSankey.py, RQ2Script.py, RQ3Script.py, and RQ4Script.py. They are expected to run in the container consecutively. To access these scripts, execute this command:
``` 
docker cp sankeyarm:getSankey.py .
docker cp sankeyarm:RQ2Script.py .
docker cp sankeyarm:RQ3Script.py .
docker cp sankeyarm:RQ4Script.py . 
```
### RQ1

Run
```
docker cp sankeyarm:commons-texts.pdf .
```
Replace cdk-data with commons-cli/commons-codec/commons-validator/cdk-data/dyn4j/jfreechart/jline-reader/joda-money/spotify-web-api for Sankey diagrams from other projects. They correspond to Figure 3 of the paper. These diagrams constitute the core results presented in our study.

### RQ2
Results of RQ2 are displayed in the terminal and correspond to the data shown in Table 2 of our paper.

### RQ3
Run
```
docker cp sankeyarm:RQ3.pdf .
```
The illustration referred to here is the same as Figure 4 in our paper.

### RQ4
Run
```
docker cp sankeyarm:"PrimitiveReturn(36338)Sankey.pdf" .
```
To view Sankey diagrams for different mutation operators, replace PrimitiveReturn(36338)Sankey.pdf with EmptyObjectReturn(27855)Sankey.pdf, or BooleanTrue(44547)Sankey.pdf, or BooleanFalse(33633)Sankey.pdf, or increment(6515)Sankey.pdf, or Math(135194)Sankey.pdf, or NullReturns(97187)Sankey.pdf, or VoidMethodCall(207997)Sankey.pdf, or NegateConditional(439264)Sankey.pdf, or ConditionalBoundary(134505)Sankey.pdf for Sankey diagrams. These diagrams illustrate the RIPR effects of individual mutation operators, as shown in Figure 5 of our paper. Ensure to include the file names in quotes. 


## Beyond Docker
We also provide additional information that facilitates the reuse of the artifact in the Zenodo artifact's Readme file.
