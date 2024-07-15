from loaders.env_loader import EnvironmentLoader
from loaders.document_loader import DocumentLoader
from vectorstore.vectorstore_creator import VectorStoreCreator
from interface.gradio_interface import GradioInterface

def main():
    archives, websites, codes, model, rules = EnvironmentLoader.load_env_variables()
    document_loader = DocumentLoader(archives, codes, websites)
    all_docs = document_loader.load_all_documents()
    retriever = VectorStoreCreator.create_vectorstore(all_docs)
    gradio_interface = GradioInterface(retriever, model, rules)

if __name__ == "__main__":
    main()
