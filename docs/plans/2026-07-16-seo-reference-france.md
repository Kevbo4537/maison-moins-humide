# Maison Moins Humide — première vague SEO nationale

> **For Hermes:** Use subagent-driven-development discipline and independent review before deployment.

**Goal:** renforcer les pages déjà visibles dans Google, la confiance éditoriale, l’indexabilité et le maillage interne sans créer de contenu artificiel ni de promesses trompeuses.

**Architecture:** conserver Astro statique et les URL existantes. Appliquer des changements incrémentaux et réversibles, puis corriger séparément la redirection OVH qui ajoute `:443`. Déployer seulement après build, contrôle SEO et revue indépendante.

**Tech Stack:** Astro 4, HTML/CSS/JavaScript statique, JSON-LD Schema.org, OVH FTP.

---

### Task 1: Renforcer les garde-fous SEO

**Files:**
- Modify: `scripts/seo-check.mjs`

**Steps:**
1. Ajouter les contrôles de canonical HTTPS/www, title/description raisonnables, robots et JSON-LD sur les pages éditoriales.
2. Exécuter `npm run build && npm run check:seo` pour obtenir les écarts réels.
3. Ajuster uniquement les pages concernées, sans allonger artificiellement les textes.

### Task 2: Rendre la méthode éditoriale transparente

**Files:**
- Create: `src/pages/notre-methode/index.astro`
- Modify: `src/layouts/BaseLayout.astro`
- Modify: `src/layouts/ArticleLayout.astro`
- Modify: `src/components/Footer.astro`

**Steps:**
1. Publier une méthode honnête : sources, sélection produit, absence de test laboratoire sauf mention, mises à jour, limites et affiliation.
2. Enrichir les données structurées WebSite/Organization/Article sans inventer d’auteur expert.
3. Afficher une note de mise à jour et un lien vers la méthode lorsqu’une date est fournie.
4. Vérifier build et rendu.

### Task 3: Renforcer les quatre intentions GSC prioritaires

**Files:**
- Modify: `src/pages/pieces/buanderie-humide/index.astro`
- Modify: `src/pages/pieces/index.astro`
- Modify: `src/pages/outils/calculateur-point-de-rosee-condensation/index.astro`
- Modify: `src/pages/guides/condensation-fenetre/index.astro`
- Modify: `src/pages/index.astro`

**Steps:**
1. Aligner titres/H1/introduction sur les formulations réellement vues dans GSC.
2. Ajouter des réponses concrètes, tableaux/étapes et liens internes utiles.
3. Ajouter des dates de mise à jour uniquement aux pages réellement revues.
4. Ne pas cibler `Hygrostop prix` avant validation du produit et de l’intention.

### Task 4: Corriger la redirection OVH

**Files:**
- Backup remote `.htaccess` before any change.
- Modify remote `.htaccess` only if the cause of `https://www...:443/` is verified.

**Steps:**
1. Sauvegarder récursivement `/www` ou au minimum les fichiers modifiés.
2. Corriger les redirections sans changer les URL canoniques.
3. Vérifier HTTP/non-www/www/index.html/URL sans slash avec `curl`.

### Task 5: Revue, test et déploiement

**Steps:**
1. Exécuter `npm run build` et `npm run check:seo`.
2. Auditer le diff et lancer une revue indépendante sécurité/logique/SEO.
3. Corriger les points bloquants et relancer les tests.
4. Sauvegarder OVH, déployer `dist`, vérifier les pages publiques sur mobile et desktop.
5. Committer seulement l’implémentation validée.

### Task 6: Suite éditoriale et affiliation

**Steps:**
1. Intégrer les conclusions des audits concurrents et monétisation.
2. Fournir à Kevin une liste précise des produits nécessaires avant tout ajout non déjà validé.
3. Prioriser les prochains contenus par potentiel, difficulté et cohérence de cluster.
4. Mettre en place un suivi hebdomadaire des impressions, clics, positions et pages indexées dès qu’un accès GSC automatisable est disponible.
