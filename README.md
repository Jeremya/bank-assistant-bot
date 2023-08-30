# bank-assistant-bot
Bank Assistant chat bot using LLM and AstraDB

## Pre-requisites

- Python 3.6+
- Launch an [AstraDB](https://astra.datastax.com/) database
- AstraDB SCB and Credentials

## Setup

- Clone the repository
- Install the dependencies
- Add your Astra info and OpenAI token in `.env` file
- Run `client_loader.py` to import fake clients data in AstraDB
- Run `main.py` using the command `streamlit run main.py`
