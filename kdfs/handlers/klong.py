import logging

import simdjson as json
from websockets import WebSocketException


class KlongHandler:
    def __init__(self, connected_clients, message_queue, klong):
        self.connected_clients = connected_clients
        self.message_queue = message_queue
        self.klong = klong

    async def run(self):
        while True:
            raw_data = await self.message_queue.get()
            messages = json.loads(raw_data)

            for message in messages:
                self.klong['msg'] = message
                processed_message = self.klong("onmsg(msg)")
                print(processed_message)
                for client, patterns in self.connected_clients.items():
                    try:
                        await client.send(json.dumps(processed_message))
                    except WebSocketException:
                        logging.info("client closed")
                        continue


