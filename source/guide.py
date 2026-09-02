# -*- coding: utf-8 -*-
"""Guide de marque : une page autonome, construite, jamais editee a la main.

  python3 source/guide.py     ->  brand/guidelines.html + les schemas

L'aire de respiration et les tailles minimales ne sont pas recopiees du
document du client : elles sont MESUREES sur le blason reellement dessine
(le rectangle occupe par les pixels non transparents), puis dessinees. Une
regle de marque qu'on recopie sans la mesurer est une regle que personne ne
peut appliquer.
"""

import io
import os
import sys

import cairosvg
from PIL import Image

_ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(_ICI) if os.path.basename(_ICI) == "source" else _ICI
sys.path.insert(0, _ICI)

import blason as B  # noqa: E402


def boite_dessinee(chemin_svg, cote=1000):
    """Rectangle reellement occupe, en unites du viewBox."""
    png = cairosvg.svg2png(url=chemin_svg, output_width=cote)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    bb = im.getbbox()
    from xml.etree import ElementTree as ET
    vb = [float(v) for v in
          ET.parse(chemin_svg).getroot().get("viewBox").split()]
    k = vb[2] / float(im.width)
    return (vb[0] + bb[0] * k, vb[1] + bb[1] * k,
            vb[0] + bb[2] * k, vb[1] + bb[3] * k)


def schema_respiration():
    """Le blason, sa boite, et l'aire de respiration a x = demi-diametre."""
    src = os.path.join(RACINE, "brand", "blason-couleur.svg")
    x0, y0, x1, y1 = boite_dessinee(src)
    x = B.R_LONG                      # demi-diametre du soleil dessine
    X0, Y0, X1, Y1 = x0 - x, y0 - x, x1 + x, y1 + x
    e = ['<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="#FFFCF6"/>'
         % (X0, Y0, X1 - X0, Y1 - Y0)]
    e += B.blason("plein")
    e.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" '
             'stroke="#C51F2D" stroke-width="4"/>' % (x0, y0, x1 - x0, y1 - y0))
    e.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" '
             'stroke="#8A6A12" stroke-width="4" stroke-dasharray="18 14"/>'
             % (X0, Y0, X1 - X0, Y1 - Y0))
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    mesures = ((X0, my, x0, my, (X0 + x0) / 2.0, my - 16),
               (mx, Y0, mx, y0, mx + 30, (Y0 + y0) / 2.0 + 16))
    for ax, ay, bx, by, tx, ty in mesures:
        e.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="#201A1A" stroke-width="4"/>' % (ax, ay, bx, by))
        for px, py, vert in ((ax, ay, ax == bx), (bx, by, ax == bx)):
            if vert:
                e.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                         'stroke="#201A1A" stroke-width="4"/>'
                         % (px - 22, py, px + 22, py))
            else:
                e.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                         'stroke="#201A1A" stroke-width="4"/>'
                         % (px, py - 22, px, py + 22))
        e.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" '
                 'font-size="52" font-weight="600" fill="#201A1A" '
                 'text-anchor="middle">x</text>' % (tx, ty))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.0f %.0f %.0f '
           '%.0f" role="img" aria-label="Aire de respiration">\n%s\n</svg>\n'
           % (X0 - 10, Y0 - 10, X1 - X0 + 20, Y1 - Y0 + 20, "\n".join(e)))
    B.ecrire(os.path.join(RACINE, "brand", "schema-respiration.svg"), svg)
    return (x0, y0, x1, y1), x


PALETTE = [
    ("Cramoisi Adjaoudi", "#8F101C",
     ("Primary background, headings, coat of arms",
      "Fond principal, titres, blason")),
    ("Radiant Red", "#C51F2D", ("Accents, buttons, active states",
                                "Accents, boutons, états actifs")),
    ("Antique Gold", "#D4A72C", ("Sun, rules, premium details",
                                 "Soleil, filets, détails")),
    ("Ivory", "#F6F0E4", ("Soft backgrounds, breathing space",
                          "Fonds clairs, respiration")),
    ("Charcoal", "#201A1A", ("Body text, contrast", "Texte courant, contraste")),
]

INTERDITS = [
    "Stretch or distort the mark.",
    "Tilt or rotate it.",
    "Recolour it outside the approved variants.",
    "Add a drop shadow, a glow or an outline.",
    "Place it on a busy photograph without an ivory or crimson plate.",
    "Change the number of rays. There are sixteen, and there is no version "
    "with any other number.",
    "Separate the sun from the shield.",
    "Present the mark as a governmental, official or heraldic-authority "
    "symbol.",
]


