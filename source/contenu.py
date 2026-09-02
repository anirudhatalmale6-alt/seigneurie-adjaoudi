# -*- coding: utf-8 -*-
"""Contenu du site de la Seigneurie Adjaoudi, en anglais et en francais.

Regle qui gouverne tout ce fichier : rien de ce qui est ecrit ici n'affirme
un fait sur la famille Adjaoudi. Aucune origine, aucune date, aucun lieu,
aucun ancetre, aucune branche, aucun membre, aucune archive. Ce qui manque
est marque d'une pastille « Awaiting authorisation / En attente
d'autorisation » — un seul vocabulaire de blanc, jamais melange avec ceux
des autres sites de ce client.

Le mot Seigneurie / Lordship est employe partout comme une designation
familiale et culturelle. Le site ne dit nulle part qu'elle est reconnue,
concedee, enregistree, ni qu'elle confere un titre, un rang, une preseance
ou une noblesse quelconque. Cette regle vient du cahier des charges du
client lui-meme.

Chaque chaine est un couple (anglais, francais).
"""

LANGUES = ("en", "fr")

MAISON = ("Adjaoudi Lordship", "Seigneurie Adjaoudi")
DEVISE = ("Heritage illuminates the future.",
          "Le patrimoine éclaire l’avenir.")
DEVISE_NOTE = ("Proposed motto, awaiting family approval.",
               "Devise proposée, en attente d’approbation familiale.")

ATTENTE = ("Awaiting authorisation", "En attente d’autorisation")
ATTENTE_LONG = (
    "Nothing is published here until the family has authorised it in writing, "
    "and until the entry carries a date and a source.",
    "Rien n’est publié ici tant que la famille ne l’a pas autorisé par écrit, "
    "et tant que l’entrée ne porte pas une date et une source.")

# --------------------------------------------------------------- navigation
PAGES = [
    # (cle, fichier_en, fichier_fr, titre_en, titre_fr, dans_le_menu)
    ("home", "index.html", "index.html", "Home", "Accueil", False),
    ("lordship", "the-lordship.html", "la-seigneurie.html",
     "The Lordship", "La Seigneurie", True),
    ("heritage", "heritage.html", "patrimoine.html",
     "Heritage", "Patrimoine", True),
    ("house", "house-of-adjaoudi.html", "la-maison.html",
     "House of Adjaoudi", "La Maison Adjaoudi", True),
    ("initiatives", "initiatives.html", "initiatives.html",
     "Initiatives", "Initiatives", True),
    ("journal", "journal.html", "journal.html", "Journal", "Journal", True),
    ("media", "media-library.html", "mediatheque.html",
     "Media Library", "Médiathèque", True),
    ("contact", "contact.html", "contact.html", "Contact", "Contact", True),
    ("circle", "private-circle.html", "cercle-prive.html",
     "Private Circle", "Cercle privé", False),
    ("legal", "legal.html", "mentions-legales.html",
     "Legal & privacy", "Mentions légales", False),
]

DECOUVRIR = ("Discover the House", "Découvrir la Maison")
RECHERCHE = ("Search", "Rechercher")
RECHERCHE_INVITE = ("Search the site", "Rechercher dans le site")
RECHERCHE_VIDE = ("No section matches that search.",
                  "Aucune section ne correspond à cette recherche.")
RECHERCHE_SANS_JS = (
    "Search needs JavaScript. Every page is reachable from the menu above.",
    "La recherche demande JavaScript. Toutes les pages sont accessibles "
    "depuis le menu ci-dessus.")
FERMER = ("Close", "Fermer")
ALLER_CONTENU = ("Skip to content", "Aller au contenu")

