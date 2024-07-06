# Estágio de Compilação
FROM python:3.10-alpine as builder

# Defina o fuso horário e prepare o ambiente virtual
ENV TZ=America/Sao_Paulo
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Instale as dependências necessárias para compilação e limpe o cache
RUN apk add --no-cache build-base libjpeg-turbo-dev libpng-dev tiff-dev \
    libwebp-dev zlib-dev libffi-dev && \
    rm -rf /var/cache/apk/*

# Copie e instale as dependências Python
WORKDIR /build
COPY rag.req .
RUN pip3 install --no-cache-dir -r rag.req

# Estágio de Execução
FROM python:3.10-alpine

# Copie o ambiente virtual do estágio de compilação
COPY --from=builder /venv /venv

# Defina o fuso horário
ENV TZ=America/Sao_Paulo
ENV PATH="/venv/bin:$PATH"

# Crie usuário e diretório de trabalho
ARG USERNAME=strokmatic
ARG PUID=1000
ARG PGID=1000
ENV DIR=/home/${USERNAME}
RUN addgroup -g ${PGID} ${USERNAME} && \
    adduser -u ${PUID} -G ${USERNAME} -D -h ${DIR} ${USERNAME}
WORKDIR ${DIR}

# Copie os arquivos do aplicativo
COPY . .

# Defina o comando de execução
CMD ["python3", "./rag.py"]