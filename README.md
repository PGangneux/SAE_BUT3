# SAE_BUT3
Navigateur de contenus vidéos

Monorepo contenant le service backend et le service frontend

## Installation et lancement local

### Prérequis
- Python 3.8+ et pip
- Node.js 16+ et npm
- Serveur Neo4j (optionnel, pour tester en local)

### Configuration initiale

#### 1. **Installer les dépendances** :
```bash
make install
```

Cette commande :
- Crée un environnement virtuel Python (`venv`)
- Installe les dépendances backend depuis `backend/requirements.txt`
- Installe les dépendances frontend avec npm


#### 2. **Initialiser les bases de données**
```bash
make migration
```

Cette commande :
- Initialise la base de données sqlite3 avec les configurations Django
- Initialise la base de données Neo4j en envoyant le schéma du model à la base de données (label et index)
    - supprime le précédent schéma du model (pas de gestion de migration de Django)

### Lancement de l'application

Terminal 1 - Backend (API Django) :
```bash
make run_back
```
Le serveur démarre sur `http://localhost:8000`

Terminal 2 - Frontend (Vue.js avec Vite) :
```bash
make run_front
```
Le serveur démarre sur `http://localhost:5173` (ou un autre port disponible)

### Exécuter les tests

**Tests backend** :
```bash
make tests
```

**Tests frontend** :
```bash
make tests_front
```

**Couverture des tests (backend)** :
```bash
make coverage
```

### Autres commandes utiles

Migrations Django :
```bash
make migration
```

Shell Django interactif :
```bash
make shell
```

Charger les données par défaut :
```bash
make load_bd
```

Créer un utilisateur administrateur Django par défaut :
```bash
make default_admin_user
# Username: admin, Password: admin
```

Nettoyer les fichiers temporaires :
```bash
make clean
```

## Backend - API

Création d'un fichier `.env` contenant les informations pour une connexion à une base de données Neo4j :

```
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_HOST=localhost
NEO4J_PORT=7687
```

