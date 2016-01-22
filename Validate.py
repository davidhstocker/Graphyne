#!/usr/bin/env python3

"""
   Validate.py: Utility for validating Memetic schemas in Graphyne.
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'



from xml.dom import minidom
from os.path import expanduser
from time import ctime
import os
import time
import sys

import Graphyne.Graph as Graph
import Graphyne.Fileutils as Fileutils

entityList = []

#Globals
resultFile = None
moduleName = 'validate'     
logType = Graph.logTypes.CONTENT
logLevel = Graph.logLevel

totalValidNonSingletons = [0,0] #[total, valid]
totalValidSingletons = [0,0]    #[total, valid]


def usage():
    print(__doc__)
    

def countTemplates():
    global totalValidNonSingletons
    global totalValidSingletons
    countMetaMemes = []
    countMemes = []
    totalTemplates = 0
    # Count the memes, metamemes and restrictions
    for templateID in Graph.templateRepository.templates.keys():
        template = Graph.templateRepository.templates[templateID]
        totalTemplates = totalTemplates + 1
        
        
        try: 
            if template.className == "MetaMeme": countMetaMemes.append(template.path.fullTemplatePath)
        except: pass
        
        try: 
            if template.className == "Meme": countMemes.append(template.path.fullTemplatePath)
        except: pass
        
    countRestrictions = totalTemplates - len(countMetaMemes) - len(countMemes)    
    
    results = {}
    results["Restrictions"] = countRestrictions
    results["MetaMemes"] = countMetaMemes
    results["Memes"] = countMemes
    results["Memes - Non Singleton"] = totalValidNonSingletons[0]
    results["Memes - Singleton"] = totalValidSingletons[0]
    results["Templates"] = totalTemplates
    return results

    
    
    
def countEntities():
    countEntities = 0
    debugHelperIDs = Graph.scriptFacade.getAllEntities()
    for unusedHelperID in debugHelperIDs:
        countEntities = countEntities + 1

    results = {"Singleton Entities" : countEntities}
    return results
    
    
    
def validateMemes():
    global totalValidNonSingletons
    global totalValidSingletons
    totalResults = []
    totalValid = 0
    
    for moduleID in Graph.templateRepository.modules.keys():
        module = template = Graph.templateRepository.modules[moduleID]
        #print(module)
        
        moduleResults = []
        moduleCount = 0
        moduleValid = 0
        for listing in module:
            try:
                template = Graph.templateRepository.resolveTemplateAbsolutely(listing[1])
                if template.className == "Meme":
                    moduleCount = moduleCount + 1
                    
                    #Increment the total counter
                    if template.isSingleton == True:
                        totalValidSingletons[0] = totalValidSingletons[0] + 1
                    else:
                        totalValidNonSingletons[0] = totalValidNonSingletons[0] + 1
                            
                    validationResults = template.validate()  #returns [isValid, errorReport]
                    if validationResults[0] == True: 
                        totalValid = totalValid + 1
                        moduleValid = moduleValid + 1
                        
                        ##Increment the valid  counter
                        if template.isSingleton == True:
                            totalValidSingletons[1] = totalValidSingletons[1] + 1
                        else:
                            totalValidNonSingletons[1] = totalValidNonSingletons[1] + 1
                    else:
                        detailedResults = {}
                        detailedResults["meme"] = template.path.fullTemplatePath
                        detailedResults["metaMeme"] = template.metaMeme
                        detailedResults["results"] = validationResults[1]
                        detailedResults["isSingleton"] = template.isSingleton
                        moduleResults.append(detailedResults)
            except Exception as e: 
                print(e)
        totalResults.append([moduleID, moduleCount, moduleValid, moduleResults])   

    #debugging aid
    stringThing = ""
    for result in totalResults:
        stringThing = "\n%s" %result
    fileObject = open("ValidationStatus.txt", "w", encoding="utf-8")
    fileObject.write(stringThing)
    fileObject.close()
    return [totalValid, totalResults]



def publishResults(validationTime, counts, validationReportMeme, css = "", outputFilename = None):
    global totalValidNonSingletons
    global totalValidSingletons
    # Create the minidom document
    doc = minidom.Document()
    
    # Create the <html> base element
    html = doc.createElement("html")
    html.setAttribute("xmlns", "http://www.w3.org/1999/xhtml")
    doc.appendChild(html)
    
    # Create the <head> element
    head = doc.createElement("head")
    style = doc.createElement("style")
    defaultCSS = doc.createTextNode(css)
    style.appendChild(defaultCSS)
    title = doc.createElement("title")
    titleText = doc.createTextNode("Repository Validation - Results")
    title.appendChild(titleText)
    head.appendChild(style)
    head.appendChild(title)
    html.appendChild(head)
    
    body = doc.createElement("body")
    h1 = doc.createElement("h2")
    h1Text = doc.createTextNode("The Repository was validated in %.1f seconds on %s" %(validationTime, ctime()))
    h1.appendChild(h1Text)
    
    #Header Table - A container for the Overview and Module Overview tables
    headerTable = doc.createElement("table")
    headerTableRow = doc.createElement("tr")
    headerTableOVContainer = doc.createElement("td")
    headerTableMOVContainer = doc.createElement("td")
    
    #Overview Table
    overviewTable = doc.createElement("table")
    overviewTableHeader = doc.createElement("thead")
    overviewTableHeaderText = doc.createTextNode("Overview" )
    overviewTableHeader.appendChild(overviewTableHeaderText)
    overviewTableHeader.setAttribute("class", "tableheader")
    overviewTable.appendChild(overviewTableHeader)
    
    headers = ["", "Count", "Valid"]
    #Header Row
    ovTableHeaderRow = doc.createElement("tr")
    for headerEntry in headers:
        cell = doc.createElement("th")
        cellText = doc.createTextNode("%s" %headerEntry)
        cell.appendChild(cellText)
        ovTableHeaderRow.appendChild(cell)
    overviewTable.appendChild(ovTableHeaderRow)
    
    for overviewLineKey in counts.keys():
        if overviewLineKey != "Templates":
            count = counts[overviewLineKey]
            if (overviewLineKey == "Memes") or (overviewLineKey == "MetaMemes"):
                count = len(count)
            
            result = ""
            
            percentageResult = 100
            if overviewLineKey == "Memes":
                if count > 0:
                    normalizedResult = validationReportMeme[0]/count
                    percentageResult = normalizedResult * 100.00
                    result = "%d%%" % percentageResult
                result = "%d%%" % percentageResult
            elif overviewLineKey == "Memes - Non Singleton":
                if count > 0:
                    normalizedResult = totalValidNonSingletons[1]/count
                    percentageResult = normalizedResult * 100.00
                    result = "%d%%" % percentageResult
                result = "%d%%" % percentageResult
            elif overviewLineKey == "Memes - Singleton":
                if count > 0:
                    normalizedResult = totalValidSingletons[1]/count
                    percentageResult = normalizedResult * 100.00
                    result = "%d%%" % percentageResult
                result = "%d%%" % percentageResult
            
            #Data Row
            dataElements = [overviewLineKey, count, result]    
            row = doc.createElement("tr")
            for dataEntry in dataElements:
                cell = doc.createElement("td")
                cellText = doc.createTextNode("%s" %dataEntry)
                cell.appendChild(cellText)
                if percentageResult < 100:
                    cell.setAttribute("class", "badOVCell")
                else:
                    cell.setAttribute("class", "goodOVCell")                   
                row.appendChild(cell)
            overviewTable.appendChild(row)

    body.appendChild(h1)
    headerTableOVContainer.appendChild(overviewTable)


    #Module Overview
    numberOfColumns = 1
    numberOfModules = len(validationReportMeme[1])
    if numberOfModules > 6:
        numberOfColumns = 2
    elif numberOfModules > 12:
        numberOfColumns = 3
    rowsPerColumn = numberOfModules//numberOfColumns + 1
    moduleReports = validationReportMeme[1]

    listPosition = 0
    icTable = doc.createElement("table")
    
    icTableHead= doc.createElement("thead")
    icTableHeadText = doc.createTextNode("Meme Validation Results - Module Breakdown" )
    icTableHead.appendChild(icTableHeadText)
    icTableHead.setAttribute("class", "tableheader")
    icTable.appendChild(icTableHead)
    
    icTableFoot= doc.createElement("tfoot")
    icTableFootText = doc.createTextNode("Modules with problem memes are detailed in tables below" )
    icTableFoot.appendChild(icTableFootText)
    icTable.appendChild(icTableFoot)
        
    icTableRow = doc.createElement("tr")
    for unusedI in range(0, numberOfColumns):
        bigCell = doc.createElement("td")
        nestedTable = doc.createElement("table")
        
        #Header
        headers = ["Module", "Total Memes", "Valid"]
        nestedTableHeaderRow = doc.createElement("tr")
        for headerElement in headers:
            nestedCell = doc.createElement("th")
            nestedCellText = doc.createTextNode("%s" %headerElement)
            nestedCell.appendChild(nestedCellText)
            nestedTableHeaderRow.appendChild(nestedCell)
            nestedTable.appendChild(nestedTableHeaderRow)  
                  
        for unusedJ in range(0, rowsPerColumn):
            currPos = listPosition
            listPosition = listPosition + 1
            if listPosition <= numberOfModules:
                try:
                    moduleReport = moduleReports[currPos]
                    result = ""
                    percentageResult = 0
                    if moduleReport[2] > 0:
                        normalizedResult = moduleReport[2]/moduleReport[1]
                        percentageResult = normalizedResult * 100.00
                        result = "%d%%" % percentageResult
                    result = "%d%%" % percentageResult
                    
                    #Write Data Row To Table
                    row = doc.createElement("tr")
                    
                    #Module Name is first cell
                    cell = doc.createElement("td")
                    cellText = doc.createTextNode("%s" %moduleReport[0])
                    if (percentageResult < 100) and (moduleReport[1] != 0):
                        #<a href="#label">Any content</a> 
                        hyperlinkNode = doc.createElement("a")
                        hyperlinkNode.setAttribute("href", "#%s" %moduleReport[0]) 
                        hyperlinkNode.appendChild(cellText)
                        cell.appendChild(hyperlinkNode)
                        cell.setAttribute("class", "badOVCell")
                    else:
                        cell.appendChild(cellText)
                        cell.setAttribute("class", "goodOVCell")                   
                    row.appendChild(cell) 

                    #Now add the other two elements of the row
                    dataElements = [moduleReport[1], result]                       
                    for dataEntry in dataElements:
                        cell = doc.createElement("td")
                        cellText = doc.createTextNode("%s" %dataEntry)
                        cell.appendChild(cellText)
                        if (percentageResult < 100) and (moduleReport[1] != 0):
                            cell.setAttribute("class", "badOVCell")
                        else:
                            cell.setAttribute("class", "goodOVCell")                   
                        row.appendChild(cell)
                    nestedTable.appendChild(row)
                except:
                    nestedTableRow = doc.createElement("tr")            
                    nestedCell = doc.createElement("td")
                    nestedCellText = doc.createTextNode("")
                    nestedCell.appendChild(nestedCellText)
                    nestedTableRow.appendChild(nestedCell)
                    nestedTable.appendChild(nestedTableRow)
        nestedTable.setAttribute("class", "subdivision")
        bigCell.appendChild(nestedTable) 
        bigCell.setAttribute("class", "vAlignment")
        icTableRow.appendChild(bigCell) 

    addADiv = doc.createElement("div") #Allows us to top align icTableRow  
    addADiv.setAttribute("class", "vAlignment")
    addADiv.appendChild(icTableRow)
    icTable.appendChild(addADiv)
    outerDiv = doc.createElement("div") #Wraps around icTable and its header/footer and gives a mount point for padding
    outerDiv.setAttribute("class", "hBlankSpace")
    outerDiv.appendChild(icTable)
    headerTableMOVContainer.appendChild(outerDiv)  

    #Pack the two header tables into the main
    headerTableRow.appendChild(headerTableOVContainer)
    headerTableRow.appendChild(headerTableMOVContainer)
    headerTableRow.setAttribute("class", "vAlignment")
    headerTable.appendChild(headerTableRow)  
    body.appendChild(headerTable)
    
        
        
    #Individual Modules    
    for moduleReport in validationReportMeme[1]:
        if len(moduleReport[3]) > 0:
            #[moduleID, moduleCount, moduleValid, moduleResults]
            
            #Meme Validation Report Table
            memeTable = doc.createElement("table")
            memeTable.setAttribute("class", "subdivision")
            
            byMemeTableHeader = doc.createElement("thead")
            byMemeTableHeaderText = doc.createTextNode("%s" %moduleReport[0])
            byMemeTableHeader.appendChild(byMemeTableHeaderText)
            byMemeTableHeader.setAttribute("class", "tableheader")
            byMemeTableAnchor = doc.createElement("a")
            byMemeTableAnchor.setAttribute("id", moduleReport[0])
            byMemeTableAnchor.appendChild(byMemeTableHeader) 
            memeTable.appendChild(byMemeTableAnchor)
            
            headers = ["Meme", "Meta Meme", "Validation Results"]
            #Header Row
            memeTableHeaderRow = doc.createElement("tr")
            for headerEntry in headers:
                cell = doc.createElement("th")
                cellText = doc.createTextNode("%s" %headerEntry)
                cell.appendChild(cellText)
                cell.setAttribute("style", "padding-bottom:5px; padding-top:5px")
                memeTableHeaderRow.appendChild(cell)
                
            memeTableHeaderRow.setAttribute("class", "subdivision")
            memeTable.appendChild(memeTableHeaderRow)
            
            for detailedResults in moduleReport[3]:
                #detailedResults["meme"] = template.path.fillTemplatePath
                #detailedResults["metaMeme"] = metaMeme
                #detailedResults["results"] = validationResults[1]
              
                rowData = [detailedResults["meme"], detailedResults["metaMeme"]]
                row = doc.createElement("tr")
                for rowElement in rowData:
                    cell = doc.createElement("td")
                    cellText = doc.createTextNode("%s" %rowElement)
                    cell.appendChild(cellText)
                    cell.setAttribute("class", "detailsCell")
                    row.appendChild(cell)
                    
                #The result column needs to be handled differently
                rowValidityCell = doc.createElement("td")
                #Only publishe the broken ones
                for bulletpoint in detailedResults["results"]:
                    if type(bulletpoint) == type([]):
                        for bulletpointElement in bulletpoint:
                            try:
                                if bulletpointElement.find("Meme flagged as inactive!") >= 0:
                                    #then mark the whole row as red
                                    row.setAttribute("class", "badDRow")
                                else:
                                    row.setAttribute("class", "goodDRow")
                            except:
                                print("bulletpointElement.find")
                            paragraph = doc.createElement("p")
                            pText = doc.createTextNode("%s" %bulletpointElement)
                            paragraph.appendChild(pText)
                            rowValidityCell.appendChild(paragraph)
                    else:
                        try:
                            if bulletpoint.find("Meme flagged as inactive!") >= 0:
                                #then mark the whole row as red
                                row.setAttribute("class", "badDRow")
                            else:
                                row.setAttribute("class", "goodDRow")
                        except:
                            print("bulletpoint.find")
                        paragraph = doc.createElement("p")
                        pText = doc.createTextNode("%s" %bulletpoint)
                        paragraph.appendChild(pText)
                        rowValidityCell.appendChild(paragraph)
                rowValidityCell.setAttribute("class", "detailsCell")
    
                    
                #row.appendChild(rowMemeCell)
                #row.appendChild(rowMMCell)
                row.appendChild(rowValidityCell)
                #row.setAttribute("style", "border-style:solid;padding-right:50px;padding-left:10px;")
            
                memeTable.appendChild(row)
            memeTableWrapper = doc.createElement("div")
            memeTableWrapper.setAttribute("class", "vBlankSpace")
            memeTableWrapper.appendChild(memeTable)
            body.appendChild(memeTableWrapper)

    #now put it all together and build the body
    

    #Let's list the memes and metamemes at the bottom
    repoLists = {}
    
    mNumberOfColumns = 1
    numberOfMemes = len(counts["Memes"])
    if numberOfMemes > 12:
        mNumberOfColumns = 3
    mRrowsPerColumn = numberOfMemes//mNumberOfColumns + 1
    repoLists["Memes"] = [mNumberOfColumns, mRrowsPerColumn, counts["Memes"]]
    
    #Let's list the memes and metamemes at the bottom
    mmNumberOfColumns = 1
    numberOfMetaMemes = len(counts["MetaMemes"])
    if numberOfMetaMemes > 12:
        mmNumberOfColumns = 3
    mmRrowsPerColumn = numberOfMetaMemes//mmNumberOfColumns + 1
    repoLists["MetaMemes"] = [mmNumberOfColumns, mmRrowsPerColumn, counts["MetaMemes"]]

    for repoListKey in repoLists.keys():
        repoListRow = repoLists[repoListKey]

        repoTable = doc.createElement("table")
        
        repoTableHead= doc.createElement("thead")
        repoTableHeadText = doc.createTextNode(repoListKey)
        repoTableHead.appendChild(repoTableHeadText)
        repoTableHead.setAttribute("class", "tableheader")
        repoTable.appendChild(repoTableHead)
        listPosition = 0
        for unusedI in range(0, repoListRow[1]):
            ourTemplates = repoListRow[2]
            ourTemplates.sort()
     
            repoTableRow = doc.createElement("tr")
            for unusedJ in range(0, repoListRow[0]): 
                currPos = listPosition
                listPosition = listPosition + 1
                if listPosition <= len(ourTemplates):
                    try:
                        cell = doc.createElement("td")
                        cellText = doc.createTextNode("%s" %ourTemplates[currPos])
                        cell.appendChild(cellText)
                        repoTableRow.appendChild(cell) 
                    except:
                        nestedTableRow = doc.createElement("tr")            
                        nestedCell = doc.createElement("td")
                        nestedCellText = doc.createTextNode("")
                        nestedCell.appendChild(nestedCellText)
                        nestedTableRow.appendChild(nestedCell)
                        nestedTable.appendChild(nestedTableRow)
            repoTable.appendChild(repoTableRow)
        repoTable.appendChild(repoTableRow)
        body.appendChild(repoTable)


    html.appendChild(body)

    if outputFilename is None:
        outputFilename = "GraphyneValidationStatus.html"    
    logRoot =  expanduser("~")
    logDir = os.path.join(logRoot, "Graphyne")
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    resultFileLoc = os.path.join(logDir, outputFilename)    
    
    fileStream = doc.toprettyxml(indent = "    ")
    #unicodeFS = unicode(fileStream, errors='ignore')
    fileObject = open(resultFileLoc, "w", encoding="utf-8")
    #fileObject.write(Fileutils.smart_str(fileStream))
    fileObject.write(fileStream)
    fileObject.close()
    #print(smart_str(fileStream)

def main(css, contentRepositories = [], outputFilename = None, lLevel = logLevel.WARNING, alsoValidateTestRepo = True, flaggedPersistenceType = 'none', persistenceArg = 'none', alsoUseTestDatabase = False):
    #method = moduleName + '.' + 'main'

    print("...Engine Start")
    #rmlEngine.start("test_info", False)
    
    time.sleep(10.0)
    Graph.startLogger(lLevel)
    
    #If we want to validate the test repo (used for regression testing) and not just the core DNA schema, then alsoValidateTestRepo will be True
    if alsoValidateTestRepo is True:
        installFilePath = os.path.dirname(__file__)
        testRepo = os.path.join(installFilePath, "Config", "Test", "TestRepository")
        contentRepositories.append(testRepo)
    
    Graph.startDB(contentRepositories, flaggedPersistenceType, persistenceArg, True, True, True)
        
    print("...Engine Started")
    
    #Flag the file busy while we work
    Fileutils.busyHTMLFile("ValidationStatus.xhtml",\
                           "Repository Validation",\
                           "The Repository is currently being validated",\
                           "Validate.py")

    #validation reports
    startTime = time.time()
    valReportMeme = validateMemes()#[totalValid, totalResults]
    endTime = time.time()
    validationTime = endTime - startTime

    #count templates        
    counts = countTemplates()
    entityCounts =  countEntities()
    counts.update(entityCounts)
    
    publishResults(validationTime, counts, valReportMeme, css, outputFilename)    
    print("...Engine Stop") 
    Graph.stopLogger()
    print("...Engine Stopped")  
    #Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    

    
if __name__ == "__main__":
    ''' 
    Four (optional) initial params:
        sys.argv[1] - Is the connection string.
            "none" - no persistence
            "memory" - Use SQLite in in-memory mode (connection = ":memory:")
            "<valid filename>" - Use SQLite, with that file as the database
            "<filename with .sqlite as extension, but no file>" - Use SQLite and create that file to use as the DB file
            "<anything else>" - Presume that it is a pyodbc connection string
            Default to None, which is no persistence

        sys.argv[2]  -  persistenceType = The type of database used by the persistence engine.  This is used to determine which flavor of SQL syntax to use.
            Enumeration of Possible values:
            Default to None, which is no persistence
            "sqlite" - Sqlite3
            "mssql" - Miscrosoft SQL Server
            "hana" - SAP Hana
            
        sys.argv[3]  - Also validate the standard regression test repository
                        
        sys.argv[4] - Is the log level.
            "info", "debug" and "warning" are valid options.    
            Default to "warning"
        
    E.g. Validate.py 'memory' 'sqlite'               #For sqlite3 database, with :memory: connection, regression validate test repo
    E.g. Vaidate.py                                  #For no persistence, validate regression test repo
    E.g. Validate.py 'memory' 'sqlite' 'false'       #For sqlite3 database, with :memory: connection, regression validate test repo
    E.g. Vaidate.py 'none' 'none' 'false'            #For no persistence, regression don't validate test repo
    
    '''
        
    print("\nTesting Validity of Graphyne Default Schema Repository")
    
    lLevel = Graph.logLevel.WARNING
    try:
        if sys.argv[4] == "info":
            lLevel = Graph.logLevel.INFO
        elif sys.argv[4] == "debug":
            lLevel = Graph.logLevel.DEBUG
    except:
        pass
    
    alsoValidateRepo = True
    try:
        if sys.argv[3] == "false":
            alsoValidateRepo = False
        elif sys.argv[3] == "False":
            alsoValidateRepo = False
    except:
        pass   

    if alsoValidateRepo == True:
        print("\n  -- also validating the standard regression test repository")

    persistenceType = None
    dbConnectionString = None
    try:
        if sys.argv[1] is not None:
            #dbConnectionString = sys.argv[1]
            dbConnectionString = sys.argv[1]
    except:
        pass
    try:
        if sys.argv[2] is not None:
            #dbConnectionString = sys.argv[1]
            persistenceType = sys.argv[2]
    except:
        pass
  
    css = Fileutils.defaultCSS()

    try:
        if sys.argv[3] == "sqlite":
            from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModule2
            main(css, [], None, lLevel, alsoValidateRepo, persistenceModule2)
            time.sleep(10.0)
            print((sys.argv))
            print("-- using sqlite persistence")
        else:
            main(css, [], None, lLevel, alsoValidateRepo)
            time.sleep(10.0)
            print((sys.argv))
            print("-- using no persistence")
    except Exception as e:
            main(css, [], None, lLevel, alsoValidateRepo)
            time.sleep(10.0)
            #print(e)
            #print (sys.argv)
            print("-- using no persistence (default)")
