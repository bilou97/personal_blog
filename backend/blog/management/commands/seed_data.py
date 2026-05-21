from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Category, Tag, Post, Comment
import random
from datetime import timedelta

CATEGORIES = [
    "Développement web",
    "Intelligence artificielle",
    "DevOps & Infrastructure",
    "Sécurité informatique",
    "Open Source",
]

TAGS = [
    "Python", "JavaScript", "Vue.js", "Django", "FastAPI",
    "Docker", "PostgreSQL", "Linux", "Git", "API REST",
    "Machine Learning", "LLM", "CI/CD", "nginx", "TypeScript",
]

POSTS = [
    {
        "title": "Construire une API REST avec FastAPI et Django",
        "slug": "api-rest-fastapi-django",
        "excerpt": "FastAPI et Django peuvent coexister dans la même application. Voici comment j'ai architecturé ce blog pour tirer le meilleur des deux frameworks.",
        "content": """## Pourquoi combiner FastAPI et Django ?

Django excelle pour l'administration, l'ORM, et la gestion des migrations. FastAPI brille pour les API performantes avec validation automatique via Pydantic. Les deux ensemble, c'est le meilleur des deux mondes.

## L'architecture

L'idée centrale : Django gère les modèles et l'admin, FastAPI expose les endpoints. Le routing se fait au niveau ASGI :

```python
# config/asgi.py
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from starlette.routing import Mount

django_app = get_asgi_application()
fastapi_app = FastAPI()

application = Starlette(routes=[
    Mount("/api", app=fastapi_app),
    Mount("/", app=django_app),
])
```

## Les avantages concrets

**Validation automatique** : FastAPI génère la doc OpenAPI sans effort. Chaque endpoint est typé, les erreurs de validation sont claires.

**ORM Django** : pas besoin de SQLAlchemy. Les modèles Django fonctionnent parfaitement dans les handlers FastAPI, à condition de bien gérer le contexte Django.

**Admin gratuit** : toute la gestion du contenu via l'interface Django admin, sans coder une seule ligne de frontend admin.

## Le piège à éviter

Django n'est pas thread-safe de la même façon que FastAPI. Il faut initialiser Django avant de créer l'app FastAPI, et s'assurer que `django.setup()` est appelé exactement une fois.

```python
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()  # avant tout import de modèles
```

## Conclusion

Cette stack est plus complexe qu'un seul framework, mais elle offre une flexibilité réelle. Pour un projet personnel, c'est aussi une excellente façon d'apprendre les deux écosystèmes en profondeur.""",
        "category": "Développement web",
        "tags": ["Python", "FastAPI", "Django", "API REST"],
        "published": True,
        "days_ago": 2,
    },
    {
        "title": "Docker Compose pour le développement local : mon workflow",
        "slug": "docker-compose-dev-workflow",
        "excerpt": "Après des années à souffrir des 'ça marche sur ma machine', Docker Compose a changé ma façon de travailler. Voici mon setup actuel.",
        "content": """## Le problème classique

Chaque développeur a une version différente de Python, PostgreSQL, Node. Les `requirements.txt` divergent. Les variables d'environnement manquent. Docker Compose résout tout ça proprement.

## Ma structure de base

```yaml
services:
  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      retries: 5

  backend:
    build: ./backend
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app  # hot reload en dev
```

Le `condition: service_healthy` est crucial. Sans ça, le backend démarre avant que Postgres soit prêt, et les migrations échouent.

## Les volumes en développement

En dev, je monte le code source comme volume :

```yaml
volumes:
  - ./backend:/app
```

Le serveur Django détecte les changements et redémarre automatiquement. En production, on copie le code dans l'image au build.

## Les variables d'environnement

Un seul fichier `.env` à la racine, jamais commité :

```
DB_NAME=blog_db
DB_USER=blog_user
DB_PASSWORD=supersecret
SECRET_KEY=...
DEBUG=True
```

`docker-compose.yml` le référence avec `env_file: .env`. Simple et sécurisé.

## Commandes utiles

```bash
# Premier démarrage
docker compose up -d --build

# Voir les logs
docker compose logs -f backend

# Entrer dans le container
docker compose exec backend python manage.py shell

# Reset complet
docker compose down -v && docker compose up -d --build
```

## Ce que j'ai appris à la dure

Ne jamais mettre de données importantes dans un volume anonyme. Toujours nommer les volumes pour pouvoir les inspecter et les sauvegarder.""",
        "category": "DevOps & Infrastructure",
        "tags": ["Docker", "PostgreSQL", "Linux"],
        "published": True,
        "days_ago": 5,
    },
    {
        "title": "Vue 3 Composition API : pourquoi j'ai abandonné Options API",
        "slug": "vue3-composition-api",
        "excerpt": "La Composition API de Vue 3 change fondamentalement la façon d'organiser la logique. Après six mois d'utilisation intensive, voici mon bilan.",
        "content": """## Options API vs Composition API

Options API organise le code par *type* : data ici, methods là, computed ailleurs. Composition API organise par *fonctionnalité*. Pour les petits composants, la différence est minime. Pour les grands, c'est le jour et la nuit.

## Un exemple concret

Imaginons un composant qui gère une liste de posts avec pagination et recherche.

**Options API** : la logique de pagination est éparpillée entre `data`, `computed`, `methods` et `watch`. Pour comprendre comment fonctionne la pagination, il faut sauter entre quatre sections.

**Composition API** :

```typescript
// composables/usePagination.ts
export function usePagination(fetchFn: Function) {
  const page = ref(1)
  const total = ref(0)
  const items = ref([])

  async function load() {
    const result = await fetchFn(page.value)
    items.value = result.items
    total.value = result.total
  }

  watch(page, load)

  return { page, total, items, load }
}
```

Toute la logique de pagination dans un fichier, réutilisable dans n'importe quel composant.

## Les composables : la vraie force

Les composables remplacent les mixins avec tous leurs défauts en moins. Pas de collision de noms, source de données claire, testables unitairement.

```typescript
// Dans le composant
const { page, total, items } = usePagination(fetchPosts)
const { query, results } = useSearch(items)
```

## Ce qui m'a convaincu définitivement

TypeScript. La Composition API et TypeScript s'intègrent naturellement. L'inférence de types fonctionne sans configuration spéciale. Les Options API nécessitent des contorsions pour obtenir le même niveau de typage.

## La courbe d'apprentissage

Honnêtement, les deux premières semaines sont difficiles. `ref` vs `reactive`, `.value` partout, la réactivité qui se perd si on déstructure mal... Il faut du temps. Mais après, on ne revient pas en arrière.""",
        "category": "Développement web",
        "tags": ["Vue.js", "JavaScript", "TypeScript"],
        "published": True,
        "days_ago": 10,
    },
    {
        "title": "Les LLM en production : ce que personne ne dit",
        "slug": "llm-en-production",
        "excerpt": "Intégrer un LLM dans une application, c'est facile. Le rendre fiable, prévisible et économique en production, c'est une autre histoire.",
        "content": """## L'illusion de la démo

Tout le monde peut faire une démo impressionnante avec un LLM en 30 minutes. Le vrai travail commence après : gérer les latences, les coûts, les hallucinations, et les comportements imprévisibles.

## Le problème de la latence

Un appel à GPT-4 ou Claude prend entre 2 et 30 secondes selon la longueur de la réponse. C'est inacceptable pour une interface synchrone.

Solutions :
- **Streaming** : envoyer les tokens au fur et à mesure (UX nettement meilleure)
- **Cache** : pour les requêtes identiques ou similaires
- **Async** : traiter en arrière-plan et notifier quand c'est prêt

## Gérer les coûts

Les tokens coûtent cher à l'échelle. Quelques règles :

1. **Prompt caching** (disponible chez Anthropic) : si votre system prompt est long et statique, le cacher réduit les coûts de 90%
2. **Choisir le bon modèle** : pas besoin de Claude Opus pour classifier un email. Haiku ou Sonnet suffisent pour 80% des tâches
3. **Limiter le contexte** : n'envoyez que ce qui est nécessaire

## La fiabilité du format de sortie

"Réponds en JSON" ne suffit pas. Le LLM va parfois répondre en prose, parfois avec du markdown autour du JSON, parfois avec un JSON invalide.

Solutions :
- **Structured outputs** (OpenAI) ou **tool use** (Anthropic) pour forcer un schéma
- Toujours parser avec try/catch et avoir un fallback
- Logger les réponses inattendues pour améliorer vos prompts

## Ce que j'ai appris

Les LLM ne sont pas des fonctions déterministes. Traitez-les comme des services externes non fiables : timeout, retry avec backoff exponentiel, circuit breaker. Et testez toujours avec des cas limites.""",
        "category": "Intelligence artificielle",
        "tags": ["LLM", "Python", "API REST"],
        "published": True,
        "days_ago": 15,
    },
    {
        "title": "PostgreSQL : les index que vous n'utilisez pas assez",
        "slug": "postgresql-index-avances",
        "excerpt": "Les index B-tree sont la valeur par défaut, mais PostgreSQL en propose bien d'autres. GIN, GiST, BRIN... voici quand et pourquoi les utiliser.",
        "content": """## Au-delà du B-tree

Le B-tree est l'index universel : rapide pour l'égalité et les ranges, bien supporté. Mais il n'est pas optimal pour tous les cas.

## GIN pour la recherche full-text

```sql
-- Créer un index GIN sur un tsvector
CREATE INDEX idx_posts_search ON posts
USING GIN(to_tsvector('french', title || ' ' || content));

-- Requête
SELECT * FROM posts
WHERE to_tsvector('french', title || ' ' || content)
      @@ plainto_tsquery('french', 'docker compose');
```

GIN est parfait pour les tableaux et la recherche full-text. Beaucoup plus rapide qu'un LIKE '%terme%' qui ne peut pas utiliser d'index.

## Index partiels : indexer moins pour aller plus vite

```sql
-- Seulement les posts publiés
CREATE INDEX idx_published_posts ON posts(published_at)
WHERE published = true;
```

Si 90% de vos requêtes ne concernent que les posts publiés, pourquoi indexer les brouillons ? L'index partiel est plus petit et plus rapide.

## Index sur expressions

```sql
-- Recherche insensible à la casse sans lower() à chaque requête
CREATE INDEX idx_posts_title_lower ON posts(lower(title));

-- La requête doit utiliser la même expression
SELECT * FROM posts WHERE lower(title) = 'mon titre';
```

## BRIN pour les données temporelles

Pour les tables énormes avec des données naturellement ordonnées dans le temps (logs, événements), BRIN prend 1000x moins de place qu'un B-tree avec des performances correctes.

## Comment savoir quels index créer

```sql
-- Requêtes lentes
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Index non utilisés (candidats à la suppression)
SELECT indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

EXPLAIN ANALYZE est votre meilleur ami. Un index inutilisé ralentit les écritures sans rien apporter.""",
        "category": "Développement web",
        "tags": ["PostgreSQL", "Python"],
        "published": True,
        "days_ago": 22,
    },
    {
        "title": "Sécuriser une API Django/FastAPI : checklist pratique",
        "slug": "securiser-api-checklist",
        "excerpt": "La sécurité d'une API n'est pas une fonctionnalité qu'on ajoute à la fin. Voici ma checklist avant chaque mise en production.",
        "content": """## Authentification et autorisation

- **JWT avec expiration courte** : access token 15min, refresh token 7 jours
- **Rotation des refresh tokens** : un refresh token utilisé devient invalide
- **Vérifier les permissions à chaque endpoint**, pas seulement à la connexion

```python
@router.get("/posts/{id}")
async def get_post(id: int, current_user = Depends(get_current_user)):
    post = await get_post_or_404(id)
    if not post.published and post.author_id != current_user.id:
        raise HTTPException(403)
    return post
```

## Variables d'environnement

Jamais de secrets dans le code. Jamais dans le dépôt. Toujours dans des variables d'environnement ou un secret manager.

```python
# Mauvais
SECRET_KEY = "ma_cle_super_secrete_1234"

# Bien
SECRET_KEY = os.environ["SECRET_KEY"]  # plante si absent
```

## Rate limiting

Sans rate limiting, votre API est vulnérable au brute force et au DDoS applicatif.

```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    ...
```

## Headers de sécurité

```python
# Django middleware ou FastAPI middleware
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"
response.headers["Strict-Transport-Security"] = "max-age=31536000"
```

## CORS configuré strictement

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://monblog.ch"],  # pas de wildcard en prod
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Validation des entrées

FastAPI avec Pydantic valide automatiquement. Ne jamais bypasser cette validation. Pour Django, utiliser les serializers DRF ou des forms pour tout ce qui vient de l'extérieur.""",
        "category": "Sécurité informatique",
        "tags": ["Python", "FastAPI", "Django", "API REST"],
        "published": True,
        "days_ago": 30,
    },
    {
        "title": "Git : les commandes que j'utilise vraiment",
        "slug": "git-commandes-utiles",
        "excerpt": "Au-delà de add/commit/push, il y a une poignée de commandes Git qui changent le quotidien. Celles que j'utilise tous les jours.",
        "content": """## git stash : sauvegarder sans commiter

```bash
git stash push -m "wip: feature en cours"
git stash list
git stash pop
```

Idéal pour basculer rapidement sur une autre branche sans perdre son travail.

## git bisect : trouver le commit fautif

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checkout automatiquement des commits intermédiaires
# Tester, puis :
git bisect good  # ou bad
# Répéter jusqu'à trouver le commit fautif
git bisect reset
```

Sur un historique de 1000 commits, bisect trouve le fautif en 10 étapes maximum.

## git log avec des options utiles

```bash
# Graphe des branches
git log --oneline --graph --all

# Modifications d'un fichier spécifique
git log -p -- backend/blog/models.py

# Commits d'un auteur sur une période
git log --author="Stéphane" --since="2024-01-01"
```

## git reflog : le filet de sécurité

```bash
git reflog
# HEAD@{0}: commit: feat: add comments
# HEAD@{1}: reset: moving to HEAD~1
# HEAD@{2}: commit: wip: broken stuff
```

Tout ce que vous avez fait est dans le reflog pendant 90 jours. Vous avez fait un `reset --hard` par erreur ? `git checkout HEAD@{2}` pour récupérer vos commits.

## git worktree : plusieurs branches en parallèle

```bash
git worktree add ../blog-hotfix hotfix/security-patch
# Travaillez dans ../blog-hotfix sans toucher à votre branche principale
git worktree remove ../blog-hotfix
```

Plus besoin de stash ou de commits temporaires pour switcher de branche.""",
        "category": "DevOps & Infrastructure",
        "tags": ["Git", "Linux"],
        "published": True,
        "days_ago": 45,
    },
    {
        "title": "Pourquoi j'ai choisi de self-héberger mon blog",
        "slug": "self-heberger-son-blog",
        "excerpt": "Medium, Substack, Ghost... j'ai testé plusieurs plateformes avant de décider de tout construire et héberger moi-même. Voici pourquoi.",
        "content": """## Le problème des plateformes

Les plateformes existantes sont pratiques. Trop pratiques, peut-être. Votre contenu appartient à leur infrastructure, leurs algorithmes décident de la visibilité, et elles peuvent fermer du jour au lendemain.

## Ce que je voulais

- **Contrôle total** sur mes données
- **Pas de traqueur** tiers
- **URL stables** pour toujours
- Un projet technique pour apprendre

## Le coût réel

Une VPS basique chez Hetzner ou DigitalOcean : 5-10€/mois. Un nom de domaine : 10-15€/an. C'est moins cher que certains abonnements Substack.

## La complexité

Je ne vais pas mentir : c'est plus complexe que d'ouvrir un compte Substack. Il faut gérer :
- Les mises à jour de sécurité
- Les sauvegardes
- Le certificat SSL
- Les déploiements

Mais c'est aussi tout ce que j'apprends en faisant ça.

## Ce que j'aurais recommandé il y a 2 ans

Si vous voulez juste écrire, utilisez Ghost (self-hébergé ou leur cloud). Interface propre, markdown natif, RSS, newsletter. Pas besoin de coder.

## Ce que je recommande maintenant

Si vous êtes développeur et que vous voulez apprendre, construisez votre outil. Vous apprendrez plus en six mois de ce projet que dans des dizaines de tutoriels.""",
        "category": "Open Source",
        "tags": ["Linux", "Docker", "nginx"],
        "published": True,
        "days_ago": 60,
    },
    {
        "title": "Draft : Réflexions sur la maintenabilité du code",
        "slug": "draft-maintenabilite-code",
        "excerpt": "Notes en vrac sur ce qui rend un projet maintenable sur le long terme.",
        "content": """## Brouillon - ne pas publier encore

Idées à développer :

- La maintenabilité se mesure au temps pour ajouter une feature
- Tests comme documentation vivante
- Nommage > commentaires
- Complexité accidentelle vs essentielle

À compléter...""",
        "category": "Développement web",
        "tags": ["Git", "Python"],
        "published": False,
        "days_ago": 1,
    },
]

