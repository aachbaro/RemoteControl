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

## État attendu

- Environnement virtuel actif
- Dépendances installées
- Variables d’environnement chargées
- Serveur Django accessible en local
