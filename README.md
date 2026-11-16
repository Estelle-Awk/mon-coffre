# 🔐 Mon Coffre

Un gestionnaire de mots de passe simple, local et chiffré, écrit en Python.

Projet réalisé par Estelle Awk, IFRI.

## Fonctionnalités

- Stockage chiffré des mots de passe ([AES / Fernet : à préciser])
- Interface simple
- Coffre local : les données restent sur ton ordinateur
- 100 % hors ligne

## Prérequis

- Python 3.9 ou plus
- Les dépendances du projet : `pip install -r requirements.txt`

## Installation

```bash
git clone https://github.com/Estelle-Awk/mon-coffre.git
cd mon-coffre
pip install -r requirements.txt
python main.py
```

## Utilisation

1. Au premier lancement, crée ton mot de passe maître
2. Ajoute, consulte ou supprime des entrées dans ton coffre

## Sécurité

- Le mot de passe maître n'est jamais stocké en clair
- Clé dérivée avec [PBKDF2 / Argon2 : à préciser]
- Si tu oublies le mot de passe maître, les données sont irrécupérables

## Auteure

Estelle Awk, IFRI

## Licence

MIT