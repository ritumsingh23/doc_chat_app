from tempfile import NamedTemporaryFile
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
# import os

# OPENAI_API_KEY=os.environ['OPENAI_API_KEY']

def main():
    load_dotenv()

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV")

    user_csv = st.file_uploader("Upload your csv file", type="csv")

    if user_csv is not None:
        with NamedTemporaryFile() as f: # Create temporary file
            f.write(user_csv.getvalue()) # Save uploaded contents to file
            f.flush()
            llm=OpenAI(temperature=0)
            user_question = st.text_input("Ask a question to your csv:")
            agent=create_csv_agent(llm, f.name, verbose=True)

        if user_question is not None and user_question != "":
            response = agent.run(user_question)

            st.write(response)


if __name__ == "__main__":
    main()