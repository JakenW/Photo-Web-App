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
    
    '''
    Below we connect to the database and pull all the album information.
    This is done so that the slideshow on the homepage displays information about
    the albums dynamically.
    '''
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ALBUM")
    albums = cur.fetchall()
    
    return render_template("index.html", data = albums)


#Route to create albums with information specified by the user
@app.route("/addalbum/", methods=["POST", "GET"])
def addalbum():
    #If the request method is post, we want to extract the album information and create the album
    if request.method == "POST":
        
        #These lines extract user data from the form
        albumName = request.form["albname"]     #album name
        albumDesc = request.form["albdes"]      #album description
        
        '''
        Check to see if a directory with the specified name already exists
        If so, redirect to a page telling them it already exists.
        '''
        os.chdir(mainDir)
        for file in os.listdir():
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".gif"):
                continue
            if file == albumName:
                os.chdir(origDir)
                return render_template("editalbum_unsuccess.html")
        
        #change back to original directory if no file matches edited name
        os.chdir(origDir)
        
        '''
        The lines below connect to the database and create a new album
        in the database based on the user's data
        '''
        con = sql.connect("photos.db")
        cur = con.cursor()
        cur.execute("insert into ALBUM(ALBNAME, ALBDESC) values (?,?)", (albumName, albumDesc))
        con.commit()
        
        '''
        Below the local file path is constructed so that there is a 
        directory on the local file system
        '''
        newDirPath = os.path.join(mainDir, albumName)
        os.mkdir(newDirPath)
        
        '''
        We then redirect to page which tells the user that the album creation
        was successful.
        '''
        return render_template("ac_success.html")
    
    else:
        #If the resuest is not a post, go to the original form
        return render_template("addalbum.html")
    
#Route which obtains photos with information specified by the user
@app.route("/getphotos/", methods=["POST", "GET"])
def getphotos():
    #If the request method is post, we want to obtain the photos
    if request.method == "POST":
        
        #These lines extract the form data
        queryPhotoName = request.form["queryName"]              #search term
        amountPhotoRequest= request.form["amountRequest"]       #number of photos
        selectedAlbum = request.form["albums"]                  #chosen album
        
        #obtain the album id so photos can be added to location table
        '''
        Below we connect to the database to obtain the album id based on the 
        album the user selected to store the photos in. The album id 
        is necessary to add the photos to the location table
        so that they will showcase on other pages
        '''
        con = sql.connect("photos.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select ID from ALBUM where ALBNAME=?", (selectedAlbum,))
        result = cur.fetchone()
        albumID = int(result[0])
        
        '''
        Even though specified in html to be a number,
        if we do not type cast the variable to integer the api
        will give errors because it is treated as a string
        '''
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
        
        #search for images based on the search parameters
        gis.search(search_params=_search_params)
        
        '''
        This for loop facilitates the downloading of multiple images.
        Additionally, within the loop is where the metadata for the images
        is obtained. 
        '''
        for image in gis.results():
            image.url  # image direct url
            image.referrer_url  # image referrer url (source) 
            
            #download image to specified path
            image.download(downloadPath)
            
            '''
            Below the file path is stored in a variable as a string
            with the backslashes replaced with forward slashes. 
            This was done because windows sometimes does not like
            the backslashes in file paths.
            '''
            orgFilePath = image.path
            orgFilePath = orgFilePath.replace("\\", "/")
            
            #get name the file is stored as (most helpful when multiple images downloaded)
            '''
            Split the file path string based on the download path to obtain
            the name that the file is stored as. The name of the file is needed
            to construct the path attribute and for the pname attribute in the
            photo table
            '''
            splitPath = orgFilePath.split(downloadPath + "/")
            oriName = splitPath[1]
            
            
            #Here the file extension is removed from the downloaded file's name
            extRem = oriName.split(".")
            orgFileName = extRem[0]
            
            #Here metadata is computed about the image based on its file path
            curSize = os.path.getsize(orgFilePath)      #file size (bytes)
            curImage = cv2.imread(orgFilePath)
            curHeight, curWidth = curImage.shape[:2]    #image height and width
            
            #Here the path is obtained to be given to the new PHOTO table item
            imagePathSplit = orgFilePath.split(origDir + "/")
            curImagePath = imagePathSplit[1]
            
            #Here we create a default description for the photo based on the user query
            defaultDesc = "This is a photo of " + queryPhotoName
            
            '''
            These statements create the new item for the PHOTO table based
            on the name, description, computed metadata, and constructed path.
            '''
            cur.execute("insert into PHOTO(PNAME, PDESC, WIDTH, HEIGHT, FILESIZE, PATH) values (?,?,?,?,?,?)", (orgFileName, defaultDesc, curWidth, curHeight, curSize, curImagePath))
            con.commit()
            
            #get photo id so it can be added to locations table
            '''
            Here the ID for newly added photo is obtained by querying for
            the image path. Image path was chosen to be used for the query
            during troubleshooting. This is because, during one implementation
            of the system, a jpg and png could have the same name, so selecting
            ID by name was not sufficient. However, a jpg and png with the same
            name have different path's, thus why path is used.
            
            In the current implementation I do not think two different file 
            types can have the same name, but two files still cannot have the 
            same path so in this sense using path for the query instead
            of name is trivial.
            '''
            cur.execute("select ID from PHOTO where PATH=?", (curImagePath,))
            pIDresult = cur.fetchone()
            curPhotoID = int(pIDresult[0])
            
            '''
            Below a new item is added to the LOCATIONS table to represent
            that the downloaded image is located in the specified folder.
            Without this, the image will not be seen on the site.
            '''
            cur.execute("insert into LOCATIONS(A_ID, P_ID) values (?,?)", (albumID, curPhotoID))
            con.commit()
            
        return render_template("getphotos_success.html")
    
    else:
        '''
        If the method is not post, the database is connected to
        so that album data can be obtained and passed the frontend
        so that the user can only choose between albums which 
        exist.
        '''
        con = sql.connect("photos.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from ALBUM")
        albums = cur.fetchall()
        
        return render_template("getphotos.html", data = albums)

