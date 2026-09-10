import sys

print("=== PYTHON BRAIN CHECK ===")
print("1. Which Python is running?:", sys.executable)

print("\n=== LANGCHAIN CHECK ===")
try:
    import langchain
    print("2. Where is LangChain located?:", langchain.__file__)
    print("3. What version is it?:", langchain.__version__)
    
    import langchain.chains
    print("4. Langchain Chains loaded successfully!")
    
except Exception as e:
    print("ERROR:", e)