import os
import json
from dotenv import load_dotenv
from ragstack_colbert import CassandraDatabase, ColbertEmbeddingModel, ColbertVectorStore

load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_DATABASE_ID = os.environ.get("ASTRA_DB_DATABASE_ID")

file = open("./data/ai-engineer-sessions.json")
data = json.load(file)

embedding = ColbertEmbeddingModel()
database = CassandraDatabase.from_astra(
    astra_token=ASTRA_DB_APPLICATION_TOKEN,
    database_id=ASTRA_DB_DATABASE_ID,
    keyspace="default_keyspace"
)
vstore = ColbertVectorStore(
    database=database,
    embedding_model=embedding
)

results = vstore.add_texts(texts=data, doc_id="ai_engineer")
print(f"\nInserted {len(results)} documents.")

