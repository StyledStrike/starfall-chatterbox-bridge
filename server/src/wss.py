from websocket_server import WebsocketServer
from json import loads, dumps, JSONDecodeError

import logger

# https://github.com/Pithikos/python-websocket-server

"""
    A utility class to handle the websocket server.
"""
class WSSManager():
    def __init__(self, host="127.0.0.1", port=8001):
        self.onMessageCallback = None
        self.onConnectCallback = None
        self.onDisconnectCallback = None

        self.server = WebsocketServer(host=host, port=port)
        self.server.set_fn_new_client(self._onConnect)
        self.server.set_fn_client_left(self._onDisconnect)
        self.server.set_fn_message_received(self._onMessage)
        self.server.run_forever(threaded=True)

    def _onMessage(self, client, server, message):
        if message == "ping":
            self.server.send_message(client, "pong")
            return 

        try:
            data = loads(message)

            if callable(self.onMessageCallback):
                self.onMessageCallback(data)

        except JSONDecodeError:
            logger.error("[WSS] Failed to parse json!")

    def _onConnect(self, client, server):
        logger.info("[WSS] Connected:", client["id"], client["address"])

        if callable(self.onConnectCallback):
            self.onConnectCallback()

    def _onDisconnect(self, client, server):
        if client is not None:
            logger.info("[WSS] Disconnected:", client["id"])

        if callable(self.onDisconnectCallback):
            self.onDisconnectCallback()

    def shutdown(self):
        self.server.shutdown_gracefully()

    def broadcast(self, data: str, log=True):
        message = dumps(data)

        if log:
            logger.debug(message)

        self.server.send_message_to_all(message)

    def broadcastError(self, text: str):
        logger.error(text)
        self.broadcast({ "error": text }, log=False)

def getStringFromDict(obj: dict, key: str, default: str | None = None):
    value = obj.get(key, default)

    if isinstance(value, str) and len(value) > 0:
        return value

def getFloatFromDict(obj: dict, key: str, default: float):
    value = obj.get(key, None)

    if isinstance(value, int):
        return float(value)

    if isinstance(value, float):
        return value

    return default
