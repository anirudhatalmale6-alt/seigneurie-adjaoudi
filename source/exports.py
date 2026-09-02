# -*- coding: utf-8 -*-
"""Exports du blason : PNG transparents et PDF, depuis les SVG maitres.

  python3 source/exports.py

Rien n'est redessine ici. Les fichiers produits sont des rendus des memes
SVG, ce qui garantit qu'un PNG et son SVG ne peuvent pas diverger.
"""

import os
import sys

import cairosvg

_ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(_ICI) if os.path.basename(_ICI) == "source" else _ICI
MARQUE = os.path.join(RACINE, "brand")
SORTIE = os.path.join(MARQUE, "exports")

# (fichier source, hauteurs PNG, PDF ?)
TRAVAUX = [
    ("blason-couleur.svg", (2048, 1024, 512, 256), True),
    ("blason-cramoisi.svg", (2048, 1024, 512), True),
    ("blason-ivoire.svg", (2048, 1024, 512), True),
    ("sceau.svg", (1024, 512, 256, 96), True),
    ("signature-en-verticale.svg", (1200, 600), True),
    ("signature-en-horizontale.svg", (600, 300), True),
    ("signature-fr-verticale.svg", (1200, 600), True),
    ("signature-fr-horizontale.svg", (600, 300), True),
]


def main():
    if not os.path.isdir(SORTIE):
        os.makedirs(SORTIE)
    faits = []
    for nom, hauteurs, pdf in TRAVAUX:
        src = os.path.join(MARQUE, nom)
        base = os.path.splitext(nom)[0]
        for h in hauteurs:
            dest = os.path.join(SORTIE, "%s-%dpx.png" % (base, h))
            cairosvg.svg2png(url=src, write_to=dest, output_height=h)
            faits.append(dest)
        if pdf:
            dest = os.path.join(SORTIE, "%s.pdf" % base)
            cairosvg.svg2pdf(url=src, write_to=dest)
            faits.append(dest)
    for f in faits:
        print("%s  %d octets" % (os.path.relpath(f, RACINE),
                                 os.path.getsize(f)))
    print("%d fichiers" % len(faits))


if __name__ == "__main__":
    sys.exit(main())
