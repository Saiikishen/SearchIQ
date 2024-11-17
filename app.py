import pandas as pd
import streamlit as st
import json
import os
import requests
from utils.file_processing import get_entities_from_column, process_uploaded_file
from utils.web_scraping import scrape_entity_data
import gspread
from google.oauth2.service_account import Credentials


# Initialize the app
st.set_page_config(page_title="SearchIQ", layout="centered")

st.title("SearchIQ")

# Styling
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .stButton>button {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
    }
    .stTextInput>div>div>input {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
    }
    .stFileUploader {
        background-color: #21262d;
        color: #c9d1d9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Google Sheets authentication
def get_google_sheet(sheet_name):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(
        "google_credentials.json", scopes=scopes
    )
    client = gspread.authorize(credentials)

    return client.open(sheet_name)


def fetch_sheet_data(sheet, worksheet_name):
    worksheet = sheet.worksheet(worksheet_name)
    data = worksheet.get_all_values()  # Fetch all rows and columns
    headers = data[0]  # First row as headers
    rows = data[1:]  # Remaining rows as data
    return pd.DataFrame(rows, columns=headers)


# Input source toggle
input_source = st.sidebar.radio("Choose your input source", ["CSV File", "Google Sheets"])

# Handle input
data_ready = False
if input_source == "CSV File":
    st.sidebar.header("Upload a CSV File")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        try:
            df, columns = process_uploaded_file(uploaded_file)
            st.sidebar.success("CSV file uploaded successfully!")
            st.write("### Uploaded Data")
            st.dataframe(df)
            data_ready = True
        except ValueError as e:
            st.sidebar.error(f"Error processing file: {e}")

elif input_source == "Google Sheets":
    st.sidebar.header("Google Sheets Input")
    sheet_name = st.sidebar.text_input("Enter Google Sheet Name", "SearchIQ Results")
    worksheet_name = st.sidebar.text_input("Enter Worksheet Name", "Sheet1")

    if st.sidebar.button("Fetch Data"):
        try:
            with st.spinner("Fetching data from Google Sheets..."):
                sheet = get_google_sheet(sheet_name)
                df = fetch_sheet_data(sheet, worksheet_name)
                st.sidebar.success(f"Data fetched from '{worksheet_name}' in '{sheet_name}'.")
                st.write("### Fetched Data")
                st.dataframe(df)
                data_ready = True
        except Exception as e:
            st.sidebar.error(f"Error fetching data: {e}")

# Process data after input is ready
if data_ready:
    selected_column = st.sidebar.selectbox("Select the main column:", df.columns)
    entities = df[selected_column].unique().tolist()

    if entities:
        st.sidebar.success("Entities extracted successfully!")
        st.write("### Extracted Entities")
        st.write(", ".join(entities))
    else:
        st.sidebar.warning("No entities found in the selected column.")


    if st.sidebar.button("Start Scraping"):
        with st.spinner("Scraping data..."):
            output_file = "scraped_data.json"
            all_results = []

            for entity in entities:
                query = f"Get me the important details regarding {entity}"
                results = scrape_entity_data(query, os.getenv("SERPAPI_KEY"))
                if results:
                    all_results.append({"entity": entity, "results": results})

            if all_results:
                with open(output_file, "w") as json_file:
                    json.dump(all_results, json_file, indent=4)
                st.sidebar.success(f"Scraped data saved to {output_file}.")
            else:
                st.sidebar.warning("No results were found for the entities.")


st.write("### Begin Your Smart Search")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

if st.sidebar.button("Start New Chat"):
    st.session_state.messages = []
    st.session_state.clear_input = True
    st.sidebar.success("New chat session started.")

user_input = st.text_input(
    "Enter your query:",
    key="user_input",
    value="" if st.session_state.clear_input else "",
)

API_URL = "http://127.0.0.1:8000/chat"
if st.button("Send"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            with st.spinner("Fetching response from AI..."):
                response = requests.post(API_URL, json={"prompt": user_input})
                if response.status_code == 200:
                    ai_response = response.json().get("response", "No response received.")
                else:
                    ai_response = f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            ai_response = f"Error connecting to the backend: {e}"

        st.session_state.messages.append({"role": "ai", "content": ai_response})
        st.session_state.clear_input = True

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**AI:** {message['content']}")
