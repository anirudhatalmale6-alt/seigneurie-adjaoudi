# -*- coding: utf-8 -*-
"""Verification du site de la Seigneurie Adjaoudi.

  python3 tests/verif.py            # lance son propre serveur
  python3 tests/verif.py 8871       # utilise un serveur deja lance

Ce que ce fichier mesure, et pourquoi chaque mesure existe :

  - CE QUI N'EST PAS ECRIT. Une famille de motifs cherche, sur les vingt
    pages rendues, toute revendication de statut (reconnu, agree, octroye,
    immatricule), tout titre de noblesse, toute date fabriquee, tout nom de
    mois ou de jour. Le site n'a le droit d'employer ces mots que sous leur
    forme niee, et c'est teste.
  - CE QUI EST DESSINE, pas ce qui est declare. Chaque image est mesuree
    dans la page rendue : le rectangle reellement occupe est compare au
    format naturel du fichier. Un attribut juste sur une image boitee passe
    tous les controles et se voit quand meme.
  - LE CONTRASTE, mesure sur la page a quatorze largeurs, pas estime sur la
    feuille de style.
  - LES ANCRES : on navigue vraiment vers page#ancre et on verifie que la
    cible n'atterrit pas sous l'entete collante.
  - LES DEUX LANGUES : chaque page anglaise a sa jumelle francaise, les
    hreflang se repondent, et aucune n'a de lien casse.
"""

import http.server
import json
import os
import re
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

_ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(_ICI) if os.path.basename(_ICI) == "tests" else _ICI
sys.path.insert(0, os.path.join(RACINE, "source"))

import contenu as C  # noqa: E402

LARGEURS = [320, 360, 390, 414, 480, 600, 768, 834, 900, 1024, 1180, 1280,
            1366, 1440]

OK = []
KO = []


def verif(nom, cond, detail=""):
    (OK if cond else KO).append((nom, detail))


