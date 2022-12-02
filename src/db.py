# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 18:43:22 2022
@author: theja
"""

import sqlite3

conn = sqlite3.connect("photos.db")

print("Databased opened")

conn.execute('''CREATE TABLE ALBUM
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         ALBNAME           TEXT    NOT NULL,
         ALBDESC           TEXT    NOT NULL);''')

conn.execute('''CREATE TABLE PHOTO
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         PNAME           TEXT    NOT NULL,
         PDESC           TEXT    NOT NULL,
         WIDTH            INTEGER     NOT NULL,
         HEIGHT            INTEGER     NOT NULL,
         FILESIZE            REAL     NOT NULL,
         PATH            TEXT    NOT NULL);''')

conn.execute('''CREATE TABLE LOCATIONS
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
          A_ID INTEGER,
          P_ID INTEGER,
          FOREIGN KEY(A_ID) REFERENCES ALBUM(id),
          FOREIGN KEY(P_ID) REFERENCES PHOTO(ID));''')

print("table created successfully")