# ------------------------------------------------------------------ accueil
MANIFESTE_TITRE = ("A living heritage", "Un patrimoine vivant")
MANIFESTE = [
    ("The Adjaoudi Lordship is a family and cultural identity. It gathers "
     "memory, values and projects, and gives them a durable place to live.",
     "La Seigneurie Adjaoudi est une identité familiale et culturelle. Elle "
     "rassemble une mémoire, des valeurs et des projets, et leur donne un "
     "lieu durable où exister."),
    ("It is not a public authority. It exercises no official function, holds "
     "no delegated power, and speaks for no state or administration. The "
     "word Lordship is used here as a family and cultural designation.",
     "Elle n’est pas une autorité publique. Elle n’exerce aucune fonction "
     "officielle, ne détient aucun pouvoir délégué, et ne parle au nom "
     "d’aucun État ni d’aucune administration. Le mot Seigneurie est employé "
     "ici comme une désignation familiale et culturelle."),
    ("This site is being built in the open. What is not yet established is "
     "shown as missing rather than filled in. Every historical entry will "
     "carry a date and a source; every portrait and every document will "
     "carry a credit and a right of use.",
     "Ce site se construit à découvert. Ce qui n’est pas encore établi est "
     "montré comme manquant plutôt que comblé. Chaque entrée historique "
     "portera une date et une source ; chaque portrait et chaque document "
     "porteront un crédit et un droit d’usage."),
]

PORTES = [
    ("lordship", ("History", "Histoire"),
     ("Where the name comes from, what it has meant, and the timeline of the "
      "House as it is established.",
      "D’où vient le nom, ce qu’il a signifié, et la chronologie de la Maison "
      "à mesure qu’elle s’établit.")),
    ("initiatives", ("Initiatives", "Initiatives"),
     ("Culture, education, solidarity, economy and environment — what the "
      "House chooses to carry.",
      "Culture, éducation, solidarité, économie et environnement — ce que la "
      "Maison choisit de porter.")),
    ("journal", ("Journal", "Journal"),
     ("Articles, statements and interviews, published under a stated "
      "editorial rule.",
      "Articles, déclarations et entretiens, publiés sous une règle "
      "éditoriale affichée.")),
]

SELECTION_TITRE = ("Editorial selection", "Sélection éditoriale")
SELECTION = [
    (("Article", "Article"), ("Journal", "Journal")),
    (("Article", "Article"), ("Journal", "Journal")),
    (("Heritage object", "Objet de patrimoine"), ("Heritage", "Patrimoine")),
]

INFOLETTRE_TITRE = ("House news", "Nouvelles de la Maison")
INFOLETTRE = (
    "A short letter, sent only when there is something to report. The "
    "subscription form is a mock-up: no address is collected, stored or sent "
    "anywhere until the House has chosen where its data lives.",
    "Une lettre brève, envoyée seulement quand il y a quelque chose à "
    "annoncer. Le formulaire d’abonnement est une maquette : aucune adresse "
    "n’est collectée, conservée ni envoyée où que ce soit tant que la Maison "
    "n’a pas choisi où résident ses données.")

# --------------------------------------------------------------- chronologie
FRISE_TITRE = ("Timeline", "Chronologie")
FRISE_VIDE = (
    "This timeline has no entries yet.",
    "Cette chronologie ne comporte aucune entrée.")
FRISE_REGLE = (
    "It is empty on purpose. An entry is added only when three things exist "
    "together: a date, a source that can be named, and the family’s written "
    "authorisation to publish it. A heritage timeline is worth exactly as "
    "much as its weakest entry.",
    "Elle est vide volontairement. Une entrée n’est ajoutée que lorsque trois "
    "choses existent ensemble : une date, une source que l’on peut nommer, et "
    "l’autorisation écrite de la famille de la publier. Une chronologie "
    "patrimoniale vaut exactement ce que vaut sa plus faible entrée.")
FRISE_CHAMPS = [
    (("Date", "Date"), ("Exact or approximate, stated as such.",
                        "Exacte ou approximative, et dite comme telle.")),
    (("Event", "Événement"), ("One sentence, factual, without adjectives.",
                              "Une phrase, factuelle, sans adjectifs.")),
    (("Place", "Lieu"), ("Named only if the source names it.",
                         "Nommé seulement si la source le nomme.")),
    (("Source", "Source"), ("Document, register, publication or attributed "
                            "testimony.",
                            "Document, registre, publication ou témoignage "
                            "attribué.")),
    (("Media", "Média"), ("Optional, with credit and right of use.",
                          "Facultatif, avec crédit et droit d’usage.")),
    (("Category", "Catégorie"), ("Family, place, object, document or "
                                 "initiative.",
                                 "Famille, lieu, objet, document ou "
                                 "initiative.")),
]

