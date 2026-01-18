# SAE_BUT3
Navigateur de contenus vidéos


## Installation et lancement local

### Prérequis
- Python 3.8+ et pip
- Node.js 16+ et npm
- Serveur Neo4j (optionnel, pour tester en local)

### Configuration initiale

1. **Installer les dépendances** :
```bash
make install
```

Cette commande :
- Crée un environnement virtuel Python (`venv`)
- Installe les dépendances backend depuis `backend/requirements.txt`
- Installe les dépendances frontend avec npm

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
make npm run test
# ou directement
cd frontend && npm test
```

**Couverture de code (backend)** :
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

Créer un utilisateur administrateur par défaut :
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

### Serveur Neo4j en Docker (optionnel)
Pour développer en local avec Neo4j :
```bash
docker run -d -p 17474:7474 -p 17687:7687 -e NEO4J_AUTH=neo4j/testtest neo4j:latest
```

