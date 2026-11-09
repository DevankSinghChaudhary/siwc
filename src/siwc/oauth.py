from __future__ import annotations

import base64
import hashlib
import secrets
import warnings

from siwc import CreateCallbackServer

code_verifier = secrets.token_urlsafe(43)
code_challenge = (
    base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("ascii")).digest())
    .rstrip(b"=")
    .decode("ascii")
)


class SIWC:
    def callback(self, PORT=None, ADDRESS=None):
        if not PORT:
            PORT = 0
            warnings.warn(
                "PORT not specified. Defaulting to 0 (assign any available port)",
                UserWarning,
            )
        if not ADDRESS:
            ADDRESS = "127.0.0.1"
            print(f"Using address: {ADDRESS}")

        try:
            server = CreateCallbackServer(ADDRESS, PORT)
            port = server.server_port
            REDIRECT_URI = f"http://{ADDRESS}:{port}/auth/callback"
            print(f"Server running on: {REDIRECT_URI}")
            server.handle_request()
            result = server.callback_result
            if result is None:
                raise ValueError("No callback recieved")
            self.code = result["code"]
            return self.code
        finally:
            server.server_close()

    def send_request(self, CODE):
        print(CODE)


client = SIWC()
server = client.callback()
client.send_request()
