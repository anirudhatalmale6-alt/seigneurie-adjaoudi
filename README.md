# Seigneurie Adjaoudi — Adjaoudi Lordship

Identité de marque et site institutionnel bilingue, construits d'après le
document *Adjaoudi Lordship — Official Website Requirements & Coat of Arms
Brand Guidelines, version 1.0*.

---

## La règle qui gouverne tout le reste

**Rien sur ce site n'affirme un fait sur la famille Adjaoudi.**

Pas une origine, pas une date, pas un lieu, pas un ancêtre, pas une branche,
pas un membre, pas une archive, pas un chiffre. Ce n'est pas une pudeur de
rédacteur : c'est la seule position tenable quand on bâtit un site de
patrimoine familial dont on ne détient aucune source. Une seule date inventée
sur une frise chronologique suffit à disqualifier tout ce qui est vrai autour
d'elle, et une frise patrimoniale ne vaut jamais plus que sa plus faible
entrée.

Ce qui manque n'est donc pas comblé, il est **montré comme manquant**, sous
un seul et même mot : *Awaiting authorisation* / *En attente d'autorisation*.
Ce vocabulaire est propre à ce site et n'est mélangé avec aucun autre.

Le cahier des charges pose lui-même trois limites, et elles sont tenues au mot
près :

| Ce que demande le document | Ce que fait le site |
| --- | --- |
| « Clearly distinguish the heritage identity from any public authority or official title. » | Le manifeste de l'accueil, une section entière de *The Lordship*, et le pied de **chacune des vingt pages** disent que la Seigneurie n'est pas une autorité publique, n'exerce aucune fonction officielle et ne confère ni titre, ni rang, ni préséance, ni noblesse. |
| « Present *Lordship* as a cultural or brand designation unless legal recognition has been demonstrated. » | Le mot n'apparaît jamais autrement. Nulle part le site ne dit que la désignation est reconnue, concédée, enregistrée, agréée ou accréditée — et une famille de motifs, testée sur les vingt pages rendues, échoue si l'une de ces formes apparaît ailleurs que niée. |
| « Geometric crest: symbolic elevation without imitating sovereign insignia. » | La crête à trois pointes de la référence lisait comme une couronne. Elle est redessinée en fronton architectural à épaulements. Le soleil garde ses seize rayons, l'écu et les lauriers gardent la composition d'origine. |

---

## Ce que contient le paquet

### Le site — vingt pages, deux langues

Les pages anglaises sont à la racine, les françaises dans `fr/`. Chaque page
déclare ses deux `hreflang`, et le sélecteur de langue reste **sur la même
page** au lieu de renvoyer à l'accueil (c'est mesuré).

| Clé | Anglais | Français |
| --- | --- | --- |
| Accueil | `index.html` | `fr/index.html` |
| La Seigneurie | `the-lordship.html` | `fr/la-seigneurie.html` |
| Patrimoine | `heritage.html` | `fr/patrimoine.html` |
| La Maison | `house-of-adjaoudi.html` | `fr/la-maison.html` |
| Initiatives | `initiatives.html` | `fr/initiatives.html` |
| Journal | `journal.html` | `fr/journal.html` |
| Médiathèque | `media-library.html` | `fr/mediatheque.html` |
| Contact | `contact.html` | `fr/contact.html` |
| Cercle privé | `private-circle.html` | `fr/cercle-prive.html` |
| Mentions légales | `legal.html` | `fr/mentions-legales.html` |

Les huit entrées du menu principal correspondent exactement au plan du
document ; `legal` est en plus, parce que le pied de page réclamé par le
cahier des charges (mentions légales, confidentialité, accessibilité) devait
bien mener quelque part.

### La marque

- `brand/blason-couleur.svg` — version principale, quadrichromie.
- `brand/blason-cramoisi.svg` — monochrome cramoisi.
- `brand/blason-ivoire.svg` — monochrome ivoire, pour fond sombre.
- `brand/sceau.svg` — écu et soleil seuls, pour les petites tailles.
- `brand/signature-{en,fr}-{verticale,horizontale}.svg` — le blason verrouillé
  au nom et à la devise, **lettrage converti en tracés** : ces fichiers
  s'affichent correctement sans qu'aucune police soit installée.
