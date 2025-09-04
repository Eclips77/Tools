
import socket
import shutil
import http.client
from typing import Tuple

class HealthCheck:
    """Generic health checks for HTTP, TCP, and disk space."""

    def check_http(self, host: str, path: str = "/", port: int = 80, timeout: int = 3) -> Tuple[bool, int]:
        """Return (ok, status_code) for a simple HTTP GET."""
        try:
            conn = http.client.HTTPConnection(host, port=port, timeout=timeout)
            conn.request("GET", path)
            resp = conn.getresponse()
            status = resp.status
            conn.close()
            return (200 <= status < 400, status)
        except Exception:
            return (False, 0)

    def check_tcp(self, host: str, port: int, timeout: int = 3) -> bool:
        """Return True if a TCP port is reachable."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except Exception:
            return False

    def check_disk(self, path: str = "/") -> Tuple[int, int, int]:
        """Return (total, used, free) bytes for a path."""
        u = shutil.disk_usage(path)
        return (u.total, u.used, u.free)

def main() -> None:
    hc = HealthCheck()
    print("HTTP google.com:", hc.check_http("google.com"))
    print("TCP localhost:22:", hc.check_tcp("localhost", 22))
    print("Disk /:", hc.check_disk("/"))

if __name__ == "__main__":
    main()
