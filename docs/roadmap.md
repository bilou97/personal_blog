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

- [ ] **Temps de lecture estimé** — calculé depuis la longueur du contenu, affiché sur la carte et dans l'article
- [ ] **Articles liés** — 3 suggestions basées sur les tags/catégorie communs, affichées en bas d'article
- [ ] **Recherche full-text** — endpoint `/api/search?q=` avec index GIN PostgreSQL, page de résultats côté frontend

### Contenu & écriture

- [ ] **Table des matières** — générée automatiquement depuis les titres `##` du markdown, sticky sur desktop
- [ ] **Upload d'images** — interface d'upload dans l'admin avec redimensionnement automatique (Pillow)
- [ ] **Planification de publication** — champ `publish_at` côté admin, tâche Celery ou cron qui publie automatiquement

### Engagement

- [ ] **Réactions** — 3 emojis (👍 ❤️ 🔥) sans compte requis, stockées par article + IP/session
- [ ] **Compteur de vues** — incrémenté à chaque visite d'article, affiché publiquement
- [ ] **Newsletter** — inscription par email, envoi automatique à la publication d'un article

### Distribution

- [ ] **RSS feed** — `/feed.xml` listant les derniers articles publiés
- [ ] **Sitemap XML** — `/sitemap.xml` pour le SEO, mis à jour à chaque publication

### Technique

- [ ] **Cache Redis** — mise en cache des endpoints `/api/posts` et `/api/posts/{slug}`, invalidation à la publication
- [ ] **Prévisualisation brouillon** — lien temporaire signé permettant de voir un article non publié
- [ ] **Mode sombre** — toggle persisté dans localStorage, respecte la préférence système par défaut
- [ ] **Refresh token** — renouvellement silencieux du JWT sans déconnecter l'utilisateur