- `brand/schema-respiration.svg` — l'aire de respiration, mesurée.
- `brand/guidelines.html` — le guide de marque, en une page autonome.
- `brand/exports/` — PNG transparents (jusqu'à 2048 px) et PDF de chaque
  fichier maître.

Tout cela sort d'**un seul fichier de géométrie**, `source/blason.py`. Les
variantes ne peuvent donc pas diverger : elles sont le même dessin, avec une
autre palette.

### Ce qui n'est délibérément pas construit

- **Aucune entrée de chronologie.** La structure est là, la page explique
  qu'une entrée exige trois choses ensemble — une date, une source que l'on
  peut nommer, et l'autorisation écrite de la famille.
- **Aucun portrait, aucune photographie.** Rien n'est généré à la place d'une
  vraie image. La médiathèque part avec ses emplacements vides et son registre
  des droits vide.
- **Aucune branche familiale nommée.** La page pose les deux conditions
  d'abord : autorisation écrite, et publication limitée à ce que cette
  autorisation couvre.
- **Le Cercle privé n'a pas de porte.** Aucun compte, aucun mot de passe,
  aucune donnée personnelle. Le champ de connexion demande une **référence de
  membre, pas une adresse e-mail** : une page de connexion qui accepte une
  adresse transforme chaque tentative échouée en réponse sur qui fait partie,
  ou non, de cette famille.
- **Les formulaires n'envoient rien.** Ils n'ont pas d'attribut `action`,
  leurs boutons sont désactivés, et chacun porte l'étiquette « Mock-up — not
  connected ». C'est vérifié sur les vingt pages.
- **Aucune mesure d'audience, aucun cookie, aucun appel extérieur.** Les
  polices sont embarquées dans le site. Une page de ce site chargée sans
  réseau après le premier chargement se comporte exactement pareil.

---

## Technique

**Aucun cadre, aucune dépendance.** HTML statique, une feuille de style, un
script de 120 lignes qui fait deux choses : ouvrir le menu sur petit écran et
chercher dans un index construit au moment de la construction. Sans
JavaScript, tout le site reste navigable — seule la recherche disparaît, et
le dit.

**Les polices du guide, embarquées.** Cormorant Garamond et Inter, en WOFF2
variable, sous licence SIL Open Font (`assets/fonts/OFL.txt`). Quatre
fichiers, environ 205 ko au total, servis par le site : rien n'est demandé à
Google, ce qui est à la fois plus rapide et beaucoup plus simple à défendre
côté vie privée.

**Recherche.** L'index (`assets/index-en.js`, `assets/index-fr.js`) est
fabriqué par le constructeur à partir des sections réellement écrites. Il est
chargé avec la page, donc la recherche fonctionne aussi depuis un dossier
local, sans serveur.

**Accessibilité.** Objectif WCAG 2.2 AA. Lien d'évitement, focus visible,
menu au clavier avec `aria-expanded`, panneau de recherche en `role="dialog"`
avec piège de tabulation et fermeture par Échap, alternative textuelle sur
chaque image, formes décoratives masquées aux lecteurs d'écran, animation
coupée sous `prefers-reduced-motion`.

**Reconstruction.** Rien ne se modifie à la main : la construction suivante
écraserait la retouche.

```
python3 source/blason.py     # le blason et toutes ses variantes
python3 source/build.py      # les vingt pages et les deux index
python3 source/guide.py      # le guide de marque et son schéma
python3 source/exports.py    # les PNG et les PDF
python3 tests/verif.py       # la vérification complète
python3 tests/captures.py    # les captures d'écran
```

---

## Vérification

`python3 tests/verif.py` lance son propre serveur, ouvre un vrai navigateur
et mesure. Ce qu'il regarde, et pourquoi :

- **Ce qui n'est pas écrit.** Une famille de motifs cherche, sur les vingt
  pages *rendues*, toute revendication de statut, tout titre, toute date
  fabriquée, tout nom de mois ou de jour. Ces mots ne sont permis que sous
  leur forme niée — et la portée de la négation est **la phrase**, pas une
  fenêtre de caractères : le pied de page dit « Neither the designation nor
  the coat of arms is claimed to be recognised, granted, registered or
  accredited by any authority », où la négation est à soixante-dix signes du
  mot surveillé.
- **Ce qui est dessiné, pas ce qui est déclaré.** Chaque image est mesurée
  dans la page rendue : le rectangle réellement occupé est comparé au format
  naturel du fichier. Un attribut juste sur une image boîtée passe tous les
  contrôles et se voit quand même.
- **Le contraste**, mesuré sur la page à quatorze largeurs — on cache
  l'élément, on photographie ce qu'il y a dessous, et on prend le 98ᵉ centile
  de luminance, c'est-à-dire le pire cas pour un texte clair.
- **Les ancres.** On navigue réellement vers `page#ancre` et on vérifie que la
  cible n'atterrit pas sous l'en-tête collante — à 390 px comme à 1280 px.
- **Le reste** : aucun lien mort, aucune image cassée, un seul `h1` par page,
  `hreflang` des deux côtés, chaque champ étiqueté, aucun formulaire
  connecté, aucun bouton d'envoi actif, aucune erreur de console, les polices
  réellement chargées, le menu et la recherche pilotés au clavier.

### Résultat

**999 vérifications, 0 échec** — 21 pages (20 pages du site + le guide de
marque) à quatorze largeurs, de 320 à 1440 px.

Contrastes mesurés sur la page rendue, jamais calculés d'après la feuille de
style :

| Texte | Mesuré | Exigé (AA) |
| --- | --- | --- |
| Titre du héros, ivoire sur cramoisi | **8,19:1** à toutes les largeurs | 3:1 (grand texte) |
| Titre de bandeau, ivoire sur cramoisi + filigrane | **6,63:1** au pire cas (1024 px) | 3:1 |
| Texte courant, charbon sur ivoire | **11,13:1** | 4,5:1 |
| Texte courant, charbon sur papier | **12,34:1** | 4,5:1 |
| Lien de navigation, cramoisi sur papier | **9,08:1** | 4,5:1 |
| Pastille d'attente, or foncé | **7,89:1** | 4,5:1 |

### Une suite verte ne prouve rien tant qu'on ne l'a pas fait échouer

Cinq mutations, chacune **d'abord prouvée dans le rendu** avant d'être jugée,
puis annulée :

| Mutation | Prouvée dans le rendu | Échecs déclenchés |
| --- | --- | --- |
| A. une revendication de statut fausse est glissée dans le texte | oui | **1** |
| B. une date fabriquée (« founded in March 1804 ») | oui | **4** |
| C. une image reçoit une boîte au mauvais format, attribut resté juste | oui | **18** |
| D. `scroll-margin-top` remis à zéro | oui | **10** |
| E. la grille reprend un minimum fixe de 310 px | oui | **4** |

Après annulation : **999 vérifications, 0 échec** à nouveau.

La mutation C mérite un mot, parce qu'elle a failli mentir. Au premier
passage, sa preuve de rendu est revenue **fausse** alors que la mutation
faisait tomber 18 vérifications — ce qui est contradictoire. La preuve
tournait à 320 px, largeur à laquelle l'élément muté est justement en
`display:none`. Ce n'est pas la mutation qui n'atteignait pas le rendu, c'est
**ma preuve qui regardait une largeur où la chose n'existe pas**. Chaque
mutation porte désormais sa propre largeur de mesure.

---

## Ce qu'il me faut de la Maison

Rien de ce qui suit n'est un détail de mise en page : chacun de ces points
décide d'un contenu qui, aujourd'hui, porte une pastille d'attente.

1. **La devise.** *Heritage illuminates the future.* est une proposition
   éditoriale du document, et le site le dit à voix haute sous le titre. Elle
   reste une proposition tant que la famille ne l'a pas approuvée.
2. **L'origine et le sens du nom.** Une source. Un document, un registre, une
   publication, un témoignage attribué — n'importe laquelle, mais une source.
   Je n'écrirai pas cette page autrement.
3. **Le contenu historique autorisé.** Quelles dates, quels lieux, quels
   noms ; et pour chacun, qui a autorisé la publication.
4. **Les branches et les portraits.** Pour chaque personne nommée :
   l'autorisation écrite, et l'étendue exacte de ce qu'elle couvre.
5. **Le niveau d'accès du Cercle privé.** Qui détient la liste des membres et
   dans quel pays ; qui peut inviter et qui peut retirer une invitation ; ce
   qu'il y a derrière la porte ; combien de temps un journal d'accès est
   conservé et qui a le droit de le lire.
6. **Le pays.** Il décide des mentions légales, du régime de confidentialité
   applicable, et de la juridiction dans laquelle le nom et le blason devront
   être examinés avant tout dépôt de marque ou usage commercial.
7. **L'éditeur.** Dénomination, adresse, numéro d'immatriculation, directeur
   de publication, hébergeur.
8. **Les canaux officiels**, s'il en existe déjà.
9. **Les vraies photographies.** Avec, pour chacune, l'auteur ou le détenteur
   et le droit d'usage — les cinq colonnes du registre des droits.

### Une note pour votre juriste, qui n'est pas sur le site

Le document parle de faire examiner le nom, la marque et le blason avant
enregistrement ou usage commercial. C'est juste, et deux points méritent
d'être posés devant lui :

- Le mot *Lordship* / *Seigneurie* et le port d'armoiries sont réglementés
  très différemment d'un pays à l'autre — certains les laissent entièrement
  libres, d'autres réservent la matriculation à une autorité, d'autres encore
  répriment l'usage de titres susceptibles d'induire en erreur. La réponse
  dépend entièrement du pays retenu, et je ne l'écris nulle part sur le site
  parce que nommer une juridiction serait déjà prendre position sur le fond.
- Les données de la famille — portraits, filiations, documents privés — sont
  des données personnelles dès qu'une personne vivante est identifiable, et
  les filiations touchent aussi des personnes qui n'ont rien demandé. D'où la
  règle de la Maison, reprise telle quelle sur le site : exclusion par défaut,
  publication sur autorisation écrite et documentée.

---

## Ce qui n'est pas encore fait, et pourquoi

Le planning du document prévoit une phase de développement sur CMS
(WordPress durci, Webflow ou architecture découplée) avec comptes, rôles et
traductions liées. Cette phase demande un accès à l'hébergement, que je n'ai
pas aujourd'hui — le SSH est fermé de mon côté. Ce qui est livré ici est
l'identité complète et la totalité du front end, conçus pour être versés dans
un CMS ensuite : gabarits réguliers, contenus séparés du code
(`source/contenu.py`), rôles déjà décrits sur la page *House of Adjaoudi*, et
une deuxième langue qui n'est qu'un dossier et une traduction — une
troisième le sera aussi.
