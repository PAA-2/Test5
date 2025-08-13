# Django Docker Starter

## Prérequis
- Docker
- Docker Compose
- Python 3.12 (pour un lancement hors Docker)

## Démarrage rapide
```bash
docker compose up --build
```
L'application est accessible sur [http://localhost:8000/](http://localhost:8000/).

## Variables d'environnement
Voir le fichier `.env.example` pour la liste complète et leurs valeurs par défaut.

## Lancer les tests et le lint
```bash
ruff check .
black --check .
pytest
```

## Structure du projet
```
manage.py
Dockerfile
docker-compose.yml
pyproject.toml
pytest.ini
config/
  settings/
  urls.py
core/
accounts/
```
