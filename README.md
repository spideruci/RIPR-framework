# RIPR-framework
This is an artifact package for the ICSE 2024 paper "Ripples of a Mutation — An Empirical Study of Propagation Effects in Mutation Testing"

# Introduction
- This is an open-source artifact that provides: (1) a functional and scalable implementation of the RIPR (Reachability, Infection, Propagation, and Reveal)  analysis framework for mutants; (2) designated subject projects for RIPR analysis, as discussed in this paper; and (3) the pertinent dataset.

# Table of Contents
- [Directory structure](#directory-structure)
- [Data](#data)
- [Demo Setup](#demo-setup)
- [Usage](#usage)
- [Set Up Beyond Docker](#set-up-beyond-docker)
  
# Directory Structure
1. code: This directory holds the source code of modified PIT, and individual instrumentation code snippets for test classes and production classes.
2. data: The data presented in the paper are under the data directory where two zip files contain the CSV dataset for 10 subject projects. 
3. mutator_ripples: This directory features the Sankey diagrams with aggregated test runs from subject projects for each individual mutation operator employed in our experiment (complete answers to RQ4).
4. subjects: This directory encompasses all the subject projects included in our experiment. Notably, each project is appropriately configured for the execution of the experiment.


# Data

The fields of the CSV dataset are explained below: 
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


# Demo Setup
Executing RIPR analysis for each subject project present in the paper can span from several hours to up to four days, depending on project size as this process necessitates ten supplementary non-mutation test runs for each mutation test run with additional probes that synchronize two test runs with and without mutation execution, check state infection, and propagation. Moreover, storage requirements for memory data range up to 300 GB per subject project.

As such, we configured dual Docker containers to accommodate both Intel/AMD and ARM architectures, thereby illustrating the pipelines and configuration of our experimental setup for running RIPR (and mutation) analyses locally pertinent to a production class and a test class from our Apache commons-text subject program. Furthermore, we provide guidance on tailoring the RIPR analysis beyond the Docker environment, with the possibility of modifying the code to pave the way for future research endeavors.

Requirements:
For Docker tutorial example: Must have the latest version of Docker installed.
General Requirments on Subject Projects: 1) Subject projects should utilize the JUnit5 framework. 2) Maven must be used as the build system. 3) Compatibility with PITest is required. 4) Each test class should include methods annotated with @BeforeAll and @AfterAll.

# Usage
## Basic Usage through Docker Examples:

For ARM-based laptops:

pull the image and run the container
``` 
docker pull qinfendeheichi/text-arm:v1
docker run --name arm qinfendeheichi/text-arm
```

To monitor the progress of our analysis, the console will display the count of processed outputs at intervals of every 100 mutants (starting from 0).

Copy Docker Configuration
This Dockerfile demonstrates a minimal example that contains configuration for the Apache commons-text subject program
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

## Raw Data Explanation

Under **everything directory**, one could understand the organizing structure of raw data of RIPR analysis: 
  1) each zip file contains raw data for one mutation and the name of the zip file is the hashed value of the mutation.
  2) mutationInfo.txt contains detailed information about a mutation.
  3) testInfo.txt contains the all test run's names.
  4) status.txt contains the mutation's status
  5) killingTests.txt and failingReasons.txt contain failing test run names and their exceptional information.
  6) MRs.txt and NMRs.txt contain all the instrumented probe information.
  7) state info related to mutation-run and no-mutation-run are stored under the MR and NMR directory.
  8) Under NMR directory, each test case have 10 no-mutation test runs where the prefix number indicates the corresponding test run out of all 10 NMRs; NMR.xml stores the infection info, AfterAll.xml and AfterAllStatic.xml store the propagation info, stateInfo.txt stores the probe info for the current test run; The MR directory is organized in similar ways except there is only one test run per test case for a mutation.

Under the **everything directory**, the organization of each mutation's raw data for RIPR analysis is as follows:

1. **Zip Files**: Each zip file contains raw data for one mutation, with the file name being the hashed value of that mutation.
2. **mutationInfo.txt**: This file holds detailed information about each mutation.
3. **testInfo.txt**: Lists the names of all test runs.
4. **status.txt**: Details the status of each mutation.
5. **killingTests.txt and failingReasons.txt**: These files contain the names of failing test runs and their respective exceptional information.
6. **MRs.txt and NMRs.txt**: Include all information regarding instrumented probes for mutation-run (MR) and no-mutation-run (NMR).
7. **MR and NMR Directories**: Store state information related to mutation-run (MR) and no-mutation-run (NMR). 
    - Under the NMR directory:
        - Each test case has 10 no-mutation test runs.
        - The prefix number of each test run indicates its order among the 10 NMRs.
        - **NMR.xml**: Stores infection information.
        - **AfterAll.xml** and **AfterAllStatic.xml**: Contain propagation information.
        - **stateInfo.txt**: Provides probe information for the current test run.
    - The MR directory:
        - Organized similarly to the NMR directory.
        - Contains only one test run per test case for a mutation.



## Major Result Illustration from the CSVs

The Docker image is equipped with scripts and configuration settings necessary for generating key findings related to research questions RQ1 through RQ4. Execution of the container typically requires approximately two minutes.

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
docker cp sankeyarm:commons-text.pdf .
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

# Running Scripts Locally

The Dockerfile provides a minimal example of the experimental configuration. In this section, we delve deeper into the functionalities of different modules used in the experiment.

## Code Directory Structure
- **PIT_STATE_DEV_with_len**: Contains the source code of the modified PIT, customized for our experiment.
- **PreTestInstrumenter**: Houses source code for instrumenting test classes. This module references variables to a collection.
- **TestInstrumenter**: Instruments test classes by surrounding test methods with try-catch blocks.
- **SourceCodeInstrumenter**: Instruments the production classes.
- The corresponding JAR files for these modules are named `p.jar`, `t.jar`, and `s.jar`, respectively.

## Install PITest
Under the PITest project directory (PIT_STATE_DEV_with_len) Run
```
mvn clean install -Dmaven.test.skip
```

## Prepare instrumentation jar files
Before Running the Experiment for the subject projects, place the corresponding jar files under the subject project's directory that contains the POM file.
s.jar instruments the production classes, p.jar and t.jar instruments the test classes, which are generated in SourceCodeInstrumente, PreTestInstrumenter, and TestInstrumenter projects. They could be customized and produced individually by running:
```
mvn clean compile assembly:single test-compile
```

## Run mutation analysis
Run:
```
mvn clean compile test-compile
cp staticFields.txt target
cp GlobalStates.txt target
mkdir target/staticFields
java -jar "p.jar" target/test-classes
java -jar "t.jar" target/test-classes
java -jar "s.jar" target/classes
mvn "-Dmaven.main.skip" pitest:mutationCoverage >info.txt 2>result.txt
```

The above experimental logic could be reasoned from the Dockerfile we provide in the Docker environment. 


