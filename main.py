#References:https://clasense4.wordpress.com/2012/07/29/python-redis-how-to-cache-python-mysql-result-using-redis/
#https://opensource.com/article/18/4/how-build-hello-redis-with-python
#https://docs.microsoft.com/en-us/azure/redis-cache/cache-python-get-started
#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, request
import urllib
import datetime
import json
import pypyodbc
import time
import random
import pickle
import hashlib
import redis

server = 'quiz8suraj.database.windows.net'
database = 'quiz8suraj'
username = 'serveradmin'
password = 'Surajk1234'
driver = '{ODBC Driver 13 for SQL Server}'
app = Flask(__name__)
R_SERVER = redis.Redis(host='surajkawthekar1.redis.cache.windows.net',
        port=6379, db=0, password='BggbcvhdtVHgXL8LLnrmLNjR6t2ylVY1Dn2YjKzootk=')

# print("Opened database successfully")

# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print("Table created successfully")
# conn.close()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    cnxn = pypyodbc.connect('DRIVER=' + driver + ';SERVER=' + server
                            + ';PORT=1443;DATABASE=' + database
                            + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    starttime = time.time()
    cursor.execute('SELECT TOP 8000 * from [Earthquake]')
    rows = cursor.fetchall()
    endtime = time.time()
    duration = endtime - starttime
    return render_template('city.html', ci=rows, timedur=duration)


@app.route('/quakerange1', methods=['GET'])
def quake1():
    # connect to DB2
    magn = float(request.args.get('mag'))
    magn1 = float(request.args.get('mag1'))
    location = request.args.get('loc')
    query1 = float(request.args.get('query'))

    cnxn = pypyodbc.connect('DRIVER=' + driver + ';SERVER=' + server
                            + ';PORT=1443;DATABASE=' + database
                            + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    starttime = time.time()
    cursor.execute("select * from [Earthquake] where mag>'"+ str(magn) +"' and mag<'"+ str(magn1) +"' and net ='"+str(location)+"'")  
    rows = cursor.fetchall()
    endtime = time.time()
    duration = endtime - starttime
    return render_template('viewrange.html',ci=rows,timedur=duration)

@app.route('/quakelocation', methods=['GET'])
def quakeradius():
    # connect to DB2
    cnxn = pypyodbc.connect('DRIVER=' + driver + ';SERVER=' + server
                            + ';PORT=1443;DATABASE=' + database
                            + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    lati = float(request.args.get('latitude'))
    longi = float(request.args.get('longitude'))
    rad = float(request.args.get('radius'))
    
    longi1 = longi-(rad*0.014)
    longi2 = longi+(rad*0.014)
    lati1 = lati-(rad*0.014)
    lati2 = lati+(rad*0.014)    

    starttime = time.time()
    cursor.execute("select * from [Earthquake] where latitude >'" + str(lati1) +"' and latitude < '" +str(lati2) +"' and longitude > '" + str(longi1) + "' and longitude < '" + str(longi2) +"'" )
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
    rows = cursor.fetchall()
    endtime = time.time()
    duration = endtime - starttime
    return render_template('viewradius.html', timedur=duration, ci=rows ,l1=lati,l2=longi,r=rad)

if __name__ == '__main__':
    app.run(debug=True)
