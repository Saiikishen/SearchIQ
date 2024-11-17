import pandas as pd

def process_uploaded_file(uploaded_file):

    try:
        df = pd.read_csv(uploaded_file)
        columns = df.columns.tolist()
        return df, columns
    except Exception as e:
        raise ValueError(f"Error processing file: {e}")

def get_entities_from_column(df, column_name):

    try:
        entities = df[column_name].dropna().tolist()
        return entities
    except KeyError:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
