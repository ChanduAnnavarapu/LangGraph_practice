import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

config={'configurable':{'thread_id':'thread_1'}}


user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
            {'messages':[HumanMessage(content=user_input)]},
            config={'configurable':{'thread_id':'thread_1'}},
            stream_mode='messages')
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
print(st.session_state)