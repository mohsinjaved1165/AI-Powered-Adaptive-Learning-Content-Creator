# Adaptive Learning Content Creator

## Overview
Generates personalized educational content using:
- Ollama (llama3)
- FAISS vector search
- LangChain RAG
- Flask + HTML template
- Docker
- Difficulty & Learning Style adaptation

## Setup
1. Ensure Docker is installed (Linux, MacOS, Windows Docker Desktop).
2. Build the project:
    make build
3. Pull llama3 model:
    make pull-model
4. Run the project:
    make run
5. Open browser at http://localhost:5000

## Sample Dataset
Located in data/sample_docs/. Add your own text files to extend content.
