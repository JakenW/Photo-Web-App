# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 18:00:18 2022
"""

from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3 as sql
import os

#Creating the flask app
app = Flask(__name__)

#Creating a secret key for the flask app. Required when using sessions.
app.secret_key = "thebestsecretkeyintheworldyep100percentthebestnodoubt"

#Defining the system path to the folder as a global variable
#Change this on your system for it to function properly
#On windows, the line will give you errors if your filepath has \ instead of /
mainDir = "C:/Users/theja/Documents/photo app test/photo storage"

#Route to the homepage of the website
@app.route("/")
def home():
    return render_template("index.html")


#Route to the search form which obtains the date from the user
@app.route("/addalbum/", methods=["POST", "GET"])
def search():
    #If the request method is post, we want to extract the date
    if request.method == "POST":
        
        #This line extracts the date from the form
        albumName = request.form["albname"]     #Album name
        albumDesc = request.form["albdes"]      #Album description
        
        #Add album information to the local database
        con = sql.connect("photos.db")
        cur = con.cursor()
        cur.execute("insert into ALBUM(ALBNAME, ALBDESC) values (?,?)", (albumName, albumDesc))
        con.commit()
        
        #Create the directory for the album locally
        newDirPath = os.path.join(mainDir, albumName)
        os.mkdir(newDirPath)
        
        #This goes to a placeholder page, we should create one which lets them know it was successfully created
        return render_template("albcreatetest.html")
    
    else:
        #If the resuest is not a post, go to the original form
        return render_template("addalbum.html")

#Route to test passing album info
@app.route("/information")
def information():
    return render_template("information.html")

#This drives the program by creating the instance of the Seivom Backend and Running the Flask App
if __name__ == "__main__":
    app.run()
    
    
