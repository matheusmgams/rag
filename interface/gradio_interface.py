import os
import gradio as gr
from rag.rag_chain import RAGChain

class GradioInterface:

    def __init__(self, retriever, model, rules):
        self.iface = gr.Interface(
            fn=lambda question: RAGChain.rag_chain(question, retriever, model, rules),
            inputs=gr.Textbox(lines=1, placeholder=os.getenv('PLACEHOLDER'), interactive=True),
            outputs=gr.Textbox(lines=0, interactive=True),
            title=os.getenv('TITLE'),
            description=os.getenv('DESCRIPTION'),
        )
    
    def launch(self):
        self.iface.launch(server_name="0.0.0.0", server_port=7860)
