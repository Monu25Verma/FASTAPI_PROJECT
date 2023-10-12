from pydantic import Field, BaseModel
import logging
from fastapi import FastAPI, Request
#from dataset import Dataset
import requests
from pymongo import MongoClient
from dotenv import dotenv_values   #to call data from .env
from fastapi.encoders import jsonable_encoder


config  = dotenv_values(".env")

#serilizer/ deserializer
class wiki_data(BaseModel):
    id : str
    title : str
    text : str

app = FastAPI()            # return in string format
#title, id, text

#to get title
@app.post("/{title}")                #url for title
def get_title(request: Request, title : str):         #to create function for title
    wiki = get_wikipedia_page(title)   #class call to pass column name
    dict(wiki)
    #print(list(request.app.database["lists"].find(limit=50)))
    list = jsonable_encoder(title)
    new_list_item = request.app.database["lists"].insert_one(list)
    created_list_item = request.app.database["lists"].find_one({"title":new_list_item.inserted_title})
    print(created_list_item)
    return {'message':'Database Entry Done'}



@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_CONNECTION_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to MONGODB database!")

@app.on_event("shutdown")
def shut_down_db_client():
    app.mongodb_client.close()

# utility/commoncode
def get_wikipedia_page(title):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'explaintext': True,
        }
    ).json() #json/dictionary
    
    page = next(iter(response['query']['pages'].values()))
    
    return {
        'id': page['pageid'],
        'title': page['title'],
        'text': page['extract'],
    }





