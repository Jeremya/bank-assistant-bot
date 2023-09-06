import chromadb
import csv
import openai
import json

from dotenv import dotenv_values

config = dotenv_values('../.env')
openai.api_key = config['OPENAI_API_KEY']
model_id = "text-embedding-ada-002"
chroma_path = config['CHROMA_PERSISTENT_PATH']
chroma_client = chromadb.PersistentClient(path=chroma_path)

collection = chroma_client.get_or_create_collection(name="bankflix")

with open('../resources/clients-dataset.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)

    for row in reader:
        # Create a dictionary for the row using headers as keys
        row_dict = dict(zip(headers, row))

        # insert client information and embedding into chroma
        json_data = json.dumps(row_dict)

        # Create embedding for client containing all the rows
        embedding_client = openai.Embedding.create(input=json_data, model=model_id)['data'][0]['embedding']

        # Retrieve CustomerId or any other field if needed
        customer_id = row_dict['CustomerId']

        # Insert the row into chroma
        collection.add(documents=[json_data], ids=[customer_id], embeddings=[embedding_client])

        print(f"Inserted client {customer_id} into ChromaDB")
