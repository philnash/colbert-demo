# ColBERT with RAGStack

This is an example project that loads data about talks from the [AI Engineer World's Fair](https://www.ai.engineer/worldsfair) into [DataStax Astra DB](https://www.datastax.com/products/datastax-astra) in two different ways:

* With vectors created by the OpenAI embedding model `text-embedding-ada-002`
* Using ColBERT via [RAGStack](https://docs.datastax.com/en/ragstack/quickstart.html)

The Flask app then runs a side-by-side comparison of the top result using regular vector search against ColBERT.

## How to run

### Prerequisites

You will need an Astra DB account, [sign up for free here](https://astra.datastax.com/signup). Then create a database and a vector enabled collection, with a vector field with 1,536 dimensions.

You will also need an [OpenAI account](https://platform.openai.com/docs/overview) with API access.

### Setting up the app

Clone the application:

```sh
git clone https://github.com/philnash/colbert-demo.git
cd colbert-demo
```

Install the dependencies:

```sh
pip install -r requirements.txt
```

Copy the `.env.example` file to `.env`. Fill in the `.env` file with details from your Astra DB and OpenAI accounts.

### Loading the data

There are two scripts available to load data into your Astra DB database. The first creates vectors using OpenAI embedding `text-embedding-ada-002`. Run it with:

```sh
python ./scripts/load_data_vector.py
```

The second creates two tables using CQL and loads the data into them creating token level embeddings using ColBERT. This may take a long time on unoptimized hardware.

```sh
python ./scripts/load_data_colbert.py
```

### Run the Flask application

You can now run the Flask application with:

```sh
flask --app vsearch run
```

Open the app to `localhost:5000` and check out the difference between ColBERT and regular vector search.