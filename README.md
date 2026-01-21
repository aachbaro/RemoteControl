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

## Persistance de l’état : remplacement de la mémoire par la base de données

Cette section remplace l’état en mémoire par un état persistant via l’ORM Django, sans modifier les routes API.

---

### 0. Pré-requis

Le serveur tourne et le terminal est positionné dans `backend/` (au niveau de `manage.py`).

---

### 1. Créer le modèle `Recording`

Définition du modèle persistant représentant l’état global.

Dans `actions/models.py` :

```python
from django.db import models


class Recording(models.Model):
    is_recording = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Recording(is_recording={self.is_recording}, started_at={self.started_at})"
```

---

### 2. Créer et appliquer les migrations

Synchronisation du modèle avec la base de données.

```bash
python manage.py makemigrations actions
python manage.py migrate
```

---

### 3. Remplacer l’état en mémoire par l’ORM

Le service devient la seule source de vérité persistante.

Remplacer entièrement `actions/services/recording.py` par :

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.utils import timezone

from actions.models import Recording


@dataclass
class RecordingState:
    is_recording: bool
    started_at: Optional[datetime]


def _get_singleton() -> Recording:
    obj, _ = Recording.objects.get_or_create(
        id=1,
        defaults={"is_recording": False, "started_at": None},
    )
    return obj


def start() -> RecordingState:
    rec = _get_singleton()
    if not rec.is_recording:
        rec.is_recording = True
        rec.started_at = timezone.now()
        rec.save(update_fields=["is_recording", "started_at", "updated_at"])
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)


def stop() -> RecordingState:
    rec = _get_singleton()
    rec.is_recording = False
    rec.started_at = None
    rec.save(update_fields=["is_recording", "started_at", "updated_at"])
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)


def status() -> RecordingState:
    rec = _get_singleton()
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)
```

---

### 4. Vérifier les vues existantes

Les vues ne changent pas si elles consomment `RecordingState`.

---

### 5. Tester la persistance

Vérification du statut.

| Linux / macOS                                   | Windows (PowerShell)                                |
| ----------------------------------------------- | --------------------------------------------------- |
| `curl http://127.0.0.1:8000/api/record/status/` | `curl.exe http://127.0.0.1:8000/api/record/status/` |

Démarrage de l’action.

| Linux / macOS                                          | Windows (PowerShell)                                       |
| ------------------------------------------------------ | ---------------------------------------------------------- |
| `curl -X POST http://127.0.0.1:8000/api/record/start/` | `curl.exe -X POST http://127.0.0.1:8000/api/record/start/` |

Redémarrage du serveur.

```bash
python manage.py runserver
```

Relecture du statut après redémarrage.

---

### 6. Validation via le shell Django (optionnel)

Inspection directe de la base de données.

```bash
python manage.py shell
```

```python
from actions.models import Recording
Recording.objects.all()
Recording.objects.get(id=1).is_recording
```

---

### État attendu

- Les endpoints fonctionnent sans changement
- L’état persiste après redémarrage du serveur
- La logique reste centralisée dans `services/`
- Les vues restent fines et déclaratives

## Sérialisation DRF : produire le JSON via un serializer

Cette section remplace le JSON “fait à la main” par un serializer DRF, sans changer les routes ni le format de réponse.

---

### 0. Point de départ

Le modèle `Recording` est en base, le service renvoie `RecordingState`, et les vues renvoient encore un dictionnaire.

---

### 1. Créer un serializer DRF

Définition explicite du contrat JSON et sérialisation automatique des datetimes.

Créer `actions/serializers.py` :

```python
from rest_framework import serializers


class RecordingStateSerializer(serializers.Serializer):
    is_recording = serializers.BooleanField()
    started_at = serializers.DateTimeField(allow_null=True)
```

---

### 2. Utiliser le serializer dans les vues

Les vues renvoient désormais `RecordingStateSerializer(state).data`.

Dans `actions/views.py` :

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RecordingStateSerializer
from .services import recording


@api_view(["POST"])
def record_start(request):
    state = recording.start()
    data = RecordingStateSerializer(state).data
    return Response(data)


@api_view(["POST"])
def record_stop(request):
    state = recording.stop()
    data = RecordingStateSerializer(state).data
    return Response(data)


