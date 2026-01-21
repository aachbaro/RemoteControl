# RemoteControl
Service backend Django + frontend React permettant de déclencher des actions côté serveur depuis une interface web locale.

## Objectif

Ce projet a pour but de me remettre à niveau sur Django et Django REST Framework
dans un contexte réaliste : exposer une API backend consommée par un frontend,
déclenchant des actions côté serveur.

Le périmètre est volontairement limité pour privilégier la structure,
la lisibilité et les bonnes pratiques.

## Stack technique

- Backend : Python, Django, Django REST Framework
- Frontend : React (Vite)
- Base de données : PostgreSQL (prévu)
- Conteneurisation : Docker / Docker Compose
- CI : GitHub Actions (tests backend)

## Fonctionnalités

- API REST permettant de :
  - démarrer une action serveur (dummy command)
  - arrêter l’action
  - consulter l’état courant
- Interface web simple pour déclencher ces actions depuis un navigateur
- Exécution locale sur le même réseau
