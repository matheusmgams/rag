import os
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

class VectorStoreCreator:
    @staticmethod
    def create_vectorstore(documents):
        if not documents:
            print("A lista de documentos está vazia. Certifique-se de que documentos foram carregados corretamente.")

        # Verifica se as variáveis de ambiente necessárias estão definidas
        chunk_size = os.getenv('CHUNK_SIZE')
        chunk_overlap = os.getenv('CHUNK_OVERLAP')

        if not chunk_size or not chunk_overlap:
            raise EnvironmentError("As variáveis de ambiente CHUNK_SIZE e CHUNK_OVERLAP devem ser definidas.")

        try:
            chunk_size = int(chunk_size)
            chunk_overlap = int(chunk_overlap)
        except ValueError:
            print("CHUNK_SIZE e CHUNK_OVERLAP devem ser inteiros válidos.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        splits = []

        for doc in tqdm(documents, desc="Processing Documents"):
            for chunk in text_splitter.split_text(doc.page_content):
                splits.append(Document(page_content=chunk, metadata=doc.metadata))

        # Verifica se a lista de splits não está vazia antes de criar o vetor de embeddings
        if not splits:
            print("Após a divisão de texto, a lista de chunks está vazia. Verifique o tamanho do chunk e a sobreposição.")

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        embeddings.base_url = os.getenv("OLLAMA_HOST_BASE", "0.0.0.0")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        return vectorstore.as_retriever()
