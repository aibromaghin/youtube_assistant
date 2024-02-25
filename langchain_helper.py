from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import streamlit as st

# Load API key
load_dotenv()
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

# Utilize embeddings from OpenAI
embeddings = OpenAIEmbeddings()

# Function to create vector database
def create_vector_db(video_url: str) -> FAISS:
    # Utilize langchain's youtube loader to get transcript
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    # Split transcript into smaller docs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    # Create FAISS vector database using the smaller docs and OpenAI's embeddings
    db = FAISS.from_documents(docs, embeddings)

    # Return the database
    return db

# Function to answer questions about document with LLM
def get_response_from_query(db, query, k=4):
    # chunk size is 1000, so can send up to 4 docs to llm (k=4)
    # Get documents most relevant to query from database
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([doc.page_content for doc in docs])
    
    # Initialize llm
    llm = OpenAI(model='gpt-3.5-turbo-instruct')

    # Build prompt template to feed to llm
    prompt = PromptTemplate(
        input_variables=['question', 'docs'],
        template="""
                You are a helpful YouTube assistant that can answer questions about videos based on the video's transcript.
                Answer the following question: {question}
                By searaching the following video transcript: {docs}
                Only use the factual information from the transcript to answer the question.
                If you don't have enough information to answer the question, say "I don't know"
                Your answers should be detailed."""
    )
    # Initialize and run the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(question=query, docs=docs_page_content)
    # Format response and return
    response = response.replace('\n', '')
    return response, docs
