# NYT-Stories-Web-Application

This repository contains a Slack bot and web application to display various analysis of New York Times Top Stories.

**Backend**
The backend first collects New York Times Top Stories and passes them to the Watson NLU API.The NLU API will analyze the stores for entities and emotion. The python script will then extract entities and one emotion - fear (degree of fear asa score) and then store the entity, emotion (only degree of fear) and date will be stored in the database

**Slackbot**

The Slack Bot will query the database and respond to questions by the user in Slack.

Database Description: The database contains one time variant table (as the data only requires a time variant table). It contains three columns- Entities (extracted from NYT Top Stories extracted using Watson NLU), Fear Component and Date.

Using the bot: The Slack Bot will be able to answer whether a certain entity has been mentioned in New York Times Top Stories by querying the entities column of the database for the particular entity requested.

Question format: "Is XXXXX mentioned in NYT Top Stories?"

_Example Question:_

_User - "Is Spain mentioned in NYT Top Stories?"_

_Bot - Thank you for asking about Spain. Spain has been mentioned in NYT Top Stories._

**Web Application**
The web application will display the data in the entities table in the database desribed above in a tabular format and will query the database for updates in real-time.
