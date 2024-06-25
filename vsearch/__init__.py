import os
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from ragstack_colbert import CassandraDatabase, ColbertEmbeddingModel
from ragstack_langchain.colbert import ColbertVectorStore as LangchainColbertVectorStore
from flask import Flask, render_template, request, redirect, url_for

load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
OPEN_AI_API_KEY = os.environ.get("OPENAI_API_KEY")
ASTRA_DB_COLLECTION = os.environ.get("ASTRA_DB_COLLECTION")
ASTRA_DB_DATABASE_ID = os.environ.get("ASTRA_DB_DATABASE_ID")

embedding = OpenAIEmbeddings()
vstore = AstraDBVectorStore(
    embedding=embedding,
    collection_name=ASTRA_DB_COLLECTION,
    token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
    api_endpoint=os.environ["ASTRA_DB_API_ENDPOINT"],
)

colbert_embedding = ColbertEmbeddingModel()
colbert_database = CassandraDatabase.from_astra(
    astra_token=ASTRA_DB_APPLICATION_TOKEN,
    database_id=ASTRA_DB_DATABASE_ID,
    keyspace="default_keyspace"
)
colbert_vstore = LangchainColbertVectorStore(
    database=colbert_database,
    embedding_model=colbert_embedding
)

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return render_template('hello-world.html')
    
    @app.route('/vector', methods=('GET', 'POST'))
    def vector():
      if request.method == 'POST':
        query = request.form['query']
        docs = vstore.similarity_search(query)
        doc_list = []
        for doc in docs:
          doc_list.append(doc.page_content)
        return doc_list
      else:
         return redirect(url_for('hello'))
      
    @app.route("/colbert", methods=('GET', 'POST'))
    def colbert():
       if request.method == "POST":
          query = request.form['query']
          docs = colbert_vstore.similarity_search(query)
          doc_list = []
          for doc in docs:
            doc_list.append(doc.page_content)
          return doc_list
          
    return app