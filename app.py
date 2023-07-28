import os
from tempfile import NamedTemporaryFile
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from utils import json_csv
#import const

#load_dotenv()

app=Flask(__name__)

openaiservicename = 'ms-openai-cosmos'
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = '2023-05-15'
os.environ["OPENAI_API_BASE"] = f"https://{openaiservicename}.openai.azure.com"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY 

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file_path')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


'''def database_connection():
     db = SQLAlchemy()
     db_name = '''''


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        if 'file' not in request.files:
            return "No File Part"
        
        user_file = request.files['file']
        
        if user_file:
                
            filename = secure_filename(user_file.filename)

            if filename.endswith(".csv"):
                user_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))      
    
                with NamedTemporaryFile() as f: # Create temporary file
                    f.write(user_file.getvalue()) # Save uploaded contents to file
                    f.flush()
                    llm=OpenAI(engine='text-davinci-002', temperature=0)
                    user_question = request.form['query']
                    agent=create_csv_agent(llm, f.name, verbose=True,  early_stopping_method="generate")

                if user_question is not None and user_question != "":
                    response = agent.run(user_question)

            elif filename.endswith(".json"):
                user_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
                json_csv(user_file.getvalue().decode('utf-8')) #converting the json file to csv for the csv agent
                llm=OpenAI(engine='text-davinci-002', temperature=0)
                user_question = request.form['query']
                file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                agent=create_csv_agent(llm, 'file_path/test.csv', verbose=True, early_stopping_method="generate")

                if user_question is not None and user_question != "":
                    response = agent.run(user_question)
                
            return response
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port="4999",debug=True)