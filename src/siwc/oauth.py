from __future__ import annotations

from siwc import CCM, CreateCallbackServer

print(CCM)
# CONSTANTS AND SERVER CREATION
server = CreateCallbackServer()
HOST, PORT = server.server_address
REDIRECT_URI = f"http://{HOST}:{PORT}/auth/callback"
print(REDIRECT_URI)

try:
    server.handle_request()

    result = server.callback_result

    if result is None:
        raise ValueError("No callback recieved")

    code = result["code"]
    print(f"Code: {code}")

finally:
    server.server_close()
