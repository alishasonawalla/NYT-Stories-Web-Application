#Import from python libraries 
from flask import Flask, render_template
from flask import request
import MySQLdb as mdb


app = Flask(__name__)

#Create a new url with /entities
#Connect to the database 
#Create a query to revterieve the data from the database 
@app.route('/entities')
def nyt_entities():
    
    entities = request.args.get('entities')
   
    #Establish connection to database
    con = mdb.connect(host = '0.0.0.0', 
                  user = 'root',
                  database = 'nyt_topstories_entities1',
                  passwd = 'dwdstudent2015', 
                  charset='utf8', use_unicode=True);

    cur = con.cursor(mdb.cursors.DictCursor)
  
    #Execute query to extract data from the tables 
    cur.execute("SELECT entities, fear, date FROM topstories_entities")
    data = cur.fetchall()
    cur.close()
    con.close()

    #Display using the entities.html template 
    return render_template('entities.html', data = data, entities = entities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
