build:
	docker compose build

run:
	docker compose up

pull-model:
	docker compose run ollama pull llama3