# ------------------------------------------------------------ la seigneurie
VALEURS_TITRE = ("Brand territory", "Territoire de marque")
VALEURS_INTRO = (
    "Five attributes, taken from the House’s own guidelines. They govern the "
    "writing as much as the design.",
    "Cinq attributs, repris du guide de la Maison. Ils gouvernent l’écriture "
    "autant que le dessin.")
VALEURS = [
    (("Heritage", "Patrimoine"), ("Memory, continuity, transmission",
                                  "Mémoire, continuité, transmission")),
    (("Light", "Lumière"), ("Knowledge, discernment, influence",
                            "Savoir, discernement, influence")),
    (("Dignity", "Dignité"), ("Restraint, composure, responsibility",
                              "Retenue, tenue, responsabilité")),
    (("Hospitality", "Hospitalité"), ("Openness, dialogue, generosity",
                                      "Ouverture, dialogue, générosité")),
    (("Modernity", "Modernité"), ("Digital capability, innovation, tangible "
                                  "projects",
                                  "Capacité numérique, innovation, projets "
                                  "concrets")),
]

SEIGNEURIE_BLOCS = [
    ("origin", ("Origin", "Origine"),
     ("Where the House places its beginning, and on the strength of which "
      "documents.",
      "Où la Maison situe son commencement, et sur la foi de quels "
      "documents.")),
    ("name", ("Meaning of the name", "Sens du nom"),
     ("What Adjaoudi means, where it is attested, and how it has been "
      "carried. This will be written from a source the family provides, and "
      "from nothing else.",
      "Ce que signifie Adjaoudi, où le nom est attesté, et comment il a été "
      "porté. Ce texte sera écrit à partir d’une source fournie par la "
      "famille, et de rien d’autre.")),
    ("today", ("The House today", "La Maison aujourd’hui"),
     ("How the House is organised, who speaks for it, and how decisions are "
      "taken.",
      "Comment la Maison est organisée, qui parle en son nom, et comment les "
      "décisions sont prises.")),
]

STATUT_TITRE = ("What this designation is, and is not",
                "Ce que cette désignation est, et n’est pas")
STATUT_EST = [
    ("A family and cultural designation, used by the House to name itself.",
     "Une désignation familiale et culturelle, dont la Maison se sert pour se "
     "nommer."),
    ("A brand under which the House gathers its heritage work and its "
     "initiatives.",
     "Une marque sous laquelle la Maison rassemble son travail patrimonial et "
     "ses initiatives."),
    ("A commitment to publish only what is dated, sourced and authorised.",
     "Un engagement à ne publier que ce qui est daté, sourcé et autorisé."),
]
STATUT_NEST_PAS = [
    ("It is not a public authority and exercises no official function.",
     "Ce n’est pas une autorité publique et elle n’exerce aucune fonction "
     "officielle."),
    ("It confers no title, no rank, no precedence and no nobility.",
     "Elle ne confère aucun titre, aucun rang, aucune préséance et aucune "
     "noblesse."),
    ("It is not claimed to be recognised, granted or registered by any "
     "authority.",
     "Elle n’est présentée comme reconnue, concédée ou enregistrée par aucune "
     "autorité."),
    ("The coat of arms is a brand emblem. It is not claimed to be granted, "
     "matriculated or entered in any armorial register.",
     "Le blason est un emblème de marque. Il n’est pas présenté comme "
     "octroyé, immatriculé ni inscrit dans un quelconque registre "
     "armorial."),
    ("Nothing on this site represents a state, a government or an "
     "administration.",
     "Rien sur ce site ne représente un État, un gouvernement ou une "
     "administration."),
]

# ------------------------------------------------------------------ patrimoine
PATRIMOINE_INTRO = (
    "Five collections. Each one is empty until an item can be published with "
    "a caption, a date, a credit and a right of use recorded in the rights "
    "register.",
    "Cinq ensembles. Chacun reste vide tant qu’une pièce ne peut pas être "
    "publiée avec une légende, une date, un crédit et un droit d’usage "
    "inscrits au registre des droits.")
