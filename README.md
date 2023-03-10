# Using KlongPy for feeds and dataframe processing

This project contains various ways of using KlongPy in networking capacities:

    * Websocket pub-sub library to use KlongPy in stream processing
    * KlongPy enabled [DFS service]() to operate on dataframes using KlongPy
    * IPC between Klong processes (TBD)

# KlongPy DataFrame Service
KlongPy enabled [DFS service](https://github.com/briangu/dfs)

# Features

* Build a Klong powered ticker plant
* Run KlongPy operations on remote (service) DataFrames
* DataFrame service that can run KlongPy on DataFrames
* Client REPL can send KlongPy operations to remote service

# Ticker Plant example

In three separate terminals:


Start the fake ticker feed:
```bash
ws_feed_fake_src --symbols AAPL,MSFT,TSLA
```

Tail the feed to see what's going on:
```bash
ws_feed_tail
```

Start the Klong handler that can process the feed:
```bash
ws_feed_klong --port 5001
```

## Run REPL

TBD