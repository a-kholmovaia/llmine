import os
from llama_index.llms import LlamaCPP
from llama_index.embeddings import HuggingFaceEmbedding

from llama_index import StorageContext, ServiceContext, VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.query_engine import RetrieverQueryEngine
from retriever import Retriever
from llama_index.prompts import PromptTemplate
import faiss

class Planner:
    MODEL_PATH = "../model/models/llama-2-13b-chat.Q5_K_S.gguf"
    EMBED_MODEL = "jinaai/jina-embeddings-v2-small-en"
    VECTORS_DB_PATH = "/vectors"

    def __init__(self):
        self.llm = LlamaCPP(
            model_url=None,
            model_path=self.MODEL_PATH,
            temperature=0.1,
            max_new_tokens=400,
            context_window=3650,
            generate_kwargs={},
            model_kwargs={"n_gpu_layers": 20},
            verbose=True,
            ) 
        self.embed_model = HuggingFaceEmbedding(model_name=self.EMBED_MODEL)
        
        self.service_context = ServiceContext.from_defaults(
            llm=self.llm, embed_model=self.embed_model
        )

        self.vector_store = FaissVectorStore.from_persist_dir(self.VECTORS_DB_PATH)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store, persist_dir=self.VECTORS_DB_PATH)
        self.index = self.load_from_index()


        self.retriever = Retriever(
        self.vector_store, self.embed_model, 
        query_mode="default", similarity_top_k=2
        )

        self.query_engine = RetrieverQueryEngine.from_args(
            self.retriever, service_context=self.service_context
        )
        self.customise_prompt_llama2()
        print('RAG initialised')

    
    def customise_prompt_llama2(self):
        custom_prompt_template = '''
        [INST] <<SYS>>Answer the users question only taking into account the following context. If the user asks for information not found in the below context, do not answer.
                <context>
                {context_str}
                </context>
                <</SYS>>
                Question: 
                {query_str} 
                Answer:
                [/INST]
        '''
        qa_template = PromptTemplate(custom_prompt_template)
        self.query_engine.update_prompts(
            {"response_synthesizer:text_qa_template": qa_template}
        )        
        

    def generate_answer(self, query: str) -> str:
        return self.query_engine.query(query)


    def load_from_index(self) -> VectorStoreIndex:
        self.index = load_index_from_storage(storage_context=self.storage_context)
        return self.index
    