PATRIMOINE = [
    ("places", ("Places", "Lieux"),
     ("Houses, land, buildings and landscapes attached to the family history.",
      "Maisons, terres, bâtiments et paysages attachés à l’histoire "
      "familiale.")),
    ("objects", ("Objects", "Objets"),
     ("Pieces held by the House, each with its provenance and its condition.",
      "Pièces détenues par la Maison, chacune avec sa provenance et son "
      "état.")),
    ("stories", ("Stories", "Récits"),
     ("Attributed testimony. The name of the person who tells it is part of "
      "the record.",
      "Témoignages attribués. Le nom de la personne qui raconte fait partie "
      "du document.")),
    ("documents", ("Documents", "Documents"),
     ("Acts, letters, registers and photographs, in the state in which they "
      "were found.",
      "Actes, lettres, registres et photographies, dans l’état où ils ont été "
      "trouvés.")),
    ("gallery", ("Gallery", "Galerie"),
     ("A visual reading of the four collections above, once they exist.",
      "Une lecture visuelle des quatre ensembles ci-dessus, lorsqu’ils "
      "existeront.")),
]

DROITS_TITRE = ("Rights register", "Registre des droits")
DROITS_INTRO = (
    "Every photograph, video, document and testimonial gets a row here before "
    "it appears anywhere on the site. The register is empty because the site "
    "carries no such item yet.",
    "Chaque photographie, vidéo, document et témoignage reçoit une ligne ici "
    "avant d’apparaître où que ce soit sur le site. Le registre est vide "
    "parce que le site ne porte encore aucune pièce de ce type.")
DROITS_COLONNES = [
    ("Item", "Pièce"), ("Type", "Type"), ("Author or holder", "Auteur ou détenteur"),
    ("Right of use", "Droit d’usage"), ("Authorisation", "Autorisation"),
]

CORRECTION_TITRE = ("Correcting or removing content",
                    "Corriger ou retirer un contenu")
CORRECTION = (
    "Heritage content is disputed sometimes, and the answer to a dispute "
    "cannot be silence. Anyone who believes an entry is wrong, or that a "
    "document or a portrait should not be public, can write to the House "
    "through the contact page. The entry is suspended from view while it is "
    "examined, the outcome is recorded, and a corrected entry says that it "
    "was corrected.",
    "Un contenu patrimonial est parfois contesté, et la réponse à une "
    "contestation ne peut pas être le silence. Toute personne qui estime "
    "qu’une entrée est erronée, ou qu’un document ou un portrait ne devrait "
    "pas être public, peut écrire à la Maison par la page de contact. "
    "L’entrée est retirée de la vue pendant son examen, l’issue est "
    "consignée, et une entrée corrigée dit qu’elle a été corrigée.")

# --------------------------------------------------------------- la maison
MAISON_INTRO = (
    "This page will present the branches of the family and the portraits the "
    "House has approved. It is empty, and it will stay empty until two "
    "conditions are met for each person named.",
    "Cette page présentera les branches de la famille et les portraits "
    "approuvés par la Maison. Elle est vide, et elle le restera tant que deux "
    "conditions ne seront pas réunies pour chaque personne nommée.")
MAISON_CONDITIONS = [
    ("The person, or the family for a person who has died, has authorised "
     "publication in writing.",
     "La personne, ou la famille pour une personne décédée, a autorisé la "
     "publication par écrit."),
    ("What is published is limited to what that authorisation covers — a "
     "name, a role, a portrait, nothing beyond.",
     "Ce qui est publié se limite à ce que cette autorisation couvre — un "
     "nom, un rôle, un portrait, rien au-delà."),
]
MAISON_DEFAUT = (
    "By default, all private family data is excluded from the public site. "
    "That is the House’s own rule, and it is the safer way round: a name is "
    "easy to add later and impossible to take back once it has been indexed.",
    "Par défaut, toute donnée familiale privée est exclue du site public. "
    "C’est la règle de la Maison elle-même, et c’est le bon sens : un nom "
    "s’ajoute facilement plus tard et ne se reprend pas une fois indexé.")
BRANCHES_TITRE = ("Branches", "Branches")
PORTRAITS_TITRE = ("Approved portraits", "Portraits approuvés")
PORTRAITS_NOTE = (
    "No portrait on this site is generated, reconstructed or retouched into "
    "something it was not. If an image is ever restored or generated, it will "
    "say so on the image itself.",
    "Aucun portrait de ce site n’est généré, reconstitué ou retouché en "
    "quelque chose qu’il n’était pas. Si une image est un jour restaurée ou "
    "générée, elle le dira sur l’image même.")

