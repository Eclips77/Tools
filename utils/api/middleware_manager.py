
from typing import Callable
from fastapi import FastAPI, Request

class MiddlewareManager:
    """Register example middlewares on a FastAPI app."""

    def add_logging(self, app: FastAPI) -> None:
        """Add a simple request logging middleware."""
        @app.middleware("http")
        async def log_requests(request: Request, call_next: Callable):
            print(f"--> {request.method} {request.url.path}")
            response = await call_next(request)
            print(f"<-- {response.status_code} {request.url.path}")
            return response

def main() -> None:
    # from fastapi import FastAPI
    import uvicorn
    app = FastAPI()
    mm = MiddlewareManager()
    mm.add_logging(app)

    @app.get("/")
    def root():
        return {"ok": True}

    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    main()
