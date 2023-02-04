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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.release_connection(self.conn)

    def get_data(self, *args, range_start=None, range_end=None, range_type="timestamp"):
        send_cmd(self.conn, 'get', file_path=args, range_start=range_start, range_end=range_end, range_type=range_type)
        return recv_df(self.conn)

    def insert_data(self, df, *args):
        send_cmd(self.conn, 'insert', file_path=args)
        send_df(self.conn, df)
        recv_status(self.conn)

    def unload(self, *args):
        send_cmd(self.conn, 'unload', file_path=args)
        recv_status(self.conn)

    def load(self, *args):
        send_cmd(self.conn, 'load', file_path=args)
        return recv_json(self.conn)

    def get_stats(self, level=None):
        send_msg(self.conn, json.dumps({'type': 'stats', 'level': level}).encode())
        return recv_json(self.conn)

