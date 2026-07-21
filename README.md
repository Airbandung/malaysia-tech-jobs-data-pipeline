# Datapipeline CSJOBS Malaysia

A data pipeline to ingest, transform, normalize, and analyze job listings focused on computer science related field jobs in Malaysia. The project provides tools to load raw job data, resolve and normalize locations against Malaysian administrative boundaries, extract skills and roles, and produce analytics summaries.

## Table of contents
- [Features](#features)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Testing](#testing)
- [Project structure](#project-structure)
- [Database & data](#database--data)
- [Development notes](#development-notes)
- [Contributing](#contributing)
- [License](#license)

## Features
✅ Ingest job listings from CSV / Kaggle sources
✅ Load Malaysian GeoJSON administrative boundaries
✅ Normalize free-text location strings to canonical geo records (`geo_id`)
✅ Extract and classify skills and roles from job descriptions
🚧 Analytics layer
🚧 REST API
🚧 Interactive Malaysia map

## Architecture
This project uses the medallion architecture as the foundation for flow of the ETL. 

```Project Architecture(High Level)

Kaggle Dataset
      │
      ▼
Extraction
      │
      ▼
raw_jobs
      │
      ▼
Transformation
      │
      ├── companies
      ├── locations
      └── jobs
             │
             ├── skills
             └── job roles
                    │
                    ▼
                Analytics
```

## Technology Stack
```mermaid
| Category        | Technology                 |
| --------------- | -------------------------- |
| Language        | Python                     |
| Database        | PostgreSQL                 |
| Spatial Data    | PostGIS                    |
| Containers      | Docker                     |
| Version Control | Git                        |
| Data Processing | Pandas                     |
| Environment     | Virtual Environment (venv) |
```


## Quickstart
Prerequisites
- Python 3.8+ (3.10 recommended)
- pip
- PostgreSQL (optional for DB-backed workflows)

Install dependencies
```bash
python -m pip install -r requirement.txt
```

Environment
- Copy `.env` (if present) and set DB credentials and other variables used by `main.py`.

Run the pipeline (example)
```bash
python main.py
```

## Usage
- Ingestion: `ingestion/load_raw_jobs.py`, `ingestion/load_geo_boundaries.py`
- Transformation and normalization: `transformation/transform_jobs.py`, `transformation/location_resolver.py`
- Enrichment: `enrichment/skill_extractor.py`, `enrichment/role_classifier.py`
- Analytics: `analytics/state_summary.py`

## Testing
Run unit tests with pytest from the project root:
```bash
pytest -q
```
Target a single test module:
```bash
pytest -q pipeline/test_location_resolver.py
```

## Project structure
Top-level layout (key folders):

```
pipeline/
├── ingestion/            # data loaders and source adapters
├── transformation/       # normalization, mapping, and transformers
│   ├── location_resolver.py
│   ├── location_normalizer.py
│   └── malaysia_location.py
├── enrichment/           # skill extraction & role classification
├── database/             # DB connection helpers
├── analytics/            # reporting and aggregation
├── utils/                # logging, helpers
├── main.py               # pipeline entrypoint / orchestrator
├── requirement.txt       # python dependencies
└── tests/                # unit tests (test_*.py)
```

## Database & data
- The transformation code expects a `malaysia_geo_reference` table and a `location_aliases` table when using DB-backed lookups. See `database/connection.py` for connection helpers.
- GeoJSON boundary files are included under `data/geo/mys_admin_boundaries/`.

## Development notes & gotchas
- Watch for regular expression escapes inside multi-line SQL strings (e.g. use `\\s` or raw strings to avoid Python "unsupported escape sequence" warnings).
- `location_resolver.py` performs multiple lookup strategies (exact name, alias table, state parsing, comma-format). Unit tests exercise expected behaviors.

## Contributing
1. Fork the repo and create a branch
2. Add tests for new behavior
3. Open a PR with a clear description

## Project Background
This project was developed as a personal learning project to strengthen practical data engineering skills and apply concepts learned through coursework and self-study.


## License
MIT

---
If you'd like, I can also open or run the test suite and fix any failing tests next.
