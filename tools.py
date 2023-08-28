from langchain.tools import BaseTool
from langchain.text_splitter import CharacterTextSplitter

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import dotenv_values
import openai

import streamlit as st

### parameters #########
config = dotenv_values('.env')
openai.api_key = config['OPENAI_API_KEY']
SECURE_CONNECT_BUNDLE_PATH = config['SECURE_CONNECT_BUNDLE_PATH']
ASTRA_CLIENT_ID = config['ASTRA_CLIENT_ID']
ASTRA_CLIENT_SECRET = config['ASTRA_CLIENT_SECRET']
ASTRA_KEYSPACE_NAME = config['ASTRA_KEYSPACE_NAME']

# Open a connection to the Astra database
cloud_config = {
    'secure_connect_bundle': SECURE_CONNECT_BUNDLE_PATH
}
auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()


### Total Revenue Reader Tool #########
class TotalRevenueReaderTool(BaseTool):
    name = "Total Revenue Reader"
    description = "This tool will read the total revenue from the Astra database"

    def _run(self, client_id):  # add user uuid
        client_id = "1"
        query = f"SELECT total_revenue FROM {ASTRA_KEYSPACE_NAME}.TotalRevenueByClient WHERE client_id = {client_id}"
        rows = session.execute(query)
        for row in rows:
            st.write(row.total_revenue)

        return row.total_revenue

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


### ClientSimilarityTool #########
class ClientSimilarityTool(BaseTool):
    name = "Client Similarity Tool"
    description = "This tool will find the most similar client to the given client on different critera like credit card"

    def _run(self, user_question):
        model_id = "text-embedding-ada-002"
        embedding = openai.Embedding.create(input=user_question, model=model_id)['data'][0]['embedding']
        query = f"SELECT client_id, surname, credit_score, location, gender, age, balance, has_credit_card, " \
                f"estimated_salary, satisfaction_score, card_type, point_earned FROM {ASTRA_KEYSPACE_NAME}.ClientById " \
                f"ORDER BY embedding_client ANN OF {embedding} LIMIT 1 "
        rows = session.execute(query)

        client_list = []
        for row in rows._current_rows:
            brand_dict = {f"client id is {row.client_id}, current balance is {row.balance}, client's surname is {row.surname}, age is {row.age}, gender is {row.gender} , card type owned by client is {row.card_type}, credit score is {row.credit_score}, satisfaction score is {row.satisfaction_score}, point earned is {row.point_earned}, this client is located in {row.location}, client has a credit card is {row.has_credit_card}"}
            client_list.append(brand_dict)

        return client_list

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")
