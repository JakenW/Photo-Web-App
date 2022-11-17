# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 18:00:18 2022
"""

from flask import Flask, redirect, url_for, render_template, request, session

#Creating the flask app
app = Flask(__name__)


#Creating a secret key for the flask app. Required when using sessions.
app.secret_key = "thebestsecretkeyintheworldyep100percentthebestnodoubt"


#Route to the homepage of the website
@app.route("/")
def home():
    if "date" in session:
        session.pop("date", None)
    return render_template("index.html")


#Route to the search form which obtains the date from the user
@app.route("/addalbum/", methods=["POST", "GET"])
def search():
    #If the request method is post, we want to extract the date
    if request.method == "POST":
        
        #This line extracts the date from the form
        albumName = request.form["albname"]
        albumDesc = request.form["albdes"]
        queryPhotoName = request.form["queryName"]
        amountPhotoRequest= request.form["amountRequest"]
        
        session["name"] = albumName            #This saves the session data so we can pass it to information
        session["desc"] = albumDesc            #This saves the session data so we can pass it to information
        session["query"] = queryPhotoName      #This saves the session data so we can pass it to information
        session["amount"] = amountPhotoRequest #This saves the session data so we can pass it to information
        
        return redirect(url_for("information"))
    
    else:
        #If the resuest is not a post, go to the original form
        #Since users can create a new search from the results page, we want to clear session data
        if "name" in session:
            session.pop("name", None)
        if "desc" in session:
            session.pop("desc", None)
            
        return render_template("addalbum.html")

#Route to test passing album info
@app.route("/information")
def information():
    #Check to confirm there is a date stored in the current session
    if "name" in session:
        #Assign the session date as a variable called date
        name = session["name"]
    
    if "desc" in session:
        #Assign the session date as a variable called date
        desc = session["desc"]
        
    if "query" in session:
        #Assign the session date as a variable called date
        desc = session["query"]    
        
    if "amount" in session:
        #Assign the session date as a variable called date
        desc = session["amount"]
        '''
        Here would be code to create the directory locally.
        I have not yet done this.
        '''
        
        return render_template("information.html", name = name, desc = desc)
    
    else:
        #If there is not date in the session and someone is trying to access this page, send them to the form.
        return redirect(url_for("addalbum"))

#This drives the program by creating the instance of the Seivom Backend and Running the Flask App
if __name__ == "__main__":
    app.run()
    
    
