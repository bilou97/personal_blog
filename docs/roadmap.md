# Roadmap

Fonctionnalités réalisées et à venir.

## Réalisé

- [x] Stack Vue3 / FastAPI / Django / PostgreSQL / Docker
- [x] Authentification JWT (register, login, logout automatique sur 401)
- [x] Liste des articles avec pagination et filtres catégorie/tag
- [x] Rendu Markdown (`marked` + `DOMPurify`)
- [x] Commentaires (authentifié, modération via admin)
- [x] Style Tailwind CSS v3 + plugin typography
- [x] SEO : balises meta dynamiques, Open Graph
- [x] Gestion des erreurs globale (intercepteur axios, toasts)
- [x] Tests backend — 21 tests, isolation transactionnelle
- [x] Données de test (`seed_data` management command)
- [x] Déploiement prod : nginx, Let's Encrypt, Docker Compose

---

## À venir

### Lecture & découverte

- [x] **Temps de lecture estimé** — calculé depuis le contenu, affiché dans l'article
- [x] **Articles liés** — 3 suggestions basées sur les tags/catégorie communs, affichées en bas d'article
- [x] **Recherche full-text** — endpoint `/api/search?q=` avec index GIN PostgreSQL, page de résultats côté frontend

### Contenu & écriture

- [x] **Table des matières** — générée automatiquement depuis les titres `##` du markdown, affichée en haut d'article
- [x] **Upload d'images** — interface d'upload dans l'admin avec redimensionnement automatique (Pillow)
- [x] **Planification de publication** — champ `publish_at` côté admin, tâche Celery ou cron qui publie automatiquement
- [ ] **Éditeur Markdown dans l'admin** — éditeur avec prévisualisation en temps réel (split-pane ou onglets) dans l'interface Django admin, remplace le textarea brut

### Engagement

- [x] **Réactions** — 3 emojis (👍 ❤️ 🔥) sans compte requis, stockées par article + IP/session
- [x] **Compteur de vues** — incrémenté à chaque visite d'article, affiché publiquement
- [x] **Newsletter** — inscription par email, envoi automatique à la publication d'un article (Mailpit en dev, backend SMTP configurable en prod)
- [ ] **Nombre de commentaires sur les cartes** — afficher le nombre de commentaires approuvés directement dans la liste des articles
- [ ] **Boutons de partage** — copie du lien, partage X (Twitter) et LinkedIn, en bas de chaque article
- [ ] **Article épinglé / mis en avant** — possibilité de mettre un article en valeur en haut de la home (flag `pinned` côté admin)

### Distribution

- [x] **RSS feed** — `/feed.xml` listant les derniers articles publiés
- [x] **Sitemap XML** — `/sitemap.xml` pour le SEO, mis à jour à chaque publication

### Style & UX

- [x] **Syntax highlighting** — coloration des blocs de code dans les articles (Highlight.js), avec bouton copier
- [x] **Transitions de pages** — animation fade entre les vues Vue Router
- [x] **Page 404 personnalisée** — page d'erreur stylisée avec lien de retour
- [x] **Skeleton loaders** — placeholders animés pendant le chargement des listes et articles, à la place des spinners
- [x] **Typographie affinée** — choix de polices (serif pour le contenu, sans-serif pour l'UI), line-height et tailles optimisés pour la lecture longue
- [x] **Lazy loading des images** — chargement différé avec placeholder flou (blur-up) pendant le chargement
- [x] **Animations au scroll** — apparition progressive des cartes d'articles (Intersection Observer, sans librairie lourde)
- [x] **Responsive mobile affiné** — navigation mobile (menu hamburger), lecture confortable sur petit écran
- [ ] **Section de présentation** — bloc en haut de la home décrivant le blog, les objectifs et la démarche de l'auteur
- [ ] **Sidebar contextuelle** — colonne latérale (home + articles) avec : archives par mois, champ de recherche, nuage de tags, articles populaires ; repliée sous le contenu sur mobile
- [ ] **Barre de progression de lecture** — indicateur de progression en haut de l'écran lors de la lecture d'un article

### Technique

- [x] **Cache Redis** — mise en cache des endpoints `/api/posts` et `/api/posts/{slug}`, invalidation à la publication
- [x] **Prévisualisation brouillon** — lien temporaire signé permettant de voir un article non publié
- [x] **Mode sombre** — toggle persisté dans localStorage, respecte la préférence système par défaut
- [x] **Refresh token** — renouvellement silencieux du JWT sans déconnecter l'utilisateur
- [x] **Docs API masquées en prod** — `/docs` et `/redoc` désactivés quand `DEBUG=False`
