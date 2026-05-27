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
- [ ] **Recherche full-text** — endpoint `/api/search?q=` avec index GIN PostgreSQL, page de résultats côté frontend

### Contenu & écriture

- [x] **Table des matières** — générée automatiquement depuis les titres `##` du markdown, affichée en haut d'article
- [ ] **Upload d'images** — interface d'upload dans l'admin avec redimensionnement automatique (Pillow)
- [ ] **Planification de publication** — champ `publish_at` côté admin, tâche Celery ou cron qui publie automatiquement

### Engagement

- [ ] **Réactions** — 3 emojis (👍 ❤️ 🔥) sans compte requis, stockées par article + IP/session
- [x] **Compteur de vues** — incrémenté à chaque visite d'article, affiché publiquement
- [ ] **Newsletter** — inscription par email, envoi automatique à la publication d'un article

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

### Technique

- [x] **Cache Redis** — mise en cache des endpoints `/api/posts` et `/api/posts/{slug}`, invalidation à la publication
- [ ] **Prévisualisation brouillon** — lien temporaire signé permettant de voir un article non publié
- [x] **Mode sombre** — toggle persisté dans localStorage, respecte la préférence système par défaut
- [x] **Refresh token** — renouvellement silencieux du JWT sans déconnecter l'utilisateur
