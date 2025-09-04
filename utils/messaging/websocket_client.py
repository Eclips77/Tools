
import asyncio
import websockets

class WebSocketClient:
    """Generic WebSocket client for sending and receiving text messages."""

    def __init__(self, uri: str) -> None:
        self.uri = uri

    async def send(self, message: str) -> None:
        """Connect and send a message, then close."""
        async with websockets.connect(self.uri) as ws:
            await ws.send(message)

    async def echo(self, message: str) -> str:
        """Send a message and wait for a single response."""
        async with websockets.connect(self.uri) as ws:
            await ws.send(message)
            return await ws.recv()

def main() -> None:
    print("WebSocketClient requires an event loop. Example:")
    print("python -c "import asyncio; from messaging.websocket_client import WebSocketClient; asyncio.run(WebSocketClient('ws://echo.websocket.events').send('hi'))"")

if __name__ == "__main__":
    main()
