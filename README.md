# KlongPy DataFrame Service 
KlongPy enabled DFS service

# Features

* Run KlongPy operations on remote (service) DataFrames
* DataFrame service that can run KlongPy on DataFrames
* Client REPL can send KlongPy operations to remote service 

# Quick start

## Start Server

```bash
$ ks_server --info
```

## Run REPL

```bash
$ ks_repl
Creating connection pool with 8 connections

Welcome to KS REPL
author: Brian Guarraci
repo  : https://github.com/briangu/kfs
crtl-c to quit

?> ! 1+1
{'result': '2'}
```
