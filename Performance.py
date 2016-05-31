#!/usr/bin/env python3

"""
   Performance.py: Performance testing utility for Graphyne; allowing the user to investigate performance and scalability of various persistence options.
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'

import Graphyne
import multiprocessing
import os
import shutil
import queue
import sys
import time
import math
import urllib.parse
import urllib.request
from xml.dom import minidom
from os.path import expanduser

import Smoketest
import Graphyne.Graph as Graph
import Graphyne.Fileutils as Fileutils


responseQueue = queue.Queue()
entityList = []
api = None


global testImplicit
testImplicit = True


#Globals
#graphDir = expanduser("~")
#graphDir = os.getcwd()
graphDir = os.path.dirname(os.path.dirname(Graph.__file__))
testDirPath = os.path.join(graphDir, "Config", "Test")
configDirPath = os.path.join(graphDir, "Config")
includeJSDirPath = os.path.join(graphDir, "Config", "js")

resultFile = None
moduleName = 'Smoketest'     
logType = Graph.logTypes.CONTENT
logLevel = Graph.logLevel



class PerformanceResults(object):
    noPersistence = {}
    sqliteInMemory = {}
    conString = {}
    maxScaleFactor = 0
    maxEntityCount = 0
    timeMax = 0.0
    xMin = 0.0
    xMax = 0.0
    yMin = 0.0
    yMax = 0.0
    
    def createFakeData(self):
        #self.noPersistence = {1: [527, 1.431999921798706]}
        #self.conString = {0: [527, 23.304999828338623], 1: [527, 13.46999979019165]}
        
        #self.noPersistence = {1: [527, 1.431999921798706], 2: [1527, 11.431999921798706]}
        self.addResult('memory', 1, 1.431999921798706, 527)
        self.addResult('memory', 2, 11.431999921798706, 1527)
        
        self.addResult(None, 1, 1.331999921798706, 527)
        self.addResult(None, 2, 10.431999921798706, 1527)
        
        #self.conString = {0: [527, 23.304999828338623], 1: [527, 13.46999979019165]}
        self.addResult('conString', 1, 13.46999979019165, 527)
        self.addResult('conString', 2, 23.304999828338623, 1527)
        
        
    def addResult(self, profileID, scaleFactor, time, entityCount):
        #ensure that the scale factor is an int
        scaleFactor = int(scaleFactor)
        entityCount = int(entityCount)
        if self.maxScaleFactor < scaleFactor:
            self.maxScaleFactor = scaleFactor
        if self.maxEntityCount < entityCount:
            self.maxEntityCount = entityCount
        if self.timeMax < time:
            self.timeMax = time
        
        if profileID is None:
            self.noPersistence[scaleFactor] = [entityCount, time]
        elif profileID == 'sqlite':
            self.sqliteInMemory[scaleFactor] = [entityCount, time]
        else:
            self.conString[scaleFactor] = [entityCount, time]
            
    def getVars(self):
        return ['noPersistence', 'sqliteInMemory', 'conString']
    
    def getProfileResults(self, profile):
        #{"testTime": "202","entityCount": "2000"}, {"testTime": "202","entityCount": "2000"}, ...
        resultset = []
        nNth = 1
        resultCount = len(profile)
        keyList = sorted(profile.keys()) 
        for profileEntryKey in keyList:
            profileEntryValue = profile[profileEntryKey]
            if nNth < resultCount:
                resultset.append('        {\"testTime\": \"%s\",\"entityCount\": \"%s\"},' %(profileEntryValue[1], profileEntryValue[0]))
            else:
                resultset.append('        {\"testTime\": \"%s\",\"entityCount\": \"%s\"}' %(profileEntryValue[1], profileEntryValue[0]))
            nNth = nNth + 1
        return resultset
    
    def getData(self):
        nNth = 1
        resultset = []
        resultset.append("data = [")
        profileNames = self.getVars()
        resultCount = len(profileNames)
        for profileName in profileNames:
            resultset.append("    [")
            try:
                profile = getattr(self, profileName)
                profileResults = self.getProfileResults(profile)
                resultset.extend(profileResults)
                if nNth < resultCount:
                    resultset.append("    ],")
                else:
                    resultset.append("    ]")
                nNth = nNth + 1
            except Graphyne.Exceptions.UtilityError as e:
                print(e)
            except Exception as e:
                pass
        resultset.append("];")
        return resultset
        
        
    def getLabels(self):
        nNth = 0
        resultset = "labels = ["
        profileNames = self.getVars()
        for profileName in profileNames:
            if nNth > 0:
                resultset = '%s, "%s"' %(resultset, profileName)
            else:
                resultset = '%s"%s"' %(resultset, profileName)
            nNth = nNth + 1
        resultset = "%s];\n" %resultset
        return resultset
            
            
    def getRanges(self):
        #ranges  = {"xMin": "527", "xMax": "1527", "yMin": "0", "yMax": "50"}; 
        xMax = self.maxEntityCount * 1.1      
        yMax = self.timeMax * 1.1
        ranges = 'ranges = {"xMin": "0", "xMax": "%s", "yMin": "0", "yMax": "%s"};\n' %(xMax, yMax)
        return ranges


def usage():
    print(__doc__)




def path2url(path):
    return urllib.parse.urljoin('file:', urllib.request.pathname2url(path))



def publishResults(testReports, fileName, runTime):
    #testReport = {"resultSet" : resultSet, "validationTime" : validationTime, "persistence" : persistence.__name__} 
    #resultSet = [u"Condition (Remote Child)", copy.deepcopy(testSetData), testSetPercentage])
    titleText = "Graphyne Performance Test Suite - Results"
    scaleFactor = "Max Scale Factor:  %s    Max Entity Count:  %s" %(testReports.maxScaleFactor, testReports.maxEntityCount)
    testTime = "Total Test Duration: %.1f seconds" %runTime
    
    persistenceTypes = "%s Persistence Types:  " %(len(testReports.getVars()))
    pTypesList = testReports.getVars()
    nNthType = 0
    for pTypesListEntry in pTypesList:
        if nNthType > 0:
            persistenceTypes = "%s, " %persistenceTypes
        persistenceTypes = "%s%s" %(persistenceTypes, pTypesListEntry)
        nNthType = nNthType + 1
        
    #File Locations
    logRoot =  expanduser("~")
    logDir = os.path.join(logRoot, "Graphyne")
    jsDir = os.path.join(logDir, "GraphynePerformanceTestResult")
        
    # Create the minidom document
    doc = minidom.Document()
    
    # Create the <html> base element
    html = doc.createElement("html")
    html.setAttribute("xmlns", "http://www.w3.org/1999/xhtml")
        
    # Create the <head> element
    head = doc.createElement("head")
    title = doc.createElement("title")
    titleTextNode = doc.createTextNode(titleText)
    title.appendChild(titleTextNode)
    head.appendChild(title)
        
    body = doc.createElement("body")
    h1 = doc.createElement("h1")
    h1Text = doc.createTextNode(titleText)
    h1.appendChild(h1Text)
    head.appendChild(h1)
    h21 = doc.createElement("h2")
    h21Text = doc.createTextNode(persistenceTypes)
    h21.appendChild(h21Text)
    head.appendChild(h21)
    h22 = doc.createElement("h2")
    h22Text = doc.createTextNode(scaleFactor)
    h22.appendChild(h22Text)
    head.appendChild(h22)
    h23 = doc.createElement("h2")
    h23Text = doc.createTextNode(testTime)
    h23.appendChild(h23Text)
    head.appendChild(h23)
    h3 = doc.createElement("h2")
    h3Text = doc.createTextNode("Tests Finished at:  %s" %(time.ctime()))
    h3.appendChild(h3Text)
    head.appendChild(h3)
    
    
    """
        The Master table wraps all the result sets.
        masterTableHeader contains all of the overview blocks
        masterTableBody contains all of the detail elements
    """  
    #<svg id="visualisation" width="1000" height="500"></svg>
    svg = doc.createElement("svg")
    svg.setAttribute("id", "visualisation")
    svg.setAttribute("width", "1000")
    svg.setAttribute("height", "500")
    svg.appendChild(doc.createTextNode('')) #Because self closing tags break most browsers :(
    body.appendChild(svg)
    
    #<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
    d3 = doc.createElement("script")
    d3.setAttribute("src", "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js")
    d3.setAttribute("charset", "utf-8")
    d3.appendChild(doc.createTextNode('')) #Because self closing tags break most browsers :(
    body.appendChild(d3)
    
    #<script src="Data.js" charset="utf-8"></script>
    #<script src="InitChart.js" charset="utf-8"></script>
    includeJSSourceData = os.path.join(jsDir, "Data.js")
    includeJSSourceFunction = os.path.join(jsDir, "InitChart.js")
    includeJSPathData = path2url(includeJSSourceData)
    includeJSPathFunction = path2url(includeJSSourceFunction)
    includeData = doc.createElement("script")
    includeData.setAttribute("src", includeJSPathData)
    includeData.setAttribute("charset", "utf-8")
    includeData.appendChild(doc.createTextNode('')) #Because self closing tags break most browsers :(
    body.appendChild(includeData)
    initChart = doc.createElement("script")
    initChart.setAttribute("src", includeJSPathFunction)
    initChart.setAttribute("charset", "utf-8")
    initChart.appendChild(doc.createTextNode('')) #Because self closing tags break most browsers :(
    body.appendChild(initChart)
    
    #The script that puts it all togther
    labels = testReports.getLabels()
    data = testReports.getData()
    ranges = testReports.getRanges()
    theScript = doc.createElement("script")
    scriptText = doc.createTextNode("InitChart();")
    theScript.appendChild(scriptText)
    body.appendChild(theScript)

    html.appendChild(head)
    html.appendChild(body)
    doc.appendChild(html)

    fileStream = doc.toprettyxml(indent = "    ")
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    resultFileLoc = os.path.join(logDir, fileName)
    fileObject = open(resultFileLoc, "w", encoding="utf-8")
    #fileObject.write(Fileutils.smart_str(fileStream))
    fileObject.write(fileStream)
    fileObject.close()
    
    #Make sure that the included JS files go with it
    includeJS = os.path.join(includeJSDirPath, "InitChart.js")
    if not os.path.exists(jsDir):
        os.makedirs(jsDir)
    copyTo = os.path.join(jsDir, "InitChart.js")
    shutil.copyfile(includeJS, copyTo)
    
    #Make dure that data.js is created and filled
    fileObject = open(includeJSSourceData, "w", encoding="utf-8")
    fileObject.write(labels)
    fileObject.write(ranges)
    for datapoint in data:
        fileObject.write('%s\n' %datapoint)
    fileObject.close()
        



def smokeTestSet(restltQueue, lLevel, css, dbConnectionString = None, persistenceType = None, scaleFactor = 100, createTestDatabase = False):
    '''
    repoLocations = a list of all of the filesystem location that that compose the repository.
    useDeaultSchema.  I True, then load the 'default schema' of Graphyne
    persistenceType = The type of database used by the persistence engine.  This is used to determine which flavor of SQL syntax to use.
        Enumeration of Possible values:
        Default to None, which is no persistence
        "sqlite" - Sqlite3
        "mssql" - Miscrosoft SQL Server
        "hana" - SAP Hana
    persistenceArg = the Module/class supplied to host the entityRepository and LinkRepository.  If default, then use the Graphyne.DatabaseDrivers.NonPersistent module.
        Enumeration of possible values:
        None - May only be used in conjunction with "sqlite" as persistenceType and will throw an InconsistentPersistenceArchitecture otherwise
        "none" - no persistence.  May only be used in conjunction with "sqlite" as persistenceType and will throw an InconsistentPersistenceArchitecture otherwise
        "memory" - Use SQLite in in-memory mode (connection = ":memory:")
        "<valid filename with .sqlite as extension>" - Use SQLite, with that file as the database
        "<filename with .sqlite as extension, but no file>" - Use SQLite and create that file to use as the DB file
        "<anything else>" - Presume that it is a pyodbc connection string and throw a InconsistentPersistenceArchitecture exception if the dbtype is "sqlite".
    createTestDatabase = a flag for creating regression test data.  This flag is only to be used for regression testing the graph and even then, only if the test 
        database does not already exist.
        
        *If persistenceType is None (no persistence, then this is ignored and won't throw any InconsistentPersistenceArchitecture exceptions)
    '''
    #import pydevd
    try:
        try:
            if persistenceType is None:
                #pydevd.settrace()
                from Graphyne.DatabaseDrivers import NonPersistent as persistenceModule1
                testReport = Smoketest.smokeTestSet(persistenceModule1, lLevel, css, "No-Persistence", dbConnectionString, persistenceType, True, True, scaleFactor)
            elif ((persistenceType == "sqlite") and (dbConnectionString== "memory")):
                #pydevd.settrace()
                from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModule2
                testReport = Smoketest.smokeTestSet(persistenceModule2, lLevel, css, "sqllite", dbConnectionString, persistenceType, True, True, scaleFactor)
            elif persistenceType == "memory":
                from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModule4
                testReport = Smoketest.smokeTestSet(persistenceModule4, lLevel, css, "sqllite", dbConnectionString, persistenceType, True, True, scaleFactor)
            else:
                #pydevd.settrace()
                from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModul3
                testReport = Smoketest.smokeTestSet(persistenceModul3, lLevel, css, persistenceType, dbConnectionString, persistenceType, True, True, scaleFactor)
            restltQueue.put(testReport)
        except Exception:
            from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModul32
            testReport = Smoketest.smokeTestSet(persistenceModul32, lLevel, css, persistenceType, dbConnectionString, persistenceType, True, True, scaleFactor)
            restltQueue.put(testReport) 
    except Exception as e:
        errorMsg = "Error in Smoketest: dbConnectionString=%s, persistenceType=%s, scaleFactor=%s, createTestDatabase=%s.  Traceback = %s"  %(dbConnectionString, persistenceType, scaleFactor, createTestDatabase, e)
        print(errorMsg)
        restltQueue.put(None)


    
if __name__ == "__main__":
    '''         
    This module runs the smoketest suite on larger datasets to test scalability (at least with regards to entity repository size)
    
    Four (optional) initial params:
        sys.argv[1] - Scale factor (S).  Given N non-singleton memes, N*S "ballast" entities will be created in the DB before starting the test suite.
    
        The user can add 0..n database connections to the performance test run.  Each requires a includes a connection-string/persistence-type pair, as outlined below.
          E.g. to test against Microsoft SQL Server and SAP Hana in the same run, you might use the following parameters:
              sys.argv[2] = SAP Hana ODBC connection string
              sys.argv[3] = "hana"
              sys.argv[4] = MSSQL Server ODBC connection string
              sys.argv[5] = MSSQL Server ODBC connection string
              
        sys.argv[2+ (even)] - Is the connection string.
            "none" - no persistence
            "memory" - Use SQLite in in-memory mode (connection = ":memory:")
            "<valid filename>" - Use SQLite, with that file as the database
            "<filename with .sqlite as extension, but no file>" - Use SQLite and create that file to use as the DB file
            "<anything else>" - Presume that it is a pyodbc connection string
            Default to None, which is no persistence

        sys.argv[3+ (odd)]     persistenceType = The type of database used by the persistence engine.  This is used to determine which flavor of SQL syntax to use.
            Enumeration of Possible values:
            Default to None, which is no persistence
            "sqlite" - Sqlite3
            "mssql" - Miscrosoft SQL Server
            "hana" - SAP Hana     
                        
        
    E.g. Performance.py 8 'memory' 'sqlite'      #For sqlite3 database, with :memory: connection and scale factor 8
    E.g. Performance.py 8                        #For no persistence and scale factor 8
    
    '''
    performanceResults = PerformanceResults()  
    
    startTime = time.time()
    
    print("\nStarting Graphyne Smoke Test")    
    
    lLevel = Graph.logLevel.ERROR

    scaleFactor = 4
    try:
        if sys.argv[1] is not None:
            scaleFactor = int(sys.argv[1])
    except:
        pass

    nNth = 1
    scale = 0
    scaleQueue = [nNth]
    while nNth <= scaleFactor:
        nNth = nNth + 1
        scaleQueue.append(math.pow(2, int(nNth)))

    #Collect the parameters for the database connections
    databaseConnections = []
    checkForConnection = True
    dbConnectionIndex = 2
    persistenceTypeIndex = 3
    while checkForConnection == True:
        persistenceType = None
        dbConnectionString = None
        try:
            dbConnectionString = sys.argv[dbConnectionIndex]
            persistenceType = sys.argv[persistenceTypeIndex]
            databaseConnections.append([dbConnectionString, persistenceType])
            dbConnectionIndex = dbConnectionIndex + 2
            persistenceTypeIndex = persistenceTypeIndex + 2
        except:
            checkForConnection = False

    echoStartMessage = "   ...params: scaleFactor = %s" %scaleFactor
    for databaseConnectionInfo in databaseConnections:
        echoStartMessage = "%s\n              db driver = %s, connection string = %s" %(echoStartMessage, databaseConnectionInfo[1], databaseConnectionInfo[0])
    print(echoStartMessage)
   
    css = Fileutils.defaultCSS()
    
    #smokeTestSet(lLevel, css, dbConnectionString = None, persistenceType = None, scaleFactor = 100, createTestDatabase = False
    persistenceConstellations = []
    persistenceConstellations.append([None, None, True])          #dbConnectionString, persistenceType, createTestDatabase
    persistenceConstellations.append(['memory', 'sqlite', True])  ##dbConnectionString, persistenceType, createTestDatabase
    for databaseConnectionInfo in databaseConnections:
        persistenceConstellations.append([databaseConnectionInfo[0], databaseConnectionInfo[1], False])   ##dbConnectionString, persistenceType, createTestDatabase
        
    
    #For each scalefactr/persistence type combination, we'll make a testrun.    
    responseQueue = multiprocessing.Queue()
    for pCon in persistenceConstellations:
        for cScaleFactor in scaleQueue:
            try:
                p = multiprocessing.Process(target=smokeTestSet, args=(responseQueue, lLevel, css, pCon[0], pCon[1], int(cScaleFactor), True,))
                p.start()    
                
                hasReturned = False
                while hasReturned == False:
                    try:
                        localResult = responseQueue.get_nowait()
                        hasReturned = True
                        
                        if localResult is not None:
                            #if we've not thrown an Empty exception, then we have our result and it is time to collect that and shut the child proccess down
                            performanceResults.addResult(pCon[1], int(cScaleFactor), localResult['validationTime'], localResult['entityCount'])
                            print("...persistence profile %s, scale factor %s has returned results with t= %s" %(pCon[1], cScaleFactor, localResult['validationTime']))
                        else:
                            print("...persistence profile %s, scale factor %s failed!" %(pCon[1], cScaleFactor))
                    except queue.Empty:
                        time.sleep(10.0)
                    except Exception as e:
                        errorMsg = "Error in Smoketest: %s, %s, %s, %s"  %(pCon[0], pCon[1], cScaleFactor, pCon[2])
                        print(errorMsg)
                endTime = time.time()
                runTime = endTime - startTime 
                publishResults(performanceResults, "GraphynePerformanceTestResult.html", runTime)
                        
                p.terminate()
                p.join(1.0)
            except Exception as e:
                print(e)
 
    endTime = time.time()
    runTime = endTime - startTime 
    print(("Finished at %s.  Total time = %s" %(endTime, runTime)))