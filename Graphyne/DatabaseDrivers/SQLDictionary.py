"""
   SQLDictionary.py: SQL Statements for Realtional Databases
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'



class SyntaxDefSQLite(object):

    
    #########################
    #Table Clearing
    #########################
    clearTable = "DELETE FROM"
    
    
    #########################
    #RelationalDatabaseModule
    #########################
    insertEntity = "INSERT INTO Entity (entityID, depricated, memePath, metaMeme, masterEntityID) VALUES (?, ?, ?, ?, ?)"
    insertEntityCatalogLinkWithMaster = "INSERT INTO EntityLink (entityLinkID, memberID1, memberID2, membershipType, masterEntity) VALUES (?, ?, ?, ?, ?)"
    insertEntityCatalogLinkNoMaster = "INSERT INTO EntityLink (entityLinkID, memberID1, memberID2, membershipType) VALUES (?, ?, ?, ?)"
    insertEntityTags = "INSERT INTO EntityTags (entityID, tag) VALUES (?, ?)"
    insertEntityList = "INSERT INTO EntityPropertyLists (entityID, propName, propVal, memePath) VALUES (?, ?, ?, ?)"
    insertEntityBoolean = "INSERT INTO EntityPropertyBooleans (entityID, propName, propVal, memePath) VALUES (?, ?, ?, ?)"
    insertEntityStringRestricted = "INSERT INTO EntityPropertyStrings (entityID, propName, propVal) VALUES (?, ?, ?)"
    insertEntityTextRestricted = "INSERT INTO EntityPropertyTexts (entityID, propName, propVal) VALUES (?, ?, ?)"
    insertEntityStringUnRestricted = "INSERT INTO EntityPropertyStrings (entityID, propName) VALUES (?, ?, ?)"
    insertEntityTextUnRestricted = "INSERT INTO EntityPropertyTexts (entityID, propName) VALUES (?, ?, ?)"
    insertEntityString = "INSERT INTO EntityPropertyStrings (entityID, propName, propVal) VALUES (?, ?, ?)"
    insertEntityText = "INSERT INTO EntityPropertyTexts (entityID, propName, propVal) VALUES (?, ?, ?)"
    insertEntityDecimalRestrictionsAll = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMin, restMax, restList, memePath) VALUES (?, ?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMinMax = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMin, restMax, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMinList = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMin, restList, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMaxList = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMax, restList, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsList = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restList, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMax = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMax, memePath) VALUES (?, ?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMin = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMin, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictions = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, memePath) VALUES (?, ?, ?, ?)"
    insertEntityIntegerRestrictionsAll = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMin, restMax, restList, memePath) VALUES (?, ?, ?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMinMax = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMin, restMax, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMinList = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMin, restList, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMaxList = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMax, restList, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsList = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restList, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMax = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMax, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMin = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMin, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictions = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, memePath) VALUES (?, ?, ?, ?)"
    insertLinkAttributeString = "INSERT INTO EntityLinkPropertyStrings (entityLinkID, propName, propVal) VALUES (?, ?, ?)"
    insertLinkAttributeBool = "INSERT INTO EntityLinkPropertyBooleans (entityLinkID, propName, propVal) VALUES (?, ?, ?)"
    insertLinkAttributeInt = "INSERT INTO EntityLinkPropertyIntegers (entityLinkID, propName, propVal) VALUES (?, ?, ?)"
    insertLinkAttributeDec = "INSERT INTO EntityLinkPropertyDecimals (entityLinkID, propName, propVal) VALUES (?, ?, ?)"

    deleteEntityList = "DELETE FROM EntityPropertyLists WHERE entityID=? AND propName=?"
    deleteEntityString = "DELETE FROM EntityPropertyStrings WHERE entityID=? AND propName=?"
    deleteEntityText = "DELETE FROM EntityPropertyTexts WHERE entityID=? AND propName=?"
    deleteEntityBoolean = "DELETE FROM EntityPropertyBooleans WHERE entityID=? AND propName=?"
    deleteEntityDecimal = "DELETE FROM EntityPropertyDecimals WHERE entityID=? AND propName=?"
    deleteEntityInteger = "DELETE FROM EntityPropertyIntegers WHERE entityID=? AND propName=?"
    deleteLink = "DELETE FROM EntityLink WHERE entityLinkID=?"
    deleteLinkBoolean = "DELETE FROM EntityLinkPropertyBooleans WHERE entityLinkID=?"
    deleteLinkString = "DELETE FROM EntityLinkPropertyStrings WHERE entityLinkID=?"
    deleteLinkDecimal = "DELETE FROM EntityLinkPropertyDecimals WHERE entityLinkID=?"
    deleteLinkInteger = "DELETE FROM EntityLinkPropertyIntegers WHERE entityLinkID=?"
    
    selectGetEntitiesByTag = "SELECT DISTINCT entityID FROM EntityTags WHERE tag IN ?"
    selectGetEntitiesByType = "SELECT DISTINCT entityID FROM Entity WHERE memePath IN (?)"
    selectGetEntitiesByMetamemeType = "SELECT DISTINCT entityID FROM Entity WHERE metaMeme IN (?)"
    selectGetAllEntities = "SELECT DISTINCT entityID FROM Entity"
    selectGetAllEntitiesActive0 = "SELECT DISTINCT entityID FROM Entity WHERE depricated=0"
    selectGetAllEntitiesActive1 = "SELECT DISTINCT entityID FROM Entity WHERE depricated=1"
    selectGetRessurectedEntities0 = "SELECT DISTINCT entityID, memePath, metaMeme, masterEntityID FROM Entity WHERE depricated=0"
    selectGetRessurectedEntities1 = "SELECT DISTINCT entityID, memePath, metaMeme, masterEntityID FROM Entity WHERE depricated=1"
    selectAddEntityTest = "SELECT entityID FROM Entity WHERE entityID=?"
    selectAllLinks = "SELECT * FROM EntityLink" 
    selectAllInboundLinks = "SELECT * FROM EntityLink WHERE memberID2=?"
    selectAllOutboundLinks = "SELECT * FROM EntityLink WHERE memberID1=?"
    selectCounterpartIndices = "SELECT DISTINCT entityLinkID FROM EntityLink WHERE memberID1=? OR memberID1=?"
    selectLinkAttributeTestBool = "SELECT DISTINCT propVal FROM EntityLinkPropertyBooleans WHERE entityLinkID=? AND propName=?"
    selectLinkAttributeTestInt = "SELECT DISTINCT propVal FROM EntityLinkPropertyIntegers WHERE entityLinkID=? AND propName=?"
    selectLinkAttributeTestDec = "SELECT DISTINCT propVal FROM EntityLinkPropertyDecimals WHERE entityLinkID=? AND propName=?"
    selectLinkAttributeTestStr = "SELECT DISTINCT propVal FROM EntityLinkPropertyStrings WHERE entityLinkID=? AND propName=?"
    selectRemoveLinkTest = "SELECT DISTINCT entityLinkID FROM EntityLink WHERE memberID1=? AND memberID2=?"
    selectEntityMeme = "SELECT DISTINCT memePath FROM Entity WHERE entityID=?"
    selectGetEntityPropertyLists = "SELECT * FROM EntityPropertyLists WHERE entityID=?"    #Returns: [entityID, propName, propVal, memePath]
    selectGetEntityPropertyBooleans = "SELECT * FROM EntityPropertyBooleans WHERE entityID=?" #Returns: [entityID, propName, propVal, memePath]
    selectGetEntityPropertyStrings = "SELECT * FROM EntityPropertyStrings WHERE entityID=?"  #Returns: [entityID, propName, propVal, restList, memePath]
    selectGetEntityPropertyTexts = "SELECT * FROM EntityPropertyTexts WHERE entityID=?"    #Returns: [entityID, propName, propVal, restList, memePath]
    selectGetEntityPropertyDecimals = "SELECT * FROM EntityPropertyDecimals WHERE entityID=?" #Returns: [entityID, propName, propVal, restMin, restMax, restList, memePath]
    selectGetEntityPropertyIntegers= "SELECT * FROM EntityPropertyIntegers WHERE entityID=?" #Returns: [entityID, propName, propVal, restMin, restMax, restList, memePath]
    
    #These select statements are for deleting entities
    removeEntityTags = "DELETE FROM EntityTags WHERE entityID=?"
    removeEntity = "DELETE FROM Entity WHERE entityID=?"
    removeLinks = "DELETE FROM EntityLink WHERE memberID1=? OR memberID2=?" 
    removeLinkAttributeBool = "DELETE FROM EntityLinkPropertyBooleans WHERE entityLinkID=?"
    removeLinkAttributeInt = "DELETE FROM EntityLinkPropertyIntegers WHERE entityLinkID=?"
    removeLinkAttributeDec = "DELETE FROM EntityLinkPropertyDecimals WHERE entityLinkID=?"
    removeLinkAttributeStr = "DELETE FROM EntityLinkPropertyStrings WHERE entityLinkID=?"
    removeEntityPropertyLists = "DELETE FROM EntityPropertyLists WHERE entityID=?"    
    removeEntityPropertyBooleans = "DELETE FROM EntityPropertyBooleans WHERE entityID=?"
    removeEntityPropertyStrings = "DELETE FROM EntityPropertyStrings WHERE entityID=?"
    removeEntityPropertyTexts = "DELETE FROM EntityPropertyTexts WHERE entityID=?"
    removeEntityPropertyDecimals = "DELETE FROM EntityPropertyDecimals WHERE entityID=?"
    removeEntityPropertyIntegers= "DELETE FROM EntityPropertyIntegers WHERE entityID=?"

    
    
    #########################
    #     Graph Module
    #########################
    selectMemesFromMetamameTable = "SELECT ? FROM ?"
    selectImplicitMemesFromMetamemeTable = "SELECT ? FROM ? WHERE ?=?"
    selectImplicitMemesForwardReferences = "SELECT ? FROM ? WHERE ?=?"
    selectImplicitMemesBackwardReferences = "SELECT ? FROM ? WHERE ?=?"
    
    
    def createRuntimeDB(self, db):
        try:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE Entity(entityID NVARCHAR(38) NOT NULL, depricated INT NOT NULL, memePath NVARCHAR(100) NOT NULL, metaMeme NVARCHAR(100) NOT NULL, masterEntityID NVARCHAR(38) NOT NULL, PRIMARY KEY (entityID))")
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
        except Exception as e:
            unusedDebug = e
        
        
    def resetRuntimeDB(self, db):
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
        self.createDB(db)
        
        
    def createTestDB(self, db):
        cursor = db.cursor()
        cursor.execute("CREATE TABLE BridgedTo (propertyF NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyF))")
        cursor.execute("CREATE TABLE IsChild (propertyD NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyD))")
        cursor.execute("CREATE TABLE IsGrandChild (propertyE NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyE))")
        cursor.execute("CREATE TABLE EndEffector (propertyAA NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyAA))")
        cursor.execute("CREATE TABLE MiddleNode (propertyQ NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyQ))")
        cursor.execute("CREATE TABLE SecondMiddleNodeHop (propertyCC NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyCC))")
        cursor.execute("CREATE TABLE FirstMiddleNodeHop (propertyBB NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyBB))")
        cursor.execute("CREATE TABLE ClonedSecondHop (propertyDD NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyDD))")
        cursor.execute("CREATE TABLE NotClonedSecondHop (propertyEE NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyEE))")
        cursor.execute("CREATE TABLE ClonedFirstHop (propertyFF NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyFF))")
        cursor.execute("CREATE TABLE NotClonedFirstHop (propertyGG NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyGG))")
        cursor.execute("CREATE TABLE SimpleMM (propertyA NVARCHAR(36) NOT NULL , propertyB NVARCHAR(36), PRIMARY KEY (propertyA))")
        cursor.execute("CREATE TABLE HasChild (propertyC NVARCHAR(36) NOT NULL, propertyH NVARCHAR(36) NOT NULL, propertyM NVARCHAR(200) NOT NULL, propertyN NVARCHAR(200) NOT NULL, propertyR NVARCHAR(36) NOT NULL, PRIMARY KEY (propertyC))")
        cursor.execute("CREATE TABLE HasChildPhase2 (propertyHH NVARCHAR(36), propertyII NVARCHAR(200), propertyJJ NVARCHAR(200), propertyKK NVARCHAR(200), propertyLL NVARCHAR(200), propertyMM NVARCHAR(200), propertyOO NVARCHAR(200), propertyPP NVARCHAR(200), propertyQQ NVARCHAR(200), propertyRR NVARCHAR(200), PRIMARY KEY (propertyHH))")
        cursor.execute("CREATE TABLE IsBRChild (propertyK NVARCHAR(36) NOT NULL, propertyL NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyK))")
        cursor.execute("CREATE TABLE IsBRGrandChild (propertyO NVARCHAR(36) NOT NULL, propertyP NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyO))")
        cursor.execute("CREATE TABLE Bridge (propertyG NVARCHAR(36) NOT NULL, propertyI NVARCHAR(200) NOT NULL, propertyJ NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyG))")
        cursor.execute("CREATE TABLE LogTable (logTime NVARCHAR(36) NOT NULL, logLevel NVARCHAR(6) NOT NULL, method NVARCHAR(50) NOT NULL, message NVARCHAR(1000) NOT NULL) ")
        cursor.execute("INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_1')")
        cursor.execute("INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_2')")
        cursor.execute("INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_3')")
        cursor.execute("INSERT INTO IsChild (propertyD) VALUES ('IsChild_1')")
        cursor.execute("INSERT INTO IsChild (propertyD) VALUES ('IsChild_2')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_00')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_01')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_02')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_03')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_04')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_05')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_06')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_07')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_08')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_09')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_10')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_11')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_12')")
        cursor.execute("INSERT INTO IsGrandChild (propertyE) VALUES ('IsGrandChild_1')")
        cursor.execute("INSERT INTO IsGrandChild (propertyE) VALUES ('IsGrandChild_2')")
        cursor.execute("INSERT INTO SimpleMM (propertyA, propertyB) VALUES ('SimpleMM_1', 'propertyB_Val')")
        cursor.execute("INSERT INTO SimpleMM (propertyA, propertyB) VALUES ('SimpleMM_2', 'propertyB_Val')")
        cursor.execute("INSERT INTO MiddleNode (propertyQ) VALUES ('MiddleNodeMeme_1')")
        cursor.execute("INSERT INTO MiddleNode (propertyQ) VALUES ('MiddleNodeMeme_2')")
        cursor.execute("INSERT INTO SecondMiddleNodeHop (propertyCC) VALUES ('SecondMiddleNodeHop_1')")
        cursor.execute("INSERT INTO SecondMiddleNodeHop (propertyCC) VALUES ('SecondMiddleNodeHop_2')")
        cursor.execute("INSERT INTO FirstMiddleNodeHop (propertyBB) VALUES ('FirstMiddleNodeHop_1')")
        cursor.execute("INSERT INTO FirstMiddleNodeHop (propertyBB) VALUES ('FirstMiddleNodeHop_2')")
        cursor.execute("INSERT INTO ClonedSecondHop (propertyDD) VALUES ('ClonedSecondHop_1')")
        cursor.execute("INSERT INTO NotClonedSecondHop (propertyEE) VALUES ('NotClonedSecondHop_1')")
        cursor.execute("INSERT INTO ClonedFirstHop (propertyFF) VALUES ('ClonedFirstHop_1')")
        cursor.execute("INSERT INTO NotClonedFirstHop (propertyGG) VALUES ('NotClonedFirstHop_1')")
        cursor.execute("INSERT INTO HasChild (propertyC, propertyH, propertyM, propertyN, propertyR) VALUES ('HasChild_1', 'propertyH_Val1', 'IsChild_1', 'ImplicitMemes.IsGrandChild_1', 'ImplicitMemes.MiddleNodeMeme_1')")
        cursor.execute("INSERT INTO HasChild (propertyC, propertyH, propertyM, propertyN, propertyR) VALUES ('HasChild_2', 'propertyH_Val1', 'IsChild_2', 'ImplicitMemes.IsGrandChild_2', 'ImplicitMemes.MiddleNodeMeme_2')")
        cursor.execute("INSERT INTO HasChildPhase2 (propertyHH, propertyII, propertyLL, propertyMM) VALUES ('HasChildPhase2_1', 'ImplicitMemes.FirstMiddleNodeHop_1', 'ImplicitMemes.SecondMiddleNodeHop_1', 'ImplicitMemes.EndEffector_00')")
        cursor.execute("INSERT INTO HasChildPhase2 (propertyHH, propertyII, propertyLL, propertyMM) VALUES ('HasChildPhase2_2', 'ImplicitMemes.FirstMiddleNodeHop_2', 'ImplicitMemes.SecondMiddleNodeHop_2', 'ImplicitMemes.EndEffector_01')")
        cursor.execute("INSERT INTO HasChildPhase2 (propertyHH, propertyJJ, propertyQQ, propertyOO) VALUES ('HasChildPhase2_3', 'ImplicitMemes.NotClonedFirstHop_1', 'ImplicitMemes.ClonedSecondHop_1', 'ImplicitMemes.EndEffector_02')")
        cursor.execute("INSERT INTO HasChildPhase2 (propertyHH, propertyKK, propertyRR, propertyPP) VALUES ('HasChildPhase2_4', 'ImplicitMemes.ClonedFirstHop_1', 'ImplicitMemes.NotClonedSecondHop_1', 'ImplicitMemes.EndEffector_03')")
        cursor.execute("INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_1', 'HasChild_1')")
        cursor.execute("INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_2', 'HasChild_1')")
        cursor.execute("INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_3', 'HasChild_2')")
        cursor.execute("INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_1', 'HasChild_1')")
        cursor.execute("INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_2', 'HasChild_1')")
        cursor.execute("INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_3', 'HasChild_2')")
        cursor.execute("INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_1', 'HasChild_1', 'BridgedTo_1')")
        cursor.execute("INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_2', 'HasChild_1', 'BridgedTo_2')")
        cursor.execute("INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_3', 'HasChild_2', 'BridgedTo_3')")
        db.commit()




class SyntaxDefMSSQL(object):
    ''' 
        MS SQL Server syntax is very similar to standard SQL syntax, with some small variations:
            Tables are cleared using TRUNCATE TABLE, instead of DELETE FROM
    '''
    
    #########################
    #Table Creation
    #########################
    createTableEntity = "CREATE TABLE Entity(entityID NVARCHAR(38) NOT NULL, depricated INT NOT NULL, memePath NVARCHAR(100) NOT NULL, metaMeme NVARCHAR(100) NOT NULL, initScript NVARCHAR(100), execScript NVARCHAR(100), terminateScript NVARCHAR(100), PRIMARY KEY (entityID))"
    createTableEntityTags = "CREATE TABLE EntityTags(entityID NVARCHAR(38) NOT NULL, tag NVARCHAR(100) NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
    createTableEntityPages = "CREATE TABLE EntityPages(entityID NVARCHAR(38) NOT NULL, page NVARCHAR(100) NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
    createTableEntityPropertyLists = "CREATE TABLE EntityPropertyLists(entityID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value NVARCHAR(1000) NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
    createTableEntityPropertyBooleans = "CREATE TABLE EntityPropertyBooleans(entityID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value INT NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
    createTableEntityPropertyStrings = "CREATE TABLE EntityPropertyStrings(entityID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value NVARCHAR(100) NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
    createTableEntityPropertyTexts = "CREATE TABLE EntityPropertyTexts(entityID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value NVARCHAR(1000) NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
    createTableEntityPropertyDecimals = "CREATE TABLE EntityPropertyDecimals(entityID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value DECIMAL(15,5) NOT NULL, FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
    createTableEntityPropertyIntegers = "CREATE TABLE EntityPropertyIntegers(entityID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value INT NOT NULL,  FOREIGN KEY(entityID) REFERENCES Entity(entityID))"
    createTableEntityLink = "CREATE TABLE EntityLink (entityLinkID NVARCHAR(38) NOT NULL, memberID1 NVARCHAR(38) NOT NULL, memberID2 NVARCHAR(38) NOT NULL, membershipType INT NOT NULL, keyLink INT NOT NULL, masterEntity INT NOT NULL, PRIMARY KEY (EntityLinkID))"
    createTableEntityLinkPropertyBooleans = "CREATE TABLE EntityLinkPropertyBooleans(entityLinkID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value INT NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))"
    createTableEntityLinkPropertyStrings = "CREATE TABLE EntityLinkPropertyStrings(entityLinkID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value NVARCHAR(1000) NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))"
    createTableEntityLinkPropertyDecimals = "CREATE TABLE EntityLinkPropertyDecimals(entityLinkID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value DECIMAL(15,5) NOT NULL, FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))"
    createTableEntityLinkPropertyIntegers = "CREATE TABLE EntityLinkPropertyIntegers(entityLinkID NVARCHAR(38) NOT NULL, property NVARCHAR(100) NOT NULL, value INT NOT NULL,  FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID))"
    createTableLinkDirection = "CREATE TABLE LinkDirection (direction NVARCHAR(13) NOT NULL, PRIMARY KEY (direction))"
    createTableLinkDirectionnbound = "INSERT INTO LinkDirection (direction) VALUES ('INBOUND')"
    createTableLinkDirectionOutbound = "INSERT INTO LinkDirection (direction) VALUES ('OUTBOUND')"
    createTableLinkDirectionBidirectional = "INSERT INTO LinkDirection (direction) VALUES ('BIDIRECTIONAL')"
    createTableLinkRepository = "CREATE TABLE LinkRepository (direction NVARCHAR(13) NOT NULL, entityLinkID NVARCHAR(39) NOT NULL, entityID NVARCHAR(38) NOT NULL, FOREIGN KEY(direction) REFERENCES LinkDirection(direction), FOREIGN KEY(entityLinkID) REFERENCES EntityLink(entityLinkID), FOREIGN KEY(entityID) REFERENCES Entity(entityID))"

    #########################
    #Table Clearing
    #########################
    clearTable = "DELETE FROM"
    
    
    #########################
    #RelationalDatabaseModule
    #########################
    insertEntity = "INSERT INTO Entity (entityID, depricated, memePath, metaMeme, masterEntityID) VALUES (?, ?, ?, ?, ?)"
    insertEntityCatalogLinkWithMaster = "INSERT INTO EntityLink (entityLinkID, memberID1, memberID2, membershipType, masterEntity) VALUES (?, ?, ?, ?, ?)"
    insertEntityCatalogLinkNoMaster = "INSERT INTO EntityLink (entityLinkID, memberID1, memberID2, membershipType) VALUES (?, ?, ?, ?)"
    insertEntityTags = "INSERT INTO EntityTags (entityID, tag) VALUES (?, ?)"
    insertEntityList = "INSERT INTO EntityPropertyLists (entityID, propName, propVal, memePath) VALUES (?, ?, ?, ?)"
    insertEntityBoolean = "INSERT INTO EntityPropertyBooleans (entityID, propName, propVal, memePath) VALUES (?, ?, ?, ?)"
    insertEntityStringRestricted = "INSERT INTO EntityPropertyStrings (entityID, propName, propVal) VALUES (?, ?, ?)"
    insertEntityTextRestricted = "INSERT INTO EntityPropertyTexts (entityID, propName, propVal) VALUES (?, ?, ?)"
    insertEntityStringUnRestricted = "INSERT INTO EntityPropertyStrings (entityID, propName) VALUES (?, ?, ?)"
    insertEntityTextUnRestricted = "INSERT INTO EntityPropertyTexts (entityID, propName) VALUES (?, ?, ?)"
    insertEntityString = "INSERT INTO EntityPropertyStrings (entityID, propName, propVal) VALUES (?, ?, ?)"
    insertEntityText = "INSERT INTO EntityPropertyTexts (entityID, propName, propVal) VALUES (?, ?, ?)"
    insertEntityDecimalRestrictionsAll = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMin, restMax, restList, memePath) VALUES (?, ?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMinMax = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMin, restMax, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMinList = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMin, restList, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMaxList = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMax, restList, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsList = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restList, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMax = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMax, memePath) VALUES (?, ?, ?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictionsMin = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, restMin, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityDecimalRestrictions = "INSERT INTO EntityPropertyDecimals (entityID, propName, propVal, memePath) VALUES (?, ?, ?, ?)"
    insertEntityIntegerRestrictionsAll = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMin, restMax, restList, memePath) VALUES (?, ?, ?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMinMax = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMin, restMax, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMinList = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMin, restList, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMaxList = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMax, restList, memePath) VALUES (?, ?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsList = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restList, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMax = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMax, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictionsMin = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, restMin, memePath) VALUES (?, ?, ?, ?, ?)"
    insertEntityIntegerRestrictions = "INSERT INTO EntityPropertyIntegers (entityID, propName, propVal, memePath) VALUES (?, ?, ?, ?)"
    insertLinkAttributeString = "INSERT INTO EntityLinkPropertyStrings (entityLinkID, propName, propVal) VALUES (?, ?, ?)"
    insertLinkAttributeBool = "INSERT INTO EntityLinkPropertyBooleans (entityLinkID, propName, propVal) VALUES (?, ?, ?)"
    insertLinkAttributeInt = "INSERT INTO EntityLinkPropertyIntegers (entityLinkID, propName, propVal) VALUES (?, ?, ?)"
    insertLinkAttributeDec = "INSERT INTO EntityLinkPropertyDecimals (entityLinkID, propName, propVal) VALUES (?, ?, ?)"

    deleteEntityList = "DELETE FROM EntityPropertyLists WHERE entityID=? AND propName=?"
    deleteEntityString = "DELETE FROM EntityPropertyStrings WHERE entityID=? AND propName=?"
    deleteEntityText = "DELETE FROM EntityPropertyTexts WHERE entityID=? AND propName=?"
    deleteEntityBoolean = "DELETE FROM EntityPropertyBooleans WHERE entityID=? AND propName=?"
    deleteEntityDecimal = "DELETE FROM EntityPropertyDecimals WHERE entityID=? AND propName=?"
    deleteEntityInteger = "DELETE FROM EntityPropertyIntegers WHERE entityID=? AND propName=?"
    deleteLink = "DELETE FROM EntityLink WHERE entityLinkID=?"
    deleteLinkBoolean = "DELETE FROM EntityLinkPropertyBooleans WHERE entityLinkID=?"
    deleteLinkString = "DELETE FROM EntityLinkPropertyStrings WHERE entityLinkID=?"
    deleteLinkDecimal = "DELETE FROM EntityLinkPropertyDecimals WHERE entityLinkID=?"
    deleteLinkInteger = "DELETE FROM EntityLinkPropertyIntegers WHERE entityLinkID=?"
    
    selectGetEntitiesByTag = "SELECT DISTINCT entityID FROM EntityTags WHERE tag IN ?"
    selectGetEntitiesByType = "SELECT DISTINCT entityID FROM Entity WHERE memePath IN (?)"
    selectGetEntitiesByMetamemeType = "SELECT DISTINCT entityID FROM Entity WHERE metaMeme IN (?)"
    selectGetAllEntities = "SELECT DISTINCT entityID FROM Entity"
    selectGetAllEntitiesActive0 = "SELECT DISTINCT entityID FROM Entity WHERE depricated=0"
    selectGetAllEntitiesActive1 = "SELECT DISTINCT entityID FROM Entity WHERE depricated=1"
    selectGetRessurectedEntities0 = "SELECT DISTINCT entityID, memePath, metaMeme, masterEntityID FROM Entity WHERE depricated=0"
    selectGetRessurectedEntities1 = "SELECT DISTINCT entityID, memePath, metaMeme, masterEntityID FROM Entity WHERE depricated=1"
    selectAddEntityTest = "SELECT entityID FROM Entity WHERE entityID=?"
    selectAllLinks = "SELECT * FROM EntityLink" 
    selectAllInboundLinks = "SELECT * FROM EntityLink WHERE memberID2=?"
    selectAllOutboundLinks = "SELECT * FROM EntityLink WHERE memberID1=?"
    selectCounterpartIndices = "SELECT DISTINCT entityLinkID FROM EntityLink WHERE memberID1=? OR memberID1=?"
    selectLinkAttributeTestBool = "SELECT DISTINCT propVal FROM EntityLinkPropertyBooleans WHERE entityLinkID=? AND propName=?"
    selectLinkAttributeTestInt = "SELECT DISTINCT propVal FROM EntityLinkPropertyIntegers WHERE entityLinkID=? AND propName=?"
    selectLinkAttributeTestDec = "SELECT DISTINCT propVal FROM EntityLinkPropertyDecimals WHERE entityLinkID=? AND propName=?"
    selectLinkAttributeTestStr = "SELECT DISTINCT propVal FROM EntityLinkPropertyStrings WHERE entityLinkID=? AND propName=?"
    selectRemoveLinkTest = "SELECT DISTINCT entityLinkID FROM EntityLink WHERE memberID1=? AND memberID2=?"
    selectEntityMeme = "SELECT DISTINCT memePath FROM Entity WHERE entityID=?"
    selectGetEntityPropertyLists = "SELECT * FROM EntityPropertyLists WHERE entityID=?"    #Returns: [entityID, propName, propVal, memePath]
    selectGetEntityPropertyBooleans = "SELECT * FROM EntityPropertyBooleans WHERE entityID=?" #Returns: [entityID, propName, propVal, memePath]
    selectGetEntityPropertyStrings = "SELECT * FROM EntityPropertyStrings WHERE entityID=?"  #Returns: [entityID, propName, propVal, restList, memePath]
    selectGetEntityPropertyTexts = "SELECT * FROM EntityPropertyTexts WHERE entityID=?"    #Returns: [entityID, propName, propVal, restList, memePath]
    selectGetEntityPropertyDecimals = "SELECT * FROM EntityPropertyDecimals WHERE entityID=?" #Returns: [entityID, propName, propVal, restMin, restMax, restList, memePath]
    selectGetEntityPropertyIntegers= "SELECT * FROM EntityPropertyIntegers WHERE entityID=?" #Returns: [entityID, propName, propVal, restMin, restMax, restList, memePath]

    #These select statements are for deleting entities
    removeEntityTags = "DELETE FROM EntityTags WHERE entityID=?"
    removeEntity = "DELETE FROM Entity WHERE entityID=?"
    removeLinks = "DELETE FROM EntityLink WHERE memberID1=? OR memberID2=?" 
    removeLinkAttributeBool = "DELETE FROM EntityLinkPropertyBooleans WHERE entityLinkID=?"
    removeLinkAttributeInt = "DELETE FROM EntityLinkPropertyIntegers WHERE entityLinkID=?"
    removeLinkAttributeDec = "DELETE FROM EntityLinkPropertyDecimals WHERE entityLinkID=?"
    removeLinkAttributeStr = "DELETE FROM EntityLinkPropertyStrings WHERE entityLinkID=?"
    removeEntityPropertyLists = "DELETE FROM EntityPropertyLists WHERE entityID=?"    
    removeEntityPropertyBooleans = "DELETE FROM EntityPropertyBooleans WHERE entityID=?"
    removeEntityPropertyStrings = "DELETE FROM EntityPropertyStrings WHERE entityID=?"
    removeEntityPropertyTexts = "DELETE FROM EntityPropertyTexts WHERE entityID=?"
    removeEntityPropertyDecimals = "DELETE FROM EntityPropertyDecimals WHERE entityID=?"
    removeEntityPropertyIntegers = "DELETE FROM EntityPropertyIntegers WHERE entityID=?"
    
    #########################
    #     Graph Module
    #########################
    selectMemesFromMetamameTable = "SELECT ? FROM ?"
    selectImplicitMemesFromMetamemeTable = "SELECT ? FROM ? WHERE ?=?"
    selectImplicitMemesForwardReferences = "SELECT ? FROM ? WHERE ?=?"
    selectImplicitMemesBackwardReferences = "SELECT ? FROM ? WHERE ?=?"
    
    
    def createRuntimeDB(self, db):
        try:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE Entity(entityID NVARCHAR(38) NOT NULL, depricated INT NOT NULL, memePath NVARCHAR(100) NOT NULL, metaMeme NVARCHAR(100) NOT NULL, masterEntityID NVARCHAR(38) NOT NULL, PRIMARY KEY (entityID))")
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
        except Exception as e:
            unusedDebug = e
        
        
    def resetRuntimeDB(self, db):
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
        self.createDB(db)
        
        
    def createTestDB(self, db):
        cursor = db.cursor()
        cursor.execute("CREATE TABLE BridgedTo (propertyF NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyF))")
        cursor.execute("CREATE TABLE IsChild (propertyD NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyD))")
        cursor.execute("CREATE TABLE IsGrandChild (propertyE NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyE))")
        cursor.execute("CREATE TABLE EndEffector (propertyAA NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyAA))")
        cursor.execute("CREATE TABLE MiddleNode (propertyQ NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyQ))")
        cursor.execute("CREATE TABLE SecondMiddleNodeHop (propertyCC NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyCC))")
        cursor.execute("CREATE TABLE FirstMiddleNodeHop (propertyBB NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyBB))")
        cursor.execute("CREATE TABLE ClonedSecondHop (propertyDD NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyDD))")
        cursor.execute("CREATE TABLE NotClonedSecondHop (propertyEE NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyEE))")
        cursor.execute("CREATE TABLE ClonedFirstHop (propertyFF NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyFF))")
        cursor.execute("CREATE TABLE NotClonedFirstHop (propertyGG NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyGG))")
        cursor.execute("CREATE TABLE SimpleMM (propertyA NVARCHAR(36) NOT NULL , propertyB NVARCHAR(36), PRIMARY KEY (propertyA))")
        cursor.execute("CREATE TABLE HasChild (propertyC NVARCHAR(36) NOT NULL, propertyH NVARCHAR(36) NOT NULL, propertyM NVARCHAR(200) NOT NULL, propertyN NVARCHAR(200) NOT NULL, propertyR NVARCHAR(36) NOT NULL, PRIMARY KEY (propertyC))")
        cursor.execute("CREATE TABLE HasChildPhase2 (propertyHH NVARCHAR(36), propertyII NVARCHAR(200), propertyJJ NVARCHAR(200), propertyKK NVARCHAR(200), propertyLL NVARCHAR(200), propertyMM NVARCHAR(200), propertyOO NVARCHAR(200), propertyPP NVARCHAR(200), propertyQQ NVARCHAR(200), propertyRR NVARCHAR(200), PRIMARY KEY (propertyHH))")
        cursor.execute("CREATE TABLE IsBRChild (propertyK NVARCHAR(36) NOT NULL, propertyL NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyK))")
        cursor.execute("CREATE TABLE IsBRGrandChild (propertyO NVARCHAR(36) NOT NULL, propertyP NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyO))")
        cursor.execute("CREATE TABLE Bridge (propertyG NVARCHAR(36) NOT NULL, propertyI NVARCHAR(200) NOT NULL, propertyJ NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyG))")
        cursor.execute("CREATE TABLE LogTable (logTime NVARCHAR(36) NOT NULL, logLevel NVARCHAR(6) NOT NULL, method NVARCHAR(50) NOT NULL, message NVARCHAR(1000) NOT NULL) ")
        cursor.execute("INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_1')")
        cursor.execute("INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_2')")
        cursor.execute("INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_3')")
        cursor.execute("INSERT INTO IsChild (propertyD) VALUES ('IsChild_1')")
        cursor.execute("INSERT INTO IsChild (propertyD) VALUES ('IsChild_2')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_00')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_01')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_02')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_03')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_04')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_05')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_06')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_07')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_08')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_09')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_10')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_11')")
        cursor.execute("INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_12')")
        cursor.execute("INSERT INTO IsGrandChild (propertyE) VALUES ('IsGrandChild_1')")
        cursor.execute("INSERT INTO IsGrandChild (propertyE) VALUES ('IsGrandChild_2')")
        cursor.execute("INSERT INTO SimpleMM (propertyA, propertyB) VALUES ('SimpleMM_1', 'propertyB_Val')")
        cursor.execute("INSERT INTO SimpleMM (propertyA, propertyB) VALUES ('SimpleMM_2', 'propertyB_Val')")
        cursor.execute("INSERT INTO MiddleNode (propertyQ) VALUES ('MiddleNodeMeme_1')")
        cursor.execute("INSERT INTO MiddleNode (propertyQ) VALUES ('MiddleNodeMeme_2')")
        cursor.execute("INSERT INTO SecondMiddleNodeHop (propertyCC) VALUES ('SecondMiddleNodeHop_1')")
        cursor.execute("INSERT INTO SecondMiddleNodeHop (propertyCC) VALUES ('SecondMiddleNodeHop_2')")
        cursor.execute("INSERT INTO FirstMiddleNodeHop (propertyBB) VALUES ('FirstMiddleNodeHop_1')")
        cursor.execute("INSERT INTO FirstMiddleNodeHop (propertyBB) VALUES ('FirstMiddleNodeHop_2')")
        cursor.execute("INSERT INTO ClonedSecondHop (propertyDD) VALUES ('ClonedSecondHop_1')")
        cursor.execute("INSERT INTO NotClonedSecondHop (propertyEE) VALUES ('NotClonedSecondHop_1')")
        cursor.execute("INSERT INTO ClonedFirstHop (propertyFF) VALUES ('ClonedFirstHop_1')")
        cursor.execute("INSERT INTO NotClonedFirstHop (propertyGG) VALUES ('NotClonedFirstHop_1')")
        cursor.execute("INSERT INTO HasChild (propertyC, propertyH, propertyM, propertyN, propertyR) VALUES ('HasChild_1', 'propertyH_Val1', 'IsChild_1', 'ImplicitMemes.IsGrandChild_1', 'ImplicitMemes.MiddleNodeMeme_1')")
        cursor.execute("INSERT INTO HasChild (propertyC, propertyH, propertyM, propertyN, propertyR) VALUES ('HasChild_2', 'propertyH_Val1', 'IsChild_2', 'ImplicitMemes.IsGrandChild_2', 'ImplicitMemes.MiddleNodeMeme_2')")
        cursor.execute("INSERT INTO HasChildPhase2 (propertyHH, propertyII, propertyLL, propertyMM) VALUES ('HasChildPhase2_1', 'ImplicitMemes.FirstMiddleNodeHop_1', 'ImplicitMemes.SecondMiddleNodeHop_1', 'ImplicitMemes.EndEffector_00')")
        cursor.execute("INSERT INTO HasChildPhase2 (propertyHH, propertyII, propertyLL, propertyMM) VALUES ('HasChildPhase2_2', 'ImplicitMemes.FirstMiddleNodeHop_2', 'ImplicitMemes.SecondMiddleNodeHop_2', 'ImplicitMemes.EndEffector_01')")
        cursor.execute("INSERT INTO HasChildPhase2 (propertyHH, propertyJJ, propertyQQ, propertyOO) VALUES ('HasChildPhase2_3', 'ImplicitMemes.NotClonedFirstHop_1', 'ImplicitMemes.ClonedSecondHop_1', 'ImplicitMemes.EndEffector_02')")
        cursor.execute("INSERT INTO HasChildPhase2 (propertyHH, propertyKK, propertyRR, propertyPP) VALUES ('HasChildPhase2_4', 'ImplicitMemes.ClonedFirstHop_1', 'ImplicitMemes.NotClonedSecondHop_1', 'ImplicitMemes.EndEffector_03')")
        cursor.execute("INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_1', 'HasChild_1')")
        cursor.execute("INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_2', 'HasChild_1')")
        cursor.execute("INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_3', 'HasChild_2')")
        cursor.execute("INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_1', 'HasChild_1')")
        cursor.execute("INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_2', 'HasChild_1')")
        cursor.execute("INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_3', 'HasChild_2')")
        cursor.execute("INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_1', 'HasChild_1', 'BridgedTo_1')")
        cursor.execute("INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_2', 'HasChild_1', 'BridgedTo_2')")
        cursor.execute("INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_3', 'HasChild_2', 'BridgedTo_3')")
        db.commit()


class SyntaxSAPHana(object):
    pass

