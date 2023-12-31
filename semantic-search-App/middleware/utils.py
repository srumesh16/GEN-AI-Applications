from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms.openai import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
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

file_path = "/Users/suchi_bigmac/Documents/GEN-AI-Applications/semantic-search-App/middleware/output.txt"

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
        res = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY).embed_documents(texts)
        
        
        return res
        '''for text in texts:
            text = re.sub(r'\n', ' ', text)
            res =  OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY).embed_documents(text)
            embeddings_array.append(res)
        return embeddings_array'''

        
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

                        print("creating embeddings for ", len(chunks), " chunks..")
                        embeddings = create_embeddings(chunks)

                           
                        print(len(embeddings), " embeddings has been created")
                        print(f"Creating {len(chunks)} vector array with id, values and metadata..")
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
                        print("upsert of vectors in index completed successfully")
                                  
        except Exception as e:
            return e
        
    except Exception as e:
        err = "Error while updating Index: " + str(e)
        return err


#Answering question over document using LLM
async def queryPineconeVectorStoreandQueryLLM(indexName, question):
    

    print("intializing pinecone index.")
    try:
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
        index = pinecone.Index(indexName)
    except Exception as e:
        return("Error while initializing pinecone index: " + str(e))
    
    print("embeding question..: " + str(question))
    try:
        queryEmbeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY).embed_query(question)
    except Exception as e:
        return("Error while embedding question: " + str(e))
    
    print("getting revelant index related to the question from pinecone (query)...")
    try:
        queryResponse = index.query(
            top_k= 10,
            vector= queryEmbeddings,
            include_metadata= True,
            include_values= True
        )

        print(f"Found {len(queryResponse['matches'])} matches..")
        
    except Exception as e:
        return("Error while quering pinecone index with question: " + str(e))
    
    
    
    print(f"Asking question: {question}")
    try:
        if len(queryResponse['matches']) != 0:
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            print("created llm chain...")
            concatenated_page_content = " ".join(
            [match['metadata']['page_content'] for match in queryResponse['matches']]
            )   
            documents = [
                {"page_content": match['metadata']['page_content']}
                for match in queryResponse['matches']
            ]
            

            print("concated relavent pages..")
            try:
                result = chain.run(
                    input_documents=queryResponse['matches'],
                    question=question,
                )

                return result
            except Exception as e:
                return("Error while answering from LLM: ", str(e))
    except Exception as e:
        return("Error while running llm: ", str(e))
    


    
async def main():
    
    res = await queryPineconeVectorStoreandQueryLLM('semantic-search-index',"What is initialize()?" )
    print(res)
if __name__ == "__main__":
    asyncio.run(main())