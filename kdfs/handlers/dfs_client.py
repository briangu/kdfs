from dfs.df_client import *
from dfs.helpers import *
import numpy as np
import simdjson as json


col_types = {
    'c': 'float32',
    'h': 'float32',
    'l': 'float32',
    'n': 'uint32',
    'o': 'float32',
    # 'otc': np.dtype(bool),
    't': 'uint64',
    'v': 'uint32', # increase for more than a week timeframe
    'vw': 'float32'
}
col_keys = [x for x in col_types.keys() if x not in ['t']]

col_remap = {
    't': 'e'
}


def create_dataframe(timestamps=None, dmap=None):
    dmap = dmap or {c:np.empty((0,), dtype=col_types[c]) for c in col_types.keys()}
    if timestamps is not None:
        df = pd.DataFrame(dmap, index=timestamps)
    else:
        df = pd.DataFrame(dmap)
        df = df.set_index('t')
    return df


def pandas_from_data(items):
    timestamps = [item['e'] for item in items]
    dmap = {}
    for k in col_keys:
        dmap[k] = np.asarray([item.get(col_remap.get(k) or k) or 0 for item in items], dtype=col_types[k])
    return create_dataframe(timestamps=timestamps, dmap=dmap)


class DfsClientHandler:
    def __init__(self, message_queue, host, port):
        self.message_queue = message_queue
        self.host = host
        self.port = port

    async def run(self):
        with DataFrameConnectionPool(self.host, self.port) as pool:
            with pool.get_connection() as c:
                while True:
                    messages = json.loads(await self.message_queue.get())
                    for message in messages:
                        df = pandas_from_data([message])
                        # TODO: need an asyncio friendly DFS client
                        print(df)
                        c.update(df, 'historical', 'minute', message['sym'])

