import json
import pandas as pd
from pandas import json_normalize

def json_csv(location):
    dictionary = json.loads(location)

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

    df1.to_csv('data_files/ready_to_use.csv')