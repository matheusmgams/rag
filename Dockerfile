FROM python:3.11-slim

# Instala dependências necessárias
RUN apt-get update && \
    apt-get install -y sqlite3 libsqlite3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verifica a versão do SQLite
RUN sqlite3 --version

# Crie usuário e diretório de trabalho
ARG USERNAME=strokmatic
ARG PUID=1000
ARG PGID=1000
ENV DIR=/home/${USERNAME}
RUN addgroup --gid ${PGID} ${USERNAME} && \
    adduser --uid ${PUID} --gid ${PGID} --home ${DIR} --disabled-password --gecos "" ${USERNAME}

# Definindo diretório de trabalho
WORKDIR ${DIR}

# Copie os arquivos do aplicativo
COPY . .

# Configurar ambiente virtual Python
ENV PATH="/venv/bin:$PATH"

# Instalando dependências Python
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Expor a porta que a aplicação irá usar
EXPOSE 7860

# Comando de entrada para iniciar o Ollama e o script Python
ENTRYPOINT ["python3 ./main.py"]
