### Introdução ao LLAMA3 com RAG

Se você é novo no conceito de RAG (Retrieval-Augmented Generation) e no uso do LLAMA3, esta documentação irá guiá-lo pelos passos necessários para configurar o ambiente e executar o modelo.

#### Passo 1: Instalação do OLLAMA

O OLLAMA é um modelo de linguagem avançado desenvolvido pela Ollama. Antes de começar, você precisa instalar o OLLAMA. 

##### 1.1. Baixar e Instalar o OLLAMA

Para instalar o LLAMA3, você precisa executar um comando que baixa e instala o software necessário. Abra o terminal (ou prompt de comando) e execute o seguinte comando:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
Este comando baixa um script de instalação do OLLAMA e o executa. Mais informações sobre o OLLAMA podem ser encontradas em https://ollama.com/library/llama3.

#### Passo 2: Iniciar o Servidor do OLLAMA

Após a instalação, você precisa iniciar o servidor OLLAMA. Abra o terminal novamente e execute:
```bash
ollama serve
```
Isso iniciará o servidor que você usará para interagir com o modelo LLAMA3.

#### Passo 3: Configuração do Segundo Console

Para usar o modelo, você precisará executar alguns comandos adicionais em um segundo terminal. Siga os passos abaixo:

##### 3.1. Instalar o Modelo LLAMA3

No segundo terminal, execute o seguinte comando para baixar e instalar o modelo LLAMA3:
```bash
ollama pull llama3
```
Este comando baixa o modelo LLAMA3 necessário para realizar inferências.

##### 3.2. Instalar o Modelo de Embeddings Nomic

Para gerar embeddings, você precisa instalar o modelo `nomic-embed-text`. Execute o comando a seguir no segundo terminal:
```bash
ollama pull nomic-embed-text
```
Este comando baixa e instala o modelo de embeddings necessário para o processo de RAG.

Recursos Adicionais

Para mais informações sobre como usar o Docker com o LLAMA3, consulte a documentação oficial do Docker: https://hub.docker.com/r/ollama/ollama.
