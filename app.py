
import sqlite3
import streamlit as st
import google.generativeai as genai
import pandas as pd
import re

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDs_CiMSSOkQP2VwluCMeDHbl0JfeVAiT0")

# Set up Streamlit app
st.title("WELCOME TO ASK SQL")

# File uploader widget
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Predefined SQL-related keywords for detection
SQL_KEYWORDS = [
    "select", "where", "order by", "group by", "sum", "count", "avg", 
    "average", "max", "min", "distinct", "join", "having", "like",
    "tell me ", "show me ", "what is", "give me", "list", "find", 
    "fetch", "retrieve", "display", "get", "how many", "number of", 
    "total", "top", "most", "least", "lowest", "highest", "with", 
    "without", "filter", "between", "more than", "less than", 
    "greater than", "smaller than", "equal to", "before", "after", "show me","show"
    "earlier", "later", "starting with", "ending with", "compare", 
    "difference", "grouped by", "segmented by", "categorized by", 
    "last week", "last month", "last year", "yesterday", "today", 
    "this week", "this month", "this year", "in the past", "since", 
    "over time", "per day", "per month", "per year", "how much", 
    "calculate", "sum up", "average out", "add up", "aggregate", 
    "combine", "link", "related to", "connected with", "Can you show me", 
    "I want to know", "Could you tell me", "I'm looking or", 
    "Help me find", "Can I see"
]

# Predefined conversational responses
def handle_conversational_input(input_text):
    input_text_lower = input_text.strip().lower()
    if input_text_lower in ["hi", "hello", "hey"]:
        return "Hello! How can I assist you today?"
    elif input_text_lower in ["how are you?", "what's up?"]:
        return "I'm great, thanks! How about you?"
    elif input_text_lower in ["what can i do here?", "what is this?", "help"]:
        return "Upload a dataset and ask questions about it using natural language or SQL-like commands."
    elif input_text_lower in ["bye", "goodbye", "exit"]:
        return "Goodbye! Have a nice day!"
    else:
        return None  # Default to None if no match

if uploaded_file:
    # Load the uploaded dataset
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    # Display the DataFrame
    st.write("### Data Preview:")
    st.dataframe(df)

    # Text input for user question
    user_question = st.text_input("Ask a question about your dataset:")

    if user_question:
        # First, handle conversational inputs
        conversational_response = handle_conversational_input(user_question)
        if conversational_response:
            st.write(conversational_response)
        else:
            # Check if the input contains SQL-related keywords
            if any(keyword in user_question.lower() for keyword in SQL_KEYWORDS):
                try:
                    # Generate SQL query using the LLM
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = (
                        "Write a valid SQLite query for the dataset. "
                        "The table name is 'user_table'. "
                        f"The dataset preview is:\n{df.head(5)}\n"
                        f"The question is: {user_question}"
                    )
                    response = model.generate_content(prompt)
                    llm_generated_query = (
                        response.text.strip()
                        .replace("```sqlite", "")
                        .replace("```", "")
                        .strip()
                    )

                    # Validate generated SQL query
                    if llm_generated_query.lower().startswith("select"):
                        conn = sqlite3.connect(":memory:")
                        df.to_sql("user_table", conn, index=False, if_exists="replace")
                        try:
                            result_df = pd.read_sql_query(llm_generated_query, conn)
                            conn.close()

                            if result_df.empty:
                                st.write("Query executed successfully, but no results were found.")
                            else:
                                st.write("Query Results:")
                                st.dataframe(result_df)
                        except Exception as sql_error:
                            st.write(f"SQL execution error: {sql_error}")
                    else:
                        st.write("The query generated doesn't seem valid. Please try rephrasing your question.")
                except Exception as generation_error:
                    st.write(f"Error generating query: {generation_error}")
            else:
                # Provide guidance for unrecognized inputs
                st.write(
                    "I couldn't recognize your input as a SQL query or a meaningful question. "
                    "Try asking something like:\n"
                    "- 'Show all rows where age > 30.'\n"
                    "- 'What is the average salary?'\n"
                    "- 'Count the number of females in the dataset.'"
                )
else:
    st.write("Please upload a dataset to proceed.")

# Sidebar instructions
st.sidebar.header("Help and Instructions")
st.sidebar.write("""
### Examples:
- "What is the average age?"
- "Show rows where salary > 5000."
- "Count entries where gender = 'Female'."
- "Group by department and sum the salaries."

Upload a dataset to get started!
""")

# The Key Issue:
# SQLite Database Connections: SQLite keeps a database connection open during read and write operations. 
# If the connection is closed prematurely (such as when the conn.close() call is made), further attempts 
# to interact with the database (e.g., executing a query) will fail with an error like Cannot operate on 
# a closed database.