# -*- coding: utf-8 -*-
"""Captures d'ecran du site, pour montrer le travail au client.

  python3 tests/captures.py [port]

Toutes les captures sont prises dans la fenetre visible, jamais en pleine
page : une capture pleine page depasse la limite de taille acceptee par la
messagerie et casse le fil.
"""

import http.server
import os
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

_ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(_ICI) if os.path.basename(_ICI) == "tests" else _ICI
SORTIE = os.path.join(RACINE, "apercus")

# (fichier, url, defilement, largeur, hauteur, action)
PLANS = [
    ("sa-01-accueil", "index.html", 0, 1280, 800, None),
    ("sa-02-manifeste", "index.html", 760, 1280, 800, None),
    ("sa-03-chronologie", "index.html", 1560, 1280, 800, None),
    ("sa-04-selection", "index.html", 2280, 1280, 800, None),
    ("sa-05-seigneurie", "the-lordship.html", 0, 1280, 800, None),
    ("sa-06-est-nest-pas", "the-lordship.html", 430, 1280, 800, None),
    ("sa-07-valeurs", "the-lordship.html", 2000, 1280, 800, None),
    ("sa-08-patrimoine", "heritage.html", 380, 1280, 800, None),
    ("sa-09-registre-droits", "heritage.html", 1080, 1280, 800, None),
    ("sa-10-maison", "house-of-adjaoudi.html", 700, 1280, 800, None),
    ("sa-11-initiatives", "initiatives.html", 380, 1280, 800, None),
    ("sa-12-journal", "journal.html", 380, 1280, 800, None),
    ("sa-13-mediatheque", "media-library.html", 380, 1280, 800, None),
    ("sa-14-contact", "contact.html", 400, 1280, 800, None),
    ("sa-15-cercle-prive", "private-circle.html", 330, 1280, 800, None),
    ("sa-16-vie-privee", "legal.html", 620, 1280, 800, None),
    ("sa-17-recherche", "index.html", 0, 1280, 800, "recherche"),
    ("sa-18-fr-accueil", "fr/index.html", 0, 1280, 800, None),
    ("sa-19-fr-seigneurie", "fr/la-seigneurie.html", 430, 1280, 800, None),
    ("sa-20-fr-mentions", "fr/mentions-legales.html", 620, 1280, 800, None),
    ("sa-21-mobile-accueil", "index.html", 0, 390, 780, None),
    ("sa-22-mobile-menu", "index.html", 0, 390, 780, "menu"),
    ("sa-23-mobile-contact", "contact.html", 620, 390, 780, None),
    ("sa-24-mobile-fr", "fr/patrimoine.html", 360, 390, 780, None),
    ("sa-25-guide-marque", "brand/guidelines.html", 0, 1280, 800, None),
    ("sa-26-guide-palette", "brand/guidelines.html", 1900, 1280, 800, None),
    ("sa-27-guide-respiration", "brand/guidelines.html", 3300, 1280, 800, None),
]


class Silencieux(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def __init__(self, *a, **k):
        super().__init__(*a, directory=RACINE, **k)


def main():
    srv = None
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        srv = socketserver.TCPServer(("127.0.0.1", 0), Silencieux)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        port = srv.server_address[1]
    base = "http://127.0.0.1:%d/" % port
    if not os.path.isdir(SORTIE):
        os.makedirs(SORTIE)

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for nom, url, y, l, h, action in PLANS:
            assert l <= 2000 and h <= 2000, nom
            ctx = nav.new_context(viewport={"width": l, "height": h},
                                  device_scale_factor=1)
            pg = ctx.new_page()
            pg.goto(base + url, wait_until="networkidle")
            if action == "recherche":
                pg.click(".loupe")
                pg.fill("#q", "rights")
                pg.wait_for_timeout(220)
            elif action == "menu":
                pg.click(".bascule")
                pg.wait_for_timeout(180)
            if y:
                pg.evaluate("(y) => window.scrollTo(0, y)", y)
                pg.wait_for_timeout(220)
            chemin = os.path.join(SORTIE, nom + ".png")
            pg.screenshot(path=chemin)
            print("%s  %d octets" % (os.path.relpath(chemin, RACINE),
                                     os.path.getsize(chemin)))
            ctx.close()
        nav.close()
    if srv:
        srv.shutdown()


if __name__ == "__main__":
    sys.exit(main())
