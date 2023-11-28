from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms.openai import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import PyPDFLoader
from langchain.docstore import document
import asyncio

from config import timeout, upsert_batch_size
from dotenv import load_dotenv

import pinecone 
import os
import re

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")


#create pinecone index
async def createPineconeIndex(indexName, vectorDimensions):
    print("Initialzing Pinecone Environment")
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    print("Checking: ", indexName)
    try:
        active_indexes = pinecone.list_indexes() 
        if indexName not in active_indexes:
            print("Creating index: ", indexName)
            status = pinecone.create_index(indexName, dimension=vectorDimensions, metric='cosine')
            print("Creating index..please wait for it to finish initialization")
            return status
        else:
            print(indexName, " already exists")
    except Exception as e:
        err = "Error while checking for Index" + str(e)
        return err
    

def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()
    return contents

def process_pdf(file_path):

    try:
        #load pdf document
        loader = PyPDFLoader(file_path)
        data = loader.load()
        #split document into chunks
        text_chunks =  RecursiveCharacterTextSplitter(chunk_size = 1000)
        documents = text_chunks.split_documents(data)
        texts = [str(docs) for docs in documents]
        return texts, documents
    except Exception as e:
        err = "Error while processing pdf file and creating chunks: ", str(e)
        return err

def create_embeddings(texts):
    try:
        embeddings_array = []
        res = None
        for text in texts:
            text = re.sub(r'\n', ' ', text)
            res =  OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY).embed_documents(text)
            embeddings_array.append(res)
        return embeddings_array
    except Exception as e:
        err = "Error while creating embeddings: ", str(e)
        return err
    



#upload data to pinecone index - indexName and docs: path to document folder
async def updatePinecone(indexName, docs):
    print("Entering updatePinecone function...")
    try:
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
        index = pinecone.Index(indexName)
        print("Pinecone index was retrieved: ", indexName)
        
        try:
            for root, dirs, files in os.walk(docs):
                
                for file_name in files:
                    if file_name.endswith(".pdf"):
                        pdf_path = os.path.join(root, file_name)
    
                        print("Processing document:", pdf_path)
                        chunks, documents = process_pdf(pdf_path)
                        
                        print(f"Calling OpenAI's embedding endpoint document with {len(chunks)} text chunks")
                        embeddings = create_embeddings(chunks)
                        for i in range(0, 1):
                            print(embeddings[i])
                        '''print(f"Creating {len(chunks)} vector array with id, values and metadata..")
                        batch = []
                        for idx in range(len(documents)):
                            chunk = documents[idx]
                            
                            vector = {
                                "id": file_name + str(idx),
                                "values": embeddings[idx],
                                "metadata": {
                                    "page_content": chunk.page_content,
                                    "source": chunk.metadata['source'],
                                    "page": chunk.metadata['page']
                                }
                            }
                            batch.append(vector)

                            if len(batch) == upsert_batch_size or idx == len(documents) - 1:
                                try:
                                    await index.upsert(
                                        vectors=batch
                                    )
                                except Exception as e:
                                    print("error while inserting: " + str(e))

                                batch = []
                        print("upsert of vectors in index completed successfully")'''
                                  
        except Exception as e:
            return e
        
    except Exception as e:
        err = "Error while updating Index: " + str(e)
        return err

async def main():
    
    
    
    res = await updatePinecone('semantic-search-index',"/Users/suchi_bigmac/Documents/GEN-AI-Applications/semantic-search-App/middleware/documents/Specification/lenshub" )
    print(res)
if __name__ == "__main__":
    asyncio.run(main())