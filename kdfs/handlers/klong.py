import logging

import simdjson as json
from websockets import WebSocketException
from klongpy.core import KGCall
import numpy as np

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
