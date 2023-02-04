import multiprocessing as mp
import os
import socket
import threading
from queue import Queue

import simdjson as json

from dfs.helpers import *
from dfs import df_client


class KsClient(df_client.DataFrameClient):
    def __init__(self, pool, conn):
        self.pool = pool
        self.conn = conn

    def remote_klongpy(self, klong):
        send_msg(self.conn, json.dumps({'type': 'klongpy', 'lambda': klong}).encode())
        return recv_json(self.conn)

