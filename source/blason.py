# -*- coding: utf-8 -*-
"""Blason solaire Adjaoudi — generateur vectoriel.

Tout le blason est construit ici, en geometrie exacte : aucun trace n'est
dessine a la main, aucune image matricielle n'entre dans le systeme. Les
variantes (couleur, cramoisi monochrome, ivoire monochrome, sceau) sortent
de la meme geometrie, ce qui garantit qu'elles restent identiques entre
elles pour toujours.

Contraintes reprises telles quelles du cahier des charges du client :
  - soleil a SEIZE rayons (le nombre est interdit de modification) ;
  - branche de laurier stylisee ;
  - crete geometrique, « elevation symbolique sans imiter une insigne
    souveraine » — c'est pourquoi la crete est un fronton architectural a
    epaulements et non un cercle a pointes ;
  - aucune arme, aucun drapeau, aucun embleme national ou royal existant.
"""

import math
import os

# ---------------------------------------------------------------- palette
OR = "#D4A72C"
CRAMOISI = "#8F101C"
ROUGE = "#C51F2D"
IVOIRE = "#F6F0E4"
CHARBON = "#201A1A"

# --------------------------------------------------------------- cadrage
LARGEUR = 1000.0
HAUTEUR = 1120.0
CX = 500.0

ECU_HAUT = 205.0
ECU_BAS = 1015.0
ECU_DEMI = 245.0

# centre du champ, ou se pose le soleil
SOLEIL_Y = 590.0


def _fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def _pts(points):
    return " ".join("%s,%s" % (_fmt(x), _fmt(y)) for x, y in points)


# ------------------------------------------------------------------- ecu
def ecu_points():
    """Ecu facette : coins superieurs coupes, flancs droits, pointe basse.

    Renvoie la liste de sommets du contour exterieur. Les couches interieures
    sont obtenues par homothetie autour du centre optique de l'ecu, ce qui
    epaissit legerement la bordure a la pointe — exactement le rendu de la
    reference fournie par le client.
    """
    g = CX - ECU_DEMI
    d = CX + ECU_DEMI
    h = ECU_HAUT
    return [
        (g, h + 32), (g + 32, h), (d - 32, h), (d, h + 32),
        (d, 640), (d - 46, 802),
        (CX + 60, 968), (CX, ECU_BAS), (CX - 60, 968),
        (g + 46, 802), (g, 640),
    ]


ECU_CY = 560.0  # centre d'homothetie des couches


def ecu_couche(k):
    return [(CX + (x - CX) * k, ECU_CY + (y - ECU_CY) * k) for x, y in ecu_points()]


# --------------------------------------------------------------- soleil
RAYONS = 16
R_COEUR = 82.0
R_LONG = 198.0
R_COURT = 147.0
DEMI_ANGLE = math.radians(360.0 / RAYONS / 2.0 * 0.62)


def rayons_soleil():
    """Seize rayons, alternes long / court, en triangles effiles."""
    out = []
    for i in range(RAYONS):
        a = -math.pi / 2 + i * 2 * math.pi / RAYONS
        rr = R_LONG if i % 2 == 0 else R_COURT
        p = [
            (CX + R_COEUR * math.cos(a - DEMI_ANGLE),
             SOLEIL_Y + R_COEUR * math.sin(a - DEMI_ANGLE)),
            (CX + rr * math.cos(a), SOLEIL_Y + rr * math.sin(a)),
            (CX + R_COEUR * math.cos(a + DEMI_ANGLE),
             SOLEIL_Y + R_COEUR * math.sin(a + DEMI_ANGLE)),
        ]
        out.append(p)
    return out


# ---------------------------------------------------------------- laurier
def laurier(cote):
    """Une branche de laurier stylisee, en dehors de l'ecu.

    cote = -1 (gauche) ou +1 (droite). La tige est une quadratique ; les
    feuilles sont des amandes (deux arcs) posees le long de la tige, la
    pointe vers le bas et vers l'exterieur, decroissantes vers le haut.
    """
    x0, y0 = CX + cote * 258, 946.0     # pied, pres de la pointe de l'ecu
    x1, y1 = CX + cote * 322, 640.0     # controle
    x2, y2 = CX + cote * 268, 272.0     # tete

    def point(t):
        u = 1 - t
        return (u * u * x0 + 2 * u * t * x1 + t * t * x2,
                u * u * y0 + 2 * u * t * y1 + t * t * y2)

    def tangente(t):
        u = 1 - t
        return (2 * u * (x1 - x0) + 2 * t * (x2 - x1),
                2 * u * (y1 - y0) + 2 * t * (y2 - y1))

    tige = ('M%s,%s Q%s,%s %s,%s' % (_fmt(x0), _fmt(y0), _fmt(x1), _fmt(y1),
                                     _fmt(x2), _fmt(y2)))
    feuilles = []
    n = 8
    for i in range(n):
        t = 0.10 + i * (0.86 / (n - 1))
        px, py = point(t)
        tx, ty = tangente(t)
        ang = math.degrees(math.atan2(ty, tx))
        lg = 112 - 50 * t          # longueur de la feuille
        la = 31 - 12 * t           # demi-largeur
        # amande dessinee a l'origine, pointe vers +x, puis posee sur la tige
        d = ("M0,0 Q%s,%s %s,0 Q%s,%s 0,0 Z"
             % (_fmt(lg * 0.45), _fmt(-la), _fmt(lg),
                _fmt(lg * 0.45), _fmt(la)))
        # la feuille part de la tige vers l'exterieur et vers le bas
        rot = ang + cote * 118
        feuilles.append((d, px, py, rot))
    return tige, feuilles


