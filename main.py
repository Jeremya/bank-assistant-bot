import streamlit as st
from dotenv import dotenv_values
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from tools import TotalRevenueReaderTool, ClientSimilarityTool

##############################
### initialize agent #########
##############################
tools = [TotalRevenueReaderTool(), ClientSimilarityTool()]
config = dotenv_values('.env')
openai_key = config['OPENAI_API_KEY']

conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

llm = ChatOpenAI(
    openai_api_key=openai_key,
    temperature=0,
    model_name="gpt-3.5-turbo"
)

agent = initialize_agent(
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    max_iterations=5,
    verbose=True,
    memory=conversational_memory,
    early_stopping_method='generate'
)

# set title
st.title('Ask a question about total revenue only please')

# set header
st.header("Please ask now")

user_question = st.text_input('Ask a question about total revenue only please:')
if user_question:
    with st.spinner(text="In progress..."):
        response = agent.run(user_question)
        st.write(response)

