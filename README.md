# RemoteControl

Backend Django + frontend React permettant de déclencher des actions serveur depuis une interface web locale.

## Objectif

Se remettre à niveau sur Django et Django REST Framework via une API consommée par un frontend local.

## Stack technique

- Backend : Python, Django, Django REST Framework
- Frontend : React (Vite)
- Base de données : PostgreSQL (prévu)
- Conteneurisation : Docker / Docker Compose
- CI : GitHub Actions

## Fonctionnalités

- Démarrage / arrêt d’une action serveur (commande dummy)
- Consultation de l’état courant
- Interface web locale simple

## Installation & setup (backend Django)

### 1. Créer l’environnement Python

Isolation des dépendances backend.

| Linux / macOS              | Windows (PowerShell)          |
| -------------------------- | ----------------------------- |
| `python3 -m venv venv`     | `python -m venv venv`         |
| `source venv/bin/activate` | `venv\\Scripts\\Activate.ps1` |

---

### 2. Installer les dépendances

Installation des dépendances backend.

```bash
pip install django djangorestframework python-dotenv
```

Génération du fichier de dépendances.

```bash
pip freeze > requirements.txt
```

---

### 3. Créer le projet Django

Initialisation du projet Django.

```bash
django-admin startproject backend
cd backend
```

Structure obtenue.

```text
backend/
├── manage.py
├── backend/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
```

---

### 4. Définir les variables d’environnement

Configuration locale via un fichier `.env`.

```env
DEBUG=True
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

Ajouter `.env` au `.gitignore`.

---

### 5. Charger le fichier `.env`

Chargement automatique des variables dans `settings.py`.

```python
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
```

---

### 6. Activer Django REST Framework

Ajout de DRF dans les applications installées.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
]
```

---

### 7. Lancer le serveur

Application des migrations et démarrage du serveur.

```bash
python manage.py migrate
python manage.py runserver
```

Accès local.

```text
http://127.0.0.1:8000/
```

---

### État attendu

- Environnement virtuel actif
- Dépendances installées
- Variables d’environnement chargées
- Serveur Django accessible en local

## Premier endpoint API : `/api/ping`

Cette section décrit la création d’un premier endpoint minimal afin de comprendre le chemin complet d’une requête HTTP dans Django.

---

### 1. Créer une app métier

Une app Django regroupe un domaine fonctionnel cohérent (routes, logique, tests).

```bash
python manage.py startapp actions
```

L’app est créée au même niveau que `manage.py`.

---

### 2. Déclarer l’app dans le projet

Django doit explicitement savoir que l’app fait partie du projet.

Dans `backend/settings.py`, ajouter :

```python
'actions',
```

dans la liste `INSTALLED_APPS`.

---

### 3. Créer une vue API minimale

Une vue est une fonction appelée lorsqu’une requête HTTP correspondante est reçue.

Dans `actions/views.py` :

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def ping(request):
    return Response({"status": "ok"})
```

Cette vue sert de gabarit pour tous les futurs endpoints API.

---

### 4. Définir les routes de l’app

Chaque app gère ses propres routes HTTP.

Créer le fichier `actions/urls.py` :

```python
from django.urls import path
from .views import ping

urlpatterns = [
    path("ping/", ping),
]
```

---

### 5. Exposer les routes de l’app

Le projet Django délègue une partie de l’URL globale à l’app.

Dans `backend/urls.py` :

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("actions.urls")),
]
```

Le routage final devient :

```text
/api/ping → actions.views.ping
```

---

### 6. Tester l’endpoint

Démarrer le serveur si nécessaire :

```bash
python manage.py runserver
```

Accéder à l’endpoint :

```text
http://127.0.0.1:8000/api/ping
```

Réponse attendue :

```json
{ "status": "ok" }
```

---

### Objectif pédagogique

Cet endpoint minimal sert de référence pour comprendre et reproduire le flux suivant :

```text
Requête HTTP → urls du projet → urls de l’app → vue → réponse JSON
```

Toutes les futures routes API (start, stop, status, etc.) suivent exactement ce même schéma.
