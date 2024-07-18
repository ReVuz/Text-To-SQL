from dotenv import load_dotenv

load_dotenv()

from langchain_community.utilities import SQLDatabase
import streamlit as st

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
  db_uri= f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return SQLDatabase.from_uri(db_uri)
from langchain_core.messages import AIMessage, HumanMessage


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm your SQL assistant.Ask me anything about your database."),
    ]


st.set_page_config(page_title="Text To SQL", page_icon=":speech_balloon:")
st.write("# Text To SQL")

with st.sidebar:
    st.subheader('Settings')
    st.title('Describe the data you want, and I\'ll generate the SQL query to fetch it.')
    st.text_input('Host', value='localhost',key='Host')
    st.text_input('Port', value='3306',key='Port')
    st.text_input('User', value='root',key='User')
    st.text_input('Password', type='password',value='admin',key='Password')
    st.text_input('Database', value='chinook',key='Database')
    if st.button('Connect'):
      with st.spinner('Connecting to the database...'):
        db = init_database(
            st.session_state['User'],
            st.session_state['Password'],
            st.session_state['Host'],
            st.session_state['Port'],
            st.session_state['Database']
        )
        st.session_state.db = db
        st.success('Connected to the database!')
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("User"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)
user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("User"):
        st.markdown(user_query)
    with st.chat_message("AI"):
            response = "I don't know about that yet, but I'm working on it."
            st.markdown(response)
            st.session_state.chat_history.append(AIMessage(content=response))