import os
import json
import sys
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
OPEN_AI_API_KEY = os.environ.get("OPENAI_API_KEY")
ASTRA_DB_COLLECTION = os.environ.get("ASTRA_DB_COLLECTION")

embedding = OpenAIEmbeddings()
vstore = AstraDBVectorStore(
    embedding=embedding,
    collection_name=ASTRA_DB_COLLECTION,
    token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
    api_endpoint=os.environ["ASTRA_DB_API_ENDPOINT"],
)

query = sys.argv[1] if len(sys.argv) > 1 else "Who is speaking about ColBERT?"
print(query)

docs = vstore.similarity_search(query)
print(f"first answer: {docs[0].page_content}")