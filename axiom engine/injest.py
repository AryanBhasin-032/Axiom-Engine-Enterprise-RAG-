import os
from supabase.client import Client, create_client
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore


SUPABASE_URL = "a url"
SUPABASE_KEY = "key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Connecting to Supabase...")

pdf_path = "myfile.pdf"
print(f"Loading {pdf_path}...")
loader = PyPDFLoader(pdf_path)
documents = loader.load()

print("Splitting document into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks.")


print("Loading HuggingFace Embedding model (this might take a minute)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


print("Uploading chunks and vectors to Supabase...")
vector_store = SupabaseVectorStore.from_documents(
    chunks,
    embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents" 
)

print("✅ Success! Your PDF is now processed and stored in the database.")