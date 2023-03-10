import simdjson as json

from dfs.helpers import *
from dfs import df_server
from klongpy import KlongInterpreter


class CommandHandler(df_server.CommandHandler):

    def process(self, conn, command):
        tinfo(json.dumps(command))
        should_continue = True
        if command['type'] == 'klongpy':
            print(command)
            send_json(conn, result=str(self.server.klong(command['lambda'])))
        else:
            should_continue = super().process(conn, command)
        return should_continue


class KdfsServer(df_server.DataFrameServer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.klong = KlongInterpreter()


