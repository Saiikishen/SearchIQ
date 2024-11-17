import uvicorn
from fastapi import FastAPI, Request, Form
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv
import os
import json
from langchain.schema import Document

load_dotenv()

app = FastAPI()
groq_api_key = os.getenv("GROQ_API_KEY")

def setup_chain():
    base_template = """
    You are a knowledgeable AI assistant with information about major technology companies. Based on the following context, provide a clear and accurate response to the user's question.
    
    Context: {context}
    Question: {question}
    
    Provide a well-structured response that includes relevant facts and information from the provided context. If the question is about something not covered in the context, politely indicate that you can only provide information about the companies in your knowledge base (OpenAI, Google, Tesla, Microsoft, and Amazon).
    
    Response:
    
    If the question is outside context politely tell the user that it is outside context and to retry, do not generate false data.
    """
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    embeddings = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    with open('scraped_data.json', 'r') as f:
        data = json.load(f)
    
    docs = []
    for company in data:
        entity = company['entity']
        for result in company['results']:
            content = f"Company: {entity}\nTitle: {result['title']}\nURL: {result['url']}\nInfo: {result['snippet']}"
            docs.append(Document(page_content=content))

    prompt = PromptTemplate(template=base_template, input_variables=["context", "question"])
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 4})  
    chain_type_kwargs = {"prompt": prompt}

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
        verbose=True
    )
    return chain

agent = setup_chain()

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    question = data.get("prompt")
    response = agent.run(question)
    return {"response": response}

def test_chain():
    print("Lauding...")
    test_chain = setup_chain()
    
    test_questions = [
        "what is OpenAI's mission?",
        "when was Tesla founded?",
        "tell me about Microsoft's mission.",
        "who is sai monkey?"
    ]
    
    print("\nRunning test questions...\n")
    for question in test_questions:
        print(f"Question: {question}")
        try:
            response = test_chain.run(question)
            print(f"Response: {response}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    test_chain()