# Adaptive Learning Content Creator

## Overview
Generates personalized educational content using:
- Ollama (llama3)
- FAISS vector search
- LangChain RAG
- Flask + HTML template
- Docker
- Difficulty & Learning Style adaptation

An interactive web application that leverages **LLaMA3 via Ollama** and **LangChain** to create adaptive learning content from text documents. Users can ask questions on the uploaded documents, and the system responds according to the user’s preferred **difficulty level** and **learning style**.

---

## Problem Statement

Traditional learning resources are static and often do not adapt to individual learner needs. Students may find it difficult to understand complex topics or retain information if the content is not presented in a suitable style. This project aims to create an **AI-powered adaptive learning assistant** that:

- Reads multiple documents (sample + user-uploaded)
- Answers user questions based on all available content
- Adjusts responses based on **difficulty** (easy, hard) and **learning style** (visual, auditory, reading)

---

## Solution

- Users can upload `.txt` files containing learning material.
- The system builds a **FAISS vector index** of all documents for semantic search.
- Queries are processed using **LLaMA3 embeddings and language model** via Ollama.
- Answers are **adapted** according to user-selected difficulty and learning style.
- The app has a simple web interface for uploading documents and asking questions.

---

## Tech Stack

- **Backend:** Python, Flask
- **AI / NLP:** Ollama (LLaMA3), LangChain, FAISS
- **Frontend:** HTML (Jinja templates)
- **Containerization:** Docker, Docker Compose
- **Data storage:** Local `data/` folder for uploaded and sample documents

---

## Project Structure

adaptive-learning/
│
├─ app.py # Flask application
├─ docker-compose.yml # Docker services (Flask + Ollama)
├─ wait_for_ollama.py # Wait script to ensure Ollama is running
├─ templates/
│ └─ index.html # Web UI template
├─ data/
│ ├─ sample_docs/ # Preloaded sample documents
│ └─ uploaded_docs/ # User-uploaded documents
└─ README.md

yaml
Copy code

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/mohsinjaved1165/AI-Powered-Adaptive-Learning-Content-Creator
cd adaptive-learning
2. Build and Start Docker Containers
Make sure Docker is installed and running.

bash
Copy code
docker-compose up --build
This will start two services:

Ollama (ollama) on port 11434
Flask app (flask-app) on port 8080

3. Pull LLaMA3 Model Inside the Ollama Container
Open a new terminal and run:

bash
Copy code
docker exec -it adaptive-learning-ollama ollama pull llama3
4. Access the Application
Open your browser:

arduino
Copy code
http://localhost:8080
You should see the Adaptive Learning Content Creator interface.

** End-User Workflow**
View Sample Documents
The app comes preloaded with sample learning documents in data/sample_docs.

Upload New Documents
Click “Upload File” and select a .txt file.
The app will save it to data/uploaded_docs and rebuild the FAISS index automatically.

Ask Questions
Enter a topic or question.
Select difficulty (easy/hard) and learning style (visual/auditory/reading).
Submit the query to get an AI-generated response adapted to your preferences.

Adaptive Answering
Responses are semantic, combining information from all uploaded and sample documents.
They are tailored according to difficulty and learning style.


**Notes**
Only .txt files are supported for upload.
FAISS vector index is rebuilt after each new upload to include new documents.
The system uses Ollama API via the host http://ollama:11434.
Ensure Docker has enough memory to run LLaMA3 model smoothly.


**Future Improvements**
Support for PDF and DOCX uploads.
Richer adaptation for learning style (images, audio, video snippets).
User authentication and document management dashboard.
