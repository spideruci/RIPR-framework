# RIPR-framework
This is an artifact package for the ICSE 2024 paper "Ripples of a Mutation — An Empirical Study of Propagation Effects in Mutation Testing"

## Purpose
- This is an open-source artifact that provides: (1) a functional and scalable implementation of the RIPR (Reachability, Infection, Propagation, and Reveal)  analysis framework for mutants; (2) designated subject projects for RIPR analysis, as discussed in this paper; and (3) the pertinent dataset.
- We aim to earn available and reusable badges as our artifact provides a practical framework for RIPR analysis in mutation testing which may be applicable to more subject projects and may be valuable to other mutant-based downstream research. 

## Provenance 
This artifact and the related paper can be obtained through link XXXXXXXXXXXXX

## Data
The data presented in the paper are under the data directory where two zip files contain the CSV dataset for 10 subject projects. For simplicity, the fields of the CSV dataset are explained in the Zenodo artifact packaage
| Field               | Description                                                 |
|---------------------|-------------------------------------------------------------|
| m_id | mutation id (hashed) |
| mutation_status         | KILLED or SURVIVED                          |
| mutator       | mutation operator                          |
| test_name | the name of the test case                             |
| test_status             | pass/fail                                       |
| mr_m_1st    | the number of times the mutated method is executed after the first mutation execution | 
| mr_m_all            | the number of times the mutated method is executed in the whole mutation run                             |
| mr_e         | 1 if the mutation was executed else 0                                         |
| nmr_m_all          | the number of times the method of concern is executed in a no-mutation run           |
| middle_same          | True: if there is infection else False                   |
| end_same                | True: if there is propagation only based on the states dumped on test finishes (if a test fails, there is still propagation)|
|mr_return         | 1 if the mutated method exits through Return else 0|
|mr_athrow    | 1 if the mutated method exits through Athrow else 0|
|mr_exception  | 1 if the mutated method exits through exogenous crashes else 0|
|nmr_return   | 1 if the method of concern in no-mutation run exits through Return else 0|
|nmr_athrow    | 1 if the method of concern in no-mutation run exits through Athrow else 0|
|nmr_exception   | 1 if the method of concern in no-mutation run exits through Exception else 0|
|MR_len_before | number of method executions before mutation is executed in a mutation test run|
|MR_len_after | number of method executions of a test run in a mutation test run|
|NMR_len_avg | average number of method executions in 10 no-mutation test runs|


## Setup
Executing RIPR analysis for each subject project present in the paper can span from several hours to up to four days, depending on project size as this process necessitates ten supplementary non-mutation test runs for each mutation test run with additional probes that synchronize two test runs with and without mutation execution, check state infection, and propagation. Moreover, storage requirements for memory data range up to 300 GB per subject project.

As such, we configured dual Docker containers to accommodate both Intel and ARM architectures, thereby illustrating the pipelines and configuration of our experimental setup for running RIPR (and mutation) analyses locally pertinent to a production class and a test class from our Apache commons-text subject program. Furthermore, we provide guidance on tailoring the RIPR analysis beyond the Docker environment, with the possibility of modifying the code to pave the way for future research endeavors.

Requirements:
Docker tutorial example: Latest Version of Docker installed. 
Beyond Docker: For customized experiments for projects outside of the paper, subject projects shall use the Junit5 framework, using maven as built system, support running with Pitest, each test class shall have methods with @BeforeAll and @AfterAll methods. 

## Usage
### Basic Usage through Docker Examples:

For Arm-based laptops:

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

**hashResult.csv** contains formatted processed data. 
**0snakey.png** demonstrates an example of localized RIPR analysis for a production class and test class for the Apache commons-text subject program. 
**everything directory** contains the raw data organization structure where each zip file contains data for one mutation
For Intel-based laptops

### Raw Data Explanation


Under **everything directory**, one could understand the organizing structure of raw data of RIPR analysis: 
  1) each zip file contains raw data for one mutation and the name of the zip file is the hashed value of the mutation.
  2) mutationInfo.txt contains detailed information about a mutation.
  3) testInfo.txt contains the all test run's names.
  4) status.txt contains the mutation's status
  5) killingTests.txt and failingReasons.txt contain failing test run names and their exceptional information.
  6) MRs.txt and NMRs.txt contain all the instrumented probe information.
  7) state info related to mutation-run and no-mutation-run are stored under the MR and NMR directory.
  8) Under NMR directory, each test case have 10 no-mutation test runs where the prefix number indicates the corresponding test run out of all 10 NMRs; NMR.xml stores the infection info, AfterAll.xml and AfterAllStatic.xml store the propagation info, stateInfo.txt stores the probe info for the current test run; The MR directory is organized in similar ways except there is only one test run per test case for a mutation.



### Major Result Illustration from the CSVs

The following docker image translates the csv data into sankey diagrams as presented in Figure 3 in the paper.

Run
``` 
docker pull qinfendeheichi/getsankey:latest
docker run --name sannkey qinfendeheichi/getsankey
```

then get individual sankey diagrams 
```
docker cp getsankey:commons-textsankey.png . 
```
Replace cdk-data with commons-cli/commons-codec/commons-validator/cdk-data/dyn4j/jfreechart/jline-reader/joda-money/spotify-web-api for all other sankey diagrams.

### Directory Structure Beyond Docker
We provide the configuration of all subject projects present in the paper under the "subjects" directory. All CSV data is under the "data" directory. All Sankey diagrams for individual mutation operators (RQ4) are present under the "mutator_ripples" directory.

