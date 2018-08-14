# In[1]:


#Import MySQL database from python libraries
#This code creates a connection to the database
from flask import Flask, render_template
from flask import request
import MySQLdb as mdb

con = mdb.connect(host = '0.0.0.0',
                  user = 'root',
                  database = 'nyt_topstories_entities1',
                  passwd = 'dwdstudent2015',
                  charset='utf8', use_unicode=True);


# In[ ]:


# This code queries the database
#for the entities, fear and date (the three columns of the table)
#It then returns the fetched data as 'data'

cur = con.cursor(mdb.cursors.DictCursor)

cur.execute("SELECT entities, fear, date FROM topstories_entities")
data = cur.fetchall()
cur.close()
con.close()

#Checkpoint: to ensure that the data
#is being fetched print every element in data
for d in data:
    print(d)
    print("-----")


# In[ ]:


#Run the webserver.py file that implements the html template
get_ipython().magic(u'run webserver.py')

