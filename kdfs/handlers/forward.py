import logging

import simdjson as json
from websockets import WebSocketException


class ForwardingHandler:
    def __init__(self, connected_clients, message_queue, all_pattern, pattern_keys):
        self.connected_clients = connected_clients
        self.message_queue = message_queue
        self.all_pattern = all_pattern
        self.pattern_keys = pattern_keys

    async def run(self):
        while True:
            raw_data = await self.message_queue.get()
            messages = json.loads(raw_data)

            for client, patterns in self.connected_clients.items():
                try:
                    if self.all_pattern in patterns:
                        await client.send(raw_data)
                    else:
                        to_send = []
                        for message in messages:
                            key = ".".join([message[k] for k in self.pattern_keys])
                            if key in patterns:
                                to_send.append(message)
                        if to_send:
                            await client.send(json.dumps(to_send))
                except WebSocketException:
                    logging.info("connection dropped, continuing")
                    continue
