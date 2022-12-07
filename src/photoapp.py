# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 18:00:18 2022
"""

from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3 as sql
import os
import shutil
from google_images_search import GoogleImagesSearch
import cv2

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
        desiredName = request.form["nameofphoto"]               #name of photo
        selectedAlbum = request.form["albums"]                  #chosen album
        
        #obtain the album id so photos can be added to location table
        con = sql.connect("photos.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select ID from ALBUM where ALBNAME=?", (selectedAlbum,))
        result = cur.fetchone()
        albumID = int(result[0])
        
        #This is needed or there is an error on submission
        #The plus 1 was added because for some strange reason the API always pulled 1 less image then asked for
        amountPhotoRequest = int(amountPhotoRequest)
        
        #setup api connection
        gis = GoogleImagesSearch('AIzaSyCEUrQCpyHvV9crC6mOnXQWi3dFmwu_H2o', '409f2a1ba9a2a4dd4')

        #defined search parameters (Taken from API site example and modified slightly)
        _search_params = {
            'q': '',
            'num': 0,
            'fileType': 'jpg|gif|png',
            'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
            'safe': 'active', ##
            'imgType': 'photo' ##
        }
        
        #modify parameters based on user input
        _search_params["q"] = queryPhotoName
        _search_params["num"] = amountPhotoRequest
        
        #create path to folder for download
        downloadPath = mainDir + "/" + selectedAlbum
        
        # search for images based on the search parameters
        gis.search(search_params=_search_params, custom_image_name = desiredName)

        for image in gis.results():
            image.url  # image direct url
            image.referrer_url  # image referrer url (source) 
            
            #Change this to your file path :D
            image.download(downloadPath)  # download image
                
            print(image.path)       #This was to test it saved to the correct location on my pc
                
            orgFilePath = image.path
            orgFilePath = orgFilePath.replace("\\", "/")
            #print(orgFilePath)
            
            #get name the file is stored as (most helpful when multiple images downloaded)
            splitPath = orgFilePath.split(downloadPath + "/")
            oriName = splitPath[1]
            
            extRem = oriName.split(".")
            orgFileName = extRem[0]
            
            curSize = os.path.getsize(orgFilePath) #bytes
            curImage = cv2.imread(orgFilePath)
            curHeight, curWidth = curImage.shape[:2]
            
            imagePathSplit = orgFilePath.split(origDir + "/")
            curImagePath = imagePathSplit[1]
            
            defaultDesc = "This is a photo of " + queryPhotoName
            
            cur.execute("insert into PHOTO(PNAME, PDESC, WIDTH, HEIGHT, FILESIZE, PATH) values (?,?,?,?,?,?)", (orgFileName, defaultDesc, curWidth, curHeight, curSize, curImagePath))
            con.commit()
            
            #get photo id so it can be added to locations table
            #IMPORTANT
            #I THINK THIS LINE IS CAUSING THE ISSUE WITH DISPLAYING THE SAME PHOTO
            #THIS SHOULD BE BECAUSE THE PHOTOS HAVE THE SAME NAME DESPITE HAVING DIFFERENT PATHS
            #snake.jpg, snake.JPG, snake.jpeg, and snake.png would all have the name of snake
            #hypothetically selecting ID based on PATH should fix
            cur.execute("select ID from PHOTO where PNAME=?", (orgFileName,))
            cur.execute("select ID from PHOTO where PATH=?", (curImagePath,))
            pIDresult = cur.fetchone()
            curPhotoID = int(pIDresult[0])
            
            cur.execute("insert into LOCATIONS(A_ID, P_ID) values (?,?)", (albumID, curPhotoID))
            con.commit()
            

        return redirect(url_for("home"))
    
    else:
        con = sql.connect("photos.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from ALBUM")
        albums = cur.fetchall()
        
        return render_template("getphotos.html", data = albums)

#Route to test passing album info
@app.route("/information")
def information():
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ALBUM")
    albums = cur.fetchall()
    
    return render_template("albumdirectory.html", data = albums)

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
    
    #I made a change here to add the if
    if(os.path.exists(photoPath)):
        os.remove(photoPath)
    
    return redirect(url_for("albumRUD"))


#This drives the program by creating the instance of the Seivom Backend and Running the Flask App
if __name__ == "__main__":
    app.run(debug=True)
    
    