from models.ollama_llama3 import OllamaLlama3

class RAGChain:
    @staticmethod
    def rag_chain(question, retriever, model, rules):
        retrieved_docs = retriever.invoke(question)
        formatted_context = "\n\n".join(doc.page_content for doc in retrieved_docs)
        print("retrieved_docs: " + formatted_context)
        return OllamaLlama3.chat(question, formatted_context, model, rules)
