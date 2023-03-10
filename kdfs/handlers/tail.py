

class TailHandler:
    def __init__(self, message_queue):
        self.message_queue = message_queue

    async def run(self):
        while True:
            raw_data = await self.message_queue.get()
            print(raw_data)