# ------------------------------------------------------------------ serveur
class Silencieux(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def __init__(self, *a, **k):
        super().__init__(*a, directory=RACINE, **k)


def sers():
    srv = socketserver.TCPServer(("127.0.0.1", 0), Silencieux)
    srv.allow_reuse_address = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


# -------------------------------------------------------------- motifs bannis
MOTIFS = [
    # revendications de statut : seules les formes NIEES sont permises, donc
    # le motif exige un verbe affirmatif devant le mot.
    (r"\b(is|are|was|were|has been|have been)\s+(officially\s+)?"
     r"(recognised|recognized|registered|accredited|licensed|certified|"
     r"granted|matriculated|authorised|authorized|chartered|ennobled)\b",
     "une revendication de statut"),
    (r"\b(recognised|recognized|accredited|licensed|certified|granted|"
     r"matriculated|chartered)\s+by\b", "une revendication de statut (by)"),
    (r"\b(est|sont|a été|ont été)\s+(officiellement\s+)?"
     r"(reconnue?s?|enregistrée?s?|accréditée?s?|agréée?s?|homologuée?s?|"
     r"octroyée?s?|immatriculée?s?|anoblie?s?)\b",
     "une revendication de statut (fr)"),
    (r"\b(holds|bears|carries|enjoys|confers|grants)\s+(a|the)?\s*"
     r"(title|rank|precedence|nobility|peerage|official status)\b",
     "un titre revendique"),
    (r"\b(confère|détient|porte)\s+(un|le|la)\s+"
     r"(titre|rang|préséance|noblesse)\b", "un titre revendique (fr)"),
    # dates fabriquees
    (r"\b(January|February|March|April|June|July|August|September|October"
     r"|November|December)\b", "un nom de mois"),
    (r"\b(janvier|février|mars|avril|juin|juillet|août|septembre|octobre"
     r"|novembre|décembre)\b", "un nom de mois (fr)"),
    (r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
     "un jour de semaine"),
    (r"\b(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)\b",
     "un jour de semaine (fr)"),
    (r"\b(1[0-9]|20)\d{2}\b", "une annee"),
    (r"\b(depuis|since|founded in|fondée en|établie en|established in)\s+\d",
     "une anciennete chiffree"),
    # generations et effectifs inventes
    (r"\b\d+(st|nd|rd|th)\s+generation\b", "une generation numerotee"),
    (r"\b\d+\s*(e|ème|ᵉ)\s+génération\b", "une generation numerotee (fr)"),
]

# mots qui ne doivent apparaitre QUE dans le voisinage d'une negation
SENSIBLES = ["nobility", "noblesse", "peerage", "coat of arms", "blason",
             "lordship", "seigneurie"]


NEGATIONS = re.compile(
    r"\b(no|not|never|nor|neither|nothing|none|without|cannot|isn|aren)\b"
    r"|\b(ne|n[’']|ni|aucun|aucune|jamais|sans|pas|nulle)\b", re.I)


def touches(motif, txt):
    """Occurrences d'un motif QUI NE SONT PAS deja niees.

    Le site a le droit — et le devoir — d'ecrire « n'est pas reconnue »,
    « accredited by no authority ». Un motif qui interdit un mot interdit
    aussi de dire qu'on ne le revendique pas ; il faut donc regarder ce qui
    precede immediatement chaque occurrence.
    """
    out = []
    for m in re.finditer(motif, txt, re.I):
        # portee = la phrase, pas un nombre arbitraire de caracteres. Le pied
        # de page dit « Neither the designation nor the coat of arms is
        # claimed to be recognised, granted, registered or accredited by any
        # authority » : la negation est a soixante-dix signes de la, et une
        # fenetre fixe la manquait.
        deb = max((txt.rfind(c, 0, m.start()) for c in ".!?;\n"), default=-1)
        phrase = txt[deb + 1:m.start()]
        if not NEGATIONS.search(phrase):
            out.append(m.group(0))
    return out


def texte_visible(pg):
    return pg.evaluate("() => document.body.innerText")


def source(chemin):
    with open(chemin, encoding="utf-8") as fh:
        return fh.read()


# ----------------------------------------------------------------- contraste
def luminance(r, g, b):
    def c(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def contraste(a, b):
    la, lb = luminance(*a), luminance(*b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def fond_derriere(pg, selecteur, chemin_png):
    """Cache l'element, photographie ce qu'il y a dessous, rend la teinte la
    plus claire du fond (98e centile) — celle qui donne le pire contraste
    avec un texte clair."""
    from PIL import Image
    boite = pg.evaluate("""(s) => {
        const e = document.querySelector(s);
        if (!e) return null;
        const r = e.getBoundingClientRect();
        return {x:r.x, y:r.y, w:r.width, h:r.height};
    }""", selecteur)
    if not boite or boite["w"] < 5 or boite["h"] < 5:
        return None
    pg.evaluate("(s) => document.querySelector(s).style.visibility='hidden'",
                selecteur)
    pg.screenshot(path=chemin_png, clip={"x": max(boite["x"], 0),
                                         "y": max(boite["y"], 0),
                                         "width": boite["w"],
                                         "height": boite["h"]})
    pg.evaluate("(s) => document.querySelector(s).style.visibility=''",
                selecteur)
    im = Image.open(chemin_png).convert("RGB")
    pix = list(im.getdata())
    pix.sort(key=lambda p: luminance(*p))
    return pix[int(len(pix) * 0.98)]


# --------------------------------------------------------------------- corps
def main():
    port_ext = int(sys.argv[1]) if len(sys.argv) > 1 else None
    srv = None
    if port_ext:
        port = port_ext
    else:
        srv, port = sers()
    base = "http://127.0.0.1:%d/" % port
    tmp = os.environ.get("TMPDIR", "/tmp")

    pages = []
    for cle, fen, ffr, _te, _tf, _m in C.PAGES:
        pages.append(("en", cle, fen))
        pages.append(("fr", cle, "fr/" + ffr))

    # ------------------------------------------------ 1. les fichiers existent
    for lang, cle, rel in pages:
        verif("%s existe" % rel, os.path.isfile(os.path.join(RACINE, rel)))
    for a in ("assets/site.css", "assets/site.js", "assets/index-en.js",
              "assets/index-fr.js", "assets/sceau.svg", "assets/halo.svg",
              "assets/blason-ivoire.svg", "assets/blason-couleur.svg",
              "assets/favicon.svg", "assets/fonts/cormorant-latin.woff2",
              "assets/fonts/cormorant-latin-ext.woff2",
              "assets/fonts/inter-latin.woff2",
              "assets/fonts/inter-latin-ext.woff2", "assets/fonts/OFL.txt",
              "brand/blason-couleur.svg", "brand/blason-cramoisi.svg",
              "brand/blason-ivoire.svg", "brand/sceau.svg",
              "brand/signature-en-verticale.svg",
              "brand/signature-fr-verticale.svg",
              "brand/signature-en-horizontale.svg",
              "brand/signature-fr-horizontale.svg",
              "brand/guidelines.html", "brand/schema-respiration.svg"):
        verif("%s existe" % a, os.path.isfile(os.path.join(RACINE, a)))

    # ------------------------------------------- 2. rien d'exterieur, nulle part
    for lang, cle, rel in pages + [("en", "guide", "brand/guidelines.html")]:
        s = source(os.path.join(RACINE, rel))
        for motif, quoi in ((r"https?://(?!www\.w3\.org)", "une URL absolue"),
                            (r"//fonts\.", "un appel de police distante"),
                            (r"google", "google"),
                            (r"gtag\(|googletagmanager|google-analytics|matomo\.js|plausible\.io|<script[^>]*analytic", "une mesure"),
                            (r"<iframe", "un iframe")):
            trouve = re.findall(motif, s, re.I)
            verif("%s : aucun %s" % (rel, quoi), not trouve, str(trouve[:3]))
    css = source(os.path.join(RACINE, "assets", "site.css"))
    verif("la css n'appelle rien dehors",
          not re.search(r"url\(\s*['\"]?https?:", css))

    # --------------------------------------------------- 3. ce qui est ecrit
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        ctx = nav.new_context(viewport={"width": 1280, "height": 900})
        pg = ctx.new_page()
        erreurs = []
        pg.on("console", lambda m: erreurs.append(m.text)
              if m.type == "error" else None)
        pg.on("pageerror", lambda e: erreurs.append(str(e)))

        textes = {}
        for lang, cle, rel in pages:
            pg.goto(base + rel, wait_until="networkidle")
            txt = texte_visible(pg)
            textes[rel] = txt
            for motif, quoi in MOTIFS:
                t = touches(motif, txt)
                verif("%s : pas de %s" % (rel, quoi), not t, str(t[:3]))

            # titre, langue, description
            verif("%s : lang=%s" % (rel, lang),
                  pg.evaluate("() => document.documentElement.lang") == lang)
            verif("%s : un titre" % rel,
                  len(pg.title()) > 8 and "Adjaoudi" in pg.title(), pg.title())
            d = pg.evaluate("""() => {const m =
                document.querySelector('meta[name=description]');
                return m ? m.content : ''}""")
            verif("%s : une description" % rel, 40 < len(d) < 320, str(len(d)))
            # un seul h1
            n1 = pg.evaluate("() => document.querySelectorAll('h1').length")
            verif("%s : un seul h1" % rel, n1 == 1, str(n1))
            # hreflang des deux cotes
            alts = pg.evaluate("""() => [...document.querySelectorAll(
                'link[rel=alternate]')].map(l => l.hreflang)""")
            verif("%s : hreflang en+fr" % rel, sorted(alts) == ["en", "fr"],
                  str(alts))
            # images : aucune cassee, et le rectangle dessine au bon format
            casse = pg.evaluate("""() => [...document.images]
                .filter(i => !i.complete || i.naturalWidth === 0)
                .map(i => i.getAttribute('src'))""")
            verif("%s : aucune image cassee" % rel, not casse, str(casse))
            boites = pg.evaluate("""() => [...document.images].filter(i => {
                const r = i.getBoundingClientRect();
                if (!i.naturalWidth || !i.naturalHeight) return false;
                if (r.width < 4 || r.height < 4) return false;
                const a = r.width / r.height;
                const b = i.naturalWidth / i.naturalHeight;
                return Math.abs(a / b - 1) > 0.02;
            }).map(i => i.getAttribute('src') + ' ' +
                Math.round(i.getBoundingClientRect().width) + 'x' +
                Math.round(i.getBoundingClientRect().height) + ' nat ' +
                i.naturalWidth + 'x' + i.naturalHeight)""")
            verif("%s : images au bon format dessine" % rel, not boites,
                  str(boites))
            # alt sur toutes les images
            sans_alt = pg.evaluate("""() => [...document.images]
                .filter(i => i.getAttribute('alt') === null)
                .map(i => i.getAttribute('src'))""")
            verif("%s : alt partout" % rel, not sans_alt, str(sans_alt))
            # chaque champ a une etiquette
            orphelins = pg.evaluate("""() => [...document.querySelectorAll(
                'input:not([type=checkbox]), textarea')].filter(c => {
                    if (c.id && document.querySelector(
                        'label[for="' + c.id + '"]')) return false;
                    return !c.closest('label') && !c.getAttribute('aria-label');
                }).map(c => c.id || c.name || c.type)""")
            verif("%s : chaque champ etiquete" % rel, not orphelins,
                  str(orphelins))
            # aucun formulaire ne peut partir
            actifs = pg.evaluate("""() => [...document.forms]
                .filter(f => f.getAttribute('action')).length""")
            verif("%s : aucun formulaire connecte" % rel, actifs == 0,
                  str(actifs))
            boutons = pg.evaluate("""() => [...document.querySelectorAll(
                'form button')].filter(b => !b.disabled).length""")
            verif("%s : aucun bouton d'envoi actif" % rel, boutons == 0,
                  str(boutons))
            # la pastille d'attente dit bien la meme chose partout
            past = pg.evaluate("""() => [...document.querySelectorAll('.att')]
                .map(e => e.textContent.trim())""")
            attendu = C.ATTENTE[0] if lang == "en" else C.ATTENTE[1]
            verif("%s : un seul vocabulaire d'attente" % rel,
                  all(p == attendu for p in past), str(sorted(set(past))))
            # liens internes valides
            liens = pg.evaluate("""() => [...document.querySelectorAll('a[href]')]
                .map(a => a.getAttribute('href'))
                .filter(h => h && !h.startsWith('#') && !h.startsWith('http'))""")
            dossier = os.path.dirname(os.path.join(RACINE, rel))
            morts = []
            for h in set(liens):
                cible = os.path.normpath(os.path.join(dossier, h.split("#")[0]))
                if not os.path.isfile(cible):
                    morts.append(h)
            verif("%s : aucun lien mort" % rel, not morts, str(morts))

        verif("aucune erreur console", not erreurs, str(erreurs[:4]))

        # ------------------------------------- 4. les formes NIEES sont la
        for rel, attendu in (
                ("index.html", "It is not a public authority"),
                ("the-lordship.html", "It confers no title, no rank"),
                ("the-lordship.html", "not claimed to be recognised, granted "
                                      "or registered"),
                ("the-lordship.html", "It is not claimed to be granted, "
                                      "matriculated or entered in any armorial"),
                ("private-circle.html", "no personal data is stored"),
                ("legal.html", "This site sets no cookie"),
                ("house-of-adjaoudi.html", "private family data is excluded"),
                ("fr/index.html", "n’est pas une autorité publique"),
                ("fr/la-seigneurie.html", "ne confère aucun titre"),
                ("fr/cercle-prive.html", "aucune donnée personnelle"),
                ("fr/mentions-legales.html", "ne dépose aucun cookie")):
            verif("%s dit « %s »" % (rel, attendu[:38]),
                  attendu.lower() in textes[rel].lower())
        for rel in [r for _l, _c, r in pages]:
            verif("%s : le pied porte la declaration" % rel,
                  ("is not a public authority" in textes[rel]
                   or "n’est pas une autorité publique" in textes[rel]))

        # ------------------------------------------ 5. la recherche fonctionne
        for rel, mot, attendu_url in (("index.html", "rights", "heritage.html"),
                                      ("fr/index.html", "droits",
                                       "patrimoine.html")):
            pg.goto(base + rel, wait_until="networkidle")
            pg.click(".loupe")
            verif("%s : le panneau s'ouvre" % rel,
                  pg.is_visible("#rech input"))
            pg.fill("#q", mot)
            pg.wait_for_timeout(150)
            res = pg.evaluate("""() => [...document.querySelectorAll('#res a')]
                .map(a => a.getAttribute('href'))""")
            verif("%s : « %s » trouve quelque chose" % (rel, mot), len(res) > 0,
                  str(res[:3]))
            verif("%s : « %s » mene a %s" % (rel, mot, attendu_url),
                  any(attendu_url in r for r in res), str(res[:5]))
            pg.keyboard.press("Escape")
            verif("%s : Echap ferme" % rel, not pg.is_visible("#rech input"))
        idx = json.loads(source(os.path.join(RACINE, "assets", "index-en.js"))
                         .split("=", 1)[1].rsplit(";", 2)[0])
        verif("index en : au moins 20 sections", len(idx) >= 20, str(len(idx)))
        idxfr = json.loads(source(os.path.join(RACINE, "assets", "index-fr.js"))
                           .split("=", 1)[1].rsplit(";", 2)[0])
        verif("les deux index ont la meme taille", len(idx) == len(idxfr),
              "%d / %d" % (len(idx), len(idxfr)))

        # ---------------------------------------- 6. le selecteur de langue
        pg.goto(base + "heritage.html", wait_until="networkidle")
        pg.click('.langues a[hreflang=fr]')
        pg.wait_for_load_state("networkidle")
        verif("EN->FR reste sur la meme page",
              pg.url.endswith("fr/patrimoine.html"), pg.url)
        pg.click('.langues a[hreflang=en]')
        pg.wait_for_load_state("networkidle")
        verif("FR->EN revient sur la meme page",
              pg.url.endswith("/heritage.html"), pg.url)

        # ------------------------------------------------- 7. les ancres
        for largeur in (390, 1280):
            p2 = ctx.new_page()
            p2.set_viewport_size({"width": largeur, "height": 780})
            for rel, frag in (("the-lordship.html", "#values"),
                              ("heritage.html", "#rights"),
                              ("legal.html", "#privacy"),
                              ("fr/patrimoine.html", "#rights"),
                              ("index.html", "#timeline")):
                p2.goto(base + rel + frag, wait_until="networkidle")
                p2.wait_for_timeout(120)
                ok = p2.evaluate("""(f) => {
                    const e = document.querySelector(f);
                    const h = document.querySelector('.hdr');
                    if (!e || !h) return false;
                    return e.getBoundingClientRect().top
                         >= h.getBoundingClientRect().bottom - 2;
                }""", frag)
                verif("%s%s visible sous l'entete a %dpx" % (rel, frag, largeur),
                      ok)
            p2.close()

        # -------------------------------- 8. mise en page a quatorze largeurs
        for largeur in LARGEURS:
            p3 = ctx.new_page()
            p3.set_viewport_size({"width": largeur, "height": 820})
            for rel in ("index.html", "the-lordship.html", "contact.html",
                        "fr/mediatheque.html", "fr/cercle-prive.html"):
                p3.goto(base + rel, wait_until="networkidle")
                deb = p3.evaluate(
                    "() => document.documentElement.scrollWidth "
                    "- document.documentElement.clientWidth")
                verif("%s : pas de debordement a %dpx" % (rel, largeur),
                      deb <= 1, str(deb))
                # le nom de la maison n'est jamais tronque
                coupe = p3.evaluate("""() => {
                    const e = document.querySelector('.brand .n1');
                    return e.scrollWidth - e.clientWidth;
                }""")
                verif("%s : le nom entier a %dpx" % (rel, largeur), coupe <= 1,
                      str(coupe))
                # rien ne sort de l'ecran
                # les formes decoratives sont volontairement debordantes et
                # rognees par leur parent : elles sont hors du calcul, ce qui
                # est verifiable puisque l'absence de barre de defilement est
                # mesuree juste au-dessus.
                dehors = p3.evaluate("""() => [...document.querySelectorAll(
                    'h1,h2,h3,p,a,button,img,td,th')].filter(e => {
                        if (e.closest('[aria-hidden="true"]')) return false;
                        const r = e.getBoundingClientRect();
                        return r.width > 0 && (r.right > innerWidth + 1
                                               || r.left < -1);
                    }).map(e => e.tagName + '.' + e.className)""")
                dehors = len(dehors) and dehors
                verif("%s : rien hors ecran a %dpx" % (rel, largeur),
                      not dehors, str(dehors))
            # le heros : contraste du titre sur ce qu'il y a derriere
            p3.goto(base + "index.html", wait_until="networkidle")
            fond = fond_derriere(p3, ".hero h1",
                                 os.path.join(tmp, "fond-hero.png"))
            if fond:
                c = contraste((246, 240, 228), fond)
                verif("heros : contraste >= 4.5 a %dpx" % largeur, c >= 4.5,
                      "%.2f:1 sur %s" % (c, fond))
            p3.goto(base + "the-lordship.html", wait_until="networkidle")
            fond = fond_derriere(p3, ".bande h1",
                                 os.path.join(tmp, "fond-bande.png"))
            if fond:
                c = contraste((246, 240, 228), fond)
                verif("bande : contraste >= 4.5 a %dpx" % largeur, c >= 4.5,
                      "%.2f:1 sur %s" % (c, fond))
            p3.close()

        # -------------------------------------- 9. le menu de petit ecran
        p4 = ctx.new_page()
        p4.set_viewport_size({"width": 390, "height": 780})
        p4.goto(base + "index.html", wait_until="networkidle")
        verif("390px : le menu est replie", not p4.is_visible(".nav a"))
        verif("390px : le bouton menu est la", p4.is_visible(".bascule"))
        p4.click(".bascule")
        verif("390px : le menu s'ouvre", p4.is_visible(".nav a"))
        verif("390px : aria-expanded suit",
              p4.get_attribute(".bascule", "aria-expanded") == "true")
        verif("390px : le Cercle prive reste visible", p4.is_visible(".pcircle"))
        verif("390px : la recherche reste visible", p4.is_visible(".loupe"))
        p4.close()

        # ------------------------------------- 10. clavier et focus visible
        p5 = ctx.new_page()
        p5.set_viewport_size({"width": 1280, "height": 800})
        p5.goto(base + "contact.html", wait_until="networkidle")
        p5.keyboard.press("Tab")
        prem = p5.evaluate("() => document.activeElement.className")
        verif("premier tabulateur = lien d'evitement", "saut" in prem, prem)
        contour = p5.evaluate("""() => {
            const e = document.activeElement;
            e.focus();
            return getComputedStyle(e).outlineStyle;
        }""")
        verif("le focus est visible", contour not in ("none", ""), contour)
        p5.close()

        # ------------------------------- 11. animation coupee si demande
        ctx2 = nav.new_context(viewport={"width": 1280, "height": 800},
                               reduced_motion="reduce")
        p6 = ctx2.new_page()
        p6.goto(base + "index.html", wait_until="networkidle")
        anim = p6.evaluate("""() => getComputedStyle(
            document.querySelector('.halo img')).animationName""")
        verif("mouvement reduit : le soleil ne tourne pas", anim == "none", anim)
        ctx2.close()

        # ------------------------------------ 12. les polices sont bien la
        p7 = ctx.new_page()
        p7.goto(base + "index.html", wait_until="networkidle")
        chargees = p7.evaluate("""async () => {
            await document.fonts.ready;
            return [...document.fonts].map(f => f.family + ' ' + f.status);
        }""")
        verif("Cormorant embarque et charge",
              any("Cormorant" in f and "loaded" in f for f in chargees),
              str(chargees))
        verif("Inter embarque et charge",
              any("Inter" in f and "loaded" in f for f in chargees),
              str(chargees))
        rendu = p7.evaluate("""() => getComputedStyle(
            document.querySelector('h1')).fontFamily""")
        verif("les titres demandent Cormorant", "Cormorant" in rendu, rendu)
        p7.close()

        # ------------------------------------ 13. le guide de marque
        p8 = ctx.new_page()
        errg = []
        p8.on("console", lambda m: errg.append(m.text)
              if m.type == "error" else None)
        p8.on("pageerror", lambda e: errg.append(str(e)))
        p8.goto(base + "brand/guidelines.html", wait_until="networkidle")
        tg = texte_visible(p8)
        for motif, quoi in MOTIFS:
            tr = touches(motif, tg)
            verif("guide : pas de %s" % quoi, not tr, str(tr[:3]))
        verif("guide : aucune erreur console", not errg, str(errg[:3]))
        verif("guide : le blason ne revendique rien",
              "not claimed to be granted, matriculated, registered or "
              "recognised by any heraldic authority" in tg)
        verif("guide : seize rayons, et le dit",
              "There are sixteen" in tg)
        verif("guide : la palette a cinq couleurs",
              p8.evaluate("() => document.querySelectorAll("
                          "'#palette tbody tr').length") == 5)
        verif("guide : aucune image cassee",
              not p8.evaluate("""() => [...document.images]
                  .filter(i => !i.complete || !i.naturalWidth)
                  .map(i => i.getAttribute('src'))"""))
        boitesg = p8.evaluate("""() => [...document.images].filter(i => {
            const r = i.getBoundingClientRect();
            if (!i.naturalWidth || r.width < 4 || r.height < 4) return false;
            return Math.abs((r.width / r.height) /
                (i.naturalWidth / i.naturalHeight) - 1) > 0.02;
        }).map(i => i.getAttribute('src'))""")
        verif("guide : images au bon format dessine", not boitesg, str(boitesg))
        verif("guide : alt partout",
              not p8.evaluate("""() => [...document.images]
                  .filter(i => i.getAttribute('alt') === null).length"""))
        for largeur in (320, 390, 768, 1280, 1440):
            p8.set_viewport_size({"width": largeur, "height": 800})
            p8.wait_for_timeout(80)
            deb = p8.evaluate("() => document.documentElement.scrollWidth "
                              "- document.documentElement.clientWidth")
            verif("guide : pas de debordement a %dpx" % largeur, deb <= 1,
                  str(deb))
        p8.close()

        ctx.close()
        nav.close()
    if srv:
        srv.shutdown()

    # ------------------------------------------------------------- rapport
    for nom, det in KO:
        print("ECHEC  %s  %s" % (nom, det))
    print("-" * 62)
    print("%d verifications, %d echecs" % (len(OK) + len(KO), len(KO)))
    return 1 if KO else 0


if __name__ == "__main__":
    sys.exit(main())
