import json
import pandas as pd
from pandas import json_normalize
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os 

Connection_String_to_blob = os.environ.get('Connection_String_to_blob')

def get_blob_service_client():
    connection_string = Connection_String_to_blob
    return BlobServiceClient.from_connection_string(connection_string)

def upload_to_blob_storage(file_path, filename):
    blob_service_client = get_blob_service_client()
    container_name = 'peearzchatdocupload'  # Create a container in your Blob storage account

    # Get a blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    # Upload the file to Blob storage
    with open(file_path, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)

def json_csv(path_to_store, file):
    dictionary = json.loads(file)

    df = None
    first = True

    for document in dictionary:
        if document == None:
            continue
        else:
            dfLeft = json_normalize(document)

        for title, value in document.items():
            if type(value) == list:
                dfLeft.drop(title, axis="columns", inplace=True)
                dfRight = json_normalize(value)
                dfRight = dfRight.add_prefix(f"{title}_")
                dfLeft = pd.concat([dfLeft, dfRight], axis = 1)    

        if first:
            df = dfLeft
            first = False
        else:
            df = pd.concat([df, dfLeft], axis = 0)

    df.reset_index(inplace=True, drop=True)

    df1 = df.T.drop_duplicates().T

    #file_location = os.path.join(app.config['UPLOAD_FOLDER'])
    #df1.to_csv('file_path/test.csv')

    df1.to_csv(os.path.join(path_to_store, 'test.csv'))
    upload_to_blob_storage(os.path.join(path_to_store, 'test.csv'), 'test.csv')

'''import os 
import sys
import json
import csv
import pandas as pd
from pandas import json_normalize
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from exception import CustomException

Connection_String_to_blob = os.environ.get('Connection_String_to_blob')

def get_blob_service_client():
    connection_string = Connection_String_to_blob
    return BlobServiceClient.from_connection_string(connection_string)

def upload_to_blob_storage(file_path, filename):
    blob_service_client = get_blob_service_client()
    container_name = 'peearzchatdocupload'  # Create a container in your Blob storage account

    # Get a blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    # Upload the file to Blob storage
    with open(file_path, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)

def fetch_file_from_blob(container_name, blob_name, destination_path):
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    with open(destination_path, "wb") as file:
        blob_data = blob_client.download_blob()
        file.write(blob_data.readall())

def json_csv(path_to_store, file):

    print("File Content:")
    print(file)
    try:
        dictionary = json.loads(file)

    except json.JSONDecodeError as e:
        print("JSON Parsing Error : ", e)
        print("FILE CONTENT : ")
        print(file)
        raise CustomException("Error parsing JSON content.", sys)
    
    except Exception as e:
        print("Unexpected Error:", e)
        raise CustomException("Unexpected error occurred while processing JSON content.", sys)    

    df = None
    first = True

    for document in dictionary:
        if document == None:
            continue
        else:
            dfLeft = json_normalize(document)

        for title, value in document.items():
            if type(value) == list:
                dfLeft.drop(title, axis="columns", inplace=True)
                dfRight = json_normalize(value)
                dfRight = dfRight.add_prefix(f"{title}_")
                dfLeft = pd.concat([dfLeft, dfRight], axis = 1)    

        if first:
            df = dfLeft
            first = False
        else:
            df = pd.concat([df, dfLeft], axis = 0)

    df.reset_index(inplace=True, drop=True)

    df1 = df.T.drop_duplicates().T

    #file_location = os.path.join(app.config['UPLOAD_FOLDER'])
    #df1.to_csv('file_path/test.csv')

    df1.to_csv(os.path.join(path_to_store, 'test.csv'))
    upload_to_blob_storage(os.path.join(path_to_store, 'test.csv'), 'test.csv')

def json_csv(json_file_path, csv_file_path):
    """
    Convert a JSON file to a CSV file.

    Parameters:
        json_file_path (str): Path to the input JSON file.
        csv_file_path (str): Path to the output CSV file.
    """
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    with open(csv_file_path, 'w', newline='') as csv_file:
        # Extract the headers from the first item in the JSON data
        headers = list(data[0].keys())

        # Create a CSV writer and write the header row
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        # Write each row to the CSV file
        writer.writerows(data)

def download_blob_to_file(container_name='peearzchatdocupload'):
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob="test.csv")
    with open(file=os.path.join(r'/Users/ankitanand/Documents/Peearz/', 'test.csv'), mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob =  download_stream.readall()
        return sample_blob'''