# ----------------------------------------------------------------- crete
def crete():
    """Crete geometrique : bandeau + fronton a epaulements.

    Volontairement architecturale. Un cercle a pointes lirait comme une
    couronne, ce que le cahier des charges du client interdit lui-meme.
    """
    bandeau = (340.0, 176.0, 320.0, 30.0)          # x, y, w, h
    incruste = (352.0, 183.0, 296.0, 16.0)
    fronton = [(404, 177), (CX, 86), (596, 177)]
    epaule_g = [(340, 177), (340, 139), (404, 139), (404, 177)]
    epaule_d = [(660, 177), (660, 139), (596, 139), (596, 177)]
    return bandeau, incruste, fronton, epaule_g, epaule_d


# ------------------------------------------------------------ assemblage
def blason(mode="plein", crete_on=True, laurier_on=True, teinte=None,
           fond=None):
    """mode : 'plein' (quadrichromie) ou 'mono' (une seule teinte)."""
    e = []
    if fond:
        e.append('<rect width="%s" height="%s" fill="%s"/>'
                 % (_fmt(LARGEUR), _fmt(HAUTEUR), fond))

    if mode == "plein":
        c_coque, c_filet, c_champ = OR, IVOIRE, CRAMOISI
        c_rayon, c_laurier, c_crete, c_incruste = OR, OR, OR, CRAMOISI
    else:
        t = teinte or CRAMOISI
        c_coque, c_filet, c_champ = t, "none", "none"
        c_rayon, c_laurier, c_crete, c_incruste = t, t, t, "none"

    # --- laurier (sous l'ecu)
    if laurier_on:
        for cote in (-1, 1):
            tige, feuilles = laurier(cote)
            e.append('<path d="%s" fill="none" stroke="%s" stroke-width="11" '
                     'stroke-linecap="round"/>' % (tige, c_laurier))
            for d, px, py, rot in feuilles:
                e.append('<path d="%s" fill="%s" transform="translate(%s,%s) '
                         'rotate(%s)"/>'
                         % (d, c_laurier, _fmt(px), _fmt(py), _fmt(rot)))

    # --- crete
    if crete_on:
        (bx, by, bw, bh), (ix, iy, iw, ih), fr, eg, ed = crete()
        e.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
                 % (_fmt(bx), _fmt(by), _fmt(bw), _fmt(bh), c_crete))
        if c_incruste != "none":
            e.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
                     % (_fmt(ix), _fmt(iy), _fmt(iw), _fmt(ih), c_incruste))
        e.append('<polygon points="%s" fill="%s"/>' % (_pts(fr), c_crete))
        e.append('<polygon points="%s" fill="%s"/>' % (_pts(eg), c_crete))
        e.append('<polygon points="%s" fill="%s"/>' % (_pts(ed), c_crete))

    # --- ecu
    if mode == "plein":
        e.append('<polygon points="%s" fill="%s"/>' % (_pts(ecu_couche(1.0)), c_coque))
        e.append('<polygon points="%s" fill="%s"/>' % (_pts(ecu_couche(0.945)), c_filet))
        e.append('<polygon points="%s" fill="%s"/>' % (_pts(ecu_couche(0.895)), c_champ))
    else:
        e.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="17" '
                 'stroke-linejoin="round"/>' % (_pts(ecu_couche(0.97)), c_coque))
        e.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="6" '
                 'stroke-linejoin="round"/>' % (_pts(ecu_couche(0.885)), c_coque))

    # --- soleil
    for p in rayons_soleil():
        e.append('<polygon points="%s" fill="%s"/>' % (_pts(p), c_rayon))
    if mode == "plein":
        e.append('<circle cx="%s" cy="%s" r="80" fill="%s"/>' % (_fmt(CX), _fmt(SOLEIL_Y), OR))
        e.append('<circle cx="%s" cy="%s" r="72" fill="%s"/>' % (_fmt(CX), _fmt(SOLEIL_Y), IVOIRE))
        e.append('<circle cx="%s" cy="%s" r="64" fill="%s"/>' % (_fmt(CX), _fmt(SOLEIL_Y), ROUGE))
        e.append('<circle cx="%s" cy="%s" r="43" fill="%s"/>' % (_fmt(CX), _fmt(SOLEIL_Y), OR))
    else:
        t = teinte or CRAMOISI
        e.append('<circle cx="%s" cy="%s" r="76" fill="none" stroke="%s" stroke-width="7"/>'
                 % (_fmt(CX), _fmt(SOLEIL_Y), t))
        e.append('<circle cx="%s" cy="%s" r="62" fill="none" stroke="%s" stroke-width="13"/>'
                 % (_fmt(CX), _fmt(SOLEIL_Y), t))
        e.append('<circle cx="%s" cy="%s" r="36" fill="%s"/>' % (_fmt(CX), _fmt(SOLEIL_Y), t))
    return e


