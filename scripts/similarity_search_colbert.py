import os
import sys
from dotenv import load_dotenv
from ragstack_colbert import CassandraDatabase, ColbertEmbeddingModel
from ragstack_langchain.colbert import ColbertVectorStore as LangchainColbertVectorStore

load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_DATABASE_ID = os.environ.get("ASTRA_DB_DATABASE_ID")

embedding = ColbertEmbeddingModel()
database = CassandraDatabase.from_astra(
    astra_token=ASTRA_DB_APPLICATION_TOKEN,
    database_id=ASTRA_DB_DATABASE_ID,
    keyspace="default_keyspace"
)
vstore = LangchainColbertVectorStore(
    database=database,
    embedding_model=embedding
)

query = sys.argv[1] if len(sys.argv) > 1 else "Who is speaking about ColBERT?"
print(query)

docs = vstore.similarity_search(query)
print(f"first answer: {docs[0].page_content}")