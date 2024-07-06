import os
import ollama
import gradio as gr
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader 
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


# Load Environment Variables
load_dotenv()

# Inicializa uma lista para armazenar todos os documentos
all_docs = []

# Defina o caminho da pasta onde estão os arquivos PDF
pdf_directory = str(os.environ.get('DOCUMENTS'))

# Lista todos os arquivos PDF na pasta
pdf_files = [os.path.join(pdf_directory, file) for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

# Itera sobre a lista de arquivos PDF, carregando cada um e adicionando-o à lista de documentos
for pdf_file in pdf_files:
    loader = PyMuPDFLoader(pdf_file)
    docs = loader.load()
    all_docs.extend(docs)

# definimos que vamos carregar o conteúdo da página do Wikipedia falando sobre Joinville
websites = str(os.environ.get('WEBSITES')).split(',')

# Itera sobre a lista de websites, carregando cada um e adicionando-o à lista de documentos
for website in websites:
    loader = WebBaseLoader(website)
    docs = loader.load()
    all_docs.extend(docs)

# Cria o divisor de texto
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=300)

# Divide o grande documento em chunks
splits = text_splitter.split_documents(all_docs)

# Cria o modelo de embeddings (substitua pelo embedding que você deseja usar)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Cria o vectorstore do chroma, armazenando todos os chunks de textos já como embedding
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# Aponta o vectorstore definido anteriormente como recuperador de informações, definindo nosso RAG
retriever = vectorstore.as_retriever()

# define a função para chamar o modelo Ollama Llama 3 com a pergunta do usuário e o contexto do banco vetorial
def ollama_llm(question, context):
    # cria o prompt que será enviado ao modelo LLM, contendo o contexto do banco vetorial e a pergunta do usuário
    formatted_prompt = f"""
        Contexto: {context}
        Importante: Responda em Português do Brasil!
        Pergunta: {question}
    """
    # chama o modelo LLM Ollama, passando o prompt gerado com papél de user
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': formatted_prompt}])
    # depois de obter a resposta, seleciona somente o conteúdo gerado pelo modelo e retorna
    return response['message']['content']

# define a função para realizar a corrente RAG, recebendo a pergunta do usuário
def rag_chain(question):
    # passa a pergunta para o nosso retriver, que por baixo dos panos converte para embedding e
    # trás todas as partes do texto, chunks, mais similares com a questão do usuário
    retrieved_docs = retriever.invoke(question)
    # formata os chunks retornados e o envia para a chamada do modelo llm
    formatted_context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    # chama o modelo ollama com a pergunta do usuário e o contexto formatado
    print("retrieved_docs: " + formatted_context)
    return ollama_llm(question, formatted_context)

# método para receber a pergunta do usuário e iniciar a corrente RAG de sincronização dos dados
def answer_user_request(question):
    print("Nova pergunta: " + question)
    # aciona a corrente RAG
    return rag_chain(question)

# Cria uma interface no Gradio, passando a função que vai lidar com a troca de mensagens
iface = gr.Interface(
  fn=answer_user_request,
  inputs=gr.Textbox(lines=2, placeholder=os.getenv('PLACEHOLDER')),
  outputs="text",
  title=os.getenv('TITLE'),
  description=os.getenv('DESCRIPTION'),
)

# starta o app Gradio
iface.launch(debug=True)