# -------------------------------------------------------------- initiatives
INITIATIVES_INTRO = (
    "Five fields the House means to work in. Each card describes the field, "
    "not a project: no initiative is announced here until it exists, has a "
    "person answerable for it, and can be described without exaggeration.",
    "Cinq domaines dans lesquels la Maison entend travailler. Chaque fiche "
    "décrit le domaine, pas un projet : aucune initiative n’est annoncée ici "
    "tant qu’elle n’existe pas, n’a pas de responsable, et ne peut pas être "
    "décrite sans exagération.")
INITIATIVES = [
    ("culture", ("Culture", "Culture"),
     ("Publication, exhibition, restoration and the transmission of practices.",
      "Publication, exposition, restauration et transmission de pratiques.")),
    ("education", ("Education", "Éducation"),
     ("Study, teaching, and support for people who carry knowledge forward.",
      "Étude, enseignement, et soutien aux personnes qui portent un savoir.")),
    ("solidarity", ("Solidarity", "Solidarité"),
     ("Help that is given without being announced, and reported afterwards "
      "without naming those helped.",
      "Une aide donnée sans être annoncée, et rapportée ensuite sans nommer "
      "ceux qui l’ont reçue.")),
    ("economy", ("Economy", "Économie"),
     ("Work, craft and enterprise connected to the House’s heritage.",
      "Travail, artisanat et entreprise liés au patrimoine de la Maison.")),
    ("environment", ("Environment", "Environnement"),
     ("Land, water and built heritage, and what it costs to keep them.",
      "Terre, eau et patrimoine bâti, et ce qu’il en coûte de les tenir.")),
]

# ------------------------------------------------------------------ journal
JOURNAL_VIDE = ("The journal has no entries yet.",
                "Le journal ne comporte aucune entrée.")
CHARTE_TITRE = ("Editorial rule", "Règle éditoriale")
CHARTE = [
    ("Institutional without rigidity, cultivated without grandiosity, "
     "accessible and factual.",
     "Institutionnel sans raideur, cultivé sans grandiloquence, accessible et "
     "factuel."),
    ("Sources, dates and attributed testimony come before adjectives.",
     "Les sources, les dates et les témoignages attribués passent avant les "
     "adjectifs."),
    ("An unverifiable claim is not written, not even in passing.",
     "Une affirmation invérifiable n’est pas écrite, pas même en passant."),
    ("A correction is published as visibly as what it corrects.",
     "Une correction est publiée aussi visiblement que ce qu’elle corrige."),
    ("The House speaks for itself only, and takes no position in the name of "
     "anyone else.",
     "La Maison ne parle que pour elle-même, et ne prend position au nom de "
     "personne d’autre."),
]
JOURNAL_TYPES = [
    ("Article", "Article"), ("Statement", "Déclaration"),
    ("Interview", "Entretien"), ("Publication", "Publication"),
]

# --------------------------------------------------------------- mediatheque
MEDIA_INTRO = (
    "Photographs, videos and downloadable documents, organised in albums, "
    "with a caption, a date, a credit and a right of use on every item. The "
    "library is empty.",
    "Photographies, vidéos et documents téléchargeables, organisés en albums, "
    "avec une légende, une date, un crédit et un droit d’usage sur chaque "
    "pièce. La médiathèque est vide.")
MEDIA_FILTRES = [
    ("All", "Tout"), ("Photographs", "Photographies"), ("Videos", "Vidéos"),
    ("Documents", "Documents"),
]
MEDIA_REGLE = (
    "No generic stock imagery is used anywhere on this site. Every image will "
    "be an authentic photograph with a caption and a date, or it will not be "
    "there at all. Restored or generated images are identified as such on the "
    "image.",
    "Aucune image générique de banque d’images n’est employée sur ce site. "
    "Chaque image sera une photographie authentique avec une légende et une "
    "date, ou elle ne sera pas là. Les images restaurées ou générées sont "
    "identifiées comme telles sur l’image.")

# ------------------------------------------------------------------ contact
CONTACT_INTRO = (
    "Three ways to write to the House. The forms below are mock-ups: they are "
    "not connected, they send nothing, and they store nothing. They are here "
    "so the wording, the fields and the consent can be agreed before anything "
    "is switched on.",
    "Trois façons d’écrire à la Maison. Les formulaires ci-dessous sont des "
    "maquettes : ils ne sont pas connectés, ils n’envoient rien et ne "
    "conservent rien. Ils sont là pour que la formulation, les champs et le "
    "consentement soient arrêtés avant que quoi que ce soit ne soit activé.")
