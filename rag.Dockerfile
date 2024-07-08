# Estágio de Compilação
FROM python:3.10-alpine as builder

# Instale as dependências necessárias para compilação e limpe o cache
RUN apk add --no-cache curl build-base libjpeg-turbo-dev libpng-dev tiff-dev \
    libwebp-dev zlib-dev libffi-dev

# Defina o fuso horário
ENV TZ=America/Sao_Paulo

# Copie e instale as dependências Python
WORKDIR /build
COPY rag.req .
RUN python3 -m venv /venv && \
    . /venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r rag.req

# Estágio de Execução
FROM chromadb/chroma:latest

# Instale o coreutils para ter o comando tail disponível
RUN apt-get update && apt-get install -y coreutils

# Copie o ambiente virtual do estágio de compilação
COPY --from=builder /venv /venv

# Defina o caminho do ambiente virtual
ENV PATH="/venv/bin:$PATH"

# Crie usuário e diretório de trabalho
ARG USERNAME=strokmatic
ARG PUID=1000
ARG PGID=1000
ENV DIR=/home/${USERNAME}
RUN groupadd -g ${PGID} ${USERNAME} && \
    useradd -u ${PUID} -g ${USERNAME} -d ${DIR} -m ${USERNAME}
WORKDIR ${DIR}

# Copie os arquivos do aplicativo
COPY . .

# Installing Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN ollama serve &

ENTRYPOINT [ "tail", "-f", "/dev/null" ]
