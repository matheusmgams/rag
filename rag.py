import os
import ollama
import gradio as gr
from dotenv import load_dotenv
from pptx import Presentation
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.docstore.document import Document

# Função para carregar variáveis de ambiente
def load_env_variables():
    load_dotenv()
    pdf_directory = os.environ.get('DOCUMENTS')
    websites = os.environ.get('WEBSITES').split(',')
    return pdf_directory, websites

# Função para carregar documentos PDF
def load_pdfs(pdf_directory):
    pdf_files = [os.path.join(pdf_directory, file) for file in os.listdir(pdf_directory) if file.endswith('.pdf')]
    all_docs = []
    for pdf_file in pdf_files:
        try:
            loader = PyMuPDFLoader(pdf_file)
            docs = loader.load()
            all_docs.extend(docs)
        except Exception as e:
            print(f"Erro ao carregar {pdf_file}: {e}")
    return all_docs

# Função para carregar documentos PPTX
def load_pptx(pdf_directory):
    pptx_files = [os.path.join(pdf_directory, file) for file in os.listdir(pdf_directory) if file.endswith('.pptx')]
    all_docs = []
    for pptx_file in pptx_files:
        try:
            doc_content = ""
            prs = Presentation(pptx_file)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        doc_content += shape.text + "\n"
            all_docs.append(Document(page_content=doc_content))
        except Exception as e:
            print(f"Erro ao carregar {pptx_file}: {e}")
    return all_docs

# Função para carregar conteúdo de websites
def load_websites(websites):
    all_docs = []
    for website in websites:
        try:
            loader = WebBaseLoader(website)
            docs = loader.load()
            all_docs.extend(docs)
        except Exception as e:
            print(f"Erro ao carregar {website}: {e}")
    return all_docs

# Função principal para carregar todos os documentos
def load_all_documents(pdf_directory, websites):
    all_docs = []
    all_docs.extend(load_pdfs(pdf_directory))
    all_docs.extend(load_pptx(pdf_directory))
    all_docs.extend(load_websites(websites))
    return all_docs

# Função para criar o vetor de embeddings
def create_vectorstore(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    return vectorstore.as_retriever()

# Função para chamar o modelo Ollama Llama 3
def ollama_llm(question, context):
    formatted_prompt = f"""
        Contexto: {context}
        Importante: Sempre Responda em Português do Brasil, Segundo as definições do SCP-DEV-1000 e dê exemplos conforme as orientações do SCP-DEV-1000.
        Pergunta: {question}
    """
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']

# Função para realizar a corrente RAG
def rag_chain(question, retriever):
    retrieved_docs = retriever.invoke(question)
    formatted_context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    print("retrieved_docs: " + formatted_context)
    return ollama_llm(question, formatted_context)

# Função para responder à pergunta do usuário
def answer_user_request(question, retriever):
    print("Nova pergunta: " + question)
    return rag_chain(question, retriever)

# Função principal
def main():
    pdf_directory, websites = load_env_variables()
    all_docs = load_all_documents(pdf_directory, websites)
    retriever = create_vectorstore(all_docs)
    
    iface = gr.Interface(
        fn=lambda question: answer_user_request(question, retriever),
        inputs=gr.Textbox(lines=2, placeholder=os.getenv('PLACEHOLDER')),
        outputs="text",
        title=os.getenv('TITLE'),
        description=os.getenv('DESCRIPTION'),
    )
    iface.launch(debug=True)

if __name__ == "__main__":
    main()