#Route which takes users to the album directory
@app.route("/albums")
def albums():
    '''
    Here the database is connected to so all the album data can be obtained
    and passed to the front end so the user can choose which album
    they would like to view.
    '''
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ALBUM")
    albums = cur.fetchall()
    
    return render_template("albumdirectory.html", data = albums)
    
#Route which takes users inside an album to see the photos inside it
@app.route("/albumspage:<string:aid>", methods=["POST", "GET"])
def albumspage(aid):
    '''
    Below the database is connected to so that the album name and
    album description are obtained
    '''
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
    result = cur.fetchone()
    albName = str(result[0])
    cur.execute("select ALBDESC from ALBUM where ID=?", (aid,))
    descresult = cur.fetchone()
    descAlb = str(descresult[0])
    
    
    #Below the photo ids of photos within the current album are obtained
    cur.execute("select * from LOCATIONS where A_ID=?", (aid,))
    photoIDs = cur.fetchall()
    
    '''
    Here a list is made to hold all the database rows containing information
    about each and every photo within the current album which is obtained
    by looping through the photoIDs list and selecting all the information
    for the specific photo id
    '''
    photoList = []
    for row in photoIDs:
        cur.execute("select * from PHOTO where ID=?", (row[2],))
        curPhoto = cur.fetchone()
        photoList.append(curPhoto)
    
    return render_template("albumpage.html", albumName = albName, albumDescription = descAlb, data = photoList)

