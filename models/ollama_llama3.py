import ollama

class OllamaLlama3:
    @staticmethod
    def chat(question, context, model, rules):
        formatted_prompt = f"""
        ============================
        DOCUMENT CONTEXT
        ============================
        {context}
        ============================
        RULES:
        {rules}
        ============================
        QUESTION: 
        {question}
        ============================
        """
        response = ollama.chat(model=model, messages=[{'role': 'user', 'content': formatted_prompt}])
        return response['message']['content']
