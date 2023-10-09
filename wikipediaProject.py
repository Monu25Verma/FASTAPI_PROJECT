from pydantic import Field, BaseModel
import logging
from fastapi import FastAPI
#from dataset import Dataset
import requests
import os


app = FastAPI()

#from pymongo.mongo_client import MongoClient

#uri = "mongodb+srv://admin:zGVimRk8Z4M6SdlE@cluster0.n3sfji4.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server

#client = MongoClient(uri)

# Send a ping to confirm a successful connection


#try:

#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)

#serilizer/ deserializer
class wiki_data(BaseModel):
    id : str
    title : str
    text : str


#title, id, text

#to get title
@app.post("/{title}")                #url for title
def get_title(title : str):         #to create function for title
    wiki = get_wikipedia_page(title)   #calss call to pass column name
    
    return (dict(wiki))

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
    ).json()
    
    page = next(iter(response['query']['pages'].values()))
    page.info("G/et Page details")
    
    return {
        'id': page['pageid'],
        'title': page['title'],
        'text': page['extract'],
    }





