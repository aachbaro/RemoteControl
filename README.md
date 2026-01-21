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

## Sommaire

Ordre strict pour comprendre Django de bout en bout sans sauter d’étapes.

1. **Endpoint minimal**
   Comprendre le flux complet requête HTTP → réponse JSON.

2. **Endpoint avec état en mémoire**
   Introduire un backend stateful et séparer vue et logique métier.

3. **Introduction au modèle (base de données)**
   Persister l’état avec l’ORM Django et comprendre le cycle de vie des données.

4. **Sérialisation avec Django REST Framework**
   Exposer des modèles proprement via des serializers.

5. **Séparation logique métier / API**
   Structurer le code avec des services indépendants des vues.

6. **Tests backend minimalistes**
   Valider les endpoints critiques avec quelques tests ciblés.

7. **Configuration production-like**
   Approcher des conditions réelles avec une config propre et sécurisée.

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

## Endpoints avec état : `start / stop / status`

Cette section ajoute des endpoints permettant de gérer un état serveur en mémoire, sans base de données.

---

### 1. Créer une logique métier séparée

La logique métier est isolée dans un service Python, indépendant des vues HTTP.

```bash
mkdir -p actions/services
touch actions/services/__init__.py
touch actions/services/recording.py
```

Dans `actions/services/recording.py` :

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RecordingState:
    is_recording: bool = False
    started_at: Optional[datetime] = None


_state = RecordingState()


def start() -> RecordingState:
    if not _state.is_recording:
        _state.is_recording = True
        _state.started_at = datetime.utcnow()
    return _state


def stop() -> RecordingState:
    _state.is_recording = False
    _state.started_at = None
    return _state


def status() -> RecordingState:
    return _state
```

---

### 2. Exposer la logique via des vues API

Les vues appellent le service et renvoient une réponse JSON.

Dans `actions/views.py` :

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import recording


@api_view(["POST"])
def record_start(request):
    state = recording.start()
    return Response({
        "is_recording": state.is_recording,
        "started_at": state.started_at.isoformat() if state.started_at else None,
    })


@api_view(["POST"])
def record_stop(request):
    state = recording.stop()
    return Response({
        "is_recording": state.is_recording,
        "started_at": None,
    })


@api_view(["GET"])
def record_status(request):
    state = recording.status()
    return Response({
        "is_recording": state.is_recording,
        "started_at": state.started_at.isoformat() if state.started_at else None,
    })
```

---

### 3. Définir les routes de l’app

Ajout des routes associées aux nouvelles actions.

Dans `actions/urls.py` :

```python
from django.urls import path
from .views import record_start, record_stop, record_status

urlpatterns += [
    path("record/start/", record_start),
    path("record/stop/", record_stop),
    path("record/status/", record_status),
]
```

---

### 4. Tester les endpoints

Démarrer le serveur si nécessaire :

```bash
python manage.py runserver
```

#### Tester l’état courant

| Linux / macOS                                   | Windows (PowerShell)                                |
| ----------------------------------------------- | --------------------------------------------------- |
| `curl http://127.0.0.1:8000/api/record/status/` | `curl.exe http://127.0.0.1:8000/api/record/status/` |

---

#### Démarrer l’action

| Linux / macOS                                          | Windows (PowerShell)                                       |
| ------------------------------------------------------ | ---------------------------------------------------------- |
| `curl -X POST http://127.0.0.1:8000/api/record/start/` | `curl.exe -X POST http://127.0.0.1:8000/api/record/start/` |

---

#### Arrêter l’action

| Linux / macOS                                         | Windows (PowerShell)                                      |
| ----------------------------------------------------- | --------------------------------------------------------- |
| `curl -X POST http://127.0.0.1:8000/api/record/stop/` | `curl.exe -X POST http://127.0.0.1:8000/api/record/stop/` |

---

### État attendu

- Les endpoints `start / stop / status` répondent correctement
- L’état est conservé en mémoire tant que le serveur tourne
- La logique métier est séparée des vues HTTP

---

### Objectif pédagogique

Cette étape permet de comprendre :

```text
HTTP → vue DRF → service Python → état en mémoire → réponse JSON
```

Ce modèle sert de base avant l’introduction d’une base de données ou d’un frontend.