#Route to a form which allows users to modify album data
@app.route("/editAlbum/<string:aid>", methods=["POST", "GET"])
def editAlbum(aid):
    if request.method == "POST":
        #Obtain user specified data
        albname = request.form["albname"]
        albdesc = request.form["albdesc"]
        
        '''
        Connect to the database to obtain the old album name
        to check and see if a change was made to the name
        '''
        con = sql.connect("photos.db")
        cur = con.cursor()
        cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
        result = cur.fetchone()
        oldAlbName = str(result[0])
        
        '''
        If the the name in the form is the same as the old name, do not check 
        if the directory already exists as they were not trying to change its name
        
        If they changed the name make sure directory does not already exist
        '''
        if(oldAlbName != albname):
            #first check if the edited name is already a directory
            #if so, direct to page telling them the directory already exists
            os.chdir(mainDir)
            for file in os.listdir():
                if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".gif"):
                    continue
                if file == albname:
                    os.chdir(origDir)
                    return render_template("editalbum_unsuccess.html")
                    #return redirect(url_for("home"))
        
        #change back to original directory if no file matches edited name
        os.chdir(origDir)
        
        #If the directory does not already exist, update album
        cur.execute("update ALBUM set ALBNAME=?, ALBDESC=? where ID=?", (albname, albdesc, aid))
        con.commit()
        
        #Change name locally
        oldPath = os.path.join(mainDir, oldAlbName)
        newPath = os.path.join(mainDir, albname)
        os.rename(oldPath, newPath)
        
        return render_template("editalbum_success.html")
    
    '''
    Connect to the database to pull the information about the album
    the user is trying to change and pass it to the front end.
    '''
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ALBUM where ID=?", (aid,))
    album = cur.fetchone()
    return render_template("editAlbum.html", data = album)

#Route to delete an album specified by the user
@app.route("/deleteAlbum/<string:aid>", methods=["GET"])
def deleteAlbum(aid):
    '''
    Connect to the database and obtain the name of the album
    being deleted. This is needed to construct the file path
    to delete the album locally.
    '''
    con = sql.connect("photos.db")
    cur = con.cursor()
    cur.execute("select ALBNAME from ALBUM where ID=?", (aid,))
    result = cur.fetchone()
    
    
    #Deleting photos and location entries based on album id
    cur.execute("select P_ID from LOCATIONS where A_ID=?", (aid,))
    photoLocIds = cur.fetchall()
        
    #This deletes all photos and locations
    for row in photoLocIds:
        cur.execute("delete from LOCATIONS where P_ID=?", (row[0],))
        con.commit()
        cur.execute("delete from PHOTO where ID=?", (row[0],))
        con.commit()
    
    #This deletes the album
    cur.execute("delete from ALBUM where ID=?", (aid,))
    con.commit()
    
    #This constructs the file path and deletes the album locally
    albumName = str(result[0])
    DirPath = os.path.join(mainDir, albumName)
    shutil.rmtree(DirPath)
    
    return render_template("deletealbum_success.html")

#Route to a form which allows users to edit photo data
@app.route("/editPhoto/<string:pid>", methods=["POST", "GET"])
def editPhoto(pid):
    if request.method == "POST":
        #Obtain specified info from user
        photoname = request.form["photoname"]   #photo name
        photodesc = request.form["photodesc"]   #photo description
        photopath = request.form["photopath"]   #photo path
        
        #honestly dont remember what this does
        splitPath = photopath.split("/")
        curAlb = splitPath[1]
        curDir = mainDir + "/" + curAlb
        
        #connect to database to obtain old photo name
        con = sql.connect("photos.db")
        cur = con.cursor()
        cur.execute("select PNAME from PHOTO where ID=?", (pid,))
        nameresult = cur.fetchone()
        oldPhotoName = str(nameresult[0])
        
        '''
        If the the name in the form is the same as the old name, do not check 
        if the file already exists as they were not trying to change its name.
        
        If they changed the name make sure file does not already exist
        '''
        if(oldPhotoName != photoname):
            #first check if the edited name is already a directory
            #if so go to a page telling them a file already has that name
            for file in os.listdir():
                #get just the name of current file in directory without extension
                currentFileSplit = file.split(".")
                currentFileName = currentFileSplit[0]
                if photoname == currentFileName:
                    os.chdir(origDir)
                    return render_template("editphoto_unsuccess.html")
        
        #change back to original directory if no file matches edited name
        os.chdir(origDir)
        
        #construct path and change name locally 
        dirList = mainDir.split("static")
        modDir = dirList[0]

        oldFilePath = modDir + photopath
        splitCur = photopath.split(oldPhotoName)
        
        newPhotoPath = splitCur[0] + photoname + splitCur[1]

        newFilePath = modDir + newPhotoPath
        
        os.rename(oldFilePath, newFilePath)
        
        #update the photo item on the database with the new info
        cur.execute("update PHOTO set PNAME=?, PDESC=?, PATH=? where ID=?", (photoname, photodesc, newPhotoPath, pid))
        con.commit()
        
        #get old album cover info
        cur.execute("select ALBIMG from ALBUM where ALBNAME=?", (curAlb,))
        coverresult = cur.fetchone()
        oldAlbCov = str(coverresult[0])
        
        #if photo was the album cover, update album to have new path to photo, otherwise continue
        if(oldAlbCov == photopath):
            #update album with new path
            cur.execute("update ALBUM set ALBIMG=? where ALBNAME=?", (newPhotoPath, curAlb))
            con.commit()
        
        return render_template("editphoto_success.html")
    
    '''
    Connect to the database to pull the information about the photo
    the user is trying to change and pass it to the front end.
    '''
    con = sql.connect("photos.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from PHOTO where ID=?", (pid,))
    photo = cur.fetchone()
    return render_template("editPhoto.html", data = photo)

