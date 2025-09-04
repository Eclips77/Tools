
from typing import Any, Dict, Optional
import requests

class APIClient:
    """Generic HTTP client with base URL, headers, and helpers for common verbs."""

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers: Dict[str, str] = {"User-Agent": "GenericAPIClient/1.0"}

    def set_header(self, key: str, value: str) -> None:
        """Set or override a default header."""
        self.headers[key] = value

    def _url(self, path: str) -> str:
        """Build absolute URL from base and path."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Send a GET request."""
        return requests.get(self._url(path), params=params, headers=self.headers, timeout=self.timeout)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Send a POST request with JSON body."""
        return requests.post(self._url(path), json=json, headers=self.headers, timeout=self.timeout)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Send a PUT request with JSON body."""
        return requests.put(self._url(path), json=json, headers=self.headers, timeout=self.timeout)

    def delete(self, path: str) -> requests.Response:
        """Send a DELETE request."""
        return requests.delete(self._url(path), headers=self.headers, timeout=self.timeout)

def main() -> None:
    client = APIClient("https://httpbin.org")
    r = client.get("/get")
    print(r.status_code, r.ok)

if __name__ == "__main__":
    main()
