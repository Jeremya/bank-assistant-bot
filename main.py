import streamlit as st
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from dotenv import dotenv_values
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from langchain.memory import CassandraChatMessageHistory
from langchain.schema import SystemMessage

config = dotenv_values('.env')
astra_or_chroma = config['ASTRA_OR_CHROMA']
openai_key = config['OPENAI_API_KEY']

### Load Tools #########
if astra_or_chroma == "astra":
    from tools.tools_astra import TotalRevenueReaderTool, ClientSimilarityTool, GetClientInformationTool
    tools = [TotalRevenueReaderTool(), ClientSimilarityTool(), GetClientInformationTool()]

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
    astraSession = cluster.connect()

    conversational_memory = CassandraChatMessageHistory(
        session_id='bankflix-conversation-666',
        session=astraSession,
        keyspace=ASTRA_KEYSPACE_NAME,
        ttl_seconds=3600,
    )
    conversational_memory.clear()
else: # chroma
    from tools.tools_chroma import ClientSimilarityTool
    tools = [ClientSimilarityTool()]
    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        ai_prefix='AI',
        k=5,
        return_messages=True
    )

system_message = SystemMessage(content="You are Bankflix, a sophisticated bank assistant, specialized in credit scores and "
                                       "currency transactions. With expert knowledge and precision, you are here to "
                                       "provide accurate information and solutions to banking queries.")

### Initialize the LangChain Agent #########
llm = ChatOpenAI(
    openai_api_key=openai_key,
    temperature=0,
    model_name="gpt-3.5-turbo"
)

agent = initialize_agent(
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    max_iterations=3,
    verbose=False,
    chat_memory=conversational_memory,
    handle_parsing_errors=True,
    early_stopping_method='generate',
    agent_kwargs={
        "system_message": system_message.content
    }
)

# set title
st.title('🏦 BankFlix Chatbot')

# set header
st.header("Welcome dear bank employee!")

user_question = st.text_input('Ask a question here:')

# if the question has more than 5 characters, run the agent
if len(user_question) > 5:
    with st.spinner(text="In progress..."):
        conversational_memory.add_user_message(user_question)
        response = agent.run(input=user_question, chat_history=conversational_memory.messages)
        st.write(response)

