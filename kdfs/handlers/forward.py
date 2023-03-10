import logging

import simdjson as json
from websockets import WebSocketException
from datetime import datetime


class ForwardingHandler:
    def __init__(self, connected_clients, message_queue, all_pattern):
        self.connected_clients = connected_clients
        self.message_queue = message_queue
        self.all_pattern = all_pattern

    async def run(self):
        while True:
            raw_data = await self.message_queue.get()
            messages = json.loads(raw_data)

            for client, patterns in self.connected_clients.items():
                try:
                    if self.all_pattern in patterns:
                        await client.send(raw_data)
                    else:
                        for message in messages:
                            to_send = []
                            if f"{message['ev']}.{message['sym']}" in patterns:
                                to_send.append(message)
                            if to_send:
                                await client.send(json.dumps(to_send))
                except WebSocketException:
                    logging.info("connection dropped, continuing")
                    continue

