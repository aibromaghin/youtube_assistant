import streamlit as st
import langchain_helper as lch
import textwrap

st.title('Hi there! :wave:')
st.header('I\'m your personal Youtube Assistant :sunglasses:')
st.subheader('I\'m here to answer any questions you have about a YouTube video.')
st.subheader('To use me, simply paste a video URL into the box on the left, write your question, and click "Submit"!:ok_hand:')

with st.sidebar:
    with st.form(key='my_form'):
        youtube_url = st.sidebar.text_area(
            label="What is the YouTube video URL?",
            max_chars=200
        )
        query = st.sidebar.text_area(
            label="Ask me about the video",
            max_chars = 100,
            key='query'
        )

        submit_button = st.form_submit_button(label='Submit')


if query and youtube_url:
    db = lch.create_vector_db(youtube_url)
    response, doc = lch.get_response_from_query(db=db, query=query)
    st.subheader('Answer: ')
    st.text(textwrap.fill(response, width=80))