@api_view(["GET"])
def record_status(request):
    state = recording.status()
    data = RecordingStateSerializer(state).data
    return Response(data)
```

---

### 3. (Optionnel) Factoriser la sérialisation

Réduire la répétition sans changer la logique.

```python
def _serialize_state(state):
    return RecordingStateSerializer(state).data
```

---

### 4. Tester que le JSON reste identique

Vérification du status.

| Linux / macOS                                   | Windows (PowerShell)                                |
| ----------------------------------------------- | --------------------------------------------------- |
| `curl http://127.0.0.1:8000/api/record/status/` | `curl.exe http://127.0.0.1:8000/api/record/status/` |

Réponse attendue.

```json
{ "is_recording": false, "started_at": null }
```

Start / Stop.

| Linux / macOS                                          | Windows (PowerShell)                                       |
| ------------------------------------------------------ | ---------------------------------------------------------- |
| `curl -X POST http://127.0.0.1:8000/api/record/start/` | `curl.exe -X POST http://127.0.0.1:8000/api/record/start/` |
| `curl -X POST http://127.0.0.1:8000/api/record/stop/`  | `curl.exe -X POST http://127.0.0.1:8000/api/record/stop/`  |

---

### 5. Objectif technique

Le serializer standardise le format datetime et centralise le contrat de réponse.

---

### État attendu

- Même API et mêmes routes
- Même JSON (clés + format)
- Réponse produite via DRF serializer

## Séparation logique métier / API (architecture claire)

Cette étape formalise une structure que tu as déjà commencée, afin que Django devienne un adaptateur HTTP autour de ton code métier.

---

### Où on en est dans l’apprentissage

À ce stade, tu as déjà mis en place :

- Routage et vues DRF
- Endpoints avec état (`start / stop / status`)
- Persistance via l’ORM Django
- Sérialisation via DRF

La suite logique est d’organiser le code pour éviter le mélange HTTP, logique métier et accès base de données.

---

### Objectif architectural

Obtenir une chaîne claire et stable.

```text
HTTP (views) → service (use-cases) → repository (DB) → modèle (ORM)
```

Les endpoints restent identiques.

---

### 1. Créer les couches du domaine `actions/`

Découpage explicite des responsabilités.

```bash
mkdir -p actions/api actions/repositories actions/services
touch actions/api/__init__.py actions/repositories/__init__.py actions/services/__init__.py
```

---

### 2. Déplacer le serializer dans la couche API

Le serializer appartient à la frontière HTTP.

Créer `actions/api/serializers.py` :

```python
from rest_framework import serializers


class RecordingStateSerializer(serializers.Serializer):
    is_recording = serializers.BooleanField()
    started_at = serializers.DateTimeField(allow_null=True)
```

---

### 3. Créer un repository pour l’accès base de données

L’ORM est isolé dans une seule couche.

Créer `actions/repositories/recording_repo.py` :

```python
from actions.models import Recording


def get_singleton() -> Recording:
    obj, _ = Recording.objects.get_or_create(
        id=1,
        defaults={"is_recording": False, "started_at": None},
    )
    return obj


def save(rec: Recording, *, update_fields=None) -> None:
    if update_fields:
        rec.save(update_fields=update_fields)
    else:
        rec.save()
```

---

### 4. Centraliser la logique métier dans un service

Les cas d’usage ne dépendent ni de HTTP ni directement des vues.

Créer `actions/services/recording_service.py` :

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.utils import timezone

from actions.repositories import recording_repo


@dataclass
class RecordingState:
    is_recording: bool
    started_at: Optional[datetime]


def start() -> RecordingState:
    rec = recording_repo.get_singleton()
    if not rec.is_recording:
        rec.is_recording = True
        rec.started_at = timezone.now()
        recording_repo.save(rec, update_fields=["is_recording", "started_at", "updated_at"])
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)


def stop() -> RecordingState:
    rec = recording_repo.get_singleton()
    rec.is_recording = False
    rec.started_at = None
    recording_repo.save(rec, update_fields=["is_recording", "started_at", "updated_at"])
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)


def status() -> RecordingState:
    rec = recording_repo.get_singleton()
    return RecordingState(is_recording=rec.is_recording, started_at=rec.started_at)
