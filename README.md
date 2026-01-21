# RemoteControl

Service backend Django + frontend React permettant de déclencher des actions côté serveur depuis une interface web locale.

## Objectif

Ce projet a pour but de me remettre à niveau sur Django et Django REST Framework dans un contexte réaliste : exposer une API backend consommée par un frontend déclenchant des actions côté serveur.

Le périmètre est volontairement limité afin de privilégier la structure, la lisibilité et les bonnes pratiques.

## Stack technique

- Backend : Python, Django, Django REST Framework
- Frontend : React (Vite)
- Base de données : PostgreSQL (prévu)
- Conteneurisation : Docker / Docker Compose
- CI : GitHub Actions

## Fonctionnalités

- API REST permettant de démarrer / arrêter une action serveur (commande dummy)
- Consultation de l’état courant
- Interface web simple utilisable depuis un navigateur local

## Installation & setup (backend Django)

Cette section permet de lancer rapidement un environnement Django fonctionnel en local.

### 1. Créer l’environnement Python

Un environnement virtuel est utilisé pour isoler les dépendances du projet.

| Linux / macOS              | Windows (PowerShell)          |
| -------------------------- | ----------------------------- |
| `python3 -m venv venv`     | `python -m venv venv`         |
| `source venv/bin/activate` | `venv\\Scripts\\Activate.ps1` |

Le terminal doit afficher `(venv)` une fois activé.

---

### 2. Installer les dépendances

Installation des dépendances backend nécessaires.

| Linux / macOS                                          | Windows                                                |
| ------------------------------------------------------ | ------------------------------------------------------ |
| `pip install django djangorestframework python-dotenv` | `pip install django djangorestframework python-dotenv` |

Figer les dépendances :

| Linux / macOS                   | Windows                         |
| ------------------------------- | ------------------------------- |
| `pip freeze > requirements.txt` | `pip freeze > requirements.txt` |

---

### 3. Créer le projet Django

Initialisation du projet Django.

| Linux / macOS                       | Windows                             |
| ----------------------------------- | ----------------------------------- |
| `django-admin startproject backend` | `django-admin startproject backend` |
| `cd backend`                        | `cd backend`                        |

Structure obtenue :

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

### 4. Variables d’environnement

Les variables locales sont définies dans un fichier `.env` (non versionné).

Créer un fichier `.env` à la racine du dossier `backend/` :

```env
DEBUG=True
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

Ajouter `.env` au `.gitignore`.

---

### 5. Chargement du `.env`

Chargement automatique des variables d’environnement dans `settings.py`.

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

Ajout de DRF aux applications installées.

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

Application des migrations et démarrage du serveur de développement.

| Linux / macOS                | Windows                      |
| ---------------------------- | ---------------------------- |
| `python manage.py migrate`   | `python manage.py migrate`   |
| `python manage.py runserver` | `python manage.py runserver` |

Accès local :

```
http://127.0.0.1:8000/
```

Si la page Django par défaut s’affiche, le setup est validé.

---

### État attendu

- Environnement virtuel actif
- Django et DRF installés
- Variables d’environnement chargées
- Serveur fonctionnel en local