COMMENTS = [
    ("Très bon article, j'utilise exactement cette architecture sur mon projet perso. Une question : comment tu gères les migrations en production avec ce setup ?", "alice"),
    ("Le point sur le healthcheck PostgreSQL est crucial, j'ai perdu des heures là-dessus avant de comprendre.", "bob"),
    ("Merci pour les exemples de code, c'est toujours plus clair avec du concret. J'aurais bien aimé un peu plus de détails sur la partie déploiement.", "charlie"),
    ("Je viens de migrer de Options API à Composition API sur un projet existant, et effectivement la courbe d'apprentissage est réelle. Mais après deux semaines, impossible de revenir en arrière.", "alice"),
    ("Excellent article sur les LLM. Le point sur le structured output est souvent sous-estimé. J'utilise tool use chez Anthropic pour forcer le format JSON et c'est beaucoup plus fiable.", "david"),
    ("Le bisect Git c'est magique, j'en avais jamais entendu parler avant. Je viens de l'utiliser pour la première fois et ça m'a sauvé la mise.", "bob"),
    ("Sur le self-hébergement : j'héberge le mien sur une VPS Hetzner depuis 3 ans. La fiabilité est excellente et le support très réactif.", "charlie"),
    ("L'index partiel PostgreSQL, c'est une pépite. Je l'avais jamais utilisé et ça change vraiment les perfs sur nos tables de logs.", "david"),
]