```

---

### 5. Déplacer les vues dans la couche API

Les vues deviennent une simple orchestration HTTP.

Créer `actions/api/views.py` :

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from actions.api.serializers import RecordingStateSerializer
from actions.services import recording_service


@api_view(["POST"])
def record_start(request):
    state = recording_service.start()
    return Response(RecordingStateSerializer(state).data)


@api_view(["POST"])
def record_stop(request):
    state = recording_service.stop()
    return Response(RecordingStateSerializer(state).data)


@api_view(["GET"])
def record_status(request):
    state = recording_service.status()
    return Response(RecordingStateSerializer(state).data)
```

---

### 6. Adapter le routage vers les nouvelles vues

Les routes pointent vers la couche API.

Dans `actions/urls.py` :

```python
from django.urls import path
from actions.api.views import record_start, record_stop, record_status
from actions.views import ping

urlpatterns = [
    path("ping/", ping),
    path("record/start/", record_start),
    path("record/stop/", record_stop),
    path("record/status/", record_status),
]
```

---

### 7. Vérifier que l’API n’a pas changé

Relancer le serveur et tester `start / stop / status`.

---

### État attendu

- Vues limitées à la couche HTTP
- Logique métier centralisée dans `services/`
- Accès base isolé dans `repositories/`
- API et JSON inchangés

Cette structure rend les tests, les évolutions et les changements de stack beaucoup plus simples.

## Tests backend minimalistes (DRF)

Cette section ajoute quelques tests ciblés pour valider que l’API fonctionne et que l’état évolue correctement.

---

### 0. Pré-requis

`rest_framework` est présent dans `INSTALLED_APPS`.

---

### 1. Créer une structure de tests dédiée

Organisation des tests par fichiers plutôt qu’un `tests.py` monolithique.

```bash
mkdir -p actions/tests
touch actions/tests/__init__.py
touch actions/tests/test_recording_api.py
```

---

### 2. Écrire 3 tests essentiels (status / start / stop)

Validation du routage, des méthodes HTTP, de l’évolution de l’état et du contrat JSON.

Dans `actions/tests/test_recording_api.py` :

```python
from django.test import TestCase
from rest_framework.test import APIClient


class RecordingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_status_default_is_false(self):
        r = self.client.get("/api/record/status/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["is_recording"], False)
        self.assertIsNone(r.json()["started_at"])

    def test_start_sets_is_recording_true(self):
        r = self.client.post("/api/record/start/", format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["is_recording"], True)
        self.assertIsNotNone(r.json()["started_at"])

    def test_stop_sets_is_recording_false(self):
        self.client.post("/api/record/start/", format="json")
        r = self.client.post("/api/record/stop/", format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["is_recording"], False)
        self.assertIsNone(r.json()["started_at"])
```

---

### 3. Comprendre l’isolation des tests

`TestCase` utilise une base de test temporaire, applique les migrations, puis supprime tout à la fin.

---

### 4. Lancer les tests

Exécution de tous les tests.

```bash
python manage.py test
```

Exécution des tests de l’app.

```bash
python manage.py test actions
```

---

### 5. Test `ping` (optionnel)

Validation rapide que l’API est accessible.

Créer `actions/tests/test_ping.py` :

```python
from django.test import TestCase
from rest_framework.test import APIClient


class PingTests(TestCase):
    def test_ping(self):
        client = APIClient()
        r = client.get("/api/ping/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ok")
```

---

### 6. Tester le service sans HTTP (optionnel)

Validation de la logique métier indépendamment de la couche API.

Créer `actions/tests/test_recording_service.py` :

```python
from django.test import TestCase
from actions.services import recording_service


class RecordingServiceTests(TestCase):
    def test_start_stop(self):
        s1 = recording_service.status()
        self.assertFalse(s1.is_recording)

        s2 = recording_service.start()
        self.assertTrue(s2.is_recording)
        self.assertIsNotNone(s2.started_at)

        s3 = recording_service.stop()
        self.assertFalse(s3.is_recording)
        self.assertIsNone(s3.started_at)
```

---

### État attendu

- `python manage.py test` passe
- 3 à 5 tests maximum, mais couvrant l’essentiel
- Base solide pour une CI GitHub Actions
