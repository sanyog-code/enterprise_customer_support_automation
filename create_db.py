import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
 
def build_db():
    print("🚀 Rebuilding database from existing CSV...")
    
    # Use the model you already have cached
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists("faiss_support_db"):
        import shutil
        shutil.rmtree("faiss_support_db")
 
    # Load the original CSV
    df = pd.read_csv("customer_support_tickets.csv")
    
    docs = []
    for _, row in df.iterrows():
        # Mapping to your exact columns from the image
        subject = str(row['Ticket Subject'])
        description = str(row['Ticket Description'])
        resolution = str(row['Resolution']) if pd.notna(row['Resolution']) else "No resolution provided."
        
        content = f"PRODUCT: {row['Product Purchased']}\nSUBJECT: {subject}\nISSUE: {description}\nRESOLUTION: {resolution}"
        docs.append(Document(page_content=content))
        
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_support_db")
    print("✅ Database built successfully using existing CSV columns.")
 
if __name__ == "__main__":
    build_db()
 