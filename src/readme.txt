As of writing this, the only file in this directory will by the Python code which enables the web applications function.

Modifications will need to be made to this file in order to add the functionality of storing photos and creating albums as well as supporting new pages.

Edit: 11/20/22
This folder now includes the db.py file which creates a local SQLite database which will store information regarding albums, photos, and which albums photos are stored in.

1st Edit on 11/27/22:
I added in the functionality which stores the album information received from the form in the local database.
Additionally, I added the functionality which makes the local directory at the specified file path on the system.

2nd Edit on 11/27/22:
Added a template route for getting photos, within it containing a comment specifying what must be done within the route itself
