# Etapa de construção
FROM python:3.11-slim-bullseye as builder

# Definindo a variável de ambiente para o fuso horário de São Paulo e a versão do Python
ENV TZ=America/Sao_Paulo \
    PYTHON_VERSION=3.11.0

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
    curl \
    wget

# Instalando dependências Python
COPY rag.req rag.req
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r rag.req

# Etapa final
FROM chromadb/chroma:latest

# Instalar dependências necessárias
RUN apt update && apt install -y \
    gnupg \
    curl

# Configurando repositório da Nvidia
RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && \
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list && \
    apt update && \
    apt install -y nvidia-container-toolkit

# Copiar ambiente Python da etapa de construção
COPY --from=builder /venv /venv

# Instalar Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

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

# Permitir execução do script
RUN chmod +x ./run.sh

# Expor a porta que a aplicação irá usar
EXPOSE 7860

# Comando de entrada para iniciar o Ollama e o script Python
ENTRYPOINT ["./run.sh"]
