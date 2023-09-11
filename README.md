# bank-assistant-bot
Bank Assistant chat bot using LLM and AstraDB
It is using OpenAI to build embeddings and Astra/Chroma to store the data.

## Pre-requisites

- Python 3.6+
- Launch an [AstraDB](https://astra.datastax.com/) database or use [Chroma](https://www.trychroma.com/)

## Setup

- Clone the repository
- Install the dependencies using `pip install -r requirements.txt`
- Add your Astra info and OpenAI token in `.env` file
- If using Astra: edit `resources/schema.cql` and replace `YOUR_KEYSPACE_NAME_HERE` with the actual name of your keyspace. Then launch the CQL script to create the schema -- _should be automated soon_
- Run `client_loader*.py` to import fake clients data in your database from `resources/clients-dataset.csv`
- Run `main.py` using the command `streamlit run main.py`
