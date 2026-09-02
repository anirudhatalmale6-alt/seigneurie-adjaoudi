# -*- coding: utf-8 -*-
"""Construit le site de la Seigneurie Adjaoudi, en anglais et en francais.

  python3 source/build.py

Ecrit les pages anglaises a la racine et les pages francaises dans fr/,
plus l'index de recherche de chaque langue. Aucune page n'est editee a la
main : tout passe par ici, sinon la prochaine construction efface la
retouche.
"""

import io
import json
import os
import re
import sys

_ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(_ICI) if os.path.basename(_ICI) == "source" else _ICI
sys.path.insert(0, _ICI)

import contenu as C  # noqa: E402

VERSION_CSS = 1
INDEX = {"en": [], "fr": []}
_page_courante = {}


# ------------------------------------------------------------------ outils
def t(paire, lang):
    return paire[0] if lang == "en" else paire[1]


def ech(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def sans_balises(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def fichier(cle, lang):
    for k, fen, ffr, _te, _tf, _m in C.PAGES:
        if k == cle:
            return fen if lang == "en" else ffr
    raise KeyError(cle)


def titre_page(cle, lang):
    for k, _fen, _ffr, te, tf, _m in C.PAGES:
        if k == cle:
            return te if lang == "en" else tf
    raise KeyError(cle)


def lien(cle, lang, depuis):
    """Lien vers la page `cle` en langue `lang`, depuis une page en `depuis`."""
    f = fichier(cle, lang)
    if depuis == "en":
        return f if lang == "en" else "fr/" + f
    return f if lang == "fr" else "../" + f


def actif(nom, depuis):
    return ("assets/" if depuis == "en" else "../assets/") + nom


# --------------------------------------------------------------- fragments
def att(lang):
    return '<span class="att">%s</span>' % ech(t(C.ATTENTE, lang))


def sec(cle_page, lang, ident, titre, corps, index=True, classe="",
        index_txt=None):
    """Une section, et son entree dans l'index de recherche."""
    if index:
        INDEX[lang].append({
            "u": fichier(cle_page, lang) + ("#" + ident if ident else ""),
            "p": titre_page(cle_page, lang),
            "t": sans_balises(titre) if titre else titre_page(cle_page, lang),
            "x": (index_txt if index_txt is not None
                  else sans_balises(corps))[:340],
        })
    ouv = '<section id="%s"%s>' % (ident, ' class="%s"' % classe if classe else "")
    tt = "<h2>%s</h2>" % titre if titre else ""
    return '%s<div class="wrap">%s%s</div></section>' % (ouv, tt, corps)


def carte(titre, texte, pied=""):
    return ('<article class="carte"><h3>%s</h3><p>%s</p>%s</article>'
            % (titre, texte, pied))


def bande(lang, sur, titre, sous):
    return ('<div class="bande">'
            '<img class="marque" src="%s" alt="" width="210" height="248" '
            'aria-hidden="true">'
            '<div class="wrap"><p class="sur">%s</p>'
            '<h1>%s</h1><p>%s</p></div></div>'
            % (actif("blason-ivoire.svg", lang), ech(sur), ech(titre),
               ech(sous)))


LOUPE = ('<svg width="16" height="16" viewBox="0 0 20 20" aria-hidden="true" '
         'focusable="false"><circle cx="8.5" cy="8.5" r="6" fill="none" '
         'stroke="currentColor" stroke-width="2"/><line x1="13" y1="13" '
         'x2="18" y2="18" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round"/></svg>')

BARRES = ('<svg width="17" height="14" viewBox="0 0 18 14" aria-hidden="true" '
          'focusable="false"><g stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round"><line x1="1" y1="1" x2="17" y2="1"/>'
          '<line x1="1" y1="7" x2="17" y2="7"/><line x1="1" y1="13" x2="17" '
          'y2="13"/></g></svg>')


def entete(cle, lang):
    liens = []
    for k, _fen, _ffr, te, tf, menu in C.PAGES:
        if not menu:
            continue
        cur = ' aria-current="page"' if k == cle else ""
        liens.append('<a href="%s"%s>%s</a>'
                     % (lien(k, lang, lang), cur, ech(te if lang == "en" else tf)))
    autre = "fr" if lang == "en" else "en"
    langues = (
        '<div class="langues">'
        '<a href="%s" hreflang="en" lang="en"%s>EN</a><span>/</span>'
        '<a href="%s" hreflang="fr" lang="fr"%s>FR</a></div>'
        % (lien(cle, "en", lang), ' aria-current="true"' if lang == "en" else "",
           lien(cle, "fr", lang), ' aria-current="true"' if lang == "fr" else ""))
    cur_c = ' aria-current="page"' if cle == "circle" else ""
    util = ('<div class="util"><div class="wrap">'
            '<button class="loupe" type="button" aria-label="%s" '
            'aria-haspopup="dialog">%s</button>%s'
            '<a class="pcircle" href="%s"%s>%s</a>'
            '</div></div>'
            % (ech(t(C.RECHERCHE, lang)), LOUPE, langues,
               lien("circle", lang, lang), cur_c,
               ech(titre_page("circle", lang))))
    return ('<a class="saut" href="#contenu">%s</a>%s'
            '<header class="hdr"><div class="wrap">'
            '<a class="brand" href="%s"><img src="%s" alt="" width="29" '
            'height="47"><span class="nm"><span class="n1">%s</span>'
            '<span class="n2">%s</span></span></a>'
            '<button class="bascule" type="button" aria-expanded="false" '
            'aria-controls="menu" aria-label="%s">%s</button>'
            '<div class="panneau" id="menu">'
            '<nav class="nav" aria-label="%s">%s</nav>'
            '<a class="cta" href="%s">%s</a>'
            '</div></div></header>'
            % (ech(t(C.ALLER_CONTENU, lang)), util,
               lien("home", lang, lang), actif("sceau.svg", lang),
               ech("Adjaoudi"),
               ech("Lordship" if lang == "en" else "Seigneurie"),
               ech("Menu"), BARRES,
               ech("Main" if lang == "en" else "Principal"), "".join(liens),
               lien("lordship", lang, lang), ech(t(C.DECOUVRIR, lang))))


def panneau_recherche(lang):
    return ('<div class="rech" id="rech" role="dialog" aria-modal="true" '
            'aria-label="%s"><div class="boite">'
            '<div class="barre"><label class="sr" for="q">%s</label>'
            '<input id="q" type="search" autocomplete="off" placeholder="%s">'
            '<button class="fermer" type="button">%s</button></div>'
            '<ul class="res" id="res"></ul>'
            '<p class="sr" id="rech-vide">%s</p></div></div>'
            % (ech(t(C.RECHERCHE, lang)), ech(t(C.RECHERCHE, lang)),
               ech(t(C.RECHERCHE_INVITE, lang)), ech(t(C.FERMER, lang)),
               ech(t(C.RECHERCHE_VIDE, lang))))


def pied(lang):
    cols = []
    liens = []
    for k, _fen, _ffr, te, tf, menu in C.PAGES:
        if k == "home":
            continue
        liens.append('<li><a href="%s">%s</a></li>'
                     % (lien(k, lang, lang), ech(te if lang == "en" else tf)))
    cols.append('<div><h4>%s</h4><ul>%s</ul></div>'
                % (ech("Sections" if lang == "en" else "Sections"),
                   "".join(liens)))
    cols.append('<div><h4>%s</h4><ul>%s</ul></div>'
                % (ech(t(C.PIED_CANAUX, lang)),
                   '<li>%s</li>' % att(lang)))
    cols.append('<div><h4>%s</h4><ul>'
                '<li><a href="%s" hreflang="en">English</a></li>'
                '<li><a href="%s" hreflang="fr">Français</a></li></ul>'
                '<p style="font-size:.83rem;color:#B0A49A">%s</p></div>'
                % (ech(t(C.PIED_LANGUES, lang)),
                   lien(_page_courante["cle"], "en", lang),
                   lien(_page_courante["cle"], "fr", lang),
                   ech(t(C.LANGUES_APRES, lang))))
    return ('<footer class="pied"><div class="wrap"><div class="cols">%s</div>'
            '<p class="decl">%s</p>'
            '<p class="bas">%s</p></div></footer>'
            % ("".join(cols), ech(t(C.PIED_DECLARATION, lang)),
               ech(t(C.MAISON, lang))))


GABARIT = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{fav}" type="image/svg+xml">
<link rel="stylesheet" href="{css}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="fr" href="{alt_fr}">
<script>document.documentElement.className+=" js";</script>
</head>
<body>
{entete}
<main id="contenu">
{corps}
</main>
{pied}
{rech}
<script src="{idx}"></script>
<script src="{js}"></script>
<noscript><p class="sr">{nojs}</p></noscript>
</body>
</html>
"""


def page(cle, lang, corps, description):
    _page_courante["cle"] = cle
    nom = t(C.MAISON, lang)
    tt = nom if cle == "home" else "%s — %s" % (titre_page(cle, lang), nom)
    return GABARIT.format(
        lang=lang, titre=ech(tt), desc=ech(description),
        fav=actif("favicon.svg", lang),
        css=actif("site.css", lang) + "?v=%d" % VERSION_CSS,
        alt_en=lien(cle, "en", lang), alt_fr=lien(cle, "fr", lang),
        entete=entete(cle, lang), corps=corps, pied=pied(lang),
        rech=panneau_recherche(lang),
        idx=actif("index-%s.js" % lang, lang),
        js=actif("site.js", lang) + "?v=%d" % VERSION_CSS,
        nojs=ech(t(C.RECHERCHE_SANS_JS, lang)))


# ------------------------------------------------------------------- pages
def p_home(lang):
    o = []
    o.append('<div class="hero"><div class="halo" aria-hidden="true">'
             '<img src="%s" alt="" width="820" height="820"></div>'
             '<div class="wrap">'
             '<img class="arm" src="%s" width="132" height="156" alt="%s">'
             '<h1>%s</h1><p class="devise">%s</p><p class="note">%s</p>'
             '<a class="cta" href="%s">%s</a></div></div>'
             % (actif("halo.svg", lang), actif("blason-ivoire.svg", lang),
                ech("Coat of arms of the Adjaoudi Lordship" if lang == "en"
                    else "Blason de la Seigneurie Adjaoudi"),
                ech(t(C.MAISON, lang)), ech(t(C.DEVISE, lang)),
                ech(t(C.DEVISE_NOTE, lang)),
                lien("lordship", lang, lang), ech(t(C.DECOUVRIR, lang))))

    man = "".join("<p>%s</p>" % ech(t(p, lang)) for p in C.MANIFESTE)
    o.append(sec("home", lang, "manifesto", ech(t(C.MANIFESTE_TITRE, lang)),
                 '<hr class="filet">%s' % man, classe="papier"))

    portes = "".join(
        carte(ech(t(nom, lang)), ech(t(txt, lang)),
              '<a class="plus" href="%s">%s</a>'
              % (lien(k, lang, lang), ech(titre_page(k, lang))))
        for k, nom, txt in C.PORTES)
    o.append(sec("home", lang, "gateways",
                 ech("Three ways in" if lang == "en" else "Trois entrées"),
                 '<div class="grille g3">%s</div>' % portes))

    o.append(sec("home", lang, "timeline", ech(t(C.FRISE_TITRE, lang)),
                 frise(lang), classe="papier"))

    sel = "".join(
        '<article class="carte"><p class="att">%s</p><h3>%s</h3>'
        '<p>%s</p></article>'
        % (ech(t(C.ATTENTE, lang)), ech(t(quoi, lang)), ech(t(ou, lang)))
        for quoi, ou in C.SELECTION)
    o.append(sec("home", lang, "selection", ech(t(C.SELECTION_TITRE, lang)),
                 '<p class="chapo">%s</p><div class="grille g3">%s</div>'
                 % (ech(t(C.ATTENTE_LONG, lang)), sel)))

    o.append(sec("home", lang, "news", ech(t(C.INFOLETTRE_TITRE, lang)),
                 '<p class="chapo">%s</p>%s'
                 % (ech(t(C.INFOLETTRE, lang)), formulaire_lettre(lang)),
                 classe="papier"))
    return "\n".join(o), t(C.MANIFESTE[0], lang)


def frise(lang):
    champs = "".join(
        '<li><span class="quoi">%s</span> — <span class="det">%s</span></li>'
        % (ech(t(nom, lang)), ech(t(txt, lang))) for nom, txt in C.FRISE_CHAMPS)
    return ('<div class="vide"><p>%s %s</p><p>%s</p></div>'
            '<h3>%s</h3><ul class="frise">%s</ul>'
            % (att(lang), ech(t(C.FRISE_VIDE, lang)),
               ech(t(C.FRISE_REGLE, lang)),
               ech("What an entry carries" if lang == "en"
                   else "Ce que porte une entrée"), champs))


def formulaire_lettre(lang):
    return ('<form class="form" onsubmit="return false"><p class="maq">%s</p>'
            '<div class="champ"><label for="lettre">%s</label>'
            '<input id="lettre" type="text" autocomplete="off"></div>'
            '<button class="bouton" type="button" disabled>%s</button></form>'
            % (ech(t(C.MAQUETTE, lang)),
               ech("How to reach you" if lang == "en"
                   else "Comment vous joindre"),
               ech(t(C.ENVOYER, lang))))


def p_lordship(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("lordship", lang),
               t(C.MANIFESTE[1], lang))]

    est = "".join("<li>%s</li>" % ech(t(x, lang)) for x in C.STATUT_EST)
    nest = "".join("<li>%s</li>" % ech(t(x, lang)) for x in C.STATUT_NEST_PAS)
    o.append(sec("lordship", lang, "designation", ech(t(C.STATUT_TITRE, lang)),
                 '<div class="grille g2">'
                 '<div class="carte"><h3>%s</h3><ul>%s</ul></div>'
                 '<div class="carte"><h3>%s</h3><ul>%s</ul></div></div>'
                 % (ech("What it is" if lang == "en" else "Ce qu’elle est"), est,
                    ech("What it is not" if lang == "en"
                        else "Ce qu’elle n’est pas"), nest),
                 classe="papier"))

    blocs = "".join(
        '<div class="carte"><p class="att">%s</p><h3>%s</h3><p>%s</p></div>'
        % (ech(t(C.ATTENTE, lang)), ech(t(nom, lang)), ech(t(txt, lang)))
        for _k, nom, txt in C.SEIGNEURIE_BLOCS)
    o.append(sec("lordship", lang, "origin",
                 ech("Origin and name" if lang == "en"
                     else "Origine et nom"),
                 '<p class="chapo">%s</p><div class="grille g3">%s</div>'
                 % (ech(t(C.ATTENTE_LONG, lang)), blocs)))

    o.append(sec("lordship", lang, "timeline", ech(t(C.FRISE_TITRE, lang)),
                 frise(lang), classe="papier"))

    val = "".join(carte(ech(t(nom, lang)), ech(t(txt, lang)))
                  for nom, txt in C.VALEURS)
    o.append(sec("lordship", lang, "values", ech(t(C.VALEURS_TITRE, lang)),
                 '<p class="chapo">%s</p><div class="grille g3">%s</div>'
                 % (ech(t(C.VALEURS_INTRO, lang)), val)))
    return "\n".join(o), "%s %s" % (t(C.STATUT_TITRE, lang),
                                   t(C.STATUT_NEST_PAS[1], lang))


def p_heritage(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("heritage", lang),
               t(C.PATRIMOINE_INTRO, lang))]
    cartes = "".join(
        '<article class="carte"><p class="att">%s</p><h3>%s</h3><p>%s</p>'
        '</article>'
        % (ech(t(C.ATTENTE, lang)), ech(t(nom, lang)), ech(t(txt, lang)))
        for _k, nom, txt in C.PATRIMOINE)
    o.append(sec("heritage", lang, "collections",
                 ech("Collections" if lang == "en" else "Ensembles"),
                 '<div class="grille g3">%s</div>' % cartes, classe="papier"))

    cols = "".join("<th scope=\"col\">%s</th>" % ech(t(c, lang))
                   for c in C.DROITS_COLONNES)
    o.append(sec("heritage", lang, "rights", ech(t(C.DROITS_TITRE, lang)),
                 '<p class="chapo">%s</p><div class="defile">'
                 '<table class="tbl"><thead><tr>%s</tr></thead><tbody>'
                 '<tr class="rien"><td colspan="%d">%s</td></tr>'
                 '</tbody></table></div>'
                 % (ech(t(C.DROITS_INTRO, lang)), cols, len(C.DROITS_COLONNES),
                    ech("No item is registered." if lang == "en"
                        else "Aucune pièce n’est enregistrée."))))

    o.append(sec("heritage", lang, "corrections",
                 ech(t(C.CORRECTION_TITRE, lang)),
                 '<p>%s</p>' % ech(t(C.CORRECTION, lang)), classe="papier"))
    return "\n".join(o), t(C.PATRIMOINE_INTRO, lang)


def p_house(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("house", lang),
               t(C.MAISON_INTRO, lang))]
    cond = "".join("<li>%s</li>" % ech(t(x, lang)) for x in C.MAISON_CONDITIONS)
    o.append(sec("house", lang, "rule",
                 ech("Two conditions" if lang == "en" else "Deux conditions"),
                 '<ul>%s</ul><div class="vide"><p>%s</p></div>'
                 % (cond, ech(t(C.MAISON_DEFAUT, lang))), classe="papier"))
    o.append(sec("house", lang, "branches", ech(t(C.BRANCHES_TITRE, lang)),
                 '<div class="vide"><p>%s %s</p></div>'
                 % (att(lang), ech(t(C.ATTENTE_LONG, lang)))))
    cases = "".join('<div class="case">%s</div>' % ech(t(C.ATTENTE, lang))
                    for _ in range(6))
    o.append(sec("house", lang, "portraits", ech(t(C.PORTRAITS_TITRE, lang)),
                 '<p class="chapo">%s</p><div class="cases">%s</div>'
                 % (ech(t(C.PORTRAITS_NOTE, lang)), cases), classe="papier"))
    roles = "".join(
        '<tr><td><strong>%s</strong></td><td>%s</td></tr>'
        % (ech(t(nom, lang)), ech(t(txt, lang))) for nom, txt in C.ROLES)
    o.append(sec("house", lang, "roles", ech(t(C.ROLES_TITRE, lang)),
                 '<p class="chapo">%s</p><div class="defile">'
                 '<table class="tbl"><tbody>%s</tbody></table></div>'
                 % (ech("Who may do what, once the site is administered from a "
                        "content system." if lang == "en"
                        else "Qui peut faire quoi, une fois le site administré "
                             "depuis un système de contenu."), roles)))
    return "\n".join(o), t(C.MAISON_INTRO, lang)


def p_initiatives(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("initiatives", lang),
               t(C.INITIATIVES_INTRO, lang))]
    cartes = "".join(
        '<article class="carte" id="%s"><h3>%s</h3><p>%s</p>'
        '<p class="att">%s</p></article>'
        % (k, ech(t(nom, lang)), ech(t(txt, lang)), ech(t(C.ATTENTE, lang)))
        for k, nom, txt in C.INITIATIVES)
    o.append(sec("initiatives", lang, "fields",
                 ech("Five fields" if lang == "en" else "Cinq domaines"),
                 '<div class="grille g3">%s</div>' % cartes, classe="papier"))
    return "\n".join(o), t(C.INITIATIVES_INTRO, lang)


def p_journal(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("journal", lang),
               t(C.JOURNAL_VIDE, lang))]
    types = "".join('<li><span>%s</span></li>' % ech(t(x, lang))
                    for x in C.JOURNAL_TYPES)
    o.append(sec("journal", lang, "entries",
                 ech("Entries" if lang == "en" else "Entrées"),
                 '<ul class="filtres">%s</ul>'
                 '<div class="vide"><p>%s %s</p><p>%s</p></div>'
                 % (types, att(lang), ech(t(C.JOURNAL_VIDE, lang)),
                    ech(t(C.ATTENTE_LONG, lang))), classe="papier"))
    regles = "".join("<li>%s</li>" % ech(t(x, lang)) for x in C.CHARTE)
    o.append(sec("journal", lang, "rule", ech(t(C.CHARTE_TITRE, lang)),
                 "<ul>%s</ul>" % regles))
    return "\n".join(o), t(C.CHARTE[0], lang)


def p_media(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("media", lang),
               t(C.MEDIA_INTRO, lang))]
    filtres = "".join('<li><span>%s</span></li>' % ech(t(x, lang))
                      for x in C.MEDIA_FILTRES)
    cases = "".join('<div class="case">%s</div>' % ech(t(C.ATTENTE, lang))
                    for _ in range(8))
    o.append(sec("media", lang, "albums",
                 ech("Albums" if lang == "en" else "Albums"),
                 '<ul class="filtres">%s</ul><div class="cases">%s</div>'
                 % (filtres, cases), classe="papier"))
    o.append(sec("media", lang, "imagery",
                 ech("Image direction" if lang == "en"
                     else "Direction des images"),
                 "<p>%s</p>" % ech(t(C.MEDIA_REGLE, lang))))
    return "\n".join(o), t(C.MEDIA_INTRO, lang)


def p_contact(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("contact", lang),
               t(C.CONTACT_INTRO, lang))]
    formulaires = []
    for k, nom, txt in C.FORMULAIRES:
        champs = []
        for etiq, genre in C.CHAMPS:
            idc = "%s-%s" % (k, sans_balises(etiq[0]).lower().replace(" ", "-"))
            if genre == "textarea":
                ch = '<textarea id="%s"></textarea>' % idc
            else:
                ch = '<input id="%s" type="text" autocomplete="off">' % idc
            champs.append('<div class="champ"><label for="%s">%s</label>%s</div>'
                          % (idc, ech(t(etiq, lang)), ch))
        formulaires.append(
            '<form class="form" id="%s" onsubmit="return false">'
            '<p class="maq">%s</p><h3>%s</h3><p>%s</p>%s'
            '<p class="accord"><input type="checkbox" id="%s-ok">'
            '<label for="%s-ok" style="text-transform:none;letter-spacing:0;'
            'font-size:.88rem;color:#3A3130">%s</label></p>'
            '<button class="bouton" type="button" disabled>%s</button></form>'
            % (k, ech(t(C.MAQUETTE, lang)), ech(t(nom, lang)),
               ech(t(txt, lang)), "".join(champs), k, k,
               ech(t(C.CONSENTEMENT, lang)), ech(t(C.ENVOYER, lang))))
    o.append(sec("contact", lang, "forms",
                 ech("Write to the House" if lang == "en"
                     else "Écrire à la Maison"),
                 '<div class="grille g2">%s</div>' % "".join(formulaires),
                 classe="papier"))
    lignes = "".join('<tr><td><strong>%s</strong></td><td>%s</td></tr>'
                     % (ech(t(x, lang)), att(lang)) for x in C.COORDONNEES)
    o.append(sec("contact", lang, "where", ech(t(C.COORDONNEES_TITRE, lang)),
                 '<div class="defile"><table class="tbl"><tbody>%s</tbody>'
                 '</table></div>' % lignes))
    return "\n".join(o), t(C.CONTACT_INTRO, lang)


def p_circle(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("circle", lang),
               t(C.CERCLE_INTRO, lang))]
    o.append(sec("circle", lang, "door",
                 ech("Sign in" if lang == "en" else "Connexion"),
                 '<div class="grille g2">'
                 '<form class="form" onsubmit="return false">'
                 '<p class="maq">%s</p>'
                 '<div class="champ"><label for="ref">%s</label>'
                 '<input id="ref" type="text" autocomplete="off" '
                 'inputmode="text"></div>'
                 '<button class="bouton" type="button" disabled>%s</button>'
                 '</form>'
                 '<div class="carte"><h3>%s</h3><p>%s</p></div></div>'
                 % (ech(t(C.MAQUETTE, lang)), ech(t(C.CERCLE_REF, lang)),
                    ech(t(C.CERCLE_ENTRER, lang)),
                    ech("Why a reference and not an email address"
                        if lang == "en"
                        else "Pourquoi une référence et non une adresse"),
                    ech(t(C.CERCLE_REF_NOTE, lang))), classe="papier"))
    dec = "".join("<li>%s</li>" % ech(t(x, lang)) for x in C.CERCLE_DECISIONS)
    o.append(sec("circle", lang, "before",
                 ech(t(C.CERCLE_DECISIONS_TITRE, lang)),
                 "<ul>%s</ul>" % dec))
    return "\n".join(o), t(C.CERCLE_INTRO, lang)


def p_legal(lang):
    o = [bande(lang, t(C.MAISON, lang), titre_page("legal", lang),
               t(C.VIE_PRIVEE_FAIT[2], lang))]
    _k, nom, txt = C.LEGAL_BLOCS[0]
    o.append(sec("legal", lang, "notices", ech(t(nom, lang)),
                 '<div class="vide"><p>%s %s</p></div>'
                 % (att(lang), ech(t(txt, lang))), classe="papier"))
    faits = "".join("<li>%s</li>" % ech(t(x, lang)) for x in C.VIE_PRIVEE_FAIT)
    o.append(sec("legal", lang, "privacy",
                 ech(t(C.LEGAL_BLOCS[1][1], lang)),
                 '<p class="chapo">%s</p><ul>%s</ul><p>%s</p>'
                 % (ech("What this site does today, stated as facts that can "
                        "be checked in the page source." if lang == "en"
                        else "Ce que fait ce site aujourd’hui, énoncé comme "
                             "des faits vérifiables dans le code de la page."),
                    faits, ech(t(C.VIE_PRIVEE_APRES, lang)))))
    acc = "".join("<li>%s</li>" % ech(t(x, lang)) for x in C.ACCESSIBILITE)
    o.append(sec("legal", lang, "accessibility",
                 ech(t(C.LEGAL_BLOCS[2][1], lang)),
                 "<ul>%s</ul>" % acc, classe="papier"))
    return "\n".join(o), t(C.VIE_PRIVEE_APRES, lang)


BATISSEURS = {
    "home": p_home, "lordship": p_lordship, "heritage": p_heritage,
    "house": p_house, "initiatives": p_initiatives, "journal": p_journal,
    "media": p_media, "contact": p_contact, "circle": p_circle,
    "legal": p_legal,
}


# ---------------------------------------------------------------- ecriture
def ecrire(chemin, texte):
    d = os.path.dirname(chemin)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(chemin, "w", encoding="utf-8") as fh:
        fh.write(texte)
    return chemin


def main():
    sortis = []
    for lang in C.LANGUES:
        INDEX[lang] = []
        for cle, _fen, _ffr, _te, _tf, _m in C.PAGES:
            corps, desc = BATISSEURS[cle](lang)
            if not 40 < len(desc) < 320:
                raise SystemExit("description %s/%s : %d caracteres"
                                 % (cle, lang, len(desc)))
            html = page(cle, lang, corps, desc)
            dossier = RACINE if lang == "en" else os.path.join(RACINE, "fr")
            sortis.append(ecrire(os.path.join(dossier, fichier(cle, lang)), html))
        sortis.append(ecrire(
            os.path.join(RACINE, "assets", "index-%s.js" % lang),
            "window.__IDX=%s;\n" % json.dumps(INDEX[lang], ensure_ascii=False)))
    for c in sortis:
        print(os.path.relpath(c, RACINE))
    print("%d fichiers" % len(sortis))


if __name__ == "__main__":
    main()
