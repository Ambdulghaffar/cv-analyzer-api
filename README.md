# CV Analyzer API

Backend d'analyse de CV propulsé par l'IA : matching automatique candidat/offre d'emploi, scoring pondéré, classement multi-candidats et génération de lettres de motivation.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688) ![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)

## Fonctionnalités

- **Analyse de CV par IA** : évaluation d'un CV (PDF) par rapport à une offre d'emploi avec un score pondéré et des recommandations détaillées
- **Classement multi-candidats** : comparaison de jusqu'à 10 CVs pour une même offre, triés par pertinence
- **CRUD d'offres d'emploi** : gestion complète des offres sauvegardées (réservé aux recruteurs)
- **Génération de lettres de motivation** : lettres personnalisées, multilingues, générées à partir du CV et de l'offre
- **Authentification sécurisée** : vérification des JWT Supabase via JWKS
- **Historique** : conservation des analyses et classements passés par utilisateur

## Stack technique

| Composant | Rôle |
|---|---|
| FastAPI | Framework web pour l'API REST |
| Python 3.12 | Langage principal |
| Supabase (PostgreSQL) | Base de données et authentification |
| Groq API + Llama 3.3 70B | Moteur d'analyse et de génération IA |
| pdfplumber | Extraction de texte depuis les CVs au format PDF |
| PyJWT (vérification JWKS) | Validation des tokens d'authentification |
| Docker | Conteneurisation et déploiement |

## Architecture du projet

```
app/
├── analyze/    # Analyse de CV vs offre, scoring, historique
├── rank/       # Classement multi-candidats
├── offers/     # CRUD des offres d'emploi
├── letters/    # Génération de lettres de motivation
├── core/       # Configuration transverse (auth, sécurité, clients externes)
├── config.py
├── dependencies.py
└── main.py
```

Le projet suit une organisation **feature-based** : chaque module métier (`analyze`, `rank`, `offers`, `letters`) regroupe ses propres routes, schémas et logique, plutôt que d'être dispersé par couche technique. Cela facilite la navigation et l'évolution indépendante de chaque fonctionnalité. Le dossier `core` centralise les éléments transverses partagés par l'ensemble de l'application (authentification, configuration, clients Supabase/Groq).

## Prérequis

- Python 3.12 ou supérieur
- Un projet [Supabase](https://supabase.com) configuré
- Une clé API [Groq](https://console.groq.com)

## Installation locale

1. **Cloner le dépôt**

   ```bash
   git clone <url-du-depot>
   cd cv-analyzer-api
   ```

2. **Créer et activer un environnement virtuel**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Créer le fichier `.env`** à la racine avec les variables suivantes :

   ```env
   SUPABASE_URL=
   SUPABASE_SERVICE_ROLE_KEY=
   GROQ_API_KEY=
   CORS_ORIGINS=
   ```

   Où récupérer chaque valeur :

   - **`SUPABASE_URL`** et **`SUPABASE_SERVICE_ROLE_KEY`** : dans le Dashboard Supabase de votre projet, section *Project Settings > API Keys* (utiliser la clé **`service_role`** de l'onglet *Legacy API Keys*)
   - **`GROQ_API_KEY`** : à générer gratuitement sur [console.groq.com](https://console.groq.com), section *API Keys*
   - **`CORS_ORIGINS`** : l'URL de votre frontend en local (`http://localhost:3000` par défaut)

   > **Note** : un projet Supabase doit être créé au préalable avec le schéma nécessaire (tables `analyses`, `ranking_sessions`, `job_offers`, `profiles`). La mise en place détaillée de ce schéma relève de la configuration de l'infrastructure du projet.

5. **Lancer le serveur**

   ```bash
   uvicorn app.main:app --reload
   ```

## Lancer avec Docker

Un `Dockerfile` est déjà présent à la racine du projet.

```bash
docker build -t cv-analyzer-api .
docker run --env-file .env -p 8000:8000 cv-analyzer-api
```

## Documentation de l'API

Une fois le serveur lancé, FastAPI génère automatiquement une documentation interactive Swagger accessible sur **[http://localhost:8000/docs](http://localhost:8000/docs)**.

## Approche du scoring et du prompt engineering

Le score de matching repose sur une pondération précise : compétences requises (35%), compétences souhaitées (10%), expérience (30%), formation (15%) et présentation du CV (10%). Les prompts envoyés au modèle sont construits selon des principes stricts — raisonnement structuré (chain-of-thought), garde-fous anti-hallucination, et sortie strictement au format JSON validée par des schémas Pydantic. Cette approche garantit des résultats cohérents, reproductibles et exploitables directement par l'API. Le détail complet de l'implémentation est disponible dans le code source des modules `analyze` et `rank`.

## Projets liés

Ce backend fonctionne de pair avec le frontend **cv-analyzer-web** <!-- https://github.com/ambdulghaffar/cv-analyzer-web --> et s'intègre dans un ensemble orchestré via Docker Compose au sein du dépôt **cv-analyzer-infra** <!-- https://github.com/ambdulghaffar/cv-analyzer-infra -->.

## Auteur

**Ambdulghaffar Ahamadi**

- GitHub : [github.com/ambdulghaffar](https://github.com/ambdulghaffar)
- LinkedIn : [linkedin.com/in/ambdulghaffar-ahamadi](https://www.linkedin.com/in/ambdulghaffar-ahamadi-7a476839a/)
