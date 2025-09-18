import time
import requests
import os

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

print("Waiting for Ollama server to be ready...")

while True:
    try:
        r = requests.get(OLLAMA_HOST)
        if r.status_code < 400:  # any 2xx/3xx response counts as ready
            print("Ollama is ready!")
            break
    except requests.exceptions.RequestException:
        pass
    time.sleep(2)
