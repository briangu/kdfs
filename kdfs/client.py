import simdjson as json
from dfs import df_client
from dfs.helpers import *


class KdfsClient(df_client.DataFrameClient):
    def __init__(self, pool, conn):
        self.pool = pool
        self.conn = conn

    def remote_klongpy(self, prog):
        send_msg(self.conn, json.dumps({'type': 'klongpy', 'lambda': prog}).encode())
        return recv_json(self.conn)['result']

