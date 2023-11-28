from langchain.document_loaders import PyPDFLoader
from langchain.chat_models.openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Initialize LLM 
llm = ChatOpenAI(
    openai_api_key = OPENAI_API_KEY,
    model_name='gpt-4',
    temperature=0.0
)

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

#create retreival chain using conversational memory
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=vectordb.as_retriever(),
    memory=conversational_memory
)


'''question1 = "Where did she do her bachelors?"
print(question1)
result = qa({"question": question1})
print(result['answer'])
print("--------------------------------")
question2 = "When did she graduate from her bachelors?"
print(question2)
result = qa({"question": question2})
print(result['answer'])
print("--------------------------------")
question3 = "Which city was her bachelors college located in?"
print(question3)
result = qa({"question": question3})
print(result['answer'])
print("--------------------------------")
question4 = "Where is she currently working and as what?"
print(question4)
result = qa({"question": question4})
print(result['answer'])
print("--------------------------------")'''
question5 = "What are her skill sets?"
print(question5)
result = qa({"question": question5})
print("--------------------------------")
print(result['answer'])
