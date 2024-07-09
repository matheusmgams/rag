#!/bin/bash

# Iniciar Ollama
ollama serve &

# Aguardar um pouco para garantir que Ollama foi iniciado corretamente
sleep 5

# Downloading models
ollama pull llama3
ollama pull nomic-embed-text

# Run applications
python3 ./rag.py