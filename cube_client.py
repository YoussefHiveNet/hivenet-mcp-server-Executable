import requests
import jwt
import time

class CubeClient:
    def __init__(self, url, secret):
        self.url = url
        self.secret = secret

    def _get_headers(self):
        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
            "sub": "claude-client"
        }
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def get_meta(self):
        r = requests.get(f"{self.url}/meta", headers=self._get_headers())
        r.raise_for_status()
        return r.json()

    def run_query(self, body):
        r = requests.post(f"{self.url}/load", json=body, headers=self._get_headers())
        r.raise_for_status()
        return r.json()
