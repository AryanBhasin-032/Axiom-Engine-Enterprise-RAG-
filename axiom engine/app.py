import os
from fastapi import FastAPI
from pydantic import BaseModel
from supabase.client import Client, create_client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Setup API keys
SUPABASE_URL = "url"
SUPABASE_KEY = "key"
os.environ["GOOGLE_API_KEY"] = "api"

# 2. App, Database & Embeddings (initialization)
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

# frontend talks to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.environ["GOOGLE_API_KEY"],
    convert_system_message_to_human=True
)

# 4. Logic
system_prompt = (
    "You are an expert assistant for the Axiom Engine. "
    "Use ONLY the provided context below to answer the question. "
    "If the answer is not contained in the context, say EXACTLY: 'I don't know'.\n\n"
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Modern LCEL Chain
generation_chain = prompt | llm | StrOutputParser()

# 5. API Data Models
class UserQuery(BaseModel):
    query: str

# 6. The API Endpoint
@app.post("/ask")
async def ask_question(request: UserQuery):
    try:
        # Converting user's query into a math vector
        query_vector = embeddings.embed_query(request.query)
        
        #Direct database search
        #Hybrid Database Search (Vector + Keyword via RRF)
        response = supabase.rpc(
            "hybrid_search", 
            {
                "query_text": request.query,       
                "query_embedding": query_vector, 
                "match_count": 3
            }
        ).execute()
        
        docs = response.data if response.data else []
        
        #Glue chunks into context
        if not docs:
            context_text = "No relevant context found in the database."
        else:
            context_text = "\n\n".join(doc.get("content", "No content") for doc in docs)
        
        #Send the context and the question to api
        answer = generation_chain.invoke({
            "input": request.query,
            "context": context_text
        })
        
        #Returm the answer and the raw sources to frontend
        return {
            "answer": answer,
            "sources": [
                {"content": d.get("content"), "metadata": d.get("metadata")} 
                for d in docs
            ]
        }

    except Exception as e:
        # If fails, print the exact error to the VS Code terminal
        print("\n--- BACKEND ERROR ---")
        print(f"Details: {str(e)}")
        print("----------------------\n")
        return {
            "answer": f"Error: {str(e)}", 
            "sources": []
        }

# This allows you to run the script directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)