class Command(BaseCommand):
    help = "Seed the database with test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Tag.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating users...")
        users = {}
        user_data = [
            ("alice", "alice@example.com", "Alice Martin"),
            ("bob", "bob@example.com", "Bob Dupont"),
            ("charlie", "charlie@example.com", "Charlie Leroy"),
            ("david", "david@example.com", "David Bernard"),
        ]
        for username, email, full_name in user_data:
            first, last = full_name.split(" ", 1)
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "first_name": first, "last_name": last},
            )
            users[username] = user

        self.stdout.write("Creating categories...")
        categories = {}
        for name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name)
            categories[name] = cat

        self.stdout.write("Creating tags...")
        tags = {}
        for name in TAGS:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags[name] = tag

        self.stdout.write("Creating posts...")
        posts = []
        for data in POSTS:
            post, created = Post.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "content": data["content"],
                    "excerpt": data["excerpt"],
                    "category": categories.get(data["category"]),
                    "published": data["published"],
                    "published_at": (
                        timezone.now() - timedelta(days=data["days_ago"])
                        if data["published"]
                        else None
                    ),
                },
            )
            if created:
                for tag_name in data["tags"]:
                    if tag_name in tags:
                        post.tags.add(tags[tag_name])
            if data["published"]:
                posts.append(post)

        self.stdout.write("Creating comments...")
        comment_texts = list(COMMENTS)
        random.shuffle(comment_texts)

        for i, (text, username) in enumerate(comment_texts):
            if i < len(posts):
                target_post = posts[i % len(posts)]
            else:
                target_post = random.choice(posts)

            Comment.objects.get_or_create(
                post=target_post,
                author=users[username],
                content=text,
                defaults={
                    "approved": True,
                    "created_at": target_post.published_at + timedelta(hours=random.randint(1, 72)),
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created:\n"
            f"  {len(users)} users\n"
            f"  {Category.objects.count()} categories\n"
            f"  {Tag.objects.count()} tags\n"
            f"  {Post.objects.count()} posts ({Post.objects.filter(published=True).count()} published)\n"
            f"  {Comment.objects.count()} comments"
        ))
