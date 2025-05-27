# About

[YeSQL](https://athenarc.github.io/YeSQL/) is an SQL extension that provides more usable, more expressive, and more perfomant Python UDFs and can be integrated into both server-based and embedded DBMSs. It enriches SQL with a functional syntax that unifies the expression of relational and user-defined functionality and optimizes the execution of both in a seamless fashion, assigning processing tasks to the DBMS or the UDF host language VM accordingly and employing efficient low-level implementation techniques. Key characteristics of the YeSQL language that enhance usability and expressiveness include (a) stateful, parametric, and polymorphic UDFs, (b) dynamically typed UDFs, (c) scalar and aggregate UDFs returning arbitrary table forms, and (d) UDF pipelining. Key performance characteristics include (a) seamless data exchange between the UDF and the DBMS, (b) JIT-compiled UDFs, (c) UDF parallelization, (d) stateful UDFs, and (e) UDF fusion.

This is a fork of the Original repo with instruction on running YeSQL Implementation on top of MonetDB. You can find the Docker Image for running the MonetDB server [here](LINK) 
# Documentation

You'll find YeSQL [documentation here](https://athenarc.github.io/YeSQL/).

## Installation with MonetDB

### Requirements

Ubuntu 20.04 with cmake version 3.12 or newer or you can get the docker image with all dependencies installed from [here]()

### Installation

Create a `.monetdb` file at your home and insert:
```
user=monetdb
password=monetdb
```

Clone the current repository and run
```
./exec.sh
```
This script contains the list of commands to install monetdb and other python and system dependencies, the commands to load the UDFs and data in MonetDB. 

You can run the following command to directly install all dependencies and start the MonetDB server in the terminal 
```
./start.sh
```

### Experiment

run end-to-end experiments with 

```
./monetdb_release/bin/mclient -d fldb -p 50000 -t performance

```

Paste query at `sql_queries/flights.sql` in the terminal.
Paste query at `sql_queries/zillow.sql` in the terminal.

You can run the udfs defined at `udfs/flights.py` and `udfs/zillow.py` in isolation to run microbenchmarks with YeSQL's implementation on MonetDB.

The user can disable default monetdb's multithreading with `set optimizer='sequential_pipe';` in the terminal and run single threaded experiments. 
Also the number of threads can be defined as shown at https://www.monetdb.org/documentation-Jan2022/admin-guide/manpages/monetdb/ with nthreads property.
This is necessary to run the scalability experiments.

Note also that with:
```
python3 YeSQL_MonetDB/monetdb.py -d fldb -H localhost -P 50000 -u monetdb -p monetdb
``` 
The YeSQL's terminal with its language extensions (syntactic inversion) can be used with MonetDB. 

## Adding New UDFs
To add new User-Defined Functions (UDFs), follow these steps:

1.  **Add a Function to the Functions Folder:** Place your Python UDF code in the appropriate directory.
2.  **Update `udfs.h`:** Add the wrapper function definition in C to `udfs.h`. The function signature will typically include:
    *   `input` (type depends on the function)
    *   `size` (always `int`)
    *   `output` (type depends on the function)
3.  **Modify `build.py`:** Add the same function definition to the `embedding_api` function within `build.py`.
4.  **Update `embedding_init_code`:** Add the function definition to `embedding_init_code`. This code, called by the function created in the next step, should invoke the UDF and manage input/output using [CFFI](https://cffi.readthedocs.io/en/stable/).
5.  **Define in `createfuncs.sql`:** Define the new SQL function in `createfuncs.sql`. The server will use this definition when executing code.
6.  **Restart Server:** Kill the currently running server process and restart the MonetDB server using the `./start.sh` command.

We have implemented somefunction from the Functions folder which has been designed for Data Analystics purposes by the original authors. You can add any other function in the same way above. 

## Important Files and Folders for Running MonetDB with YeSQL

Here's a breakdown of key files and folders involved in integrating YeSQL with MonetDB:

1.  **`YeSQL_MonetDB/cffi_wrappers/build.py`**: This script is responsible for building the binary file that acts as a wrapper between SQL and Python User-Defined Functions (UDFs).
2.  **`YeSQL_MonetDB/cffi_wrappers/createfuncs.sql`**: This file defines the custom UDFs that can be invoked from the MonetDB server.
3.  **`YeSQL_MonetDB/cffi_wrappers/udf.h`**: This header file contains the C definitions for the wrapper functions called by the database server.
4.  **`YeSQL_MonetDB/functions`**: This directory houses custom UDFs, originally created by the YeSQL authors, for data analytics purposes.
5.  **`udf`**: This folder contains initial prototype UDFs shared by the original authors.

Using above instructions you will be able to implemented these UDFs in any server based database.

## SQL Lite
You can find how to run SQLite from [original repo](https://github.com/athenarc/YeSQL.git). 

For comparisons with `tuplex` and `pyspark` we used the implementations available at 
https://github.com/tuplex/tuplex/tree/master/benchmarks/flights (python files `runpyspark.py` and `runtuplex.py`)
and
https://github.com/tuplex/tuplex/tree/master/benchmarks/zillow/Z2 (python files `runpyspark.py` and `runtuplex.py`)

Instruction to install tuplex and run these scripts are available at https://github.com/tuplex/tuplex

##
