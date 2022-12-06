# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 18:00:18 2022
"""

from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3 as sql
import os
import shutil

#Creating the flask app
app = Flask(__name__)

#Creating a secret key for the flask app. Required when using sessions.
app.secret_key = "thebestsecretkeyintheworldyep100percentthebestnodoubt"

#Defining the system path to the folder as a global variable
#Change this on your system for it to function properly
#On windows, the line will give you errors if your filepath has \ instead of /
mainDir = "C:/Users/theja/Documents/photo app test/static"
origDir = "C:/Users/theja/Documents/photo app test"


#Route to the homepage of the website
@app.route("/")
def home():
    #anytime we come back to the home page change os's directory back to the original
    os.chdir(origDir)
    return render_template("index.html")


#Route to create albums with information specified by the user
@app.route("/addalbum/", methods=["POST", "GET"])
def addalbum():
    #If the request method is post, we want to extract the album information
    if request.method == "POST":
        
        #This line extracts the date from the form
        albumName = request.form["albname"] #query
        albumDesc = request.form["albdes"] #num photos
        
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
    
#Route obtain photos with information specified by the user
@app.route("/getphotos/", methods=["POST", "GET"])
def getphotos():
    #If the request method is post, we want to extract the album information
    if request.method == "POST":
        
        #This line extracts the date from the form
        queryPhotoName = request.form["queryName"]              #search term
        amountPhotoRequest= request.form["amountRequest"]       #number of photos
        
        '''
        before returning the html template, there are a few things to do:
        1. Modify the search parameters to represent the term and number 
        specified by the user. (This can be done based off the apicase.py
        file on github by modifying dictionary values)
        2. Search the api based on the newly created search parameters (
        this can also be based on the apicase.py file.)
        3. Inside the for loop for results from the api, the photo needs
        to be downloaded locally and then meta-data about each
        image must be tracked and placed within the database.
        
        Grayson: Work on 1 and 2 in this area as it relates with the API,
        if you need help I (Jaken) can help you with it
        
        Once the API is pulling images based on the user input information,
        I (Jaken) will add in the code for part 3 which will collect 
        the meta-data and store it on the database 
        '''
        
        #redirect(url_for("albcreatetest.html"))
        #Should render a placeholder template which says photos properly downloaded or something
        #The text placeholder will need to be replaced with an HTML file 
        return render_template("placeholder")
    
    else:
        #If the resuest is not a post, go to the original form
        return render_template("getphotos.html")

#Route to test passing album info
@app.route("/information")
def information():
        #return redirect(url_for("information.html"))
        return render_template("information.html")

#Route to test passing album info
@app.route("/albums")
def albums():
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ALBUM")
    albums = cur.fetchall()
    
    return render_template("albums.html", data = albums)

'''
#Route to test passing album info
@app.route("/albumspage/<string:aid>")
def albumspage(aid):
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
    result = cur.fetchone()
    albName = str(result[0])
    cur.execute("select ALBDESC from ALBUM where ID=?", (aid,))
    descresult = cur.fetchone()
    descAlb = str(descresult[0])
    
    cur.execute("select * from LOCATIONS where A_ID=?", (aid,))
    photoIDs = cur.fetchall()
        
    photoList = []
    for row in photoIDs:
        cur.execute("select * from PHOTO where ID=?", (row[2],))
        curPhoto = cur.fetchone()
        photoList.append(curPhoto)
    
    return render_template("albumspage.html", albumName = albName, albumDescription = descAlb, data = photoList)

@app.route("/selTest2:<string:aid>", methods=["POST", "GET"])
def selTest2(aid):
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
    result = cur.fetchone()
    albName = str(result[0])
    
    cur.execute("select * from LOCATIONS where A_ID=?", (aid,))
    photoIDs = cur.fetchall()
        
    photoList = []
    for row in photoIDs:
        cur.execute("select * from PHOTO where ID=?", (row[2],))
        curPhoto = cur.fetchone()
        photoList.append(curPhoto)
        
    return render_template("seltest.html", albumName = albName, data = photoList)
'''
    
#Route to test passing album info
@app.route("/albumspage:<string:aid>", methods=["POST", "GET"])
def albumspage(aid):
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
    result = cur.fetchone()
    albName = str(result[0])
    cur.execute("select ALBDESC from ALBUM where ID=?", (aid,))
    descresult = cur.fetchone()
    descAlb = str(descresult[0])
    
    cur.execute("select * from LOCATIONS where A_ID=?", (aid,))
    photoIDs = cur.fetchall()
        
    photoList = []
    for row in photoIDs:
        cur.execute("select * from PHOTO where ID=?", (row[2],))
        curPhoto = cur.fetchone()
        photoList.append(curPhoto)
    
    return render_template("albumspage.html", albumName = albName, albumDescription = descAlb, data = photoList)



'''
Below are routes I used for testing stuff on my end
'''
@app.route("/JKNtesting")
def test():
    return render_template("JKNtesting.html")

#Album Specific Stuff
@app.route("/albumRUD")
def albumRUD():
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ALBUM")
    albums = cur.fetchall()
    return render_template("albumRUD.html", data = albums)

@app.route("/editAlbum/<string:aid>", methods=["POST", "GET"])
def editAlbum(aid):
    if request.method == "POST":
        albname = request.form["albname"]
        albdesc = request.form["albdesc"]
        
        #first check if the edited name is already a directory
        #if so return to the main page
        
        os.chdir(mainDir)
        for file in os.listdir():
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                continue
            if albname == file:
                return redirect(url_for("home"))
        
        #change back to original directory if no file matches edited name
        os.chdir(origDir)
        
        
        con = sql.connect("photos.db")
        cur = con.cursor()
        cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
        result = cur.fetchone()
        
        '''
        cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
        result = cur.fetchone()
        '''
        cur.execute("update ALBUM set ALBNAME=?, ALBDESC=? where ID=?", (albname, albdesc, aid))
        con.commit()
        
        #Change name locally
        #Need to think about names already existing D:
        oldAlbName = str(result[0])
        oldPath = os.path.join(mainDir, oldAlbName)
        newPath = os.path.join(mainDir, albname)
        os.rename(oldPath, newPath)
        
        return redirect(url_for("albumRUD"))
    
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ALBUM where ID=?", (aid,))
    album = cur.fetchone()
    return render_template("editAlbum.html", data = album)

@app.route("/deleteAlbum/<string:aid>", methods=["GET"])
def deleteAlbum(aid):
    con = sql.connect("photos.db")
    cur = con.cursor()
    cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
    result = cur.fetchone()
    cur.execute("delete from ALBUM where ID=?", (aid,))
    con.commit()
    
    albumName = str(result[0])
    DirPath = os.path.join(mainDir, albumName)
    shutil.rmtree(DirPath)
    
    return redirect(url_for("albumRUD"))

@app.route("/selectAlbum", methods=["POST", "GET"])
def selectAlbum():
    if request.method == "POST":
        
        #This line extracts the date from the form
        selID = request.form["selalbum"] 
        
        session["selalbum"] = selID    #This saves the session data so we can pass it to information
        
        #This goes to a placeholder page, we should create one which lets them know it was successfully created
        return redirect(url_for("selTest"))
    
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ALBUM")
    albums = cur.fetchall()
    return render_template("selectAlbum.html", data = albums)

@app.route("/selTest", methods=["POST", "GET"])
def selTest():
    if "selalbum" in session:
        #Assign the session date as a variable called date
        selAlbID = session["selalbum"]
        session.pop("selalbum", None)
    
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select ALBNAME from ALBUM where ID=?", (selAlbID,))
    result = cur.fetchone()
    albName = str(result[0])
    
    cur.execute("select * from LOCATIONS where A_ID=?", (selAlbID,))
    photoIDs = cur.fetchall()
        
    photoList = []
    for row in photoIDs:
        cur.execute("select * from PHOTO where ID=?", (row[2],))
        curPhoto = cur.fetchone()
        photoList.append(curPhoto)
        
    return render_template("seltest.html", albumName = albName, data = photoList)

@app.route("/selTest2:<string:aid>", methods=["POST", "GET"])
def selTest2(aid):
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
    result = cur.fetchone()
    albName = str(result[0])
    
    cur.execute("select * from LOCATIONS where A_ID=?", (aid,))
    photoIDs = cur.fetchall()
        
    photoList = []
    for row in photoIDs:
        cur.execute("select * from PHOTO where ID=?", (row[2],))
        curPhoto = cur.fetchone()
        photoList.append(curPhoto)
        
    return render_template("seltest.html", albumName = albName, data = photoList)


@app.route("/editPhoto/<string:pid>", methods=["POST", "GET"])
def editPhoto(pid):
    if request.method == "POST":
        photoname = request.form["photoname"]
        photodesc = request.form["photodesc"]
        photopath = request.form["photopath"]
        
        #first check if the edited name is already in the folder
        #if so return to the main page
        splitPath = photopath.split("/")
        curAlb = splitPath[1]
        curDir = mainDir + "/" + curAlb
        
        os.chdir(curDir)
        for file in os.listdir():
            if photoname in file:
                return redirect(url_for("home"))
        
        #change back to original directory if no file matches edited name
        os.chdir(origDir)
        
        con = sql.connect("photos.db")
        cur = con.cursor()
        cur.execute("select PNAME from PHOTO where ID=?", (pid,))
        nameresult = cur.fetchone()
        
        #Change name locally
        #Need to think about names already existing D:
        oldPhotoName = str(nameresult[0])
        
        dirList = mainDir.split("static")
        modDir = dirList[0]

        oldFilePath = modDir + photopath
        splitCur = photopath.split(oldPhotoName)
        
        newPhotoPath = splitCur[0] + photoname + splitCur[1]

        newFilePath = modDir + newPhotoPath
        
        os.rename(oldFilePath, newFilePath)
        
        cur.execute("update PHOTO set PNAME=?, PDESC=?, PATH=? where ID=?", (photoname, photodesc, newPhotoPath, pid))
        con.commit()
        
        return redirect(url_for("albumRUD"))
    
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from PHOTO where ID=?", (pid,))
    photo = cur.fetchone()
    return render_template("editPhoto.html", data = photo)

@app.route("/deletePhoto/<string:pid>", methods=["GET"])
def deletePhoto(pid):
    con = sql.connect("photos.db")
    cur = con.cursor()
    cur.execute("select PATH from PHOTO where ID=?", (pid,))
    pathresult = cur.fetchone()
    cur.execute("delete from LOCATIONS where P_ID=?", (pid,))
    con.commit()
    cur.execute("delete from PHOTO where ID=?", (pid,))
    con.commit()
    
    oldPhotoPath = str(pathresult[0])

    dirList = mainDir.split("static")
    modDir = dirList[0]
    photoPath = modDir + oldPhotoPath
    
    os.remove(photoPath)
    
    return redirect(url_for("albumRUD"))


#This drives the program by creating the instance of the Seivom Backend and Running the Flask App
if __name__ == "__main__":
    app.run(debug=True)
    
    