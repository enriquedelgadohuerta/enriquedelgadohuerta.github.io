#!/usr/bin/env python3
"""Obtiene el refresh token de tu OneDrive personal para el Worker de subidas.

Uso (en tu Mac, una sola vez o cuando el token caduque):
    python3 onedrive_token.py <CLIENT_ID>

Abre el navegador para que inicies sesión con tu cuenta Microsoft, recibe el
código en http://localhost:8400 y escribe el refresh token en
refresh_token.txt (no lo subas al repositorio). Solo usa la biblioteca estándar.
"""
import base64
import hashlib
import http.server
import json
import secrets
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser

AUTH = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
TOKEN = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
SCOPE = "Files.ReadWrite offline_access"
REDIRECT = "http://localhost:8400"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    client_id = sys.argv[1]
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h2>Listo. Ya puedes cerrar esta pestaña y volver a la terminal.</h2>".encode())
            threading.Thread(target=self.server.shutdown).start()

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("localhost", 8400), Handler)
    url = AUTH + "?" + urllib.parse.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT,
        "scope": SCOPE,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "prompt": "select_account",
    })
    print("Abriendo el navegador para iniciar sesión en Microsoft…\nSi no se abre, copia esta URL:\n" + url)
    webbrowser.open(url)
    server.serve_forever()

    if result.get("state") != state or "code" not in result:
        sys.exit("Error en el inicio de sesión: " + json.dumps(result, ensure_ascii=False))

    data = urllib.parse.urlencode({
        "client_id": client_id,
        "grant_type": "authorization_code",
        "code": result["code"],
        "redirect_uri": REDIRECT,
        "code_verifier": verifier,
        "scope": SCOPE,
    }).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN, data=data)) as r:
        tok = json.load(r)
    if "refresh_token" not in tok:
        sys.exit("Microsoft no ha devuelto refresh_token: " + json.dumps(tok, ensure_ascii=False))
    with open("refresh_token.txt", "w") as f:
        f.write(tok["refresh_token"])
    print("Refresh token guardado en refresh_token.txt")


if __name__ == "__main__":
    main()
