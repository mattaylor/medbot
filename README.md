# MedBot

An AI system that reasons about treatment options using a **Clinical Trials Knowledge Graph (CTKG)** and **Patient Records**, powered by **FalkorDB** and **LLMs**.

## Features

- **Clinical Trials Knowledge Graph**: Downloads and parses data from ClinicalTrials.gov into a graph structure.
- **Patient Record Integration**: Parses FHIR patient records and links them to clinical trial data.
- **Natural Language Interface**: Ask questions via a Web UI or Discord Bot.
- **RAG & Reasoning**: Mocked implementation of Retrieval-Augmented Generation for treatment analysis.
- **Graph Updates**: Supports updating patient records with outcomes (e.g., PHQ9 scores, adverse events).

## Prerequisites

- Python 3.8+
- Node.js 18+
- FalkorDB (Docker container or local installation)

## Installation

### 1. Clone & Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Frontend

```bash
cd frontend
npm install
```

### 3. Setup Discord Bot (Optional)

Create a `.env` file in `discord-bot/`:

```bash
cp discord-bot/.env.example discord-bot/.env
# Edit .env and add your DISCORD_TOKEN
```

## Usage

### 1. Generate & Import Data

First, download clinical trials data and generate CSV files for FalkorDB:

```bash
# Download sample data
python3 backend/ctkg/downloader.py

# Generate CTKG import files
python3 -m backend.ctkg.importer

# Generate Patient import files
python3 -m backend.patient.importer
```

This will create CSV files in `data/ctkg/import` and `data/patient/import`. You can load these into FalkorDB using the `falkordb-bulk-loader`.

### 2. Run the API Server

Start the backend API (runs on port 8001):

```bash
python3 -m backend.api.server
```

### 3. Run the Web Interface

Start the Next.js frontend:

```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` to interact with the agent.

### 4. Run the Discord Bot

```bash
python3 discord-bot/bot.py
```

## API Endpoints

- **POST** `/query`
  - Body: `{"text": "your question", "patient_id": "optional_id"}`
  - Response: Agent's reasoning and answer.
- **POST** `/patient/{id}/update`
  - Body: `{"data": {"type": "observation", "text": "...", "date": "..."}}`
  - Supported types: `observation`, `adverse_event`, `phq9`.

## Development

- **`backend/ctkg/`**: Clinical Trials parsing logic.
- **`backend/patient/`**: FHIR patient data parsing.
- **`backend/graph/`**: Cypher query generation for graph updates.
- **`backend/rag/`**: Vector store and LLM integration (currently mocked).

To extend the system, implement real connections in `backend/rag/engine.py` (for LLM) and `backend/graph/updater.py` (for FalkorDB).
