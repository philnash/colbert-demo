import os
import json
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
OPEN_AI_API_KEY = os.environ.get("OPENAI_API_KEY")
ASTRA_DB_COLLECTION = os.environ.get("ASTRA_DB_COLLECTION")

file = open("./data/ai-engineer-sessions.json")
data = json.load(file)

embedding = OpenAIEmbeddings()
vstore = AstraDBVectorStore(
    embedding=embedding,
    collection_name=ASTRA_DB_COLLECTION,
    token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
    api_endpoint=os.environ["ASTRA_DB_API_ENDPOINT"],
)

docs = []
for entry in data:
    doc = Document(page_content=entry)
    docs.append(doc)
  
inserted_ids = vstore.add_documents(docs)
print(f"\nInserted {len(inserted_ids)} documents.")

