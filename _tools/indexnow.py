#!/usr/bin/env python3
"""Avisa a Bing (y por tanto a Copilot y ChatGPT search) y a Yandex de las URLs
del sitemap mediante IndexNow. Ejecutar tras publicar cambios:

    python3 _tools/indexnow.py            # todas las URLs del sitemap
    python3 _tools/indexnow.py URL [URL]  # solo las indicadas
"""
import glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "informeperitoinformatico.es"
key = next(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, "*.txt"))
           if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(p)))
urls = sys.argv[1:] or re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
body = json.dumps({"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.status, len(urls), "URLs enviadas")  # 200/202 = aceptado
