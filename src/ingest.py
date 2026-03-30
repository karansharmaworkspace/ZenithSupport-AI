import os
import re
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def build_index(data_dir, index_dir):
    print(f"Loading documents from {data_dir}...")
    loader = DirectoryLoader(data_dir, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    print(f"Splitting {len(documents)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        add_start_index=True
    )
    docs = text_splitter.split_documents(documents)
    
    for i, doc in enumerate(docs):
        doc.metadata["chunk_id"] = f"chunk_{i}"
        content = doc.page_content
        headers = re.findall(r"(?:^|\n)(#+ .*?)(?:\n|$)", content)
        if headers:
            doc.metadata["section"] = headers[-1].strip("# ")
        else:
            doc.metadata["section"] = "General Policy"
    
    print(f"Creating embeddings for {len(docs)} chunks...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
    
    vectorstore.save_local(index_dir)
    print(f"Index saved to {index_dir}")

if __name__ == "__main__":
    DATA_DIR = os.path.join("ecommerce_agent", "data", "policies")
    INDEX_DIR = os.path.join("ecommerce_agent", "data", "index")
    build_index(DATA_DIR, INDEX_DIR)
