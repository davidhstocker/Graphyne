"""
   CreateRunTimeData.py: Generate the schema for the runtime database

    Alternatively, if this module is imported, another db may be supplied (e.g. :memory:
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'

import sqlite3
import os
import sys
from os.path import expanduser

def createDB(db):
    cursor = db.cursor()
    cursor.execute("CREATE TABLE Entity(entityID NVARCHAR(38) NOT NULL, depricated INT NOT NULL, memePath NVARCHAR(100) NOT NULL, metaMeme NVARCHAR(100) NOT NULL, PRIMARY KEY (entityID))")
    cursor.execute("CREATE TABLE EntityTags(entityID NVARCHAR(38) NOT NULL, tag NVARCHAR(100) NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))")
    cursor.execute("CREATE TABLE EntityPropertyLists(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal NVARCHAR(1000) NOT NULL, memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))")
    cursor.execute("CREATE TABLE EntityPropertyBooleans(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal INT NOT NULL, memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))")
    cursor.execute("CREATE TABLE EntityPropertyStrings(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal NVARCHAR(100) NOT NULL, restList NVARCHAR(100), memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))")
    cursor.execute("CREATE TABLE EntityPropertyTexts(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal NVARCHAR(1000) NOT NULL, memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))")
    cursor.execute("CREATE TABLE EntityPropertyDecimals(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal DECIMAL(15,5) NOT NULL, restMin DECIMAL(15,5), restMax DECIMAL(15,5), restList NVARCHAR(100), memePath NVARCHAR(100), FOREIGN KEY(entityID) REFERENCES Entity(entityID))")
    cursor.execute("CREATE TABLE EntityPropertyIntegers(entityID NVARCHAR(38) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal INT NOT NULL, restMin INT, restMax INT, restList NVARCHAR(100), memePath NVARCHAR(100),  FOREIGN KEY(entityID) REFERENCES Entity(entityID))")
    cursor.execute("CREATE TABLE EntityLink (entityLinkID NVARCHAR(39) NOT NULL, memberID1 NVARCHAR(38) NOT NULL, memberID2 NVARCHAR(38) NOT NULL, membershipType INT NOT NULL, masterEntity NVARCHAR(38), PRIMARY KEY (EntityLinkID), FOREIGN KEY(memberID1) REFERENCES Entity(entityID), FOREIGN KEY(memberID2) REFERENCES Entity(entityID), FOREIGN KEY(masterEntity) REFERENCES Entity(entityID))")
    cursor.execute("CREATE TABLE EntityLinkPropertyBooleans(entityLinkID NVARCHAR(39) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal INT NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))")
    cursor.execute("CREATE TABLE EntityLinkPropertyStrings(entityLinkID NVARCHAR(39) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal NVARCHAR(1000) NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))")
    cursor.execute("CREATE TABLE EntityLinkPropertyDecimals(entityLinkID NVARCHAR(39) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal DECIMAL(15,5) NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))")
    cursor.execute("CREATE TABLE EntityLinkPropertyIntegers(entityLinkID NVARCHAR(39) NOT NULL, propName NVARCHAR(100) NOT NULL, propVal INT NOT NULL,  FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))")
    db.commit()
    
    
def resetDB(db):
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE EntityLinkPropertyBooleans")
        cursor.execute("DROP TABLE EntityLinkPropertyStrings")
        cursor.execute("DROP TABLE EntityLinkPropertyDecimals")
        cursor.execute("DROP TABLE EntityLinkPropertyIntegers")
        cursor.execute("DROP TABLE EntityLink")
        cursor.execute("DROP TABLE EntityTags")
        cursor.execute("DROP TABLE EntityPropertyLists")
        cursor.execute("DROP TABLE EntityPropertyBooleans")
        cursor.execute("DROP TABLE EntityPropertyStrings")
        cursor.execute("DROP TABLE EntityPropertyTexts")
        cursor.execute("DROP TABLE EntityPropertyDecimals")
        cursor.execute("DROP TABLE EntityPropertyIntegers")
        cursor.execute("DROP TABLE Entity")
        db.commit()
    except: pass    
    createDB(db)

if __name__ == "__main__":
    dbName = sys.argv[1]
    userDir =  expanduser("~")
    dbLoc = os.path.join(userDir, "Graphyne", dbName)
    db = sqlite3.connect(dbLoc)
    createDB(db)