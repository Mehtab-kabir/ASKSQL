Project:  Ask SQL - A Natural Language Query System

Overview:
This project is a user-friendly interface built with Streamlit that allows users to interact with datasets in a conversational manner. Users can upload CSV or Excel files, and the system will allow them to ask SQL-like questions using natural language. The backend generates SQL queries using a generative AI model and returns the results based on the uploaded dataset.

Key Features:
1. File Upload: Users can upload CSV or Excel files directly into the system.
2. Data Preview: The system provides a preview of the first few rows of the dataset after upload, giving users an immediate look at the data.
3. Natural Language Query: Users can ask questions in plain English, like "What is the average age?" or "Show all rows where salary > 5000."
4. AI-Generated SQL Queries: The backend uses a Google Generative AI model to convert user input into SQL queries, even if the user doesn’t know SQL.
5. Query Execution**: After generating a valid SQL query, the system executes it and returns the results.

How It Works:
1. Upload Dataset: The user uploads a CSV or Excel file.
![image](https://github.com/user-attachments/assets/3bb8a31a-97a5-4515-b7b9-532be955c9e6)

2. Data Preview: Once the file is uploaded, a preview of the dataset is displayed.
![image](https://github.com/user-attachments/assets/dc2c233b-5b87-4fe4-9710-eb463dcf1efd)

3. 4. Ask Questions: The user can input natural language queries. The system will identify SQL-related keywords in the input.
5. AI Query Generation: The system sends the question to the generative AI model (Google Gemini), which returns a valid SQL query.
6. Query Execution: The system executes the generated SQL query on the uploaded dataset and displays the results.
![image](https://github.com/user-attachments/assets/6b94ea0a-c3bb-4094-bdf2-44c7a91263d4)

7. Conversational Responses: For non-SQL questions or greetings, the system responds with predefined conversational responses.

Technologies Used:
- Streamlit: For building the interactive user interface.
- Google Generative AI (Gemini) For generating SQL queries from natural language input.
- Pandas For data manipulation and previewing datasets.

Instructions for Use:
1. Upload a CSV or Excel file using the file uploader.
2. Ask a question about your dataset in natural language.
3. The system will generate an SQL query, execute it on the dataset, and return the results.

Example Questions:
- "What is the average salary?"
- "Show all rows where age > 30."
- "Count the number of males in the dataset."
- "Group by department and sum the salaries."

Installation:
Clone the repository and install the required packages:

```bash
git clone <repository-url>
cd <project-directory>
pip install -r requirements.txt
```

Run the application with:

```bash
streamlit run app.py
```
---
