As of writing this, the only file in this directory will by the Python code which enables the web applications function.

Modifications will need to be made to this file in order to add the functionality of storing photos and creating albums as well as supporting new pages.

Edit: 11/20/22
This folder now includes the db.py file which creates a local SQLite database which will store information regarding albums, photos, and which albums photos are stored in.

1st Edit on 11/27/22:
I added in the functionality which stores the album information received from the form in the local database.
Additionally, I added the functionality which makes the local directory at the specified file path on the system.

2nd Edit on 11/27/22:
Added a template route for getting photos, within it containing a comment specifying what must be done within the route itself

12/1/22:
An edit was made to db.py which adds an additional attribute to PHOTOS to store partial information about the file path alongside the image. This is used to help with display through flask (which is semi-tedious). 

12/6/22:
Uploaded a new version of photoapp.py which includes some functional routes for the pages alongside some routes which were used for testing (which will be removed prior to the submission of the project). Some pages are currently implemented and functional, but some still need to be implemented. Additionally, the code currently lacks comments (which I will add later explaining what specific pieces do).

12/7/22:
Uploaded a new version of photoapp.py which now has the API implemented. Currently it has some strange issue with a photo being downloaded twice and saving over itself when it is the same photo. I will experiment with preventing this.
