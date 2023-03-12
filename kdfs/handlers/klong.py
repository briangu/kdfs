import logging

import simdjson as json
from websockets import WebSocketException
from klongpy.core import KGCall, KGFn
import numpy as np
import time
from kdfs.helpers import count_event_rate

class KlongHandler:
    def __init__(self, connected_clients, message_queue, klong):
        self.connected_clients = connected_clients
        self.message_queue = message_queue
        self.klong = klong

    async def run(self):
        # event_count = 0
        # last_event_time = time.time()
        while True:
            raw_data = await self.message_queue.get()

            messages = json.loads(raw_data)

            onmsg = self.klong['onmsg']
            r = self.klong.call(KGCall(a=onmsg.a,args=[np.array(messages,dtype=object)],arity=onmsg.arity))
            print(r)
            # TODO: create new ev types for klong outputs

            # for client, patterns in self.connected_clients.items():
            #     try:
            #         await client.send(raw_data)
            #     except WebSocketException:
            #         logging.info("client closed")
            #         continue
            # event_count, last_event_time = count_event_rate(event_count+1, last_event_time, print_rate=True, units=1)
