# SAE BUT3 - Service api

Service api de l'application

- Installation et lancement local
- Commandes utiles
- Déploiement
- Développement
- TODO

## Installation et lancement local

L'ensemble des instructions se trouvent dans le README du projet

### Prérequis
- Python 3.8+ et pip
- Serveur Neo4j (optionnel, pour tester en local)

### Configuration du service et dépendances

L'ensemble des commandes sont utilisables depuis le répertoire racine

#### Variables d'environnements

Un fichier **.env** à la racine du projet avec les paramètres de connexion à la base de données.

    NEO4J_USER=neo4j
    NEO4J_PASSWORD=your_password
    NEO4J_HOST=localhost
    NEO4J_PORT=7687

Ne pas versionner ni utiliser en production, utiliser des variables d'environnements à la place


#### Installer les dépendances

```bash
make install
```

Installe les dépendances du backend dans un environnement virtuel Python (`venv`)

Installe les dépendance frontend avec npm dans `frontend/node_modules`

#### Initialiser les bases de données


```bash
make migration
```

Initialise la base de données sqlite3 avec les configurations Django.

Initialise la base de données Neo4j en envoyant le schéma du model à la base de données (label et index). Supprime le précédent schéma du model (pas de gestion de migration de Django).

### Lancement du service

```bash
make run_back
```
Le serveur démarre sur `http://localhost:8000`

## Commandes utiles


### Exécuter les tests
```bash
make tests
```

Nécessite un serveur Neo4j local sur le port 17687 (à changer pour plus modulaire avec des variables d'environnement) 

### Taux de couverture des tests
```bash
make coverage
```

### Mise à jour des bases de données
```bash
make migration
```

### Shell Django interactif
```bash
make shell
```

### Charger les données par défaut (ne pas utiliser en production)
```bash
make load_bd
# Compte admin (pseudo: Test Admin, password: adminmdp)
# Compte utilisateur (pseudo: Test Utilisateur, password: testmdp)
```

### Créer un utilisateur administrateur (Neo4j / frontend)
```bash
make neo4j_create_admin pseudo=<pseudo> password=<password> email=<email>
```

### Créer un utilisateur administrateur Django par défaut (pas Neo4j / frontend)
```bash
make default_admin_user
# Username: admin, Password: admin
```

## Déploiement

Encore en mode développement.

Dockerfile (`backend/dockerfile`) complet.

Nécessite d'externaliser des variables d'environnements du fichier `backend/backend/settings.py` et en générer de nouvelles (voir TODO settings.py).

Configurer le service en mode production, autoriser l'accès au service pour le frontend (voir TODO settings.py).

## Développement

### Dépendences

Pour développer l'api, on utilise neomodel pour gérer la connexion avec la base de données et la gestion des données du model et Django REST Framework pour créer les serializers et les vues de l'api. On utilise également divers extentions de ce dernier module pour le compléter.

Pour plus d'informations, regarder les dépendences (`backend/requierements.txt`).

### Modèle

Pour ajouter et modifier des nodes du modèle, les ajouter dans le fichier `backend/API/models.py`.

### Serializers

Pour ajouter et modifier des serializers, utiliser les classes créer dans le module `base` dans le répertoire `backend/API/serializers`.

**BaseSerializer** : Pour créer des serializers de nodes du modèle.

**BaseRelationShipSerializer** : Pour créer des serializers de relationship du modèle.

Pour plus d'informations, regarder la documentation du code.

### Vues

Pour ajouter et modifier des vues, utiliser les classes créer dans le module `base` dans le répertoire `backend/API/views`.

**BaseGenericViewSet** : Classe générique contenant les méthodes générales des vues du projet.

**BaseModelViewSet** : Pour créer des vues sur les nodes du modèle.

**SubBaseModelViewSet** : Pour créer des vues sur les nodes du modèle dépendant d'une relation avec un autre node.

**BaseRelationShipViewSet** : Pour créer des vues sur les relationships du modèles.

### Tests

Dans le répertoire tests, sont répartis les tests en plusieurs modules en fonctions des modules testés. Les tests ne couvrent pas l'ensemble du code mais la majorité des fonctionnalités et notamment les plus critiques ont été testé.

Afin d'avoir des tests fonctionnels avec une base de données Neo4j, nous avons un runner custom (`backend/backend/runner.py`) et une classe de test custom (`backend/API/tests/__init__.py` ) dont hérite la majorité des classes de tests, remplaçant la classe de test par défaut de Django.

## TODO

Liste des choses restantes à faire.

- Mise à jour des tests (coverage -> 100%)
- Mettre à jour la cardinalité de certaines relationship de manière cohérente (code serializer présent, update model, import csv et frontend)
- Supprimer les tags, les occasions et les audios quand connecter à aucun autres nodes (lors d'un deconnexion à d'autres nodes)
- Noms des classes et propriétés du modèle (et autres) dans des langues différentes, unifier les langues
- Champ email Utilisateur actuellement StringProperty -> EmailProperty (si possible, possiblement bugger, problème de neomodel)
- Mettre à jour la gestion des variables d'environnements (SECRET_KEY, DEBUG, connexion database production et tests) et hôtes autorisés (ALLOWED_HOSTS), CORS (CORS_ALLOWED_ORIGINS), etc...
