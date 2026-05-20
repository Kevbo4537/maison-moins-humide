# Maison Moins Humide — cadrage Claude Code

## Objectif
Créer une V1 Astro statique, rapide, mobile-first, SEO-friendly, pour le site **Maison Moins Humide**.

Positionnement : conseils simples pour comprendre, mesurer et réduire l’humidité dans une maison ou un appartement, sans dramatiser et sans vendre de solution miracle.

## Rôle du site
Aider le visiteur à répondre à :
1. Est-ce grave ?
2. Que faire tout de suite ?
3. Quel produit ou professionnel peut aider ?

## Ton éditorial
- clair, rassurant, pratique, sérieux ;
- pas anxiogène ;
- pas médicalisant ;
- pas trop technique ;
- prudent sur santé/bâtiment.

Phrases/positionnement à respecter :
- Un produit peut aider, mais ne remplace pas la recherche de la cause.
- Mesurer avec un hygromètre sur plusieurs jours avant d’acheter.
- Si infiltration, moisissures étendues, mur mouillé, salpêtre ou symptômes : diagnostic professionnel / assurance / professionnel de santé.
- Humidité intérieure de repère : 40 à 60 %, température autour de 18 à 22 °C selon les pièces.

À éviter :
- promesses miracle ;
- “meilleur produit du marché” ;
- diagnostic définitif ;
- affiliation agressive ;
- images/ton catastrophiste.

## Stack
- Astro statique ;
- Markdown/MDX ou pages Astro simples ;
- CSS simple, pas de framework lourd sauf nécessité ;
- sitemap XML ;
- robots.txt ;
- JSON-LD : WebSite, Organization, BreadcrumbList, Article, FAQPage si vraie FAQ.

## Design
Ambiance : propre, calme, fiable, maison saine.
Palette : blanc cassé, gris très clair, bleu doux, vert sauge, texte bleu nuit/gris charbon, boutons bleu foncé, alertes beige/jaune doux.
Mobile-first : intro courte, réponse rapide, sommaire cliquable, paragraphes courts, CTA sobres, tableaux mobile-friendly.

## Arborescence V1
Accueil : `/`
Guides :
- `/guides/humidite-maison-que-faire/`
- `/guides/taux-humidite-ideal-maison/`
- `/guides/humidite-maison-70-pourcent/`
- `/guides/moisissure-mur-danger/`
- `/guides/condensation-fenetre/`
- `/guides/odeur-humidite-maison/`
Pièces :
- `/pieces/salle-de-bain-humide/`
- `/pieces/chambre-humide/`
- `/pieces/cave-humide/`
- `/pieces/placard-humide/`
- `/pieces/buanderie-humide/`
Comparatifs :
- `/comparatifs/meilleur-deshumidificateur-maison/`
- `/comparatifs/meilleur-absorbeur-humidite/`
- `/comparatifs/meilleur-hygrometre-maison/`
- `/comparatifs/deshumidificateur-ou-absorbeur/`
Pages :
- `/a-propos/`
- `/contact/`
- `/mentions-legales/`
- `/politique-confidentialite/`
- `/politique-affiliation/`
- `/avertissement/`

## Menu
Principal : Guides humidité, Solutions par pièce, Comparatifs, Produits utiles, À propos.
Footer : Contact, Mentions légales, Politique de confidentialité, Politique d’affiliation, Avertissement santé / bâtiment.

## Composants souhaités
- Header.astro
- Footer.astro
- ArticleCard.astro
- ProductCard.astro
- AlertBox.astro
- Toc.astro
- AffiliateDisclosure.astro
- Breadcrumbs.astro
- SeoHead ou logique SEO dans BaseLayout

## Layouts souhaités
- BaseLayout.astro
- ArticleLayout.astro
- ComparisonLayout.astro

## SEO minimum
Chaque page : title unique, meta description unique, H1 unique, canonical si possible, maillage interne, structure H2 claire, données structurées quand pertinent.

## Transparence affiliation
Phrase générique :
“Certains liens présents sur ce site sont des liens affiliés. Si vous achetez via ces liens, le site peut recevoir une commission, sans coût supplémentaire pour vous. Cela n’influence pas notre volonté de présenter des conseils utiles, prudents et adaptés aux problèmes d’humidité.”

Phrase Amazon si Amazon est utilisé plus tard :
“En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.”

## Règles de travail Claude Code
- Ne pas improviser une usine à gaz.
- Ne pas ajouter de backend.
- Ne pas ajouter de popups.
- Ne pas surcharger en JS.
- Privilégier lisibilité, SEO et rapidité.
- Après chaque lot : `npm run build` doit passer.