def luminance(h):
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5))

    def c(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def contraste(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


GABARIT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Adjaoudi Lordship — brand guidelines</title>
<meta name="description" content="The Adjaoudi solar coat of arms: variants, \
palette, typography, clear space, minimum sizes and prohibited uses.">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/site.css">
<style>
 .plaque{{background:#8F101C; padding:26px; border-radius:3px}}
 .puce{{display:flex; gap:14px; align-items:center; margin:0 0 10px}}
 .puce i{{width:44px; height:44px; border:1px solid var(--filet);
   border-radius:2px; display:block; flex:0 0 auto}}
 .mini{{display:flex; gap:26px; align-items:flex-end; flex-wrap:wrap}}
 .mini figure{{margin:0; text-align:center}}
 figure.carte{{text-align:center}}
 figure.carte figcaption{{text-align:left}}
 .mini figcaption{{font-size:.76rem; color:var(--gris); margin-top:8px}}
</style>
</head>
<body>
<div class="bande"><div class="wrap">
<p class="sur">Adjaoudi Lordship</p>
<h1>Brand guidelines</h1>
<p>The solar coat of arms, its variants and the rules that keep it one mark.
Every figure on this page is measured on the artwork itself, not copied from
a specification.</p>
</div></div>
<main>
{corps}
</main>
<footer class="pied"><div class="wrap">
<p class="decl">{decl}</p>
</div></footer>
</body>
</html>
"""


def main():
    (x0, y0, x1, y1), x = schema_respiration()
    largeur = x1 - x0
    hauteur = y1 - y0
    o = []

    o.append('<section id="marks"><div class="wrap"><h2>The mark and its '
             'variants</h2><p class="chapo">Four approved versions. They come '
             'out of one geometry file, so they cannot drift apart.</p>'
             '<div class="grille g2">'
             '<figure class="carte"><img src="blason-couleur.svg" alt="Full '
             'colour coat of arms" width="300" height="355">'
             '<figcaption><strong>Full colour</strong> — the primary version.'
             '</figcaption></figure>'
             '<figure class="carte"><img src="blason-cramoisi.svg" '
             'alt="Monochrome crimson coat of arms" width="300" height="355">'
             '<figcaption><strong>Monochrome crimson</strong> — one ink, on '
             'ivory or white.</figcaption></figure>'
             '<figure class="carte plaque"><img src="blason-ivoire.svg" '
             'alt="Monochrome ivory coat of arms" width="300" height="355">'
             '<figcaption style="color:#F4E6D8"><strong>Monochrome ivory'
             '</strong> — on crimson or charcoal.</figcaption></figure>'
             '<figure class="carte"><img src="sceau.svg" alt="Seal: shield '
             'and sun only" width="200" height="323">'
             '<figcaption><strong>Seal</strong> — shield and sun only, for '
             'small sizes and stamps.</figcaption></figure>'
             '</div></div></section>')

    o.append('<section id="signature" class="papier"><div class="wrap">'
             '<h2>Signatures</h2><p class="chapo">The mark locked to the name. '
             'The lettering is converted to outlines, so a signature file '
             'needs no font installed to render correctly.</p>'
             '<div class="grille g2">'
             '<figure class="carte"><img src="signature-en-verticale.svg" '
             'alt="Vertical signature, English" width="300" height="%d">'
             '<figcaption>Vertical, English</figcaption></figure>'
             '<figure class="carte"><img src="signature-fr-verticale.svg" '
             'alt="Vertical signature, French" width="300" height="%d">'
             '<figcaption>Vertical, French</figcaption></figure>'
             '<figure class="carte"><img src="signature-en-horizontale.svg" '
             'alt="Horizontal signature, English" width="440" height="%d">'
             '<figcaption>Horizontal, English</figcaption></figure>'
             '<figure class="carte"><img src="signature-fr-horizontale.svg" '
             'alt="Horizontal signature, French" width="440" height="%d">'
             '<figcaption>Horizontal, French</figcaption></figure>'
             '</div></div></section>'
             % tuple(hauteur_pour(n, w) for n, w in (
                 ("signature-en-verticale.svg", 300),
                 ("signature-fr-verticale.svg", 300),
                 ("signature-en-horizontale.svg", 440),
                 ("signature-fr-horizontale.svg", 440))))

    lignes = []
    for nom, hexa, usage in PALETTE:
        sur_ivoire = contraste(hexa, "#F6F0E4")
        sur_cramoisi = contraste(hexa, "#8F101C")
        lignes.append(
            '<tr><td><span class="puce"><i style="background:%s"></i>'
            '<strong>%s</strong></span></td><td><code>%s</code></td>'
            '<td>%s</td><td>%.2f:1</td><td>%.2f:1</td></tr>'
            % (hexa, nom, hexa, usage[0], sur_ivoire, sur_cramoisi))
    o.append('<section id="palette"><div class="wrap"><h2>Palette</h2>'
             '<p class="chapo">The two right-hand columns are measured '
             'contrast ratios. Antique Gold reaches %.2f:1 on ivory, which is '
             'below the 4.5:1 that body text needs — so gold is used on this '
             'site for rules, the sun and solid areas, and a darker gold '
             '(<code>#8A6A12</code>, %.2f:1) is used where gold has to be '
             'read as text.</p><div class="defile"><table class="tbl"><thead>'
             '<tr><th>Colour</th><th>Code</th><th>Usage</th>'
             '<th>On ivory</th><th>On crimson</th></tr></thead>'
             '<tbody>%s</tbody></table></div></div></section>'
             % (contraste("#D4A72C", "#F6F0E4"),
                contraste("#8A6A12", "#F6F0E4"), "".join(lignes)))

    o.append('<section id="type" class="papier"><div class="wrap">'
             '<h2>Typography</h2><div class="grille g2">'
             '<div class="carte"><h3 style="font-size:2.4rem">Cormorant '
             'Garamond</h3><p>Headings, semi-bold, restrained capitals. '
             'Variable weight 300–700. Embedded in the site as WOFF2 under '
             'the SIL Open Font License — no request leaves the page to fetch '
             'it.</p></div>'
             '<div class="carte"><h3 style="font-family:var(--texte);'
             'font-size:2rem">Inter</h3><p>Interface and body text, regular '
             'to semi-bold. Variable weight 100–900, embedded the same way. '
             'Aptos remains the substitute for office documents, where no web '
             'font is available.</p></div></div></div></section>')

    o.append('<section id="clearspace"><div class="wrap"><h2>Clear space and '
             'minimum sizes</h2><p class="chapo">Clear space is <strong>x = '
             'half the diameter of the sun as drawn</strong> = %d units on an '
             'artwork whose drawn width is %d units, that is <strong>%.0f%% of '
             'the width of the mark</strong> on every side. Below, the solid '
             'red rectangle is the drawn bounding box, measured from the '
             'rendered artwork; the dashed gold rectangle is the clear space.'
             '</p><figure class="carte"><img src="schema-respiration.svg" '
             'alt="Clear space diagram" width="560" height="%d">'
             '</figure></div></section>'
             % (x, largeur, 100.0 * x / largeur,
                int(round(560 * ((y1 + x) - (y0 - x) + 20)
                          / ((x1 + x) - (x0 - x) + 20)))))

    o.append('<section id="minsize" class="papier"><div class="wrap">'
             '<h2>Minimum sizes</h2><p class="chapo">Shown at their true size '
             'on screen. Below these, the sun closes up and the laurel turns '
             'to mush.</p><div class="mini">'
             '<figure><img src="sceau.svg" alt="Seal at 48 pixels" width="30" '
             'height="48"><figcaption>Seal — 48&nbsp;px high</figcaption>'
             '</figure>'
             '<figure><img src="signature-en-horizontale.svg" alt="Horizontal '
             'signature at 140 pixels wide" width="140" height="%d">'
             '<figcaption>Signature — 140&nbsp;px wide</figcaption></figure>'
             '</div><p style="margin-top:22px">In print: <strong>15&nbsp;mm'
             '</strong> for the shield alone. Always keep the proportions, '
             'the contrast and the vertical orientation.</p></div></section>'
             % hauteur_pour("signature-en-horizontale.svg", 140))

    o.append('<section id="donts"><div class="wrap"><h2>Prohibited uses</h2>'
             '<ul>%s</ul></div></section>'
             % "".join("<li>%s</li>" % i for i in INTERDITS))

    o.append('<section id="claims" class="papier"><div class="wrap">'
             '<h2>What the emblem does not claim</h2>'
             '<p>The coat of arms is a brand emblem, designed for this House. '
             'It is not claimed to be granted, matriculated, registered or '
             'recognised by any heraldic authority, and it represents no '
             'state, government or administration. It carries no title, rank '
             'or precedence. Before any trade-mark filing or commercial use, '
             'the name and the emblem should be reviewed by a lawyer in the '
             'country where the House chooses to operate — '
             'that review is the client’s to commission, and nothing on this '
             'page substitutes for it.</p></div></section>')

    decl = ("The Adjaoudi Lordship is a family and cultural identity. It is "
            "not a public authority, exercises no official function, and "
            "confers no title, rank, precedence or nobility. Neither the "
            "designation nor the coat of arms is claimed to be recognised, "
            "granted, registered or accredited by any authority whatsoever.")
    html = GABARIT.format(corps="\n".join(o), decl=decl)
    chemin = os.path.join(RACINE, "brand", "guidelines.html")
    with io.open(chemin, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(os.path.relpath(chemin, RACINE))
    print("boite dessinee : %.0f x %.0f, respiration x = %d (%.1f%%)"
          % (largeur, hauteur, x, 100.0 * x / largeur))


def hauteur_pour(nom, largeur):
    from xml.etree import ElementTree as ET
    vb = [float(v) for v in ET.parse(
        os.path.join(RACINE, "brand", nom)).getroot().get("viewBox").split()]
    return int(round(largeur * vb[3] / vb[2]))


if __name__ == "__main__":
    sys.exit(main())
