# Using KlongPy for feeds and dataframe processing

This project contains various ways of using [KlongPy](https://github.com/briangu/klongpy) in networking capacities:

    * Websocket based Ticker Plant example showing how to use KlongPy in stream processing
    * KlongPy enabled [DFS service]() to operate on dataframes using KlongPy
    * IPC between Klong processes (TBD)

# Related

* [KlongPy](https://github.com/briangu/klongpy)
* [DFS service](https://github.com/briangu/dfs)


# Ticker Plant example

A ticker plant is a pub-sub tree of consumers typically with a primary feed producer at the root.  It's common for the feed to produce stock market ticker data and consumers to receive these updates, process the data and possibly pass the new data long to their consumers.

This example uses a fake stock ticker data generator as the root node and subscribers listen for updates.  One of the subscribers is a "tail" which simply outputs what it receives.  The other is a Klong subscriber which runs a Klong handler routine for each received message.

To see this in action, in separate terminals:

Start the fake ticker feed:
```bash
ws_feed_fake_src --symbols AAPL,MSFT,TSLA
```

Tail the feed to see what's going on:
```bash
$ ws_feed_tail
```
You should see an array of stock messages flow by when tailing the fake source.

Next we, start the Klong handler that can process the feed.  We can define custom handlers in Klong that are loaded and 'onmsg" is called every message:  Here, a trivial function definition to create an average for the batch of symbols:

```
onmsg::{[a d];d:::{};d,["ev" "AVG"];a::{x?"c"}'x;d,"a",+/a%#a}
```

Specify the avg.kg when launching:
```bash
$ ws_feed_klong kg/avg.kg --log INFO --port 5001
INFO:root:Opening connection to 0.0.0.0 port 5001
INFO:root:Server running...
INFO:root:Client running...
INFO:root:Handler task running...
INFO:websockets.server:server listening on 0.0.0.0:5001
INFO:root:authorizing
INFO:root:{"ev": "status", "status": "auth_success", "message": "authenticated"}
INFO:root:{"ev": "status", "status": "success", "message": "subscribed to: AM.*"}
INFO:root:{'ev': 'AVG', 'a': 52.288999999999994}
INFO:root:{'ev': 'AVG', 'a': 52.290000000000006}
```

Tail the feed to see the Klong handler output:
```bash
ws_feed_tail --uri ws://localhost:5001
{"ev": "AVG", "a": 52.2865}
{"ev": "AVG", "a": 52.2865}
```

New handlers and listeners can be added to achieve the stream processing goals.

The Klong handler utilizes the simple Klong <-> Python interop as follows.  Upon receiving new messages array, we can passit directly to the Klong 'onmsg' function:

```python
class KlongHandler:
    def __init__(self, connected_clients, message_queue, klong):
        self.connected_clients = connected_clients
        self.message_queue = message_queue
        self.klong = klong

    async def run(self):
        while True:
            raw_data = await self.message_queue.get()
            messages = json.loads(raw_data)

            # Call the Klong onmsg handler with messages
            r = self.klong['onmsg'](messages)

            logging.info(r)

            for client, patterns in self.connected_clients.items():
                try:
                    await client.send(json.dumps(r))
                except WebSocketException:
                    logging.info("client closed")
                    continue
```


# DFS example

Start a DFS server:

```bash
kdfs --log INFO server --dir /tmp/dfs
```

Start the ws -> dfs client handler which will store the streaming stock data into DFS
```
ws_feed_dfs_client
```

You can now inspect the DFS server to see what's there:

List the dataframes stored in the backing directory:
```bash
ls -al /tmp/dfs/historical/minute/
```

Connect to the DFS process and check the stats:
```bash
$ kdfs --log INFO repl

Welcome to KDFS REPL
author: Brian Guarraci
repo  : https://github.com/briangu/kdfs
crtl-c to quit

INFO:root:Creating connection pool with 19 connections
?> stats
{
  "memory": {
    "used": "387360",
    "free": "1073354464",
    "max": "1073741824"
  },
  "config": {
    "root_path": "/tmp/dfs",
    "max_memory": "1073741824"
  }
}
```
