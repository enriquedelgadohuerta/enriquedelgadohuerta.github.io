#!/usr/bin/env python3
"""Genera el enlace de subida de un expediente.

Uso:
    export SUBIDAS_SECRET='el mismo valor que LINK_SECRET del Worker'
    python3 enlace_subida.py EXP-2026-014            # válido 15 días
    python3 enlace_subida.py EXP-2026-014 --dias 30

El código es HMAC-SHA256(secreto, "<expediente>|<AAAAMMDD>") truncado a 12
caracteres hexadecimales. El Worker lo recalcula: sin el secreto no se puede
fabricar un enlace válido, y al caducar deja de funcionar.
"""
import argparse
import datetime
import hashlib
import hmac
import os
import re
import sys

BASE = "https://informeperitoinformatico.es/enviar-archivos/"


def main():
    ap = argparse.ArgumentParser(description="Genera el enlace de subida de un expediente")
    ap.add_argument("expediente")
    ap.add_argument("--dias", type=int, default=15, help="días de validez (por defecto 15)")
    a = ap.parse_args()

    secret = os.environ.get("SUBIDAS_SECRET")
    if not secret:
        sys.exit("Define la variable SUBIDAS_SECRET con el mismo valor que LINK_SECRET del Worker.")
    if not re.fullmatch(r"[A-Za-z0-9-]{3,40}", a.expediente):
        sys.exit("El expediente solo puede tener letras sin tilde, números y guiones (3 a 40 caracteres).")

    cad = (datetime.datetime.now(datetime.timezone.utc).date() + datetime.timedelta(days=a.dias)).strftime("%Y%m%d")
    code = hmac.new(secret.encode(), f"{a.expediente}|{cad}".encode(), hashlib.sha256).hexdigest()[:12]
    print(f"{BASE}#e={a.expediente}&x={cad}&c={code}")


if __name__ == "__main__":
    main()
