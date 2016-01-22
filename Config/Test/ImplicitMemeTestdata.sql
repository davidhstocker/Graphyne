CREATE TABLE BridgedTo (propertyF NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyF));
CREATE TABLE IsChild (propertyD NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyD));
CREATE TABLE IsGrandChild (propertyE NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyE));
CREATE TABLE EndEffector (propertyAA NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyAA));
CREATE TABLE MiddleNode (propertyQ NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyQ));
CREATE TABLE SecondMiddleNodeHop (propertyCC NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyCC));
CREATE TABLE FirstMiddleNodeHop (propertyBB NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyBB));
CREATE TABLE ClonedSecondHop (propertyDD NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyDD));
CREATE TABLE NotClonedSecondHop (propertyEE NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyEE));
CREATE TABLE ClonedFirstHop (propertyFF NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyFF));
CREATE TABLE NotClonedFirstHop (propertyGG NVARCHAR(36) NOT NULL , PRIMARY KEY (propertyGG));
CREATE TABLE SimpleMM (propertyA NVARCHAR(36) NOT NULL , propertyB NVARCHAR(36), PRIMARY KEY (propertyA));
CREATE TABLE HasChild (propertyC NVARCHAR(36) NOT NULL, propertyH NVARCHAR(36) NOT NULL, propertyM NVARCHAR(200) NOT NULL, propertyN NVARCHAR(200) NOT NULL, propertyR NVARCHAR(36) NOT NULL, PRIMARY KEY (propertyC));
CREATE TABLE HasChildPhase2 (propertyHH NVARCHAR(36), propertyII NVARCHAR(200), propertyJJ NVARCHAR(200), propertyKK NVARCHAR(200), propertyLL NVARCHAR(200), propertyMM NVARCHAR(200), propertyOO NVARCHAR(200), propertyPP NVARCHAR(200), propertyQQ NVARCHAR(200), propertyRR NVARCHAR(200), PRIMARY KEY (propertyHH));
CREATE TABLE IsBRChild (propertyK NVARCHAR(36) NOT NULL, propertyL NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyK));
CREATE TABLE IsBRGrandChild (propertyO NVARCHAR(36) NOT NULL, propertyP NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyO));
CREATE TABLE Bridge (propertyG NVARCHAR(36) NOT NULL, propertyI NVARCHAR(200) NOT NULL, propertyJ NVARCHAR(200) NOT NULL, PRIMARY KEY (propertyG));
CREATE TABLE LogTable (logTime NVARCHAR(36) NOT NULL, logLevel NVARCHAR(6) NOT NULL, method NVARCHAR(50) NOT NULL, message NVARCHAR(1000) NOT NULL) 


INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_1');
INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_2');
INSERT INTO BridgedTo (propertyF) VALUES ('BridgedTo_3');

INSERT INTO IsChild (propertyD) VALUES ('IsChild_1');
INSERT INTO IsChild (propertyD) VALUES ('IsChild_2');

INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_00');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_01');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_02');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_03');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_04');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_05');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_06');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_07');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_08');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_09');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_10');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_11');
INSERT INTO EndEffector (propertyAA) VALUES ('EndEffector_12');

INSERT INTO IsGrandChild (propertyE) VALUES ('IsGrandChild_1');
INSERT INTO IsGrandChild (propertyE) VALUES ('IsGrandChild_2');

INSERT INTO SimpleMM (propertyA, propertyB) VALUES ('SimpleMM_1', 'propertyB_Val');
INSERT INTO SimpleMM (propertyA, propertyB) VALUES ('SimpleMM_2', 'propertyB_Val');

INSERT INTO MiddleNode (propertyQ) VALUES ('MiddleNodeMeme_1');
INSERT INTO MiddleNode (propertyQ) VALUES ('MiddleNodeMeme_2');

INSERT INTO SecondMiddleNodeHop (propertyCC) VALUES ('SecondMiddleNodeHop_1');
INSERT INTO SecondMiddleNodeHop (propertyCC) VALUES ('SecondMiddleNodeHop_2');

INSERT INTO FirstMiddleNodeHop (propertyBB) VALUES ('FirstMiddleNodeHop_1');
INSERT INTO FirstMiddleNodeHop (propertyBB) VALUES ('FirstMiddleNodeHop_2');

INSERT INTO ClonedSecondHop (propertyDD) VALUES ('ClonedSecondHop_1');

INSERT INTO NotClonedSecondHop (propertyEE) VALUES ('NotClonedSecondHop_1');

INSERT INTO ClonedFirstHop (propertyFF) VALUES ('ClonedFirstHop_1');

INSERT INTO NotClonedFirstHop (propertyGG) VALUES ('NotClonedFirstHop_1');

INSERT INTO HasChild (propertyC, propertyH, propertyM, propertyN, propertyR) VALUES ('HasChild_1', 'propertyH_Val1', 'IsChild_1', 'ImplicitMemes.IsGrandChild_1', 'ImplicitMemes.MiddleNodeMeme_1');
INSERT INTO HasChild (propertyC, propertyH, propertyM, propertyN, propertyR) VALUES ('HasChild_2', 'propertyH_Val1', 'IsChild_2', 'ImplicitMemes.IsGrandChild_2', 'ImplicitMemes.MiddleNodeMeme_2');

INSERT INTO HasChildPhase2 (propertyHH, propertyII, propertyLL, propertyMM) VALUES ('HasChildPhase2_1', 'ImplicitMemes.FirstMiddleNodeHop_1', 'ImplicitMemes.SecondMiddleNodeHop_1', 'ImplicitMemes.EndEffector_00');
INSERT INTO HasChildPhase2 (propertyHH, propertyII, propertyLL, propertyMM) VALUES ('HasChildPhase2_2', 'ImplicitMemes.FirstMiddleNodeHop_2', 'ImplicitMemes.SecondMiddleNodeHop_2', 'ImplicitMemes.EndEffector_01');
INSERT INTO HasChildPhase2 (propertyHH, propertyJJ, propertyQQ, propertyOO) VALUES ('HasChildPhase2_3', 'ImplicitMemes.NotClonedFirstHop_1', 'ImplicitMemes.ClonedSecondHop_1', 'ImplicitMemes.EndEffector_02');
INSERT INTO HasChildPhase2 (propertyHH, propertyKK, propertyRR, propertyPP) VALUES ('HasChildPhase2_4', 'ImplicitMemes.ClonedFirstHop_1', 'ImplicitMemes.NotClonedSecondHop_1', 'ImplicitMemes.EndEffector_03');

INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_1', 'HasChild_1');
INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_2', 'HasChild_1');
INSERT INTO IsBRChild (propertyK, propertyL) VALUES ('IsBRChild_3', 'HasChild_2');

INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_1', 'HasChild_1');
INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_2', 'HasChild_1');
INSERT INTO IsBRGrandChild (propertyO, propertyP) VALUES ('IsBRGrandChild_3', 'HasChild_2');

INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_1', 'HasChild_1', 'BridgedTo_1');
INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_2', 'HasChild_1', 'BridgedTo_2');
INSERT INTO Bridge (propertyG, propertyI, propertyJ) VALUES ('Bridge_3', 'HasChild_2', 'BridgedTo_3');
