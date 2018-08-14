# In[1]:


#Imports from python library
import requests
import MySQLdb as mdb
import json
from datetime import datetime
import time


# In[2]:


# Retrieve information from New York Times Top Stories using key
url_topstories = 'https://api.nytimes.com/svc/topstories/v2/home.json?api-key=3d02ac6746804ce5b50afd4be21088d5'


# In[3]:


#results_topstories stories data retrieved from api url call
results_topstories = requests.get(url_topstories).json()

#Check the output of the json
results_topstories


# In[4]:


#Define a new function to pass a url to watson and extracts entities, sentiment and emotion
def processURL(url_to_analyze):
    endpoint_watson = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
    params = {
        'version': '2017-02-27',
    }
    headers = {
        'Content-Type': 'application/json',
    }
    watson_options = {
      "url": url_to_analyze,
      "features": {
        "entities": {
          "sentiment": True,
          "emotion": True,
          "limit": 10
        }
      }
    }

    username = "802a033d-ff91-4b02-a6c4-a40703ac1b16"
    password = "TBWFrRx6xwmc"

    resp = requests.post(endpoint_watson, data=json.dumps(watson_options),
                         headers=headers, params=params, auth=(username, password) )
    return resp.json()


# In[5]:


#Create list to store top story urls
nytimes_topstories = []


# In[6]:


#Append each url from top story to the list created above
for elements in results_topstories ["results"]:
    topstories = elements['url']
    nytimes_topstories.append(topstories)


# In[7]:


# Create a function to extract entities
# from the IBM Watson API and returns a list
# of entities that are relevant (above threshold)
# to the article
def getEntities(data, threshold):
    result = []
    for entity in data["entities"]:
        relevance = float(entity['relevance'])
        if relevance > threshold:
            result.append({"entities": entity['text'], "fear": entity ['emotion']['fear']})
    return result


# In[8]:


#Create a new list to store output from watson API
watson_output = []

#Pass each of the in the list of urls, pass it to processUrl to get entities
for url in nytimes_topstories:
    element = processURL (url)

    #Set a threshhold of 0.7 and above for the entitities
    results = getEntities(element, 0.7)
    watson_output.append(results)

#Check output into the list
print(watson_output)


# In[9]:


# This code creates a connection to the database
con = mdb.connect(host = 'localhost',
                  user = 'root',
                  passwd = 'dwdstudent2015',
                  charset='utf8', use_unicode=True);


# In[10]:


# Run a query to create a database that will hold the data
db_name = 'nyt_topstories_entities1'
create_db_query = "CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET 'utf8'".format(db=db_name)

# Create a database
cursor = con.cursor()
cursor.execute(create_db_query)
cursor.close()


# In[11]:


# Create the table for storing entities, fear component and date/time
cursor = con.cursor()
table_name = 'topstories_entities'
create_table_query = '''CREATE TABLE IF NOT EXISTS {db}.{table}
                                (entities varchar (250),
                                 fear varchar(250),
                                 date datetime,
                                 PRIMARY KEY(date, entities)
                                )'''.format(db=db_name, table=table_name)
cursor.execute(create_table_query)
cursor.close()


# In[12]:


# Create a query template and extract query parameters

query_template = '''INSERT IGNORE INTO {db}.{table}(entities,
                                                    fear,
                                                    date)
                    VALUES (%s, %s, %s)'''.format(db=db_name, table=table_name)
cursor = con.cursor()

for entry in watson_output:
    for data in entry:
        entities = data['entities']
        fear = data ['fear']
        date = datetime.now()
        time.sleep(2)
        query_parameters = (entities, fear, date)
        cursor.execute(query_template, query_parameters)

con.commit()
cursor.close()

