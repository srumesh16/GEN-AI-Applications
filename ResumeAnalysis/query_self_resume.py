from langchain.document_loaders import PyPDFLoader
from langchain.chat_models.openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

from dotenv import load_dotenv
import os

import streamlit as st

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇",
    placeholder="Paste your OpenAI API key, sk-",
    type="password")

uploaded_file = st.sidebar.file_uploader("#### Upload Resume", type="pdf")

#resume uploaded
if uploaded_file:

    #store resume in data/
    resume_path = os.path.join("data", uploaded_file.name)
    with open(resume_path, "wb") as f:  # Use "wb" for writing in binary mode
        f.write(uploaded_file.read()) 
    
    st.sidebar.success("Resume uploaded successfully")
    #Load PDF Document
    loader = PyPDFLoader("data/Resume-Self.pdf")

    #Split the PDF document into pages
    pages = loader.load_and_split()

    #Initialize chunk size and split the pages into smaller chuncks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 150
    )
    docs = text_splitter.split_documents(pages)

    #Create OPENAI Embeddings
    embeddings = OpenAIEmbeddings()

    #Chroma VectorStore to store the embeddings of the pdf chunks
    persist_directory = ""
    vectordb = Chroma.from_documents(
        documents = docs,
        embedding=embeddings,
        persist_directory = persist_directory
    )

    #Create conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key = 'chat_history',
        k = 5,
        return_message = True
    )

    #Initialize LLM 
    if user_api_key is not None:
        llm = ChatOpenAI(
            openai_api_key = user_api_key,
            model_name='gpt-4',
            temperature=0.0
        )
    else:
        #Initialize LLM 
        llm = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY,
            model_name='gpt-4',
            temperature=0.0
        )


    #create retreival chain using conversational memory
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectordb.as_retriever(),
        memory=conversational_memory
    )


    if 'history' not in st.session_state:
        st.session_state.history = []

     # User input at the bottom of the page
    user_input = st.text_input("Type your query here..")

    if st.button("Send"):
        if user_input:
            # Add user message to history
            st.session_state.history.append(("user", user_input))

            # Get bot response
            result = qa({"question": user_input})
            bot_response = result['answer']

            # Add bot response to history
            st.session_state.history.append(("bot", bot_response))
            user_input = ""
    
    # Display chat history
    for sender, message in st.session_state.history:
        if sender == "user":
            st.text_input("You:", message, key=f"user_{message}")
        elif sender == "bot":
            st.text_input("Bot:", message, key=f"bot_{message}")
        

   