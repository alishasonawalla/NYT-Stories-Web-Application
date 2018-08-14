# In[1]:


#Imports from python library
import time
import re
import requests
import json
import MySQLdb as mdb
from slackclient import SlackClient


# In[2]:


#This function allows our bot to determine if the message is for our bot
#The function takes in the text of the message in the Slack channel and
#the user ID of the Bot
def message_is_for_our_bot(user_id, message_text):
    '''
    Check if the username and the word 'bot' appears in the text
    '''
    regex_expression = '.*@' + user_id + '.*bot.*'
    regex = re.compile(regex_expression)
    # Check if the message text matches the regex above
    match = regex.match(message_text)
    # returns true if the match is not None (ie the regex had a match)
    return match != None


# In[3]:


#This funtion extracts the entity mentioned by the user
#in the question to the Bot
#It takes in the message by the user
def extract_entity_mention(message_text):
    '''
    Extract the entity name mentioned after "Is" and before "mentioned".
    The regex relies on the question following the given pattern,
    so that we can extract the name of the entity.
    '''
    regex_expression = 'Is (.+) mentioned in NYT Top Stories?'
    regex= re.compile(regex_expression)
    matches = regex.finditer(message_text)
    for match in matches:
        # return the first captured phrase
        # which is between "Is" and "mentioned"
        #in case the user mentions multiple entities
        return match.group(1)

    # if there were no matches, return None
    return None


# In[4]:


#This function takes in the name of the entity being requested.
#It then connects to the database and queries the databse for the entity
#It returns "exists" if the entity was found and "doesn't exist" if the entity wasn't found
def get_nyt_topstories(entity):

    #Establish connection to the database
    con = mdb.connect(host = 'localhost',
                  user = 'root',
                  database = 'nyt_topstories_entities1',
                  passwd = 'dwdstudent2015',
                  charset='utf8', use_unicode=True)

    #Design a query template to search
    #the database for how many times the entity was mentioned.
    #Topstories_entities is the name of the table .
    query_template = '''
        SELECT COUNT(entities)
        FROM topstories_entities
        WHERE entities = %s
    '''
    #Execute the query using the input from the user "entity"
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(query_template, (entity,) )
    entity = cur.fetchall()
    cur.close()
    con.close()

    #If the count == 0, then the entity doesn't exist
    #Then return "doesn't exist"
    if (entity[0]['COUNT(entities)'] == 0):
        return "doesn't exist"

    #Else, if the count != 0, then the entity does exist
    #Then return "exists"
    else:
        return "exists"

#Checkpoint: pass through a random string of charachters "hgkl"
#This phrase should obviously not exist in the Top Stories
#Therefore, the function must return "doesn't exist", which it does
#So the function works!
get_nyt_topstories('hgkl')


# In[5]:


#This function determins what message must be returned to the user
#This function takes in the entity to be searched for in the database
def create_message(entity):

    #If the entity isn't empty then thenk the user for asking about the entity
    if entity != None:
        message = "Thank you for asking about " + entity + ". "

        # Call the function get_nyt_topstories to query the database
        #for the entity requested by the user
        # We search the database for entities that match "entity"
        matching_entity = get_nyt_topstories(entity)

        # If the count of "entity" is not 0
        # Then the function should have returned "exists"
        # So if matching_entity has "exists"
        # Then we tell the user that the entity has been mentioned in NYT Top Stories
        if matching_entity == "exists":
            message += entity +" has been mentioned in NYT Top Stories.\n"

        # Otherwise, if the count of "entity" is 0
        # Then the function should have returned "doesn't exist"
        # So if matching_entity has "doesn't exist"
        # Then we tell the user that the entity hasn't been mentioned in NYT Top Stories
        if matching_entity == "doesn't exist":
            message += entity + " hasn't been mentioned in NYT top stories.\n"

    #If the message from the user is not in the desired regex format
    #Then tell the user that the Bot couldn't understand and that the
    #user must input in the specified format
    else:
        message = "Unfortunately I did not understand the entity you are asking for.\n"
        message += "Ask me `Is XXXXX mentioned in NYT Top Stories ?` and I will try to answer."
    return message

#Checkpoint: if a random string is passed into the function it should return
#Thank you for asking about gggkjlk. gggkjlk hasn't been mentioned in NYT top stories
#So the function works!
create_message('gggkjlk')


# In[6]:


#This function processes a slack event
#The Slack RTM (real time messaging) generates a lot of events.
#We want to examine them all but only react to:
    #1. Messages
    #2. ...that come from a user
    #3. ...that ask our bot to do something
    #4. ...and act only for messages for which we can extract the data we need

#If we manage to extract an entity name, we proceed to query the database

def process_slack_event(event):

    # Check that the event is a message. If not, ignore and proceed to the next event.
    if event.get("type") != 'message':
        return None

    # Check that the message comes from a user. If not, ignore and proceed to the next event.
    # We do not reply to bots, to avoid getting into infinite loops of discussions with other bots
    if event.get("user") == None:
        return None

    # Check that the message is asking the bot to do something. If not, ignore and proceed to the next event.
    message_text = event.get('text')
    if not message_is_for_our_bot(bot_user_id, message_text):
        return None

    # Extract the entity name from the user's message
    entity = extract_entity_mention(message_text)

    # Prepare the message that we will sent back to the user
    message = create_message(entity)

    #Return the message
    return message


# In[ ]:


# This is the beginning of the program. We just read
# the access token from the file and create the Slack Client
secrets_file = 'slack_secret.json'
f = open(secrets_file, 'r')
content = f.read()
f.close()

auth_info = json.loads(content)
auth_token = auth_info["access_token"]
bot_user_id = auth_info["user_id"]

# Connect to the Real Time Messaging API of Slack and process the events
sc = SlackClient(auth_token)

#Checkpoint: If acces has been granted return True
sc.rtm_connect()


# In[ ]:


# We are going to be polling the Slack API for recent events continuously
while True:
    # We are going to wait 1 second between monitoring attempts
    time.sleep(1)
    # If there are any new events, we will get a list of events.
    # If there are no events, the response will be empty
    events = sc.rtm_read()
    for event in events:

        # Check if we should generate a response for the event
        response = process_slack_event(event)

        if response:
            # Post a message to Slack channel with our response
            message = response
            sc.api_call("chat.postMessage", channel="#assignment2_bots", text=message)

