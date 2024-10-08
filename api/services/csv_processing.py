import os
import sqlite3
import re
import requests

from django.conf import settings
import pandas as pd
from openai import OpenAI as OpenAIAPI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from transformers import pipeline
from langchain_openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key for OpenAI is not set.")

client = OpenAIAPI(api_key = api_key)

def csv_processing(document, query):
    """
    Process the CSV file and augment the data with the given query.
    """

    file_name = document.file_name
    csv_path = os.path.join(settings.MEDIA_ROOT, 'documents', file_name)

    db_file = 'data.db'
    csv_to_sqlite(csv_path, db_file, 'data')

    # Convert the query to SQL and execute it
    result = query_to_sql(query, db_file)
    
    # Augment the result with the query
    augmented_result = augment_data_with_query(result, query)

    return augmented_result

def query_to_sql(query, db_file):
    """
    Convert the natural language query to SQL and execute it on the database.
    """

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    db = SQLDatabase.from_uri(f"sqlite:///{db_file}")

    # Initialize the language model
    llm = OpenAI(api_key=api_key)
    chain = create_sql_query_chain(llm, db)
    
    # Invoke the chain to get the SQL query response
    response = chain.invoke({"question": query})

    # Execute the SQL query and return the result
    result = db.run(response)

    return result

def augment_data_with_query(db_results, question):
    """
    Augment the data with the given query.
    """

    if not db_results:
        print("No data available for augmentation.")
        return None
    
    # Prepare the prompt
    prompt = f"Using only the following data:\n{db_results}\n\nProvide a direct answer to the question: '{question}' without adding any additional information."

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that synthesizes a response given a query and a search result."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message 

    
def csv_to_sqlite(csv_file, db_file, table_name):
    """
    Read a CSV file and write its contents to a SQLite database table.
    """

    # Read the CSV file
    try:
        df = pd.read_csv(csv_file)
        print("CSV file read successfully.")
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        return
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        return
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the CSV file.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file)

    # Write the DataFrame to the SQLite table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Validate dimensions
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]

    cursor.execute(f"PRAGMA table_info({table_name})")
    column_count = len(cursor.fetchall())

    # Close the cursor
    cursor.close()

    # Check if dimensions match
    if (row_count, column_count) == df.shape:
        print(f"Validation successful: Database dimensions match CSV ({row_count} rows, {column_count} columns).")
    else:
        print(f"Validation failed: Database dimensions ({row_count} rows, {column_count} columns) do not match CSV ({df.shape[0]} rows, {df.shape[1]} columns).")

    # Commit and close the connection
    conn.commit()

    # Print out the content of the database table
    df_from_db = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    print("\nContent of the database:")
    print(df_from_db)



