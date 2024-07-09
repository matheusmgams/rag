FROM python:3.10-slim-bullseye

# Definindo a variável de ambiente para o fuso horário de São Paulo e a versão do Python
ENV TZ=America/Sao_Paulo \
    PYTHON_VERSION=3.10.9

# Instale dependências necessárias para construção
RUN apt update && apt upgrade -y && apt install -y \
    build-essential \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    zlib1g-dev \
    libffi-dev \
    bash \
    curl

# Instalar Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Crie usuário e diretório de trabalho
ARG USERNAME=strokmatic
ARG PUID=1000
ARG PGID=1000
ENV DIR=/home/${USERNAME}
RUN addgroup --gid ${PGID} ${USERNAME} && \
    adduser --uid ${PUID} --gid ${PGID} --home ${DIR} --disabled-password --gecos "" ${USERNAME}

# Definindo diretorio
WORKDIR ${DIR}

# Copie os arquivos do aplicativo
COPY . .

# Installing requirements
RUN pip3 install -r rag.req

# Comando de entrada para iniciar o Ollama e o script Python
ENTRYPOINT ["ollama", "serve"]
