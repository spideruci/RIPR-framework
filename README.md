# RIPR-framework
This is an artifact package for the ICSE 2024 paper "Ripples of a Mutation — An Empirical Study of Propagation Effects in Mutation Testing"

**Purpose:** 
	- This is an open-source artifact that provides: (1) a functional and scalable implementation of the RIPR (Reachability, Infection, Propagation, and Reveal)  analysis framework for mutants; (2) designated subject projects for RIPR analysis, as discussed in this paper; and (3) the pertinent dataset.
	- We aim to earn available and reusable badges as our artifact provides a practical framework for RIPR analysis in mutation testing which may be applicable to more subject projects and may be valuable to other mutant-based downstream research. 

**Provenance:** This artifact and the related paper can be obtained XXXX

**Data:** The data presented in the paper are under the data directory where two zip files contain the CSV dataset for 10 subject projects. The fields of the CSV dataset are explained below: 
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

