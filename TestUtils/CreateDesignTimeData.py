'''
Created on Dec 7, 2014

@author: Dave

Generate the test data in memory or for the design time repo test.  This will create an sqlite database file, Config/Test/DesignTimeDB if it does not already exist and populate it

Alternatively, if this module is imported, another db may be supplied (e.g. :memory:
'''

import sqlite3

def createDB(db):
    try:
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
    except Exception:
        pass

if __name__ == "__main__":
    db = sqlite3.connect('Config/Test/DesignTimeDB')
    createDB(db)