#Route to delete a photo specified by the user
@app.route("/deletePhoto/<string:pid>", methods=["GET"])
def deletePhoto(pid):
    '''
    Connect to the database to obtain the old path for the photo
    and the album id for where the photo is stored
    '''
    con = sql.connect("photos.db")
    cur = con.cursor()
    cur.execute("select PATH from PHOTO where ID=?", (pid,))
    pathresult = cur.fetchone()
    cur.execute("select A_ID from LOCATIONS where P_ID=?", (pid,))
    albumIDResult = cur.fetchone()
    
    oldPhotoPath = str(pathresult[0])
    currentAlbumID = str(albumIDResult[0])
    
    #if deleting photo that was album cover, change album cover back to default
    if(oldPhotoPath != "static/1.jpeg"):
        #get old album cover from database
        cur.execute("select ALBIMG from ALBUM where ID=?", (currentAlbumID,))
        curCoverRes = cur.fetchone()
        curCovPath = str(curCoverRes[0])
        
        #compare with photo being deleted, if the same, set to default
        if(curCovPath == oldPhotoPath):
            cur.execute("update ALBUM set ALBIMG=? where ID=?", ("static/1.jpeg", currentAlbumID))
            con.commit()
    
    #Delete any LOCATIONS items containing the photo id
    cur.execute("delete from LOCATIONS where P_ID=?", (pid,))
    con.commit()
    
    #delte the photo from the photo table
    cur.execute("delete from PHOTO where ID=?", (pid,))
    con.commit()

    #delete the photo locally by constructing path
    dirList = mainDir.split("static")
    modDir = dirList[0]
    photoPath = modDir + oldPhotoPath
    
    #I made a change here to add the if
    if(os.path.exists(photoPath)):
        os.remove(photoPath)
    
    return render_template("deletephoto_success.html")

#Route which assigns a photo to be the album cover
@app.route("/assignPhoto/<string:pid>", methods=["GET"])
def assignPhoto(pid):
    '''
    Connect to the database and obtain the photo path for the specified
    photo and the album id where the current photo is stored
    '''
    con = sql.connect("photos.db")
    cur = con.cursor()
    cur.execute("select PATH from PHOTO where ID=?", (pid,))
    pathresult = cur.fetchone()
    cur.execute("select A_ID from LOCATIONS where P_ID=?", (pid,))
    albumIDResult = cur.fetchone()
    
    currentPhotoPath = str(pathresult[0])
    currentAlbumID = str(albumIDResult[0])
    
    #update the album to have its cover point to the path of the assigned photo
    cur.execute("update ALBUM set ALBIMG=? where ID=?", (currentPhotoPath, currentAlbumID))
    con.commit()
    
    return render_template("assign_success.html")


#This drives the program by Running the Flask App
if __name__ == "__main__":
    app.run(debug=True)
    
    