FORMULAIRES = [
    ("general", ("General enquiry", "Demande générale"),
     ("For anyone writing to the House for the first time.",
      "Pour toute personne écrivant à la Maison pour la première fois.")),
    ("partnership", ("Partnership", "Partenariat"),
     ("Cultural, academic and economic partners.",
      "Partenaires culturels, académiques et économiques.")),
    ("media", ("Media and research", "Presse et recherche"),
     ("Journalists and researchers, including requests to consult sources.",
      "Journalistes et chercheurs, y compris les demandes de consultation de "
      "sources.")),
]
CHAMPS = [
    (("Name", "Nom"), "text"),
    (("Organisation", "Organisation"), "text"),
    (("How to reach you", "Comment vous joindre"), "text"),
    (("Your message", "Votre message"), "textarea"),
]
CONSENTEMENT = (
    "I agree that the House may keep this message in order to reply to it.",
    "J’accepte que la Maison conserve ce message afin d’y répondre.")
ENVOYER = ("Send", "Envoyer")
MAQUETTE = ("Mock-up — not connected", "Maquette — non connectée")
COORDONNEES_TITRE = ("Where to find the House", "Où trouver la Maison")
COORDONNEES = [
    ("Postal address", "Adresse postale"),
    ("Telephone", "Téléphone"),
    ("Official channels", "Canaux officiels"),
]

# ------------------------------------------------------------- cercle prive
CERCLE_INTRO = (
    "The Private Circle holds restricted archives and content, by invitation. "
    "It does not exist yet: no account has been created, no password has been "
    "set, and no personal data is stored anywhere on this site.",
    "Le Cercle privé abrite des archives et des contenus restreints, sur "
    "invitation. Il n’existe pas encore : aucun compte n’a été créé, aucun "
    "mot de passe n’a été défini, et aucune donnée personnelle n’est "
    "conservée où que ce soit sur ce site.")
CERCLE_REF = ("Member reference", "Référence de membre")
CERCLE_REF_NOTE = (
    "The form asks for a member reference rather than an email address, and "
    "that is deliberate. A sign-in page that accepts an address turns every "
    "failed attempt into an answer about who is, and is not, part of this "
    "family.",
    "Le formulaire demande une référence de membre plutôt qu’une adresse "
    "e-mail, et c’est délibéré. Une page de connexion qui accepte une adresse "
    "transforme chaque tentative échouée en réponse sur qui fait partie, ou "
    "non, de cette famille.")
CERCLE_ENTRER = ("Enter", "Entrer")
CERCLE_DECISIONS_TITRE = ("Four things to settle before it opens",
                          "Quatre points à trancher avant l’ouverture")
CERCLE_DECISIONS = [
    ("Who holds the member list, and in which country it is held.",
     "Qui détient la liste des membres, et dans quel pays elle est détenue."),
    ("Who may invite, and who may withdraw an invitation.",
     "Qui peut inviter, et qui peut retirer une invitation."),
    ("What is behind the door: which archives, at which level of detail.",
     "Ce qu’il y a derrière la porte : quelles archives, à quel niveau de "
     "détail."),
    ("How long an access log is kept, and who is allowed to read it.",
     "Combien de temps un journal d’accès est conservé, et qui a le droit de "
     "le lire."),
]

# ------------------------------------------------------------------- roles
ROLES_TITRE = ("Roles", "Rôles")
ROLES = [
    (("Super Administrator", "Super administrateur"),
     ("Configuration, security and role management.",
      "Configuration, sécurité et gestion des rôles.")),
    (("Editor-in-Chief", "Rédacteur en chef"),
     ("Approval and publishing.", "Approbation et publication.")),
    (("Contributor", "Contributeur"),
     ("Drafting, without the right to publish alone.",
      "Rédaction, sans droit de publier seul.")),
    (("Archivist", "Archiviste"),
     ("Metadata, sources, rights and classification.",
      "Métadonnées, sources, droits et classement.")),
    (("Translator", "Traducteur"),
     ("Access limited to language versions.",
      "Accès limité aux versions linguistiques.")),
]

