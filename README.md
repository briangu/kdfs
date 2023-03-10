# Networked KlongPy

This project contains various ways of using KlongPy in networking capacities:

    * Websocket pub-sub library to use KlongPy in stream processing
    * KlongPy enabled [DFS service]() to operate on dataframes using KlongPy

# Features

* Run KlongPy operations on remote (service) DataFrames
* DataFrame service that can run KlongPy on DataFrames
* Client REPL can send KlongPy operations to remote service

# Quick start

## Start Server

```bash
$ kdfs --server
```

## Run REPL

```bash
$ kdfs
Creating connection pool with 8 connections

Welcome to KS REPL
author: Brian Guarraci
repo  : https://github.com/briangu/kfs
crtl-c to quit

?> ! 1+1
{'result': '2'}
```
