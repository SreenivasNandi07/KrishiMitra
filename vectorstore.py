from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class KnowledgeBase:
    def __init__(self):
        # Local, lightweight embedding model (HuggingFace)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db_path = "faiss_index"

    def create_knowledge_base(self, texts):
        """Converts text manuals into searchable vectors."""
        docs = [Document(page_content=t) for t in texts]
        vector_db = FAISS.from_documents(docs, self.embeddings)
        vector_db.save_local(self.db_path)
        return vector_db

    def search(self, query):
        """Finds the most relevant info for the LLM."""
        db = FAISS.load_local(self.db_path, self.embeddings, allow_dangerous_deserialization=True)
        results = db.similarity_search(query, k=2)
        return "\n".join([res.page_content for res in results])