def halo():
    """Anneau solaire tres large, en trait fin : le fond anime du heros.

    Seize rayons, comme le blason. Il ne porte aucun sens heraldique : c'est
    une trame, et il est masque aux lecteurs d'ecran.
    """
    e = []
    for i in range(RAYONS):
        a = -math.pi / 2 + i * 2 * math.pi / RAYONS
        rr = 470.0 if i % 2 == 0 else 352.0
        e.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                 'stroke-width="7" stroke-linecap="round"/>'
                 % (_fmt(CX + 150 * math.cos(a)), _fmt(CX + 150 * math.sin(a)),
                    _fmt(CX + rr * math.cos(a)), _fmt(CX + rr * math.sin(a)), OR))
    e.append('<circle cx="%s" cy="%s" r="128" fill="none" stroke="%s" '
             'stroke-width="7"/>' % (_fmt(CX), _fmt(CX), OR))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" '
            'aria-hidden="true" focusable="false">\n%s\n</svg>\n'
            % "\n".join(e))


def cadre(elements, x, y, w, h, titre, desc):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s %s %s %s" '
            'role="img" aria-labelledby="t d">\n'
            '<title id="t">%s</title>\n<desc id="d">%s</desc>\n%s\n</svg>\n'
            % (_fmt(x), _fmt(y), _fmt(w), _fmt(h), titre, desc, "\n".join(elements)))


# ------------------------------------------------------- mot-marque texte
def _instance(chemin, poids):
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    f = TTFont(chemin)
    return instancer.instantiateVariableFont(f, {"wght": poids}, inplace=False)


def mot_en_traces(texte, chemin_police, poids, taille, interlettre=0.0):
    """Rend une chaine en traces SVG (le fichier reste autonome, sans police).

    Renvoie (path_d, largeur, hauteur_em, ascendante).
    """
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Identity

    f = _instance(chemin_police, poids)
    upem = f["head"].unitsPerEm
    ech = taille / float(upem)
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hmtx = f["hmtx"]

    stylo = SVGPathPen(gs)
    x = 0.0
    for ch in texte:
        nom = cmap.get(ord(ch))
        if nom is None:
            x += taille * 0.35 + interlettre
            continue
        tr = Identity.translate(x, 0).scale(ech, -ech)
        gs[nom].draw(TransformPen(stylo, tr))
        x += hmtx[nom][0] * ech + interlettre
    if texte:
        x -= interlettre
    asc = f["hhea"].ascent * ech
    desc = f["hhea"].descent * ech
    f.close()
    return stylo.getCommands(), x, asc, desc


# ------------------------------------------------------------------ sortie
def ecrire(chemin, contenu):
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(contenu)
    return os.path.basename(chemin)


_ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(_ICI) if os.path.basename(_ICI) == "source" else _ICI
POLICES = os.path.join(RACINE, "assets", "fonts")

TITRE = "Blason solaire de la Seigneurie Adjaoudi"
DESC = ("Ecu cramoisi charge d'un soleil d'or a seize rayons, filet d'ivoire, "
        "crete geometrique et deux branches de laurier. Embleme familial et "
        "culturel ; il ne represente aucune autorite publique.")


