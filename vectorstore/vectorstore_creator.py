import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

class VectorStoreCreator:
    @staticmethod
    def create_vectorstore(documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=int(os.environ.get('CHUNK_SIZE')), 
                                                       chunk_overlap=int(os.environ.get('CHUNK_OVERLAP')))
        splits = []
        for doc in documents:
            for chunk in text_splitter.split_text(doc.page_content):
                splits.append(Document(page_content=chunk, metadata=doc.metadata))
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        return vectorstore.as_retriever()
