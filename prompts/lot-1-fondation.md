# Lot 1 — Fondation technique Maison Moins Humide

Tu es Claude Code dans un projet neuf. Utilise le fichier CLAUDE.md comme cadrage.

Objectif de ce lot : créer uniquement la fondation technique Astro V1, sans rédiger les 15 articles complets.

À faire :
1. Initialiser un projet Astro statique compatible Node 20 dans le dossier courant.
2. Créer une structure propre :
   - public/images/
   - public/favicon.svg
   - public/robots.txt
   - src/components/
   - src/layouts/
   - src/pages/
   - src/styles/global.css
   - src/data/navigation.json si utile
3. Créer les composants :
   - Header.astro
   - Footer.astro
   - ArticleCard.astro
   - AlertBox.astro
   - AffiliateDisclosure.astro
   - Breadcrumbs.astro
4. Créer les layouts :
   - BaseLayout.astro avec title/meta/canonical basiques + JSON-LD WebSite/Organization sur accueil si simple.
   - ArticleLayout.astro pour les guides/pièces.
   - ComparisonLayout.astro pour les comparatifs.
5. Créer la page d’accueil `/` avec contenu V1 court :
   - H1 : Humidité dans la maison : comprendre, mesurer et agir efficacement
   - intro courte
   - entrées rapides par problème
   - guides populaires
   - solutions par pièce
   - produits utiles
   - encadré prudence
6. Créer les pages légales/confiance avec contenu placeholder propre :
   - /a-propos/
   - /contact/
   - /mentions-legales/
   - /politique-confidentialite/
   - /politique-affiliation/
   - /avertissement/
7. Préparer des pages placeholders utiles pour les catégories :
   - /guides/
   - /pieces/
   - /comparatifs/
   - /produits-utiles/
8. Installer/configurer sitemap si raisonnable.
9. Ajouter README.md avec commandes.
10. Lancer `npm run build` et corriger jusqu’à ce que ça passe.

Contraintes :
- Pas de rédaction longue des articles maintenant.
- Pas de liens affiliés réels.
- Pas de dépendances lourdes inutiles.
- Design sobre, responsive mobile-first.
- Pas de promesses santé/bâtiment excessives.
- Ne touche pas à autre chose que ce dossier projet.

Réponds à la fin avec : fichiers créés, build OK ou erreurs restantes, prochaines étapes.