from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/auth/callback"):
            self.send_response(200)
            url = urlparse(self.path)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<h1>Authentication Successful. <br> You can close this window.</h1>"
            )
            params = parse_qs(url.query)

            code = params.get("code", [None])[0]
            state = params.get("state", [None])[0]
            error = params.get("error", [None])[0]

            self.server.callback_result = {"code": code, "state": state, "error": error}

        else:
            self.send_error(404, "Not Found")


def CreateCallbackServer(ADDRESS, PORT):
    server = HTTPServer((ADDRESS, PORT), CallbackHandler)
    server.callback_result = None
    return server
