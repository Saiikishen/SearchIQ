# **SearchIQ**

SearchIQ is a user-friendly application that combines intelligent data extraction, entity scraping, and AI-powered question-answering to help you gain insights from your data. With support for CSV file uploads and Google Sheets as data sources, SearchIQ enables seamless integration of your data into an AI-driven workflow.

---

## **Features**
- **Dual Input Sources**:
  - Upload `.csv` files for processing.
  - Use data directly from Google Sheets.
- **Entity Extraction**:
  - Extract key entities from your selected column.
- **Web Scraping**:
  - Automatically scrape details for extracted entities using the SerpAPI.
- **AI-Powered Q&A**:
  - Ask questions based on your data and get precise responses powered by a Retrieval-Augmented Generation (RAG) pipeline.
- **Dynamic Chat Interface**:
  - Chat with the AI assistant in a sleek, user-friendly interface.
  - Start new chat sessions seamlessly.

---

## **Technologies Used**
- **Backend**:
  - [FastAPI](https://fastapi.tiangolo.com/): For API-based RAG model integration.
- **Frontend**:
  - [Streamlit](https://streamlit.io/): For a clean and interactive user interface.
- **Google Sheets API**:
  - Fetch data directly from Google Sheets.
- **FAISS**:
  - Fast indexing and similarity search for embeddings.
- **SerpAPI**:
  - For web scraping and extracting additional details about entities.
- **LangChain**:
  - To implement RAG-based AI workflows.
- **SentenceTransformers**:
  - For embedding generation and vectorization.

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/<your-username>/SearchIQ.git
cd SearchIQ
```

### **2. Set Up the Environment**
Create a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### **3. Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### **4. Set Up API Keys**
* **SerpAPI**:
  * Create an account at SerpAPI.
  * Add your API key to your environment variables:
    ```bash
    export SERPAPI_KEY="your-serpapi-key"
    ```
* **Groq API**:
   * Create an acout at Groq
   * Add your API key to environment variables:
  ```bash
    export GROQ_API_KEY="your-groq_api-key"
    ```
     
* **Google Sheets API**:
  * Download the `google_credentials.json` file from your Google Cloud project.
  * Place it in the project directory.

### **5. Run the Application**
Start the **FastAPI** backend:
```bash
uvicorn llm_rag:app --reload
```

Start the **Streamlit** frontend:
```bash
streamlit run app.py
```

  ![SearchIQ Dataflow](/sys_arch.png)

  Video Link:
  ```
https://saikishen-pv.neetorecord.com/watch/45a10482-79ac-4fbb-ba51-d74c420323d6```

