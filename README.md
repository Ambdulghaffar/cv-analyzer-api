# CV Analyzer API

AI-powered CV analysis backend: automatic candidate/job matching, weighted scoring, multi-candidate ranking, and cover letter generation.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688) ![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)

## Features

- **AI-powered CV analysis**: evaluation of a CV (PDF) against a job offer with a weighted score and detailed recommendations
- **Multi-candidate ranking**: comparison of up to 10 CVs for a single job offer, sorted by relevance
- **Job offer CRUD**: full management of saved job offers (restricted to recruiters)
- **Cover letter generation**: personalized, multilingual cover letters generated from the CV and the job offer
- **Secure authentication**: Supabase JWT verification via JWKS
- **History**: persistence of past analyses and rankings per user

## Tech Stack

| Component | Role |
|---|---|
| FastAPI | Web framework for the REST API |
| Python 3.12 | Main language |
| Supabase (PostgreSQL) | Database and authentication |
| Groq API + Llama 3.3 70B | AI analysis and generation engine |
| pdfplumber | Text extraction from CVs in PDF format |
| PyJWT (JWKS verification) | Authentication token validation |
| Docker | Containerization and deployment |

## Project Architecture

```
app/
├── analyze/    # CV vs. offer analysis, scoring, history
├── rank/       # Multi-candidate ranking
├── offers/     # Job offer CRUD
├── letters/    # Cover letter generation
├── core/       # Cross-cutting configuration (auth, security, external clients)
├── config.py
├── dependencies.py
└── main.py
```

The project follows a **feature-based** organization: each business module (`analyze`, `rank`, `offers`, `letters`) groups its own routes, schemas, and logic, rather than being scattered across technical layers. This makes it easier to navigate and evolve each feature independently. The `core` folder centralizes cross-cutting concerns shared across the whole application (authentication, configuration, Supabase/Groq clients).

## Prerequisites

- Python 3.12 or higher
- A configured [Supabase](https://supabase.com) project
- A [Groq](https://console.groq.com) API key

## Local Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd cv-analyzer-api
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create the `.env` file** at the root with the following variables:

   ```env
   SUPABASE_URL=
   SUPABASE_SERVICE_ROLE_KEY=
   GROQ_API_KEY=
   CORS_ORIGINS=
   ```

   Where to get each value:

   - **`SUPABASE_URL`** and **`SUPABASE_SERVICE_ROLE_KEY`**: available in your project's Supabase Dashboard, under *Project Settings > API Keys* (use the **`service_role`** key from the *Legacy API Keys* tab)
   - **`GROQ_API_KEY`**: generate it for free at [console.groq.com](https://console.groq.com), under *API Keys*
   - **`CORS_ORIGINS`**: the URL of your local frontend (`http://localhost:3000` by default)

   > **Note**: a Supabase project must be set up beforehand with the required schema (tables `analyses`, `ranking_sessions`, `job_offers`, `profiles`). The detailed setup of this schema is part of the project's infrastructure configuration.

5. **Start the server**

   ```bash
   uvicorn app.main:app --reload
   ```

## Running with Docker

A `Dockerfile` is already present at the root of the project.

```bash
docker build -t cv-analyzer-api .
docker run --env-file .env -p 8000:8000 cv-analyzer-api
```

## API Documentation

Once the server is running, FastAPI automatically generates interactive Swagger documentation available at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

## Scoring and Prompt Engineering Approach

The matching score is based on a precise weighting: required skills (35%), desired skills (10%), experience (30%), education (15%), and CV presentation (10%). The prompts sent to the model are built following strict principles — structured reasoning (chain-of-thought), anti-hallucination safeguards, and strictly structured JSON output validated by Pydantic schemas. This approach ensures consistent, reproducible results that are directly usable by the API. The full implementation details are available in the source code of the `analyze` and `rank` modules.

## Related Projects

This backend works together with the **cv-analyzer-web** frontend <!-- https://github.com/ambdulghaffar/cv-analyzer-web --> and is part of a suite orchestrated via Docker Compose in the **cv-analyzer-infra** repository <!-- https://github.com/ambdulghaffar/cv-analyzer-infra -->.

## Author

**Ambdulghaffar Ahamadi**

- GitHub: [github.com/ambdulghaffar](https://github.com/ambdulghaffar)
- LinkedIn: [linkedin.com/in/ambdulghaffar-ahamadi](https://www.linkedin.com/in/ambdulghaffar-ahamadi-7a476839a/)
