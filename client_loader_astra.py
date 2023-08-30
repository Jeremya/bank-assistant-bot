import csv

import openai
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from dotenv import dotenv_values
from cassandra.query import SimpleStatement

# Description: This file will load the clients dataset into Astra DB

# parameters #########
config = dotenv_values('.env')
openai.api_key = config['OPENAI_API_KEY']
SECURE_CONNECT_BUNDLE_PATH = config['SECURE_CONNECT_BUNDLE_PATH']
ASTRA_CLIENT_ID = config['ASTRA_CLIENT_ID']
ASTRA_CLIENT_SECRET = config['ASTRA_CLIENT_SECRET']
ASTRA_KEYSPACE_NAME = config['ASTRA_KEYSPACE_NAME']
model_id = "text-embedding-ada-002"

# Open a connection to the Astra database
cloud_config = {
    'secure_connect_bundle': SECURE_CONNECT_BUNDLE_PATH
}
auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# This function will load a CSV and insert values into the Astra database
# Input format:
# RowNumber,CustomerId,Surname,
# CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Exited,
# Complain,Satisfaction Score,Card Type,Point Earned
#
# Astra table columns:
# client_id, surname, credit_score, location, gender, age, balance, has_credit_card,
# estimated_salary, satisfaction_score, card_type, point_earned, embedding_client


with open('resources/clients-dataset.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader) # skip header row
    query = SimpleStatement(f"INSERT INTO {ASTRA_KEYSPACE_NAME}.ClientById (client_id, surname, credit_score, location, gender, age, " \
            "balance, has_credit_card, estimated_salary, satisfaction_score, card_type, point_earned, " \
            "embedding_client) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    for row in reader:
        client_id = int(row[1])
        surname = row[2]
        credit_score = int(row[3])
        location = row[4]
        gender = row[5]
        age = int(row[6])
        balance = float(row[8])
        has_credit_card = bool(row[10])
        estimated_salary = float(row[12])
        satisfaction_score = int(row[14])
        card_type = row[16]
        point_earned = int(row[17])

        # Create embedding for client containing all the rows
        embedding_client = openai.Embedding.create(input=row, model=model_id)['data'][0]['embedding']

        # Insert values into Astra database
        session.execute(query, (client_id, surname, credit_score, location, gender, age, balance, has_credit_card,
                                estimated_salary, satisfaction_score, card_type, point_earned, embedding_client))

## TODO
# failed to bind prepared statement on embedding type
# cassandra.InvalidRequest: Error from server: code=2200 [Invalid query] message="cannot parse '?' as hex bytes"