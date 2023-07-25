import os
from tempfile import NamedTemporaryFile
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent
from dotenv import load_dotenv
import const

#load_dotenv()

app=Flask(__name__)

openaiservicename = 'ms-openai-cosmos'
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = '2023-05-15'
os.environ["OPENAI_API_BASE"] = f"https://{openaiservicename}.openai.azure.com"
os.environ["OPENAI_API_KEY"] = const.OPENAI_API_KEY 

def database_connection():
     db = SQLAlchemy()
     db_name = ''


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        if request.files['file']:
                
                user_csv = request.files['file']

                if user_csv is not None:
                    with NamedTemporaryFile() as f: # Create temporary file
                        f.write(user_csv.getvalue()) # Save uploaded contents to file
                        f.flush()
                        llm=OpenAI(engine='text-davinci-002', temperature=0)
                        user_question = request.form['query']
                        agent=create_csv_agent(llm, f.name, verbose=True)

                    if user_question is not None and user_question != "":
                        response = agent.run(user_question)

        return response
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port="4999",debug=True)