# ------------------------------------------------------------------- legal
LEGAL_BLOCS = [
    ("notices", ("Legal notices", "Mentions légales"),
     ("The publisher’s legal name, address, company number and publication "
      "director, and the name and address of the host.",
      "La dénomination légale de l’éditeur, son adresse, son numéro "
      "d’immatriculation et son directeur de publication, ainsi que le nom et "
      "l’adresse de l’hébergeur.")),
    ("privacy", ("Privacy", "Confidentialité"), None),
    ("accessibility", ("Accessibility", "Accessibilité"), None),
]
VIE_PRIVEE_FAIT = [
    ("This site sets no cookie.", "Ce site ne dépose aucun cookie."),
    ("It runs no analytics and no measurement of any kind.",
     "Il n’exécute aucune mesure d’audience, d’aucune sorte."),
    ("It makes no request to any third party. Fonts, images and styles are "
     "served from the site itself.",
     "Il n’adresse aucune requête à un tiers. Les polices, les images et les "
     "styles sont servis par le site lui-même."),
    ("The forms are not connected and transmit nothing.",
     "Les formulaires ne sont pas connectés et ne transmettent rien."),
    ("No account exists, so no password and no personal data are stored.",
     "Aucun compte n’existe, donc aucun mot de passe ni aucune donnée "
     "personnelle ne sont conservés."),
]
VIE_PRIVEE_APRES = (
    "This will change the day a form is connected or the Private Circle "
    "opens. On that day this page has to say what is collected, why, for how "
    "long it is kept, and who can ask for it back — and it has to say it "
    "before the feature is switched on, not after.",
    "Cela changera le jour où un formulaire sera connecté ou où le Cercle "
    "privé ouvrira. Ce jour-là, cette page devra dire ce qui est collecté, "
    "pourquoi, combien de temps c’est conservé, et qui peut le récupérer — et "
    "elle devra le dire avant la mise en service, pas après.")
ACCESSIBILITE = [
    ("Target: WCAG 2.2 level AA on every template of this site.",
     "Objectif : WCAG 2.2 niveau AA sur chaque gabarit de ce site."),
    ("Text contrast is measured on the rendered page at fourteen screen "
     "widths, not estimated from the stylesheet.",
     "Le contraste des textes est mesuré sur la page rendue à quatorze "
     "largeurs d’écran, et non estimé d’après la feuille de style."),
    ("Every interactive element is reachable and usable with the keyboard "
     "alone, and shows where the focus is.",
     "Chaque élément interactif est atteignable et utilisable au clavier "
     "seul, et montre où se trouve le focus."),
    ("Animation is limited to short transitions and is switched off entirely "
     "for anyone who has asked their system to reduce motion.",
     "L’animation se limite à de courtes transitions et se coupe entièrement "
     "pour toute personne ayant demandé à son système de réduire les "
     "animations."),
    ("Every image carries a text alternative; decorative shapes are hidden "
     "from screen readers rather than described.",
     "Chaque image porte une alternative textuelle ; les formes décoratives "
     "sont masquées aux lecteurs d’écran plutôt que décrites."),
]

# ------------------------------------------------------------------- footer
PIED_DECLARATION = (
    "The Adjaoudi Lordship is a family and cultural identity. It is not a "
    "public authority, exercises no official function, and confers no title, "
    "rank, precedence or nobility. Neither the designation nor the coat of "
    "arms is claimed to be recognised, granted, registered or accredited by "
    "any authority whatsoever.",
    "La Seigneurie Adjaoudi est une identité familiale et culturelle. Elle "
    "n’est pas une autorité publique, n’exerce aucune fonction officielle, et "
    "ne confère aucun titre, rang, préséance ou noblesse. Ni la désignation "
    "ni le blason ne sont présentés comme reconnus, concédés, enregistrés ou "
    "accrédités par une quelconque autorité.")
PIED_CANAUX = ("Official channels", "Canaux officiels")
PIED_LANGUES = ("Languages", "Langues")
LANGUES_APRES = (
    "Arabic and Tamazight versions are planned. The site is built so that a "
    "third language is a folder and a translation, not a rebuild.",
    "Des versions en arabe et en tamazight sont prévues. Le site est bâti "
    "pour qu’une troisième langue soit un dossier et une traduction, pas une "
    "reconstruction.")
