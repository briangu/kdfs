#!/usr/bin/python3

import asyncio
import logging

import simdjson as json
from websockets import ConnectionClosed, WebSocketException, connect


class WSServer:
    def __init__(self, pattern_prefixes=None):
        self.connected_clients = {}
        self.pattern_prefixes = pattern_prefixes

    def is_valid_subscription(self, patterns):
        if self.pattern_prefixes is None:
            return True
        for x in patterns:
            valid = False
            for prefix in self.pattern_prefixes:
                if x.startswith(prefix):
                    valid = True
                    break
            if not valid:
                logging.info(f"invalid subscription: {x}")
                return False
        return True

    def handle_auth(self, msg):
        return {"ev": "status", "status": "auth_success", "message": "authenticated"}

    async def handle_client(self, websocket):
        try:
            async for message in websocket:
                logging.info(f"Received message from client: {message}")
                try:
                    data = json.loads(message)
                    if data["action"] == "subscribe":
                        patterns = data["params"].split(",")
                        logging.info(f"subscribing: {patterns}")
                        if self.is_valid_subscription(patterns):
                            self.connected_clients[websocket] = patterns
                            response = {"ev": "status", "status": "success", "message": f"subscribed to: {','.join(patterns)}"}
                            logging.info(f"Client subscribed to patterns: {patterns}")
                        else:
                            response = {"ev": "status", "status": "error", "message": f"invalid subscription: {','.join(patterns)}"}
                            logging.info(f"Client failed to subscribe to patterns: {patterns}")
                        await websocket.send(json.dumps(response))
                    elif data["action"] == "auth":
                        await websocket.send(json.dumps(self.handle_auth(data)))
                except:
                    pass
        finally:
            # Remove client from set of connected clients
            logging.info("client closed connection")
            if websocket in self.connected_clients:
                self.connected_clients.pop(websocket)


class WSClient:
    def __init__(self, uri, auth_token, patterns):
        self.uri = uri
        self.auth_token = auth_token
        self.patterns = patterns
        self.message_queue = asyncio.Queue()

    async def run(self):
        async for websocket in connect(self.uri):
            try:
                logging.info("authorizing")
                message = {"action": "auth", "params": self.auth_token}
                await websocket.send(json.dumps(message))
                ack = await websocket.recv()
                logging.info(ack)
                message = {"action": "subscribe", "params": self.patterns}
                await websocket.send(json.dumps(message))
                ack = await websocket.recv()
                logging.info(ack)
                while True:
                    raw_data = await websocket.recv()
                    await self.message_queue.put(raw_data)
            except ConnectionClosed:
                logging.info("connection dropped, reconnecting")
                continue


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


