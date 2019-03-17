# NYT-Stories-Web-Application

This repository contains a Slack bot and web application to display analysis of New York Times Top Stories.

**Server**

The server first collects New York Times Top Stories and sends them to the Watson NLU API.The NLU API will analyze the stories for entities and emotion. Next, the python script extracts entities and one emotion - fear (degree of fear as a score) and stores them with a timestamp in the database

**Database**

The database contains one time variant table. The table contains three columns - Entities (extracted from NYT Top Stories through Watson NLU), Fear Component and Date.

**Slackbot Client**

The Slack Bot answers whether a certain entity has been mentioned in New York Times Top Stories by querying the entities column of the database for the particular request.

Question format: "Is XXXXX mentioned in NYT Top Stories?"

_Example Question:_

_User - "Is Spain mentioned in NYT Top Stories?"_

_Bot - Thank you for asking about Spain. Spain has been mentioned in NYT Top Stories._

**Web Application**

The web application displays the data from the entities table in the database described above in a tabular format and retrieves updates in real-time.
