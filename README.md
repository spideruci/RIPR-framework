# RIPR-framework
This is an artifact package for the ICSE 2024 paper "Ripples of a Mutation — An Empirical Study of Propagation Effects in Mutation Testing". A non-permanent link to our artifact can be found here:
https://github.com/spideruci/RIPR-framework

# Introduction
- This is an open-source artifact that provides: (1) a functional and scalable implementation of the RIPR (Reachability, Infection, Propagation, and Reveal)  analysis framework for mutants; (2) designated subject projects for RIPR analysis, as discussed in this paper; and (3) the pertinent dataset.

# Table of Contents
- [Directory structure](#directory-structure)
- [Data](#data)
- [Demo Setup](#demo-setup)
- [Usage](#usage)
- [Reusing Our Framework to Analyze New Subject Programs](#reusing-our-framework-to-analyze-new-subject-programs)
  
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

Make sure that the docker images' ".tar" files exist at the same path of the terminal's working path.

For ARM-based laptops:

load the image and run the container
``` 
docker load -i text-arm.tar
docker run --name arm qinfendeheichi/text-arm:v1
```

To monitor the progress of our analysis, the console will display the count of processed outputs at intervals of every 100 mutants (starting from 0). If there are less than 100 mutations, the console will print "processed 0 mutations", which is not an error. 

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

load the image and run the container
``` 
docker load -i text-amd.tar
docker run --name amd qinfendeheichi/text-amd:v1
```
Copy Docker Configuration
```
docker cp amd:/commons-text/project/Dockerfile .
```

Copy Core Output
```
docker cp amd:/commons-text/project/hashResult.csv .
docker cp amd:/commons-text/project/0sankey.png .
docker cp amd:/commons-text/project/target/everything/ .
```


**hashResult.csv:** contains CSV-formatted processed data. 
**0sankey.png:** demonstrates an example of localized RIPR analysis for a specific production class and test class for the Apache commons-text subject program. 
**everything directory:** This directory houses the raw data organization structure. Each compressed (zip) file within this directory encapsulates data pertaining to a specific mutation. More explanation is in the artifact package.

Expected results if analysis runs correctly:
The hashResult.csv file should contain 33 lines, each representing a test run. 12 of these will show that the test passed, and 11 of them will show that the test failed. Additionally, there should be seven zip files, each representing one mutant, under target/everything directory.


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
docker load -i getsankey.tar
docker run --name sankeyarm qinfendeheichi/getsankey:v1
```

### For Intel/AMD-based machines, run
``` 
docker load -i getsankeyamd.tar
docker run --name sankeyamd qinfendeheichi/getsankeyamd:v1

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
Replace commons-text with commons-cli/commons-codec/commons-validator/cdk-data/dyn4j/jfreechart/jline-reader/joda-money/spotify-web-api for Sankey diagrams from other projects. They correspond to Figure 3 of the paper. These diagrams constitute the core results presented in our study.

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

# Reusing Our Framework to Analyze New Subject Programs

The overall process for analyzing the execution of the bug/mutation, infection of the state, propagation of the infection, and revealing the failure (i.e., the RIPR analysis), as well as generating all of the figures in our paper can be described as such:

1. **Choose New Subject Project**: First, subject programs should be chosen based upon the following criteria: they should (1) utilize the JUnit5 framework; (2) use Maven as the build system; (3) ensure compatibility with PITest. If these criteria are not met, the subject program would need to be adapted to fit the criteria.

2. **Prepare the Subject Project**: Modify (by hand) the subject program in the following ways
   
 - 2.1 Include methods annotated with @BeforeAll and @AfterAll in each test class for probe initialization and state dumping. If the test class already has these methods, that is fine. If it does not, introduce empty methods with these annotations — these will be used by the instrument.

 - 2.2 Prepare an instrumentation utility package by moving the package located under src/test/java/inst to the concerned subject project. We will be making some changes to this in a future step, but for now, simply copying an existing package works fine.

 - 2.3 Configure xstream, zeroturnaround, and commons-lang3 as dependencies in the project's POM file, referencing the dependencies from an existing subject project’s POM file. 

 - 2.4 Prepare Instrumentation Jar Files: For the subject projects, it is essential to prepare jar files that are capable of instrumenting both the source code and the test code. This task typically involves configuring the dependencies of the subject project's POM file. Such configuration ensures that the jar files can correctly instrument the target projects. In the GitHub repository, there is a directory called “code”, which has contained directories of “PreTestInstrumenter”, “TestInstrumenter”, and “sourceCodeInstrumenter”. In your local repository, in each of these subdirectories, copy their Maven configuration to their POM files as dependencies. Then, compile and install each of these tools in these directories. This would produce three jar files under target directory, named, “p.jar”, “t.jar”, and “s.jar”. Move them to the subject directory at the same level of the subject program’s POM file.

 - 2.5 Install our modified PITest, which is found in the directory code/PIT_STATE_DEV_with_len, by running “maven clean install -Dmaven.test.skip” in that directory. Configure our modified PITest for your new subject project by following the instructions given by the original PIT project.

 - 2.6 Run a pre-analysis to initialize the static field hashcodes, by creating two empty text files named “staticFields.txt” and “GlobalStates.txt” in the directory containing 
the POM file, and then, executing our customized version of PIT. Follow the official PIT instructions to run PIT.

 - 2.7 Customize the instrumentation utility package. Begin by examining our subject programs’ src/test/java/inst directories to learn how to adapt them to your new subject program. Each subject program requires some customization. The steps involved are:

   - 2.7.1 Customization 1: Clean polluted static fields. We attempt to clean any static fields that are polluted between test runs, or even between mutations, by observing their state for multiple runs. To do this: Identify the hash code of static fields dumped under “target/staticFields/” directory. Then hard code the hash value of static fields under dumpStatic method in InstrumentationUtils.java file. This method performs checks on the hash value of static fields which are not the same as the hard-coded ones. Then run the analysis again. If “target/staticFields/” directory is not empty, it indicates some dumped static fields’ hash code is not the same as the hard-coded one. If so, perform diffs between two dumped xml files, identify the polluted portion, and write cleaners to overwrite the polluted states in clearStatic method in the same file. To inform this process, examine the existing subject programs’ clearStatic methods.

   - 2.7.2 Customization 2: Ignore flaky state. We attempt to ignore states that are nondeterministic (for example, random values, hash codes, date/time values, etc.) so that they do not affect our analyses. This step can be performed at this step and/or augmented as the experiment matures. You will likely augment this step as you learn more about your subject program and its analysis. To do this, analyze each subject program to identify flaky states in a similar way that we identified polluted static fields in Customization 1. Identify the flakiness across 10 NMRs (no mutation runs) by comparing dumped states under the NMR directory of each mutation directory. Then put specific portions of states to be ignored under the shouldSerializeMember method. 

3. **Run Analysis**: Before running the experiment, ensure that the two text files named “staticFields.txt” and “GlobalStates.txt” are in the directory containing the POM file (from Step 2.6). Then, execute our customized version of PIT. This specialized version is designed to collect comprehensive data for our experiment. The output from this run will be stored in the “target/everything” directory, encompassing all the raw data necessary for further analysis.

4. **Interpret Data**: Convert the raw data in the “target/everything” directory into CSV files. This format conversion facilitates the subsequent data analysis process. This conversion is performed by a script that may need to be customized per subject program. Use the script provided for commons-text in the Docker container as a baseline for your conversion, and if it crashes and needs some specialization, you may need to investigate and modify our script accordingly.
  
5. **Execute Scripts for Data Analysis**: Run each script (one for generating the Sankey diagrams for RQ1, and one for each of the remaining research questions RQ2–RQ4). 
These scripts take the CSV file as input (hard-coded in scripts) and output their respective analyzed data (Sankey diagram figure, table).
Run anyalsis by executing:
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

Also, depending on the chosen subject program, you may also encounter additional challenges such as flaky states introduced by mocked objects, difficulties with compatibility with Xstream, and static fields that have private or protected modifiers. In such cases, some modifications to the subject programs may be necessary (such as making a private static field to be public, or customize the instrumentation to not collect states for mocked variables). These challenges cannot be exhaustively predicted, and will need to be addressed as they are discovered.

Our customized version of PIT and projects that perform instrumentation can be found under the code directory. PreTestInstrumenter, TestInstrumenter, and sourceCodeInstrumenter projects perform instrumentation related to referencing variables to collections for test classes and inserting probes, surrounding methods with try-catch blocks for test classes, and for source-code classes. 
The prepared subject projects can be found under the subjects directory. 
The interpreting scripts for RQs and the raw data interpretation template can be found under scripts directory.