def tout():
    marque = os.path.join(RACINE, "brand")
    actifs = os.path.join(RACINE, "assets")
    if not os.path.isdir(marque):
        os.makedirs(marque)
    faits = []

    # 1. blason complet, quadrichromie
    faits.append(ecrire(os.path.join(marque, "blason-couleur.svg"),
                        cadre(blason("plein"), 60, 40, 880, 1040, TITRE, DESC)))
    # 2. monochrome cramoisi
    faits.append(ecrire(os.path.join(marque, "blason-cramoisi.svg"),
                        cadre(blason("mono", teinte=CRAMOISI), 60, 40, 880, 1040,
                              TITRE + " — monochrome cramoisi", DESC)))
    # 3. monochrome ivoire sur fond sombre
    faits.append(ecrire(os.path.join(marque, "blason-ivoire.svg"),
                        cadre(blason("mono", teinte=IVOIRE), 60, 40, 880, 1040,
                              TITRE + " — monochrome ivoire", DESC)))
    # 4. sceau : ecu et soleil seuls
    faits.append(ecrire(os.path.join(marque, "sceau.svg"),
                        cadre(blason("plein", crete_on=False, laurier_on=False),
                              240, 190, 520, 840, "Sceau Adjaoudi", DESC)))
    # 5. le meme sceau pour le site
    ecrire(os.path.join(actifs, "sceau.svg"),
           cadre(blason("plein", crete_on=False, laurier_on=False),
                 240, 190, 520, 840, "Sceau Adjaoudi", DESC))
    ecrire(os.path.join(actifs, "blason-couleur.svg"),
           cadre(blason("plein"), 60, 40, 880, 1040, TITRE, DESC))
    ecrire(os.path.join(actifs, "blason-ivoire.svg"),
           cadre(blason("mono", teinte=IVOIRE), 60, 40, 880, 1040,
                 TITRE + " — monochrome ivoire", DESC))

    # 6. favicon : sceau reduit, lisible a 16 px
    fav = blason("plein", crete_on=False, laurier_on=False)
    faits.append(ecrire(os.path.join(actifs, "favicon.svg"),
                        cadre(fav, 250, 200, 500, 830, "Adjaoudi", DESC)))

    # 6b. halo du heros
    faits.append(ecrire(os.path.join(actifs, "halo.svg"), halo()))

    # 7. signatures (texte converti en traces : aucun besoin de police)
    for cle, nom, devise, fichier in (
            ("en", "ADJAOUDI LORDSHIP", "Heritage illuminates the future.",
             "signature-en"),
            ("fr", "SEIGNEURIE ADJAOUDI", "Le patrimoine éclaire l'avenir.",
             "signature-fr")):
        for sens in ("verticale", "horizontale"):
            faits.append(signature(nom, devise, sens,
                                   os.path.join(marque, "%s-%s.svg"
                                                % (fichier, sens))))
    return faits


def signature(nom, devise, sens, chemin):
    cor = os.path.join(POLICES, "cormorant-latin.woff2")
    inter = os.path.join(POLICES, "inter-latin.woff2")
    d_nom, l_nom, a_nom, _ = mot_en_traces(nom, cor, 600, 68, interlettre=6.0)
    d_dev, l_dev, a_dev, _ = mot_en_traces(devise, inter, 400, 23, interlettre=0.8)

    if sens == "verticale":
        ech = 0.42
        bw, bh = 880 * ech, 1040 * ech
        L = max(bw, l_nom, l_dev) + 80
        H = bh + 30 + a_nom + 26 + a_dev + 36
        e = ['<g transform="translate(%s,20) scale(%s) translate(-60,-40)">'
             % (_fmt((L - bw) / 2), _fmt(ech))]
        e += blason("plein")
        e.append('</g>')
        y1 = 20 + bh + 30 + a_nom
        e.append('<path d="%s" fill="%s" transform="translate(%s,%s)"/>'
                 % (d_nom, CRAMOISI, _fmt((L - l_nom) / 2), _fmt(y1)))
        y2 = y1 + 26 + a_dev
        e.append('<path d="%s" fill="%s" transform="translate(%s,%s)"/>'
                 % (d_dev, CHARBON, _fmt((L - l_dev) / 2), _fmt(y2)))
        return ecrire(chemin, cadre(e, 0, 0, L, H, nom, DESC))

    ech = 0.30
    bw, bh = 880 * ech, 1040 * ech
    ecart = 40
    L = bw + ecart + max(l_nom, l_dev) + 20
    H = max(bh + 40, 200)
    e = ['<g transform="translate(10,%s) scale(%s) translate(-60,-40)">'
         % (_fmt((H - bh) / 2), _fmt(ech))]
    e += blason("plein")
    e.append('</g>')
    bloc = a_nom + 26 + a_dev
    y1 = (H - bloc) / 2 + a_nom
    x = 10 + bw + ecart
    e.append('<path d="%s" fill="%s" transform="translate(%s,%s)"/>'
             % (d_nom, CRAMOISI, _fmt(x), _fmt(y1)))
    e.append('<path d="%s" fill="%s" transform="translate(%s,%s)"/>'
             % (d_dev, CHARBON, _fmt(x), _fmt(y1 + 26 + a_dev)))
    return ecrire(chemin, cadre(e, 0, 0, L, H, nom, DESC))


if __name__ == "__main__":
    for f in tout():
        print(f)
