
from typing import Any, Dict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

class APIServer:
    """Generic FastAPI server with basic routes and CORS middleware."""

    def __init__(self) -> None:
        self.app = FastAPI(title="Generic API Server")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._register_routes()

    def _register_routes(self) -> None:
        """Register a few example routes."""
        @self.app.get("/health")
        def health() -> Dict[str, str]:
            return {"status": "ok"}

        @self.app.get("/echo/{text}")
        def echo(text: str) -> Dict[str, str]:
            return {"echo": text}

        @self.app.post("/mirror")
        async def mirror(req: Request) -> Dict[str, Any]:
            return {"body": await req.json()}

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Run the uvicorn server."""
        uvicorn.run(self.app, host=host, port=port)

def main() -> None:
    server = APIServer()
    server.run()

if __name__ == "__main__":
    main()
