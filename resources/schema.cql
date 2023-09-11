USE YOUR_KEYSPACE_NAME_HERE;

DROP TABLE IF EXISTS ClientById;

CREATE TABLE IF NOT EXISTS TotalRevenueByClient (
    client_id INT PRIMARY KEY,
    total_revenue DECIMAL,
    update_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ClientById (
    client_id INT,
    surname TEXT,
    credit_score INT,
    location TEXT,
    gender TEXT,
    age INT,
    balance DECIMAL,
    has_credit_card BOOLEAN,
    estimated_salary DECIMAL,
    satisfaction_score INT,
    card_type TEXT,
    point_earned INT,
    embedding_client vector<float, 1536>,
    PRIMARY KEY (client_id)
);

CREATE TABLE IF NOT EXISTS TransactionByCustomer (
    client_id INT,
    embedding_transaction vector<float, 1536>,
    PRIMARY KEY (client_id)
);

CREATE CUSTOM INDEX IF NOT EXISTS openai_client ON ClientById (embedding_client) USING 'org.apache.cassandra.index.sai.StorageAttachedIndex';

INSERT INTO TotalRevenueByClient (client_id, total_revenue, update_time) VALUES (1, 123123.42, dateOf(now()));
