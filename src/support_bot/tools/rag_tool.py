from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
 
class RAGSearchSchema(BaseModel):
    query: str = Field(..., description="The query to search in the knowledge base.")
 
class TicketRAGTool(BaseTool):
    name: str = "Hybrid Knowledge Base Search"
    description: str = "Searches the official knowledge base using Hybrid Retrieval (Semantic FAISS + Keyword Filtering)."
    args_schema: type[BaseModel] = RAGSearchSchema
 
    def _run(self, query: str) -> str:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db_path = "faiss_support_db"
        
        if not os.path.exists(db_path):
            return "Knowledge base not initialized."
 
        try:
            # 1. Semantic Search (FAISS)
            vectorstore = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
            semantic_docs = vectorstore.similarity_search(query, k=5)
            
            # 2. Keyword Filter (Simulating Hybrid BM25 approach)
            keywords = [word.lower() for word in query.split() if len(word) > 3]
            hybrid_results = []
            
            for doc in semantic_docs:
                content_lower = doc.page_content.lower()
                # Boost score if keywords exist in the semantic match
                match_score = sum(1 for kw in keywords if kw in content_lower)
                if match_score > 0 or len(keywords) == 0:
                    hybrid_results.append(doc.page_content)
 
            if not hybrid_results:
                return "No official resolution found in the database."
            
            # Return top 3 hybrid matches
            return "\n---\n".join(hybrid_results[:3])
        except Exception as e:
            return f"Database error: {str(e)}"
 