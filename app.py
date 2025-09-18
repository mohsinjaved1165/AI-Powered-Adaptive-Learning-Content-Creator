from flask import Flask, render_template, request, redirect, url_for, flash
import os

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

# Initialize LLM and embeddings
llm = OllamaLLM(model="llama3", host=OLLAMA_HOST)
embeddings = OllamaEmbeddings(model="llama3")

# Directories for data
SAMPLE_DIR = os.path.join("data", "sample_docs")
UPLOAD_DIR = os.path.join("data", "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Helper: Load all documents (sample + uploaded) ---
def load_all_documents():
    docs = []
    for folder in [SAMPLE_DIR, UPLOAD_DIR]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                if filename.endswith(".txt"):
                    filepath = os.path.join(folder, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        docs.append(content)
                        print(f"Loaded {filename}, {len(content)} chars")  # Debug
    return docs

# --- Helper: Build FAISS index ---
def build_vectorstore():
    docs = load_all_documents()
    if not docs:
        return None

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # Split all docs into chunks
    texts = []
    for d in docs:
        chunks = splitter.split_text(d)
        texts.extend(chunks)

    # Wrap chunks as Documents
    documents = [Document(page_content=t) for t in texts]

    return FAISS.from_documents(documents, embeddings)

# Initialize vectorstore + QA chain
vectorstore = build_vectorstore()
qa_chain = None
if vectorstore:
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# --- Adaptation logic ---
def adapt_answer(answer, difficulty, learning_style):
    if difficulty == "easy":
        answer = f"(Simplified) {answer}"
    elif difficulty == "hard":
        answer = f"(Detailed) {answer}"

    if learning_style == "visual":
        answer += " [Use diagrams or visuals.]"
    elif learning_style == "auditory":
        answer += " [Explain verbally or with audio.]"
    elif learning_style == "reading":
        answer += " [Provide clear text-based explanation.]"
    return answer

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        query = request.form.get("query")
        difficulty = request.form.get("difficulty")
        learning_style = request.form.get("learning_style")

        if not qa_chain:
            flash("No dataset available. Please upload a file first.", "error")
            return redirect(url_for("index"))

        if query:
            raw_answer = qa_chain.run(query)
            answer = adapt_answer(raw_answer, difficulty, learning_style)
    return render_template("index.html", answer=answer)

@app.route("/upload", methods=["POST"])
def upload_file():
    global vectorstore, qa_chain

    if "file" not in request.files:
        flash("No file part in request.", "error")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected.", "error")
        return redirect(url_for("index"))

    if file and file.filename.endswith(".txt"):
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        file.save(filepath)
        flash(f"File '{file.filename}' uploaded successfully!", "success")

        # Rebuild FAISS index
        vectorstore = build_vectorstore()
        if vectorstore:
            retriever = vectorstore.as_retriever()
            qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
            flash(f"FAISS index rebuilt with {len(vectorstore.docstore._dict)} documents", "info")  # Safe check
        else:
            qa_chain = None
            flash("No documents found to build FAISS index.", "error")
    else:
        flash("Only .txt files are allowed.", "error")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
