#!/usr/bin/env python3

"""
   Smoketest.py: Regression testing utility for Graphyne.  Multiprocessing wrapper for Smokest, allowing multiple simultaneous tests against different persistence types.
"""
from tkinter.test.runtktests import this_dir_path

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'



from xml.dom import minidom
from time import ctime
from os.path import expanduser
import copy
import os
import codecs
import time
import decimal
import queue
import sys
import argparse
#from os.path import expanduser

import Graphyne.Graph as Graph
import Graphyne.Fileutils as Fileutils
import Graphyne.Exceptions as Exceptions

responseQueue = queue.Queue()
entityList = []
api = None


global testImplicit
testImplicit = True


#Globals
#graphDir = expanduser("~")
#graphDir = os.getcwd()
graphDir = os.path.dirname(os.path.abspath(__file__))
testDirPath = os.path.join("Config", "Test")
configDirPath = os.path.join("utils", "Config")
        
resultFile = None
moduleName = 'Smoketest'     
logType = Graph.logTypes.CONTENT
logLevel = Graph.logLevel




class DBError(ValueError):
    pass


def testMetaMemeProperty():
    method = moduleName + '.' + 'testMetaMemeProperty'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, "MetaMeme_Properties.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        n = n+1
        stringArray = str.split(eachReadLine)
        testArgumentMap = {stringArray[1] : stringArray[2]}
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, metameme %s" %(n, stringArray[0])])

        #colums after 2 can me repeated in pairs.  4/3 and 6/5 can also contain argument/vlaue pairs
        try: testArgumentMap[str(stringArray[3])] = str(stringArray[4])
        except: pass
        try: testArgumentMap[str(stringArray[5])] = str(stringArray[6])
        except: pass   
        try: testArgumentMap[str(stringArray[7])] = str(stringArray[8])
        except: pass
        try: testArgumentMap[str(stringArray[9])] = str(stringArray[10])
        except: pass   
        try: testArgumentMap[str(stringArray[11])] = str(stringArray[12])
        except: pass 
        
        removeMe = 'XXX'
        try:
            del testArgumentMap[removeMe]
        except: pass   

        allTrue = True
        errata = []
    
        try:
            mmToTest = Graph.templateRepository.templates[stringArray[0]]
            props = mmToTest.properties
            Graph.logQ.put( [logType , logLevel.DEBUG , method , "testing metameme %s, props = %s" %(mmToTest.path.fullTemplatePath, props)])
            for testKey in testArgumentMap.keys():
                testType = testArgumentMap[testKey]
                Graph.logQ.put( [logType , logLevel.DEBUG , method , "testKey = %s, testType = %s" %(testKey, testType)])
                #ToDo: Fix Me.  We should not be using temp properties anymore
                try:
                    prop = mmToTest.getProperty(testKey)
                    Graph.logQ.put( [logType , logLevel.DEBUG , method , "prop = %s" %(prop)])
                    splitName = testKey.rpartition('.')
                    if (prop is not None) and (prop.name.find(splitName[2]) < 0):
                        Graph.logQ.put( [logType , logLevel.DEBUG , method , "property %s and test property %s don't match" %(prop.name, testKey)])
                        allTrue = False
                    else:
                        Graph.logQ.put( [logType , logLevel.DEBUG , method , "property %s and test property %s match" %(prop.name, testKey)])
        
                    if prop is not None:
                        if prop.propertyType != testType:
                            Graph.logQ.put( [logType , logLevel.WARNING , method , "property %s type %s and testType %s do not match" %(prop.name, prop.propertyType, testType)])
                            allTrue = False
                        else:
                            Graph.logQ.put( [logType , logLevel.DEBUG , method , "property %s type %s and testType %s match" %(prop.name, prop.propertyType, testType)])
                    else:
                        Graph.logQ.put( [logType , logLevel.WARNING , method , "property %s is invalid" %(testKey)])
                except Exception as e:
                    Graph.logQ.put( [logType , logLevel.ERROR , method , "Error pulling testkey %s from %s's properties.  Traceback = %s" %(testKey, mmToTest.path.fullTemplatePath, e)])
                    allTrue = False
            if allTrue == False:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , "testkey %s has no match" %(testKey)])
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(allTrue)
        expectedResult = stringArray[13]
        results = [n, testcase, allTrueResult, expectedResult, copy.deepcopy(errata)]
        resultSet.append(results)
        
        del errata
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    
    
    

def testMetaMemeSingleton():
    method = moduleName + '.' + 'testMetaMemeSingleton'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []

        
    #try:
    testFileName = os.path.join(testDirPath, "MetaMeme_Singleton.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, metameme %s" %(n, stringArray[0])])

        expectedTestResult = False
        if stringArray[1] == 'TRUE': 
            expectedTestResult = True
        Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Metameme %s is expected to be a singleton == %s' %(stringArray[0], expectedTestResult)])
        testResult = False
        
        try:
            mmToTest = Graph.templateRepository.resolveTemplateAbsolutely(stringArray[0])
            if mmToTest.isSingleton == True:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Metameme %s is a singleton' %(stringArray[0])])
                testResult = True
            else:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Metameme %s is not a singleton' %(stringArray[0])])
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[1]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    
    
    
def testMetaMemeSwitch():
    method = moduleName + '.' + 'testMetaMemeSwitch'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []

        
    #try:
    testFileName = os.path.join(testDirPath, "MetaMeme_Switch.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, metameme %s" %(n, stringArray[0])])

        expectedTestResult = False
        if stringArray[1] == 'TRUE': 
            expectedTestResult = True
        Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Metameme %s is expected to be a singleton == %s' %(stringArray[0], expectedTestResult)])
        testResult = False
        
        try:
            mmToTest = Graph.templateRepository.resolveTemplateAbsolutely(stringArray[0])
            if mmToTest.isSwitch == True:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Metameme %s is a switch' %(stringArray[0])])
                testResult = True
            else:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Metameme %s is not a switch' %(stringArray[0])])
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[1]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testMetaMemeEnhancements():
    method = moduleName + '.' + 'testMetaMemeEnhancements'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []

        
    #try:
    testFileName = os.path.join(testDirPath, "MetaMeme_Enhances.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        testArgumentList = []
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, metameme %s" %(n, stringArray[0])])

        #columns 1&2 may contain data
        if stringArray[1] != 'XXX':
            testArgumentList.append(stringArray[1])
        if stringArray[2] != 'XXX':
            testArgumentList.append(stringArray[2])

        allTrue = False
        try:
            mmToTest = Graph.templateRepository.resolveTemplateAbsolutely(stringArray[0])
            Graph.logQ.put( [logType , logLevel.DEBUG , method , "testing metameme %s, enhancements = %s" %(mmToTest.path.fullTemplatePath, mmToTest.enhances)])
            for testArgument in testArgumentList:
                #Hack alert!  If we have no enhancements in the testcase, the result should be false.  
                #    Hence we initialize to false, but if we actually have test cases, we re-initialize to True
                allTrue = True
            for testArgument in testArgumentList:
                amIextended = Graph.templateRepository.resolveTemplate(mmToTest.path, testArgument)
                Graph.logQ.put( [logType , logLevel.DEBUG , method , "checking to see if %s, enhances %s" %(mmToTest.path.fullTemplatePath, amIextended.path.fullTemplatePath)])
                
                #iterate over the enhancement list and see if we have a match
                testResult = False 
                for enhancement in mmToTest.enhances:
                    Graph.logQ.put( [logType , logLevel.DEBUG , method , "testing enhancement %s against %s" %(enhancement, amIextended.path.fullTemplatePath)])
                    try:
                        enhancedMetaMeme = Graph.templateRepository.resolveTemplate(mmToTest.path, enhancement)
                        if enhancedMetaMeme.path.fullTemplatePath == amIextended.path.fullTemplatePath:
                            testResult = True
                            Graph.logQ.put( [logType , logLevel.DEBUG , method , "enhancement %s == %s" %(enhancement, amIextended.path.fullTemplatePath)])
                        else:
                            Graph.logQ.put( [logType , logLevel.DEBUG , method , "enhancement %s != %s" %(enhancement, amIextended.path.fullTemplatePath)])
                    except:
                        Graph.logQ.put( [logType , logLevel.DEBUG , method , "tested metameme %s extends metameme %s, but is not in the repository." %(enhancement, mmToTest.path.fullTemplatePath)])
                if testResult == False:
                    allTrue = False
                if allTrue == False:
                    Graph.logQ.put( [logType , logLevel.DEBUG , method , "tested metameme %s does not have sought tested enhancement %s" %(mmToTest.path.fullTemplatePath, amIextended.path.fullTemplatePath)])
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(allTrue)
        expectedResult = stringArray[3]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet    
    
    
    
def testMemeValidity():
    method = moduleName + '.' + 'testMemeValidity'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, "Meme_Validity.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    memeValid = False
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, metameme %s" %(n, stringArray[0])])

        expectedTestResult = False
        if stringArray[1] == 'TRUE': 
            expectedTestResult = True
        try:
            memeToTest = Graph.templateRepository.resolveTemplateAbsolutely(stringArray[0])
            memeValidReport = memeToTest.validate([])
            memeValid = memeValidReport[0]
            if expectedTestResult != memeValid:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , "testkey %s has an unexpected validity status" %(memeToTest.path.fullTemplatePath)])
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(memeValid)
        expectedResult = stringArray[1]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    
    
    
def testMemeSingleton():
    method = moduleName + '.' + 'testMemeSingleton'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, "Meme_Singleton.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, metameme %s" %(n, stringArray[0])])

        expectedTestResult = False
        if stringArray[1] == 'TRUE': 
            expectedTestResult = True
        testResult = False
        try:
            mmToTest = Graph.templateRepository.templates[stringArray[0]]
            if expectedTestResult == mmToTest.isSingleton:
                if mmToTest.entityUUID is not None:
                    testResult = True
                else:
                    Graph.logQ.put( [logType , logLevel.DEBUG , method , "meme %s has no deployed entity" %(stringArray[0])])
            else:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , "meme %s has an unexpected singleton status" %(stringArray[0])])
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[1]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
        


def testEntityPhase1(phaseName = 'testEntityPhase1', fName = "Entity_Phase1.atest"):
    ''' Create the entity from the meme and add it to the entity repo.  
        Retrieve the entity.  
        Check to see if it has the properties it is supposed to, 
            if the type is correct and if the value is correct. 
    
    Entity Phase 5 also uses this function        
    '''
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            entityID = Graph.api.createEntityFromMeme(stringArray[0])
            Graph.logQ.put( [logType , logLevel.DEBUG , method , "Entity UUID = %s" %(entityID)])
            propTypeCorrect = False
            propValueCorrect = False
            
            Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])
            hasProp = Graph.api.getEntityHasProperty(entityID, stringArray[1])
            if hasProp == False:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , "entity from meme %s does not have property %s" %(entityID, stringArray[1])])
            else:
                propType = Graph.api.getEntityPropertyType(entityID, stringArray[1])
                if stringArray[2] == propType:
                    propTypeCorrect = True
                else:
                    Graph.logQ.put( [logType , logLevel.DEBUG , method , "property %s in entity from meme %s is wrong type.  Expected %s.  Got %s" %(stringArray[1], entityID, stringArray[2], propType)])
                
                propValue = Graph.api.getEntityPropertyValue(entityID, stringArray[1])
                if propType == 'Boolean':
                    expValue = False
                    if stringArray[3].lower() == "true":
                        expValue = True
                    if propValue == expValue:
                        propValueCorrect = True
                elif propType == 'Decimal':
                    expValue = decimal.Decimal(stringArray[3])
                    if propValue == expValue:
                        propValueCorrect = True
                elif propType == 'Integer':
                    expValue = int(stringArray[3])
                    if propValue == expValue:
                        propValueCorrect = True
                else:
                    if propValue == stringArray[3]:
                        propValueCorrect = True
    
                if propValueCorrect == False:
                    Graph.logQ.put( [logType , logLevel.DEBUG , method , "property %s in entity from meme %s is wrong value.  Expected %s.  Got %s" %(stringArray[1], stringArray[0], stringArray[3], propValue)])
    
            if (propValueCorrect == True) and (propTypeCorrect == True) and (hasProp == True):
                testResult = True
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[4]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    
    
    
def testEntityPhase1_1(phaseName = 'testEntityPhase1_1', fName = "Entity_Phase1.atest"):
    ''' a repeat of testEntityPhase1, but using the Python script interface instead of going directly against Graph.api 
        Tests the following script commands:
            createEntityFromMeme
            getEntityHasProperty
            getEntityPropertyType
            getEntityPropertyValue
    '''
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            #entityID = Graph.api.createEntityFromMeme(stringArray[0])
            entityID = api.createEntityFromMeme(stringArray[0])
            Graph.logQ.put( [logType , logLevel.DEBUG , method , "Entity UUID = %s" %(entityID)])
            propTypeCorrect = False
            propValueCorrect = False
            
            Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])
            #hasProp = Graph.api.getEntityHasProperty(entityID, stringArray[1])
            hasProp = api.getEntityHasProperty(entityID, stringArray[1])
            if hasProp == False:
                Graph.logQ.put( [logType , logLevel.DEBUG , method , "entity from meme %s does not have property %s" %(entityID, stringArray[1])])
            else:
                #propType = Graph.api.getEntityPropertyType(entityID, stringArray[1])
                propType = api.getEntityPropertyType(entityID, stringArray[1])
                if stringArray[2] == propType:
                    propTypeCorrect = True
                else:
                    Graph.logQ.put( [logType , logLevel.DEBUG , method , "property %s in entity from meme %s is wrong type.  Expected %s.  Got %s" %(stringArray[1], entityID, stringArray[2], propType)])
                
                #propValue = Graph.api.getEntityPropertyValue(entityID, stringArray[1])
                propValue = api.getEntityPropertyValue(entityID, stringArray[1])
                if propType == 'Boolean':
                    expValue = False
                    if stringArray[3].lower() == "true":
                        expValue = True
                    if propValue == expValue:
                        propValueCorrect = True
                elif propType == 'Decimal':
                    expValue = decimal.Decimal(stringArray[3])
                    if propValue == expValue:
                        propValueCorrect = True
                elif propType == 'Integer':
                    expValue = int(stringArray[3])
                    if propValue == expValue:
                        propValueCorrect = True
                else:
                    if propValue == stringArray[3]:
                        propValueCorrect = True
    
                if propValueCorrect == False:
                    Graph.logQ.put( [logType , logLevel.DEBUG , method , "property %s in entity from meme %s is wrong value.  Expected %s.  Got %s" %(stringArray[1], stringArray[0], stringArray[3], propValue)])
    
            if (propValueCorrect == True) and (propTypeCorrect == True) and (hasProp == True):
                testResult = True
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[4]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet

    
    
    
def testEntityPhase2(testPhase = 'testEntityPhase2', fileName = 'Entity_Phase2.atest'):
    ''' Change the values of the various properties.  
        Can we change the value to the desired value and are constraints working? '''
    method = moduleName + '.' + testPhase
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, fileName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            entityID = Graph.api.createEntityFromMeme(stringArray[0])
            Graph.api.setEntityPropertyValue(entityID, stringArray[1], stringArray[2])
            getter = Graph.api.getEntityPropertyValue(entityID, stringArray[1])
            propType = Graph.api.getEntityPropertyType(entityID, stringArray[1])
            
            #reformat the expected result from unicode string to that which is expected in the property
            expectedResult = None
            if propType == "String":
                expectedResult = stringArray[2]
            elif propType == "Integer":    
                expectedResult = int(stringArray[2])
            elif propType == "Decimal":    
                expectedResult = decimal.Decimal(stringArray[2])
            else:    
                expectedResult = False
                if str.lower(stringArray[2]) == 'true':
                    expectedResult = True
        
            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if getter == expectedResult:
                testResult = True

        except Exceptions.ScriptError as e:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[3]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    
    
    
def testEntityPhase2_1( testPhase = 'testEntityPhase2_1', fileName = 'Entity_Phase2.atest'):
    ''' a repeat of testEntityPhase2, but using the Python script interface instead of going directly against Graph.api 
        Tests the following script commands:
            setEntityPropertyValue
            getEntityPropertyValue
            getEntityPropertyType 
    '''
    method = moduleName + '.' + testPhase
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, fileName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            entityID = api.createEntityFromMeme(stringArray[0])
            api.setEntityPropertyValue(entityID, stringArray[1], stringArray[2])
            getter = api.getEntityPropertyValue(entityID, stringArray[1])
            propType = api.getEntityPropertyType(entityID, stringArray[1])
            
            #reformat the expected result from unicode string to that which is expected in the property
            expectedResult = None
            if propType == "String":
                expectedResult = stringArray[2]
            elif propType == "Integer":    
                expectedResult = int(stringArray[2])
            elif propType == "Decimal":    
                expectedResult = decimal.Decimal(stringArray[2])
            else:    
                expectedResult = False
                if str.lower(stringArray[2]) == 'true':
                    expectedResult = True

            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if getter == expectedResult:
                testResult = True

        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[3]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    
    


def testEntityPhase3():
    ''' Add and remove properties.  
        Remove custom properties.  
        
        Tests the following script commands:
            addEntityDecimalProperty
            addEntityIntegerProperty
            addEntityStringProperty
            addEntityBooleanProperty
            removeAllCustomPropertiesFromEntity
            removeEntityProperty
        
        Step 1.  add a prop and test its existence and value
        Step 2.  remove that custom prop and check to make sure it is gone (getHasProperty == False)
        Step 3.  add the prop again, test its existence and then use removeAllCustomPropertiesFromEntity to remove it'''
    method = moduleName + '.' + 'testEntityPhase3'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, "Entity_Phase3.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        
        step1Result = False
        step2Result = False
        step3Result = False
        try:

            entityID = Graph.api.createEntityFromMeme(stringArray[0])
            
            #step 1
            if stringArray[2] == "String":
                Graph.api.addEntityStringProperty(entityID, stringArray[1], stringArray[3])
                expectedResult = stringArray[3]
            elif stringArray[2] == "Integer":
                Graph.api.addEntityIntegerProperty(entityID, stringArray[1], stringArray[3])
                expectedResult = int(stringArray[3])
            elif stringArray[2] == "Decimal":
                Graph.api.addEntityDecimalProperty(entityID, stringArray[1], stringArray[3])
                expectedResult = decimal.Decimal(stringArray[3])
            else:
                Graph.api.addEntityBooleanProperty(entityID, stringArray[1], stringArray[3])
                expectedResult = False
                if str.lower(stringArray[3]) == 'true':
                    expectedResult = True
                    
            getter = Graph.api.getEntityPropertyValue(entityID, stringArray[1])
            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if getter == expectedResult:
                step1Result = True
                
            #step 2
            Graph.api.removeEntityProperty(entityID, stringArray[1])
            getter = Graph.api.getEntityHasProperty(entityID, stringArray[1])
            if getter == False:
                step2Result = True
                
            #step 3
            if stringArray[2] == "String":
                Graph.api.addEntityStringProperty(entityID, stringArray[1], stringArray[3])
            elif stringArray[2] == "Integer":
                Graph.api.addEntityIntegerProperty(entityID, stringArray[1], stringArray[3])
            elif stringArray[2] == "Decimal":
                Graph.api.addEntityDecimalProperty(entityID, stringArray[1], stringArray[3])
            else:
                Graph.api.addEntityBooleanProperty(entityID, stringArray[1], stringArray[3])
            Graph.api.removeAllCustomPropertiesFromEntity(entityID)
            getter = Graph.api.getEntityHasProperty(entityID, stringArray[1])
            if getter == False:
                step3Result = True

        except Exceptions.ScriptError as e:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)
            
        if (step1Result == True) and (step2Result == True) and (step3Result == True):
            testResult = True

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    
    
    
def testEntityPhase3_1():
    ''' a repeat of testEntityPhase3, but using the Python script interface instead of going directly against Graph.api  
        
        Tests the following script commands:
            addEntityDecimalProperty
            addEntityIntegerProperty
            addEntityStringProperty
            addEntityBooleanProperty
            removeAllCustomPropertiesFromEntity
            removeEntityProperty
    '''
    method = moduleName + '.' + 'testEntityPhase3_1'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, "Entity_Phase3.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        
        step1Result = False
        step2Result = False
        step3Result = False
        try:

            entityID = api.createEntityFromMeme(stringArray[0])
            
            #step 1
            if stringArray[2] == "String":
                #Graph.api.addEntityStringProperty(entityID, stringArray[1], stringArray[3])
                api.addEntityStringProperty(entityID, stringArray[1], stringArray[3])
                expectedResult = stringArray[3]
            elif stringArray[2] == "Integer":
                #Graph.api.addEntityIntegerProperty(entityID, stringArray[1], stringArray[3])
                api.addEntityIntegerProperty(entityID, stringArray[1], stringArray[3])
                expectedResult = int(stringArray[3])
            elif stringArray[2] == "Decimal":
                #Graph.api.addEntityDecimalProperty(entityID, stringArray[1], stringArray[3])
                api.addEntityDecimalProperty(entityID, stringArray[1], stringArray[3])
                expectedResult = decimal.Decimal(stringArray[3])
            else:
                Graph.api.addEntityBooleanProperty(entityID, stringArray[1], stringArray[3])
                expectedResult = False
                if str.lower(stringArray[3]) == 'true':
                    expectedResult = True
                    
            #getter = Graph.api.getEntityPropertyValue(entityID, stringArray[1])
            getter = api.getEntityPropertyValue(entityID, stringArray[1])
            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if getter == expectedResult:
                step1Result = True
                
            #step 2
            #Graph.api.removeEntityProperty(entityID, stringArray[1])
            #getter = Graph.api.getEntityHasProperty(entityID, stringArray[1])
            api.removeEntityProperty(entityID, stringArray[1])
            getter = api.getEntityHasProperty(entityID, stringArray[1])
            if getter == False:
                step2Result = True
                
            #step 3
            if stringArray[2] == "String":
                #Graph.api.addEntityStringProperty(entityID, stringArray[1], stringArray[3])
                api.addEntityStringProperty(entityID, stringArray[1], stringArray[3])
            elif stringArray[2] == "Integer":
                #Graph.api.addEntityIntegerProperty(entityID, stringArray[1], stringArray[3])
                api.addEntityIntegerProperty(entityID, stringArray[1], stringArray[3])
            elif stringArray[2] == "Decimal":
                #Graph.api.addEntityDecimalProperty(entityID, stringArray[1], stringArray[3])
                api.addEntityIntegerProperty(entityID, stringArray[1], stringArray[3])
            else:
                #Graph.api.addEntityBooleanProperty(entityID, stringArray[1], stringArray[3])
                api.addEntityBooleanProperty(entityID, stringArray[1], stringArray[3])
            #Graph.api.removeAllCustomPropertiesFromEntity(entityID)
            #getter = Graph.api.getEntityHasProperty(entityID, stringArray[1])
            api.removeAllCustomPropertiesFromEntity(entityID)
            getter = api.getEntityHasProperty(entityID, stringArray[1])
            if getter == False:
                step3Result = True

        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)
            
        if (step1Result == True) and (step2Result == True) and (step3Result == True):
            testResult = True

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])  
    return resultSet  
    
    
    
    
def testEntityPhase4():
    ''' Revert the entity to original condition. 
        
        Tests the following script commands:
            revertEntityPropertyValues
        
        Step 1.  change a standard value
        Step 2.  use revertEntityPropertyValues to return it to stock'''
        
    method = moduleName + '.' + 'testEntityPhase4'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, "Entity_Phase4.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            entityID = Graph.api.createEntityFromMeme(stringArray[0])
            baseValue = Graph.api.getEntityPropertyValue(entityID, stringArray[1])
            
            Graph.api.setEntityPropertyValue(entityID, stringArray[1], stringArray[2])
            getter = Graph.api.getEntityPropertyValue(entityID, stringArray[1])
            propType = Graph.api.getEntityPropertyType(entityID, stringArray[1])
            
            #reformat the expected result from unicode string to that which is expected in the property
            expectedResult = None
            if propType == "String":
                expectedResult = stringArray[2]
            elif propType == "Integer":    
                expectedResult = int(stringArray[2])
            elif propType == "Decimal":    
                expectedResult = decimal.Decimal(stringArray[2])
            else:    
                expectedResult = False
                if str.lower(stringArray[2]) == 'true':
                    expectedResult = True

            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if getter == expectedResult:
                Graph.api.revertEntityPropertyValues(entityID, False)
                getter = Graph.api.getEntityPropertyValue(entityID, stringArray[1])
                if getter == baseValue:
                    testResult = True

        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    
    
    
    
def testEntityPhase4_1():
    ''' a repeat of testEntityPhase3, but using the Python script interface instead of going directly against Graph.api '''
        
    method = moduleName + '.' + 'testEntityPhase4.1'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, "Entity_Phase4.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            entityID = api.createEntityFromMeme(stringArray[0])
            baseValue = api.getEntityPropertyValue(entityID, stringArray[1])
            
            api.setEntityPropertyValue(entityID, stringArray[1], stringArray[2])
            getter = api.getEntityPropertyValue(entityID, stringArray[1])
            propType = api.getEntityPropertyType(entityID, stringArray[1])
            
            #reformat the expected result from unicode string to that which is expected in the property
            expectedResult = None
            if propType == "String":
                expectedResult = stringArray[2]
            elif propType == "Integer":    
                expectedResult = int(stringArray[2])
            elif propType == "Decimal":    
                expectedResult = decimal.Decimal(stringArray[2])
            else:    
                expectedResult = False
                if str.lower(stringArray[2]) == 'true':
                    expectedResult = True

            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if getter == expectedResult:
                api.revertEntityPropertyValues(entityID, False)
                getter = api.getEntityPropertyValue(entityID, stringArray[1])
                if getter == baseValue:
                    testResult = True

        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testRevertEntity():
    ''' a repeat of the testEntityPhase4 tests, but using revertEntity'''
        
    method = moduleName + '.' + 'testRevertEntity'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, "Entity_Phase4.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    #First, re-run the 4 tests with revertEntity()
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = True
        try:
            entityID = api.createEntityFromMeme(stringArray[0])
            baseValue = api.getEntityPropertyValue(entityID, stringArray[1])
            
            api.setEntityPropertyValue(entityID, stringArray[1], stringArray[2])
            getter = api.getEntityPropertyValue(entityID, stringArray[1])
            propType = api.getEntityPropertyType(entityID, stringArray[1])
            
            #reformat the expected result from unicode string to that which is expected in the property
            expectedResult = None
            if propType == "String":
                expectedResult = stringArray[2]
            elif propType == "Integer":    
                expectedResult = int(stringArray[2])
            elif propType == "Decimal":    
                expectedResult = decimal.Decimal(stringArray[2])
            else:    
                expectedResult = False
                if str.lower(stringArray[2]) == 'true':
                    expectedResult = True

            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if getter == expectedResult:
                api.revertEntity(entityID, False)
                getter = api.getEntityPropertyValue(entityID, stringArray[1])
                if getter != baseValue:
                    testResult = False
                    
        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
        
    #Second, test with a custom property with revertEntity()
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = True
        try:
            entityID = api.createEntityFromMeme(stringArray[0])
            
            #Create a property named after the current n count and give it the n value
            currValue = "%s" %n
            Graph.api.addEntityIntegerProperty(entityID, currValue, currValue) 
            getter = Graph.api.getEntityHasProperty(entityID, currValue)  
            if getter != True:
                testResult = False
            Graph.api.revertEntity(entityID, currValue)
            getter = Graph.api.getEntityHasProperty(entityID, currValue) 
            if getter == True:
                testResult = False

        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
        
    #Lastly, rerun test 4 and then add a property and test revertEntity()
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = True
        try:
            entityID = api.createEntityFromMeme(stringArray[0])
            baseValue = api.getEntityPropertyValue(entityID, stringArray[1])
            
            api.setEntityPropertyValue(entityID, stringArray[1], stringArray[2])
            getter = api.getEntityPropertyValue(entityID, stringArray[1])
            propType = api.getEntityPropertyType(entityID, stringArray[1])
            
            #reformat the expected result from unicode string to that which is expected in the property
            expectedResult = None
            if propType == "String":
                expectedResult = stringArray[2]
            elif propType == "Integer":    
                expectedResult = int(stringArray[2])
            elif propType == "Decimal":    
                expectedResult = decimal.Decimal(stringArray[2])
            else:    
                expectedResult = False
                if str.lower(stringArray[2]) == 'true':
                    expectedResult = True

            #Create a property named after the current n count and give it the n value
            currValue = "%s" %n
            Graph.api.addEntityIntegerProperty(entityID, currValue, currValue) 
            getter = Graph.api.getEntityHasProperty(entityID, currValue)  
            if getter != True:
                testResult = False

            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if getter == expectedResult:
                api.revertEntity(entityID, False)
                getter = api.getEntityPropertyValue(entityID, stringArray[1])
                if getter != baseValue:
                    testResult = False
             
            #Make sure the custom property is gone       
            Graph.api.revertEntity(entityID, currValue)
            getter = Graph.api.getEntityHasProperty(entityID, currValue)
            getter = Graph.api.revertEntity(entityID, currValue)  
            if getter == True:
                testResult = False

        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    



def testEntityPhase6():
    ''' Check and see if the meme is a singleton
    
    Tests getMemeIsSingleton
    Tests getEntityFromMeme in singleton context
    
    
    Strategy - 
    If the meme is a singleton, then it should have had an entity created already
    1 - Is the meme a singleton?
        2a - If not, then entity.uuid should be non-existent
        2b - If so, then entity.uuid should have a UUID
            3b - create an entiity
            4b - is the UUID the same as before?  It should be
    '''
    method = moduleName + '.' + 'testEntityPhase6'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, "Entity_Phase6.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        expectedTestResult = False
        if stringArray[1] == 'TRUE': 
            expectedTestResult = True
        testResult = False
        
        
        mSingletonFlagCorrect = False
        mEntityUUIDCorrect = False
        eSingletonFlagCorrect = False
        eSameUUIDasInMeme = False

        try: 
        
            isSingleton = Graph.api.getIsMemeSingleton(stringArray[0])
            if expectedTestResult == isSingleton:
                mSingletonFlagCorrect = True
                
            meme = Graph.templateRepository.resolveTemplateAbsolutely(stringArray[0])  
            oldEntityID = None
            
            #Is the meme a singleton?  
            if isSingleton == False:
                #2a - If not, then entity.uuid should be non-existent
                try:
                    if meme.entityUUID is None:
                        mEntityUUIDCorrect = True
                except:
                    mEntityUUIDCorrect = True
            else:
                #2b - If so, then entity.uuid should have a UUID
                if meme.entityUUID is not None:
                    mEntityUUIDCorrect = True
                    oldEntityID = meme.entityUUID 
    
    
                
            entityID = Graph.api.createEntityFromMeme(stringArray[0])
            entityIsSingleton = Graph.api.getIsEntitySingleton(entityID)
            if isSingleton == False:
                if entityIsSingleton == False:
                    eSingletonFlagCorrect = True
                eSameUUIDasInMeme = True
            else:
                if (entityIsSingleton == True) and (entityID == oldEntityID):
                    eSingletonFlagCorrect = True
                    eSameUUIDasInMeme = True
                
            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if (mSingletonFlagCorrect == True) and (mEntityUUIDCorrect == True) and (eSingletonFlagCorrect == True) and (eSameUUIDasInMeme == True):
                testResult = True

        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet

    
    
    
def testEntityPhase6_1():
    ''' Repeat 6 using python script interface.
    
    Tests the following script functions:
        getIsEntitySingleton
        getIsMemeSingleton
    '''
    method = moduleName + '.' + 'testEntityPhase6.1'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    testFileName = os.path.join(testDirPath, "Entity_Phase6.atest")
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.DEBUG , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        expectedTestResult = False
        if stringArray[1] == 'TRUE': 
            expectedTestResult = True
        testResult = False
        
        
        mSingletonFlagCorrect = False
        mEntityUUIDCorrect = False
        eSingletonFlagCorrect = False
        eSameUUIDasInMeme = False

        try: 
        
            isSingleton = api.getIsMemeSingleton(stringArray[0])
            if expectedTestResult == isSingleton:
                mSingletonFlagCorrect = True
                
            meme = Graph.templateRepository.resolveTemplateAbsolutely(stringArray[0])  
            oldEntityID = None
            
            #Is the meme a singleton?  
            if isSingleton == False:
                #2a - If not, then entity.uuid should be non-existent
                try:
                    if meme.entityUUID is None:
                        mEntityUUIDCorrect = True
                except:
                    mEntityUUIDCorrect = True
            else:
                #2b - If so, then entity.uuid should have a UUID
                if meme.entityUUID is not None:
                    mEntityUUIDCorrect = True
                    oldEntityID = meme.entityUUID 
    
    
                
            entityID = api.createEntityFromMeme(stringArray[0])
            entityIsSingleton = api.getIsEntitySingleton(entityID)
            if isSingleton == False:
                if entityIsSingleton == False:
                    eSingletonFlagCorrect = True
                eSameUUIDasInMeme = True
            else:
                if (entityIsSingleton == True) and (entityID == oldEntityID):
                    eSingletonFlagCorrect = True
                    eSameUUIDasInMeme = True
                
            #now compare getter to the reformatted stringArray[2] and see if we have successfully altered the property
            if (mSingletonFlagCorrect == True) and (mEntityUUIDCorrect == True) and (eSingletonFlagCorrect == True) and (eSameUUIDasInMeme == True):
                testResult = True

        except Exceptions.ScriptError:
            #Some test cases violate restriction constraints and will raise an exception.
            # This works as intended  
            testResult = False
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = "True"
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])    
    return resultSet





def testEntityPhase7(phaseName = 'testEntityPhase7', fName = "Entity_Phase7.atest"):
    ''' Create entities from the meme in the first two colums.
        Add a link between the two at the location on entity in from column 3.
        Check and see if each is a counterpart as seen from the other using the addresses in columns 4&5 (CheckPath & Backpath)
            & the filter.  
        
        The filter must be the same as the type of link (or None)
        The check location must be the same as the added loation.
        
      
    '''
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    lresultSet = []
    del lresultSet[:]
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            entityID0 = Graph.api.createEntityFromMeme(stringArray[0])
            entityID1 = Graph.api.createEntityFromMeme(stringArray[1])
            
            #Attach entityID1 at the mount point specified in stringArray[2]
            if stringArray[2] != "X":
                mountPoints = api.getLinkCounterpartsByType(entityID0, stringArray[2], 1)
                                
                unusedMountPointsOverview = {}
                for mountPoint in mountPoints:
                    try:
                        mpMemeType = api.getEntityMemeType(mountPoint)
                        unusedMountPointsOverview[mountPoint] = mpMemeType
                    except Exception as e:
                        #errorMessage = "debugHelperMemeType warning in Smoketest.testEntityPhase7.  Traceback = %s" %e
                        #Graph.logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                        raise e
                
                for mountPoint in mountPoints:
                    api.addEntityLink(mountPoint, entityID1, {}, int(stringArray[5]))
            else:
                api.addEntityLink(entityID0, entityID1, {}, int(stringArray[5]))
              
            backTrackCorrect = False
            linkType = None
            if stringArray[6] != "X":
                linkType = int(stringArray[6])
            
            #see if we can get from entityID0 to entityID1 via stringArray[3]
            addLocationCorrect = False
            addLocationList = api.getLinkCounterpartsByType(entityID0, stringArray[3], linkType)
            if len(addLocationList) > 0:
                addLocationCorrect = True
                
            #see if we can get from entityID1 to entityID0 via stringArray[4]
            backTrackCorrect = False
            backTrackLocationList = api.getLinkCounterpartsByType(entityID1, stringArray[4], linkType)
            if len(backTrackLocationList) > 0:
                backTrackCorrect = True   
            
            if (backTrackCorrect == True) and (addLocationCorrect == True):
                testResult = True
                
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[7]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        lresultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return lresultSet



def testLinkCounterpartsByMetaMemeType(phaseName = 'LinkCounterpartsByMetaMemeType', fName = "LinkCounterpartsByMetaMemeType.atest"):
    ''' Repeat Phase 7, but traversing with metameme paths, instead of meme paths.
        LinkCounterpartsByMetaMemeType.atest differs from TestEntityPhase7.atest only in that cols D and E use metameme paths.
    
        Create entities from the meme in the first two colums.
        Add a link between the two at the location on entity in from column 3.
        Check and see if each is a counterpart as seen from the other using the addresses in columns 4&5 (CheckPath & Backpath)
            & the filter.  
        
        The filter must be the same as the type of link (or None)
        The check location must be the same as the added loation.
        
      
    '''
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    lresultSet = []
    del lresultSet[:]
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            entityID0 = Graph.api.createEntityFromMeme(stringArray[0])
            entityID1 = Graph.api.createEntityFromMeme(stringArray[1])
            
            #Attach entityID1 at the mount point specified in stringArray[2]
            if stringArray[2] != "X":
                mountPoints = api.getLinkCounterpartsByType(entityID0, stringArray[2], 1)
                                
                unusedMountPointsOverview = {}
                for mountPoint in mountPoints:
                    try:
                        mpMemeType = api.getEntityMemeType(mountPoint)
                        unusedMountPointsOverview[mountPoint] = mpMemeType
                    except Exception as e:
                        #errorMessage = "debugHelperMemeType warning in Smoketest.testEntityPhase7.  Traceback = %s" %e
                        #Graph.logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                        raise e
                
                for mountPoint in mountPoints:
                    api.addEntityLink(mountPoint, entityID1, {}, int(stringArray[5]))
            else:
                api.addEntityLink(entityID0, entityID1, {}, int(stringArray[5]))
              
            backTrackCorrect = False
            linkType = None
            if stringArray[6] != "X":
                linkType = int(stringArray[6])
            
            #see if we can get from entityID0 to entityID1 via stringArray[3]
            addLocationCorrect = False
            addLocationList = api.getLinkCounterpartsByMetaMemeType(entityID0, stringArray[3], linkType)
            if len(addLocationList) > 0:
                addLocationCorrect = True
                
            #see if we can get from entityID1 to entityID0 via stringArray[4]
            backTrackCorrect = False
            backTrackLocationList = api.getLinkCounterpartsByMetaMemeType(entityID1, stringArray[4], linkType)
            if len(backTrackLocationList) > 0:
                backTrackCorrect = True   
            
            if (backTrackCorrect == True) and (addLocationCorrect == True):
                testResult = True
                
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[7]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        lresultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return lresultSet




def testEntityPhase9(phaseName = 'testEntityPhase9', fName = "Entity_Phase9.atest"):
    ''' A modified phase 7 test with entity link removal after testing.
        Add a link between the two at the location on entity in from column 3.
        Check and see if each is a counterpart as seen from the other using the addresses in columns 4&5 (CheckPath & Backpath)
            & the filter.  
        The filter must be the same as the type of link (or None)
        The check location must be the same as the added loation.
        
        
        (So far, so good.  this is the same as in phase 7)
        added:
            Now remove the link
            Check again to make sure that the link no longer exists         
      
    '''
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        part1TestResult = False
        testResult = False
        try:
            entityID0 = Graph.api.createEntityFromMeme(stringArray[0])
            entityID1 = Graph.api.createEntityFromMeme(stringArray[1])
            
            #Attach entityID1 at the mount point specified in stringArray[2]
            rememberMe = {}
            
            mountPoints = api.getLinkCounterpartsByType(entityID0, stringArray[2], 1)
            for mountPoint in mountPoints:
                api.addEntityLink(mountPoint, entityID1, {}, int(stringArray[5]))
                rememberMe[mountPoint] = entityID1
             
            backTrackCorrect = False
            linkType = None
            if stringArray[6] != "X":
                linkType = int(stringArray[6])
            
            addLocationCorrect = False
            addLocationList = api.getLinkCounterpartsByType(entityID0, stringArray[3], linkType)
            if len(addLocationList) > 0:
                addLocationCorrect = True
                
            #see if we can get from entityID1 to entityID0 via stringArray[4]
            backTrackCorrect = False
            backTrackLocationList = api.getLinkCounterpartsByType(entityID1, stringArray[4], linkType)
            if len(backTrackLocationList) > 0:
                backTrackCorrect = True   
            
            if (backTrackCorrect == True) and (addLocationCorrect == True):
                part1TestResult = True
                
            #Time for phase 2    
            #Now remove that added member.  This is why we kept track of that added member; to speed up removal
            for mountPoint in rememberMe.keys():
                api.removeEntityLink(mountPoint, entityID1)
    
            secondAddLocationCorrect = False
            addLocationList = api.getLinkCounterpartsByType(entityID0, stringArray[3], linkType)
                
            if len(addLocationList) == 0:
                secondAddLocationCorrect = True
                
            if (part1TestResult == True) and (secondAddLocationCorrect == True):
                testResult = True 
                    
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[7]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"]) 
    return resultSet
   



def testEntityPhase10(phaseName = 'testEntityPhase10', fName = "Entity_Phase10.atest"):
    """ Create two entities from the meme in the first two colums.
        Both will should have the same singleton in their association (link) networks
        Try to traverse from one to the other
        
        This tests the 'singleton bridge' with respect to souble and triple wildcards  
        
      
    """
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        
        try:
            entityID0 = Graph.api.createEntityFromMeme(stringArray[0])
            
            trackLocationList = api.getLinkCounterpartsByType(entityID0, stringArray[2], None)
            if len(trackLocationList) > 0:
                testResult = True
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[3]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testTraverseParams(phaseName = 'testTraverseParams', fName = "TraverseWithParams.atest"):
    """ Create a TraverseParameters.A and TraverseParameters.B.  Attach them and assign values to the edges (links).
        Then fpor each test case:
            1 -Try to select A (with or without params, depending on the test case)
            2 -Try to navigate to B (with or without node/traverse params, depending on the test case
            3 -Compare our cuccessful reaching of B with the expected outcome.
              
    """
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = eachReadLine.split(' | ')
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])
        
        if n == 40:
            unusedCatch = True

        testResult = False
        
        try:
            entityID0 = Graph.api.createEntityFromMeme("TraverseParameters.A")
            entityID1 = Graph.api.createEntityFromMeme("TraverseParameters.B")
            Graph.api.addEntityLink(entityID0, entityID1, {'a':4}, 0)
            
            if n == 70:
                unusedCatchMe = True
            
            traversePath = stringArray[0].strip()
            trackLocationList = api.getLinkCounterpartsByType(entityID0, traversePath, None)
            if len(trackLocationList) > 0:
                testResult = True
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[1].strip()
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet





def testNumericValue(filename):
    #NumericValue.atest
    method = moduleName + '.' + 'testNumericValue'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])   
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        testArgumentMap = {}

        testResult = False
        try:
            entityIDList = api.getEntitiesByMemeType(stringArray[0])
            for entityIDListEntry in entityIDList:
                entityID = entityIDListEntry
            numberListS = api.evaluateEntity(entityID, testArgumentMap)
            numberList = []
            for numberString in numberListS:
                dec = decimal.Decimal(numberString)
                numberList.append(dec)
            argAsDecimal = decimal.Decimal(stringArray[1])
            if argAsDecimal in numberList:
                testResult = True
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[2]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet 




def testImplicitMeme(phaseName = 'testImplicitMeme', fName = "ImplicitMeme.atest"):
    ''' Create entities from the meme in the first two colums.
        Add a link between the two at the location on entity in from column 3, if it is not direct.  Otherwise diorectly to entity 0
        Check and see if each is a counterpart as seen from the other using the addresses in columns 4&5 (CheckPath & Backpath)
            & the filter.  
        
        The filter must be the same as the type of link (or None)
        The check location must be the same as the added loation.      
    '''
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])
        #debug
        #print ("Starting testcase %s, meme %s" %(n, stringArray[0]))
        #if n == 30:
        #    pass
        #/debug
        testResult = False
        try:
            try:
                entityID0 = Graph.api.createEntityFromMeme(stringArray[0])
            except Exception as e:
                raise DBError(stringArray[0])
            try:
                entityID1 = Graph.api.createEntityFromMeme(stringArray[1])
            except Exception as e:
                raise DBError(stringArray[1])
                
            
            #Attach entityID1 at the mount point specified in stringArray[2]
            if (stringArray[2] != '**DIRECT**'):
                mountPoints = api.getLinkCounterpartsByType(entityID0, stringArray[2], 1)
                for mountPoint in mountPoints:
                    api.addEntityLink(mountPoint, entityID1)
            else:
                #If we have a **DIRECT** mount, then attach entity 1 to entity 0
                api.addEntityLink(entityID0, entityID1)
              
            backTrackCorrect = False
            linkType = None
            
            #see if we can get from entityID0 to entityID1 via stringArray[3]
            addLocationCorrect = False
            addLocationList = api.getLinkCounterpartsByType(entityID0, stringArray[3], linkType)
            if len(addLocationList) > 0:
                addLocationCorrect = True
                
            #see if we can get from entityID1 to entityID0 via stringArray[4]
            backTrackCorrect = False
            backTrackLocationList = api.getLinkCounterpartsByType(entityID1, stringArray[4], linkType)
            if len(backTrackLocationList) > 0:
                backTrackCorrect = True   
            
            if (backTrackCorrect == True) and (addLocationCorrect == True):
                testResult = True
        
        except DBError as e:
            errorMsg = ('Database Error!  Check to see if the Database has been started and that meme %s is in the appropriate table.' % (e) )
            errata.append(errorMsg)                    
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[2])
        allTrueResult = str(testResult)
        expectedResult = stringArray[5]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet



def testCondition(filename):
    method = moduleName + '.' + 'testCondition'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        
        entityIDList = api.getEntitiesByMemeType(stringArray[0])
        for entityIDListEntry in entityIDList:
            subjectID = entityIDListEntry
            testArgumentMap = {stringArray[2] : stringArray[1]}
        try:
            testArgumentMap[stringArray[4]] = stringArray[3]
        except:
            pass
        try:
            testArgumentMap[stringArray[6]] = stringArray[5]
        except:
            pass
        try:
            del testArgumentMap['XXX']
        except:
            pass


        testResult = False
        try:
            entityIDList = api.getEntitiesByMemeType(stringArray[0])
            for entityIDListEntry in entityIDList:
                entityID = entityIDListEntry
            testResult = api.evaluateEntity(entityID, testArgumentMap)
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[7]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet



def testAACondition(filename):
    method = moduleName + '.' + 'testAACondition'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        testArgumentMap = {}
        subjectID = api.createEntityFromMeme(stringArray[1])
        objectID = None
        try:
            objectID = Graph.api.createEntityFromMeme(stringArray[2])
        except:
            pass

        if objectID is None:
            objectID = subjectID
            
        try:
            del testArgumentMap['XXX']
        except:
            pass
        
        testResult = False
        try:
            entityIDList = api.getEntitiesByMemeType(stringArray[0])
            for entityIDListEntry in entityIDList:
                cEntityID = entityIDListEntry
            testResult = api.evaluateEntity(cEntityID, testArgumentMap, None, subjectID, objectID)
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[3]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testSourceCreateMeme(filename):
    method = moduleName + '.' + 'testSourceCreateMeme'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
       
    #Phase 1 -  explicit Metameme and Meme declaration
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        metamemePath = stringArray[0]
        modulePath = stringArray[1]
        memeName = stringArray[2]
        operationResult = {}
        
        testResult = False
        try:
            operationResult = api.sourceMemeCreate(memeName, modulePath, metamemePath)
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            operationResult = {"memeID" : "%s.%s" %(modulePath, memeName), "ValidationResults" : [False, errorMsg]}
            errata.append(errorMsg)

        testcase = str(operationResult["memeID"])
        validation = operationResult["ValidationResults"]
        if validation[0] == True:
            testResult = True
        else:
            testResult = False
            errata = testResult[1]
        
        allTrueResult = str(testResult)
        expectedResult = stringArray[3]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
        
    #Phase 2 - Default Metameme, default module
    testResult = False
    memeName = "DefaultMetamemeMeme"
    try:
        operationResult = api.sourceMemeCreate(memeName)
    except Exception as e:
        errorMsg = ('Error!  Traceback = %s' % (e) )
        operationResult = {"memeID" : "%s.%s" %("Graphyne", memeName), "ValidationResults" : [False, errorMsg]}
        errata.append(errorMsg)

    testcase = str(operationResult["memeID"])
    validation = operationResult["ValidationResults"]
    if validation[0] == True:
        testResult = True
    else:
        testResult = False
        errata = testResult[1]
    
    allTrueResult = str(testResult)
    expectedResult = "True"
    results = [n, testcase, allTrueResult, expectedResult, errata]
    resultSet.append(results)

    #Phase 3 - Default Metameme, custom module
    testResult = False
    try:
        operationResult = api.sourceMemeCreate(memeName, "CustomModule")
    except Exception as e:
        errorMsg = ('Error!  Traceback = %s' % (e) )
        operationResult = {"memeID" : "%s.%s" %("Graphyne", memeName), "ValidationResults" : [False, errorMsg]}
        errata.append(errorMsg)

    testcase = str(operationResult["memeID"])
    validation = operationResult["ValidationResults"]
    if validation[0] == True:
        testResult = True
    else:
        testResult = False
        errata = testResult[1]
    
    allTrueResult = str(testResult)
    expectedResult = "True"
    results = [n, testcase, allTrueResult, expectedResult, errata]
    resultSet.append(results)

    
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet



def testSourceProperty(filename):
    method = moduleName + '.' + 'testSourceProperty'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        metamemePath = stringArray[0]
        modulePath = stringArray[1]
        memeName = stringArray[2]
        propName = stringArray[3]
        propValueStr = stringArray[4]
        operationResult = {}
        
        testResult = "False"
        try:
            sourceMeme = api.sourceMemeCreate(memeName, modulePath, metamemePath)
            operationResult = api.sourceMemePropertySet(sourceMeme["memeID"], propName, propValueStr)
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            operationResult = {"memeID" : "%s.%s" %(modulePath, memeName), "ValidationResults" : [False, errorMsg]}
            errata.append(errorMsg)

        testcase = "%s with property %s, %s" %(testResult[0], propName, propValueStr)
        
        validation = operationResult["ValidationResults"]
        if validation[0] == True:
            testResult = str(True)
        else:
            testResult = str(False)
            errata = validation[1]
        
        expectedResult = stringArray[5]
        results = [n, testcase, testResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet



def testSourcePropertyRemove(filename):
    method = moduleName + '.' + 'testSourcePropertyRemove'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        metamemePath = stringArray[0]
        modulePath = "%s_remove" %stringArray[1]
        memeName = stringArray[2]
        propName = stringArray[3]
        propValueStr = stringArray[4]
        sourceMeme = []
        
        testResult = str(False)
        try:
            sourceMeme = api.sourceMemeCreate(memeName, modulePath, metamemePath)
            unusedAddProp = api.sourceMemePropertySet(sourceMeme["memeID"], propName, propValueStr)
            operationResult = api.sourceMemePropertyRemove(sourceMeme["memeID"], propName)
            
            #list: [u'SourceProperty1_remove.L', [True, []]]
            validation = operationResult["ValidationResults"]
            if validation[0] == True:
                testResult = str(True)
            else:
                testResult = str(False)
                errata = validation[1]
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            operationResult = {"memeID" : "%s.%s" %(modulePath, memeName), "ValidationResults" : [False, errorMsg]}
            errata.append(errorMsg)

        testcase = "%s with property %s, %s removed" %(sourceMeme["memeID"], propName, propValueStr)
        expectedResult = stringArray[5]
        results = [n, testcase, testResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testSourceMember(filename):
    method = moduleName + '.' + 'testSourceMember'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        #e.g. (Examples.M, SourceMember3, M, Examples.L, SourceMember3, L, 2, False)
        
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        metamemePath = stringArray[0]
        modulePath = stringArray[1]
        memeName = stringArray[2]
        memberMetamemePath = stringArray[3]
        memberModulePath = stringArray[4]
        memberMemeName = stringArray[5]
        occurrence = stringArray[6]
        sourceMeme = ['']
        sourceMemberMeme = ['']
        
        testResult = str(False)
        try:
            sourceMeme = api.sourceMemeCreate(memeName, modulePath, metamemePath)
            sourceMemberMeme = api.sourceMemeCreate(memberMemeName, memberModulePath, memberMetamemePath)
            operationResult = api.sourceMemeMemberAdd(sourceMeme["memeID"], sourceMemberMeme["memeID"], occurrence)
            validation = operationResult["ValidationResults"]
            if validation[0] == True:
                testResult = str(True)
            else:
                testResult = str(False)
                errata = validation[1]
        except Exception as e:
            errorMsg = ('Error in testcase testSourceMember!  Traceback = %s' % (e) )
            api.writeError(errorMsg)
            errata.append(errorMsg)

        testcase = "%s has member %s" %(sourceMeme["memeID"], sourceMemberMeme["memeID"])
        expectedResult = stringArray[7]
        results = [n, testcase, testResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testSourceMemberRemove(filename):
    method = moduleName + '.' + 'testSourceMemberRemove'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        metamemePath = stringArray[0]
        modulePath = "%s_remove" %stringArray[1]
        memeName = stringArray[2]
        memberMetamemePath = stringArray[3]
        memberModulePath = "%s_remove" %stringArray[4]
        memberMemeName = stringArray[5]
        occurrence = stringArray[6]
        sourceMeme = ['']
        sourceMemberMeme = ['']
        
        testResult = str(False)
        try:
            sourceMeme = api.sourceMemeCreate(memeName, modulePath, metamemePath)
            sourceMemberMeme = api.sourceMemeCreate(memberMemeName, memberModulePath, memberMetamemePath)
            unusedAdd = api.sourceMemeMemberAdd(sourceMeme["memeID"], sourceMemberMeme["memeID"], occurrence)
            operationResult = api.sourceMemeMemberRemove(sourceMeme["memeID"], sourceMemberMeme["memeID"])
            validation = operationResult["ValidationResults"]
            if validation[0] == True:
                testResult = str(True)
            else:
                testResult = str(False)
                errata = validation[1]
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            operationResult = {"memeID" : "%s.%s" %(modulePath, memeName), "ValidationResults" : [False, errorMsg]}
            errata.append(errorMsg)

        testcase = "%s has member %s" %(sourceMeme["memeID"], sourceMemberMeme["memeID"])
        expectedResult = "True"
        results = [n, testcase, testResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
    



def testSourceEnhancement(filename):
    method = moduleName + '.' + 'testSourceEnhancement'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        metamemePath = stringArray[0]
        modulePath = stringArray[1]
        memeName = stringArray[2]
        enhancedMetamemePath = stringArray[3]
        enhancedModulePath = stringArray[4]
        enhancedMemeName = stringArray[5]
        sourceMeme = ['']
        sourceMemberMeme = ['']
        
        testResult = str(False)
        try:
            sourceMeme = api.sourceMemeCreate(memeName, modulePath, metamemePath)
            sourceMemberMeme = api.sourceMemeCreate(enhancedMemeName, enhancedModulePath, enhancedMetamemePath)
            operationResult = api.sourceMemeEnhancementAdd(sourceMeme["memeID"], sourceMemberMeme["memeID"])
            validation = operationResult["ValidationResults"]
            if validation[0] == True:
                testResult = str(True)
            else:
                testResult = str(False)
                errata = validation[1]
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            operationResult = {"memeID" : "%s.%s" %(modulePath, memeName), "ValidationResults" : [False, errorMsg]}
            errata.append(errorMsg)

        testcase = "%s enhancing %s" %(sourceMeme["memeID"], sourceMemberMeme["memeID"])
        
        expectedResult = stringArray[6]
        results = [n, testcase, testResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
        
    #Part 2 - Create two generic memes and use one to enhance the other
    # Create the two memes
    # Add a property to each
    # Create entities from the two memes
    # Check to ensure that they have the peoper properties
    # Use one meme to enhanece the other.
    # Create a new entity.
    # Test that it has all properties
    
    part2AllTrue = True
    # Create the two memes
    enhancingMeme = api.sourceMemeCreate("Enhancing")
    enhancedMeme = api.sourceMemeCreate("Enhanced")
    testcase = "Generic enhancing Generic"
    try:
        # Add a property to each
        api.sourceMemePropertySet(enhancingMeme["memeID"], "A", "A")
        api.sourceMemePropertySet(enhancedMeme["memeID"], "B", "B")
        
        # Create entities from the two memes
        entityA = api.createEntityFromMeme(enhancingMeme["memeID"])
        entityB = api.createEntityFromMeme(enhancedMeme["memeID"])
        
        # Check to ensure that they have the peoper properties
        entityAhasA = Graph.api.getEntityHasProperty(entityA, "A")
        entityBhasA = Graph.api.getEntityHasProperty(entityB, "A")
        entityAhasB = Graph.api.getEntityHasProperty(entityA, "B")
        entityBhasB = Graph.api.getEntityHasProperty(entityB, "B")
        if entityAhasA == False:
            part2AllTrue = False
        if entityBhasA == True:
            part2AllTrue = False
        if entityAhasB == True:
            part2AllTrue = False
        if entityBhasB == False:
            part2AllTrue = False
        
        # Use one meme to enhanece the other.
        unusedReturn = api.sourceMemeEnhancementAdd(enhancingMeme["memeID"], enhancedMeme["memeID"])
        
        # Test that it has all properties
        entityAB = api.createEntityFromMeme(enhancedMeme["memeID"])
        entityABhasA = Graph.api.getEntityHasProperty(entityAB, "A")
        entityABhasB = Graph.api.getEntityHasProperty(entityAB, "B")
        if entityABhasA == False:
            part2AllTrue = False
        if entityABhasB == False:
            part2AllTrue = False
            
        part2AllTrue = str(part2AllTrue)
        results = [n, testcase, part2AllTrue, "True", []]
        resultSet.append(results)
    except Exception as e:
        results = [n, testcase, "False", "True", []]
        resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet





def testSourceEnhancementRemove(filename):
    method = moduleName + '.' + 'testSourceEnhancementRemove'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        metamemePath = stringArray[0]
        modulePath = "%s_remove" %stringArray[1]
        memeName = stringArray[2]
        enhancedMetamemePath = stringArray[3]
        enhancedModulePath = "%s_remove" %stringArray[4]
        enhancedMemeName = stringArray[5]
        sourceMeme = ['']
        sourceMemberMeme = ['']
        
        testResult = str(False)
        try:
            sourceMeme = api.sourceMemeCreate(memeName, modulePath, metamemePath)
            sourceMemberMeme = api.sourceMemeCreate(enhancedMemeName, enhancedModulePath, enhancedMetamemePath)
            unusedAddEnhancement = api.sourceMemeEnhancementAdd(sourceMeme["memeID"], sourceMemberMeme["memeID"])
            operationResult = api.sourceMemeEnhancementRemove(sourceMeme["memeID"], sourceMemberMeme["memeID"])
            validation = operationResult["ValidationResults"]
            if validation[0] == True:
                testResult = str(True)
            else:
                testResult = str(False)
                errata = validation[1]
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            operationResult = {"memeID" : "%s.%s" %(modulePath, memeName), "ValidationResults" : [False, errorMsg]}
            errata.append(errorMsg)

        testcase = "%s enhancing %s" %(sourceMeme["memeID"], sourceMemberMeme["memeID"])
        expectedResult = "True"
        results = [n, testcase, testResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
        
    #Part 2 - Create two generic memes and use one to enhance the other
    # Create the two memes
    # Add a property to each
    # Create entities from the two memes
    # Check to ensure that they have the peoper properties
    # Use one meme to enhanece the other.
    # Create a new entity.
    # Test that it has all properties
    # Remove the enhancement
    # Create a new entity and test that the enhancing property is not there
    
    part2AllTrue = True
    # Create the two memes
    enhancingMeme = api.sourceMemeCreate("Enhancing")
    enhancedMeme = api.sourceMemeCreate("Enhanced")
    testcase = "Generic enhancing Generic"
    try:
        # Add a property to each
        api.sourceMemePropertySet(enhancingMeme["memeID"], "A", "A")
        api.sourceMemePropertySet(enhancedMeme["memeID"], "B", "B")
        
        # Create entities from the two memes
        entityA = api.createEntityFromMeme(enhancingMeme["memeID"])
        entityB = api.createEntityFromMeme(enhancedMeme["memeID"])
        
        # Check to ensure that they have the peoper properties
        entityAhasA = Graph.api.getEntityHasProperty(entityA, "A")
        entityBhasA = Graph.api.getEntityHasProperty(entityB, "A")
        entityAhasB = Graph.api.getEntityHasProperty(entityA, "B")
        entityBhasB = Graph.api.getEntityHasProperty(entityB, "B")
        if entityAhasA == False:
            part2AllTrue = False
        if entityBhasA == True:
            part2AllTrue = False
        if entityAhasB == True:
            part2AllTrue = False
        if entityBhasB == False:
            part2AllTrue = False
        
        # Use one meme to enhanece the other.
        unusedReturn = api.sourceMemeEnhancementAdd(enhancingMeme["memeID"], enhancedMeme["memeID"])
        
        # Test that it has all properties
        entityAB = api.createEntityFromMeme(enhancedMeme["memeID"])
        entityABhasA = Graph.api.getEntityHasProperty(entityAB, "A")
        entityABhasB = Graph.api.getEntityHasProperty(entityAB, "B")
        if entityABhasA == False:
            part2AllTrue = False
        if entityABhasB == False:
            part2AllTrue = False
            
        # Remove the enhancement
        unusedReturn = api.sourceMemeEnhancementRemove(enhancingMeme["memeID"], enhancedMeme["memeID"])
        
        # Create a new entity and test that the enhancing property is not there
        entityABRemoved = api.createEntityFromMeme(enhancedMeme["memeID"])
        entityABRemovedHasA = Graph.api.getEntityHasProperty(entityABRemoved, "A")
        entityABRemovedHasB = Graph.api.getEntityHasProperty(entityABRemoved, "B")
        if entityABRemovedHasA == True:
            part2AllTrue = False
        if entityABRemovedHasB == False:
            part2AllTrue = False
            
        part2AllTrue = str(part2AllTrue)
        results = [n, testcase, part2AllTrue, "True", []]
        resultSet.append(results)
    except Exception as e:
        results = [n, testcase, "False", "True", []]
        resultSet.append(results)
        
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet





def testSourceSingletonSet(filename):
    method = moduleName + '.' + 'testSourceEnhancementRemove'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    resultSet = []
        
    #try:
    testFileName = os.path.join(testDirPath, filename)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
        
    for eachReadLine in allLines:
        errata = []
        n = n+1
        unicodeReadLine = str(eachReadLine)
        stringArray = str.split(unicodeReadLine)
        metamemePath = stringArray[0]
        modulePath = "%s_singleton" %stringArray[1]
        memeName = stringArray[2]
        sourceMeme = ['']
        
        testResult = str(False)
        afterSingleton = False
        afterRemoval = False
        operationResult = {}
        try:
            sourceMeme = api.sourceMemeCreate(memeName, modulePath, metamemePath)
            
            setAsSingleton = api.sourceMemeSetSingleton(sourceMeme["memeID"], True)
            afterSingleton = api.getIsMemeSingleton(sourceMeme["memeID"])
            if afterSingleton == False:
                verboseResults = setAsSingleton["ValidationResults"]
                errata.append(verboseResults[1]) 
                
            setAsNonSingleton = api.sourceMemeSetSingleton(sourceMeme["memeID"], False)
            afterRemoval = api.getIsMemeSingleton(sourceMeme["memeID"])
            if afterRemoval == True:
                verboseResults = setAsNonSingleton["ValidationResults"]
                errata.append(verboseResults[1]) 
                
            operationResult = {"memeID" : sourceMeme["memeID"], "ValidationResults" : [True, []]}
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            operationResult = {"memeID" : "%s.%s" %(modulePath, memeName), "ValidationResults" : [False, errorMsg]}
            errata.append(errorMsg)

        if (afterSingleton == True) and (afterRemoval == False):
            testResult = str(True)
            
        testcase = str(operationResult["memeID"])

        expectedResult = "True"
        results = [n, testcase, testResult, expectedResult, errata]
        resultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet



def testGeneric():
    """
        Greate a generic meme; one of type Graphyne.Generic.
    """
    method = moduleName + '.' + 'testGeneric'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    resultSet = []
    errata = []
    testResult = False
       
    expectedResult = "True" 
    try:
        testEntityID = api.createEntity()
        memeType = api.getEntityMemeType(testEntityID)
        if memeType == "Graphyne.Generic":
            operationResult = {"memeID" : "Graphyne.Generic", "ValidationResults" : [True, []]}
            testResult = "True"
        else:
            errorMsg = ('Generic Entity Has meme type = %s' % (memeType) )
            operationResult = {"memeID" : "Graphyne.Generic", "ValidationResults" : [True, []]}
    except Exception as e:
        errorMsg = ('Error!  Traceback = %s' % (e) )
        operationResult = {"memeID" : "Graphyne.Generic", "ValidationResults" : [False, errorMsg]}
        errata.append(errorMsg)
        
    testcase = str(operationResult["memeID"])
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet


def testDeleteEntity():
    """
        Test Entity Removal.
        Create 5 entities of type Graphyne.Generic.  
        Chain them together: E1 >> E2 >> E3 >> E4 >> E5
        
        Check that they are functional
        Traverse from E1 to E5
        Traverse from E5 to E1
        
        Delete E3
        We should not be able to traverse form E1 to E5
        We should not be able to traverse form E5 to E1
        We should not be able to traverse from E2 to E3
        We should not be able to traverse from E3 to E2
        We should not be able to traverse from E4 to E3
        We should not be able to traverse from E3 to E4
        We should be able to traverse from E1 to E2
        We should be able to traverse from E2 to E1
        We should be able to traverse from E4 to E5
        We should be able to traverse from E5 to E4
        
        We should not be able to aquire E3 via getEntity()
        
        
    """
    method = moduleName + '.' + 'testDeleteEntity'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create 5 entities of type Graphyne.Generic.  Chain them together: E1 >> E2 >> E3 >> E4 >> E5
    try:
        testEntityID1 = api.createEntity()
        testEntityID2 = api.createEntity()
        testEntityID3 = api.createEntity()
        testEntityID4 = api.createEntity()
        testEntityID5 = api.createEntity()
        api.addEntityLink(testEntityID1, testEntityID2)
        api.addEntityLink(testEntityID2, testEntityID3)
        api.addEntityLink(testEntityID3, testEntityID4)
        api.addEntityLink(testEntityID4, testEntityID5)
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error creating entities!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #Navitate to end of chain and back
    try:
        uuid15 = api.getLinkCounterpartsByType(testEntityID1, "Graphyne.Generic::Graphyne.Generic::Graphyne.Generic::Graphyne.Generic")
        uuid11 = api.getLinkCounterpartsByType(uuid15[0], "Graphyne.Generic::Graphyne.Generic::Graphyne.Generic::Graphyne.Generic")
        if (uuid15[0] != testEntityID5) or (uuid11[0] != testEntityID1): 
            testResult = "False"
            errorMsg = ('%sShould be able to navigate full chain and back before deleting middle entity, but could not!\n')
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error deleting Entity!  Traceback = %s' % (e) )
        errata.append(errorMsg)
      
    #Delete E3
    try:
        api.destroyEntity(testEntityID3)
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error deleting Entity!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #E3 should no longer be there
    try:
        e3 = api.getEntity(testEntityID3)
        if e3 is not None:
            testResult = "False"
            errorMsg = ('Deleted entity still present!')
            errata.append(errorMsg)
    except Exceptions.NoSuchEntityError as e:
        #We expect a NoSuchEntityError here
        pass
    except Exception as e:
        #But we ONLY expect a NoSuchEntityError exception.  Anything else is a problem
        testResult = "False"
        errorMsg = ('Unexpected Error while checking for previously deleted entity!  Traceback = %s' % (e) )
        errata.append(errorMsg)        
    
    #But E4 should remain
    try:
        e4 = api.getEntity(testEntityID4)
        if e4 is None:
            testResult = "False"
            errorMsg = ('Entity that should not be deleted was!')
            errata.append(errorMsg)
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error while checking to see if entity that was not supposed to be deleted is still present!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #Post delete navigation
    try:
        #First hops should work
        uuid22 = api.getLinkCounterpartsByType(testEntityID1, "Graphyne.Generic")
        uuid24 = api.getLinkCounterpartsByType(testEntityID5, "Graphyne.Generic")
        if (len(uuid22) == 0) or (len(uuid24) == 0) : 
            testResult = "False"
            errorMsg = ('%sShould be able to navigate between undeleted entities, but can not!\n' %errorMsg)
    except Exception as e:
        testResult = "False"
        errorMsg = ('%sProblem in spost delete navigation between undeleted entities.  Traceback = %s' %(errorMsg, e))

    
    try:
        #This should not
        uuid25 = api.getLinkCounterpartsByType(testEntityID1, "Graphyne.Generic::Graphyne.Generic::Graphyne.Generic::Graphyne.Generic")
        uuid21 = api.getLinkCounterpartsByType(testEntityID5, "Graphyne.Generic::Graphyne.Generic::Graphyne.Generic::Graphyne.Generic")
        if (len(uuid25) > 0) or (len(uuid21) > 0) : 
            testResult = "False"
            errorMsg = ('%sShould not be able to navigate full chain and back, but did!\n' %errorMsg)
    except: pass       

    try:
        #neither should this
        nearestNeighbors = api.getLinkCounterpartsByType(testEntityID2, "*")
        if (testEntityID1 not in nearestNeighbors) or (testEntityID4 in nearestNeighbors) : 
            testResult = "False"
            errorMsg = ('%sShould not be able to navigate full chain and back, but did!\n' %errorMsg)
    except: pass 
        
    testcase = "Deletion"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet


def testSubatomicLinks():
    """
        Test creating and traversing subatomic links
        Create 3 entities of type Graphyne.Generic.
    """
    method = moduleName + '.' + 'testSubatomicLinks'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create 5 entities of type Graphyne.Generic and get the Examples.MemeA4 singleton as well.  
    #Chain them together: E1 >> E2 >> E3 >> E4 >> Examples.MemeA4 << E5
    try:
        testEntityID1 = api.createEntity()
        testEntityID2 = api.createEntity()
        testEntityID3 = api.createEntity()
        api.addEntityLink(testEntityID1, testEntityID2)         #Atomic
        api.addEntityLink(testEntityID2, testEntityID3, {}, 1)  #Subatomic
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error creating entities!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #Atomic Navigation
    try:
        uuid12 = api.getLinkCounterpartsByType(testEntityID2, "Graphyne.Generic", 0)
        if len(uuid12) != 1: 
            testResult = "False"
            errorMsg = ('%sError in getLinkCounterpartsByType() chile checking for Atomic links.  Memberlist should return exactly one entry.  Actually returned %s members!\n' %len(uuid12))
        elif uuid12[0] != testEntityID1: 
            testResult = "False"
            errorMsg = ('%sError in getLinkCounterpartsByType() chile checking for Atomic links.  Wrong cluster sibling returned.!\n')
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error traversing atomic link!  Traceback = %s' % (e) )
        errata.append(errorMsg)
      
    #SubAtomic Navigation
    try:
        uuid23 = api.getLinkCounterpartsByType(testEntityID2, "Graphyne.Generic", 1)
        if len(uuid23) != 1: 
            testResult = "False"
            errorMsg = ('%sError in getLinkCounterpartsByType() chile checking for SubAtomic links.  Memberlist should return exactly one entry.  Actually returned %s members!\n' %len(uuid12))
        elif uuid23[0] != testEntityID3: 
            testResult = "False"
            errorMsg = ('%sError in getLinkCounterpartsByType() chile checking for SubAtomic links.  Wrong cluster sibling returned.!\n')
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error traversing subatomic link  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #Universal Navigation
    try:
        uuidBoth = api.getLinkCounterpartsByType(testEntityID2, "Graphyne.Generic")
        if len(uuidBoth) != 2: 
            testResult = "False"
            errorMsg = ('%sError in getLinkCounterpartsByType() chile checking for SubAtomic links.  Memberlist should return exactly two entries.  Actually returned %s members!\n' %len(uuid12))
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error traversing link!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    testcase = "Subatomic Links"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet

  


def testGetClusterMembers():
    """
        Test Getting Clister Members.
        Create 6 entities of type Graphyne.Generic.  
        Chain four of them together: E1 >> E2 >> E3 >> E4
        Connect E4 to a singleton, Examples.MemeA4
        Connect E5 to Examples.MemeA4
        Connect E3 to E6 via a subatomic link
        
        Check that we can traverse from E1 to E5.
        Get the cluseter member list of E3 with linktype = None.  It should include E2, E3, E4, E6
        Get the cluseter member list of E3 with linktype = 0.  It should include E2, E3, E4
        Get the cluseter member list of E3 with linktype = 1.  It should include E6
        Get the cluseter member list of E5.  It should be empty
        
        memeStructure = script.getClusterMembers(conditionContainer, 1, False)
        
        
    """
    method = moduleName + '.' + 'testGetClusterMembers'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create 5 entities of type Graphyne.Generic and get the Examples.MemeA4 singleton as well.  
    #Chain them together: E1 >> E2 >> E3 >> E4 >> Examples.MemeA4 << E5
    try:
        testEntityID1 = api.createEntity()
        testEntityID2 = api.createEntity()
        testEntityID3 = api.createEntity()
        testEntityID4 = api.createEntity()
        testEntityID5 = api.createEntity()
        testEntityID6 = api.createEntity()
        theSingleton = Graph.api.createEntityFromMeme("Examples.MemeA4")
        api.addEntityLink(testEntityID1, testEntityID2)
        api.addEntityLink(testEntityID2, testEntityID3)
        api.addEntityLink(testEntityID3, testEntityID4)
        api.addEntityLink(testEntityID3, testEntityID6, {}, 1)
        api.addEntityLink(testEntityID4, theSingleton)
        api.addEntityLink(testEntityID5, theSingleton)
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error creating entities!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #Navitate to end of chain and back
    try:
        uuid15 = api.getLinkCounterpartsByType(testEntityID1, "Graphyne.Generic::Graphyne.Generic::Graphyne.Generic::Examples.MemeA4::Graphyne.Generic")
        uuid11 = api.getLinkCounterpartsByType(uuid15[0], "Examples.MemeA4::Graphyne.Generic::Graphyne.Generic::Graphyne.Generic::Graphyne.Generic")
        if (uuid15[0] != testEntityID5) or (uuid11[0] != testEntityID1): 
            testResult = "False"
            errorMsg = ('%sShould be able to navigate full chain and back before measuring cluster membership, but could not!\n')
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error measuring cluster membership!  Traceback = %s' % (e) )
        errata.append(errorMsg)
      
    #From E3, atomic
    try:
        entityListRaw = api.getClusterMembers(testEntityID3)
        entityList1 = []
        for entityUUID in entityListRaw:
            entityList1.append(entityUUID)
        if testEntityID1 not in entityList1:
            testResult = "False"
            errorMsg = ('%E1 should be in atomic link cluster of E3, but is not!\n' %errorMsg)
        if testEntityID2 not in entityList1:
            testResult = "False"
            errorMsg = ('%E2 should be in atomic link cluster of E3, but is not!\n' %errorMsg)
        if testEntityID4 not in entityList1:
            testResult = "False"
            errorMsg = ('%E4 should be in atomic link cluster of E3, but is not!\n' %errorMsg)  
        if theSingleton not in entityList1:
            testResult = "False"
            errorMsg = ('%Examples.MemeA4 should be in atomic link cluster of E3, but is not!\n' %errorMsg) 
        if len(entityList1) != 4: 
            testResult = "False"
            errorMsg = ('%E3 should have 3 siblings in its atomic link cluster, but it has %s!\n' %(errorMsg, len(entityList1)))      
    except Exception as e:
        testResult = "False"
        errorMsg = ('Getting atomic cluster of E3!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #From E3, subatomic
    try:
        entityList2 = api.getClusterMembers(testEntityID3, 1)
        if testEntityID6 not in entityList2:
            testResult = "False"
            errorMsg = ('%E6 should be in subatomic link cluster of E3, but is not!\n' %errorMsg)  
        if len(entityList2) != 1: 
            testResult = "False"
            errorMsg = ('%E3 should have 1 sibling in its atomic link cluster, but it has %s!\n' %(errorMsg, len(entityList1)))      
    except Exception as e:
        testResult = "False"
        errorMsg = ('Getting atomic cluster of E3!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #From E5, atomic
    try:
        entityList3 = api.getClusterMembers(testEntityID5)
        if theSingleton not in entityList3:
            testResult = "False"
            errorMsg = ('%Examples.MemeA4 should be in atomic link cluster of E3, but is not!\n' %errorMsg)
        if len(entityList3) != 1: 
            testResult = "False"
            errorMsg = ('%E5 should have 0 siblings in its atomic link cluster, but it has %s!\n' %(errorMsg, len(entityList1)))      
    except Exception as e:
        testResult = "False"
        errorMsg = ('Getting atomic cluster of E5!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #From E5, subatomic
    try:
        entityList4 = api.getClusterMembers(testEntityID5)
        if len(entityList4) != 1: 
            testResult = "False"
            errorMsg = ('%E5 should have 1 sibling in its atomic link cluster, but it has %s!\n' %(errorMsg, len(entityList1)))      
    except Exception as e:
        testResult = "False"
        errorMsg = ('Getting atomic cluster of E5!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    testcase = "getClusterMembers()"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testGetHasCounterpartsByType(phaseName = 'getHasCounterpartsByType', fName = "Entity_Phase7.atest"):
    ''' 
        Basically a repeat of Phase 7, but with getHasCounterpartsByType()
    
        Create entities from the meme in the first two colums.
        Add a link between the two at the location on entity in from column 3.
        Check and see if each is a counterpart as seen from the other using the addresses in columns 4&5 (CheckPath & Backpath)
            & the filter.  
        
        The filter must be the same as the type of link (or None)
        The check location must be the same as the added loation.
        
      
    '''
    method = moduleName + '.' + phaseName
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    results = []
    lresultSet = []
    del lresultSet[:]
        
    #try:
    testFileName = os.path.join(testDirPath, fName)
    readLoc = codecs.open(testFileName, "r", "utf-8")
    allLines = readLoc.readlines()
    readLoc.close
    n = 0
    
    for eachReadLine in allLines:
        errata = []
        n = n+1
        stringArray = str.split(eachReadLine)
        Graph.logQ.put( [logType , logLevel.INFO , method , "Starting testcase %s, meme %s" %(n, stringArray[0])])

        testResult = False
        try:
            entityID0 = Graph.api.createEntityFromMeme(stringArray[0])
            entityID1 = Graph.api.createEntityFromMeme(stringArray[1])
            entityID2 = Graph.api.createEntityFromMeme(stringArray[1])
            
            #Attach entityID1 at the mount point specified in stringArray[2]
            if stringArray[2] != "X":
                mountPoints = api.getLinkCounterpartsByType(entityID0, stringArray[2], 1)
                                
                unusedMountPointsOverview = {}
                for mountPoint in mountPoints:
                    try:
                        mpMemeType = api.getEntityMemeType(mountPoint)
                        unusedMountPointsOverview[mountPoint] = mpMemeType
                    except Exception as e:
                        #errorMessage = "debugHelperMemeType warning in Smoketest.testEntityPhase7.  Traceback = %s" %e
                        #Graph.logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                        raise e
                
                for mountPoint in mountPoints:
                    api.addEntityLink(mountPoint, entityID1, {}, int(stringArray[5]))
            else:
                api.addEntityLink(entityID0, entityID1, {}, int(stringArray[5]))
              
            backTrackCorrect = False
            linkType = None
            if stringArray[6] != "X":
                linkType = int(stringArray[6])
              
            backTrackCorrect = False
            linkType = None
            if stringArray[6] != "X":
                linkType = int(stringArray[6])
            
            #see if we can get from entityID0 to entityID1 via stringArray[3]
            addLocationCorrect = api.getHasCounterpartsByType(entityID0, stringArray[3], linkType)
                
            #see if we can get from entityID1 to entityID0 via stringArray[4]
            backTrackCorrect = api.getHasCounterpartsByType(entityID1, stringArray[4], linkType)
            
            #see if we can get from entityID2 to entityID0 via stringArray[4]
            e3Attached = api.getHasCounterpartsByType(entityID2, stringArray[4], linkType)
            
            if (backTrackCorrect == True) and (addLocationCorrect == True) and (e3Attached == False):
                testResult = True
                
        except Exception as e:
            errorMsg = ('Error!  Traceback = %s' % (e) )
            errata.append(errorMsg)

        testcase = str(stringArray[0])
        allTrueResult = str(testResult)
        expectedResult = stringArray[7]
        results = [n, testcase, allTrueResult, expectedResult, errata]
        lresultSet.append(results)
        
        Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(n)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return lresultSet



def testGetEntityMetaMemeType():
    """
        Greate a generic meme; one of type Graphyne.Generic.
        Ensure that it's metameme is Graphyne.GenericMetaMeme
    """
    method = moduleName + '.' + 'testGetEntityMetaMemeType'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    resultSet = []
    errata = []
    testResult = False
       
    expectedResult = "True" 
    try:
        testEntityID = api.createEntity()
        metaMemeType = api.getEntityMetaMemeType(testEntityID)
        if metaMemeType == "Graphyne.GenericMetaMeme":
            operationResult = {"metamemeID" : "Graphyne.GenericMetaMeme", "ValidationResults" : [True, []]}
            testResult = "True"
        else:
            errorMsg = ('Generic Entity Has metameme type = %s' % (metaMemeType) )
            operationResult = {"metamemeID" : "Graphyne.GenericMetaMeme", "ValidationResults" : [True, []]}
    except Exception as e:
        errorMsg = ('Error!  Traceback = %s' % (e) )
        operationResult = {"metamemeID" : "Graphyne.GenericMetaMeme", "ValidationResults" : [False, errorMsg]}
        errata.append(errorMsg)
        
    testcase = str(operationResult["metamemeID"])
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testInstallExecutor():
    """
        Greate a generic meme; one of type Graphyne.Generic.
        Ensure that it's metameme is Graphyne.GenericMetaMeme
    """
    method = moduleName + '.' + 'testInstallExecutor'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    resultSet = []
    errata = []
    testResult = "True"
    errorMsg = ""
       
    expectedResult = "True" 
    try:
        testEntityID = api.createEntity()
        e2MemeType = api.getEntityMemeType(testEntityID)
        
        from Config.Test.TestRepository import InstallPyExecTest as testMod
        
        testExec = testMod.TestClass(e2MemeType)
        api.installPythonExecutor(testEntityID, testExec)
        
        #The execute() method of testMod.TestClass hould return the memeID when 
        returnVal1 = api.evaluateEntity(testEntityID)
        if returnVal1 != e2MemeType:
            testResult = "False"
            errorMsg = ("%Calling TestClass.execute() should return %s, but %s was returned instead!\n" %(errorMsg, e2MemeType, returnVal1))
        else:
            operationResult = {"metamemeID" : "Graphyne.GenericMetaMeme", "ValidationResults" : [True, errorMsg]} 

        if testResult == "True":
            returnVal2 = api.evaluateEntity(testEntityID, {"returnMe" : "Hello World"})
            if returnVal2 != "Hello World":
                testResult = "False"
                errorMsg = ("%Calling TestClass.execute() with 'returnMe' in runtime parameter keys should return 'Hello World', but %s was returned instead!\n" %(errorMsg, returnVal2)) 
            else:
                operationResult = {"metamemeID" : "Graphyne.GenericMetaMeme", "ValidationResults" : [True, []]}
        
        if testResult == "True":  
            try:
                returnVal3 = api.evaluateEntity(testEntityID, {"thisWontReturnAnything" : "Hello World"})
                testResult = "False"
                errorMsg = ("%Calling TestClass.execute() 'thisWontReturnAnything' in runtime parameter keys should return a keyError exception, but %s was returned instead!\n" %(errorMsg, returnVal2)) 
            except Exceptions.EventScriptFailure as e:
                #We should have this result
                operationResult = {"metamemeID" : "Graphyne.GenericMetaMeme", "ValidationResults" : [True, errorMsg]}

    except Exception as e:
        testResult = "False"
        errorMsg = ('Error!  Traceback = %s' % (e) )
        operationResult = {"metamemeID" : "Graphyne.GenericMetaMeme", "ValidationResults" : [False, errorMsg]}
        errata.append(errorMsg)
        
    testcase = str(operationResult["metamemeID"])
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testGetCluster():
    """
        Test Getting Cluster Dictionary.
        Create 6 entities of type Graphyne.Generic.  
        Chain four of them together: E1 >> E2 >> E3 >> E4
        Connect E4 to a singleton, Examples.MemeA4
        Connect E5 to Examples.MemeA4
        Connect E3 to E6 via a subatomic link
        
        Check that we can traverse from E1 to E5.
        Get the cluster member list of E3 with linktype = None.  It should include E2, E3, E4, E6
        Get the cluster member list of E3 with linktype = 0.  It should include E2, E3, E4
        Get the cluster member list of E3 with linktype = 1.  It should include E6
        Get the cluster member list of E5.  It should be empty
        
        memeStructure = script.getClusterMembers(conditionContainer, 1, False)
        
        
    """
    method = moduleName + '.' + 'testGetClusterMembers'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create 5 entities of type Graphyne.Generic and get the Examples.MemeA4 singleton as well.  
    #Chain them together: E1 >> E2 >> E3 >> E4 >> Examples.MemeA4 << E5
    try:
        testEntityID1 = api.createEntity()
        testEntityID2 = api.createEntity()
        testEntityID3 = api.createEntity()
        testEntityID4 = api.createEntity()
        testEntityID5 = api.createEntity()
        testEntityID6 = api.createEntity()
        theSingleton = Graph.api.createEntityFromMeme("Examples.MemeA4")
        api.addEntityLink(testEntityID1, testEntityID2)
        api.addEntityLink(testEntityID2, testEntityID3)
        api.addEntityLink(testEntityID3, testEntityID4)
        api.addEntityLink(testEntityID3, testEntityID6, {}, 1)
        api.addEntityLink(testEntityID4, theSingleton)
        api.addEntityLink(testEntityID5, theSingleton)
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error creating entities!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #Navitate to end of chain and back
    try:
        uuid15 = api.getLinkCounterpartsByType(testEntityID1, ">>Graphyne.Generic>>Graphyne.Generic>>Graphyne.Generic>>Examples.MemeA4<<Graphyne.Generic", None, True)
        uuid11 = api.getLinkCounterpartsByType(uuid15[0], "Examples.MemeA4<<Graphyne.Generic<<Graphyne.Generic<<Graphyne.Generic<<Graphyne.Generic", None, True)
        if (testEntityID5 not in uuid15) or (testEntityID1 not in uuid11): 
            testResult = "False"
            errorMsg = ('%sShould be able to navigate full chain and back before measuring cluster membership, but could not!\n')
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error measuring cluster membership!  Traceback = %s' % (e) )
        errata.append(errorMsg)
      
    #From E3, atomic
    try:
        entityListRaw = api.getCluster(testEntityID3)
        entityClusterJSON1 = api.getClusterJSON(testEntityID3)
        entityList1 = []
        for entityNode in entityListRaw["nodes"]:
            entityList1.append(entityNode['id'])
        if str(testEntityID1) not in entityList1:
            testResult = "False"
            errorMsg = ('%E1 should be in atomic link cluster of E3, but is not!\n' %errorMsg)
        if str(testEntityID2) not in entityList1:
            testResult = "False"
            errorMsg = ('%E2 should be in atomic link cluster of E3, but is not!\n' %errorMsg)
        if str(testEntityID4) not in entityList1:
            testResult = "False"
            errorMsg = ('%E4 should be in atomic link cluster of E3, but is not!\n' %errorMsg)  
        if str(theSingleton) not in entityList1:
            testResult = "False"
            errorMsg = ('%Examples.MemeA4 should be in atomic link cluster of E3, but is not!\n' %errorMsg) 
        if len(entityList1) != 5: 
            testResult = "False"
            errorMsg = ('%E3 should have 5 members in its atomic link cluster - itself, 3 generics and the singleton - in its atomic link cluster, but it has %s members!\n' %(errorMsg, len(entityList1)))      
    except Exception as e:
        testResult = "False"
        errorMsg = ('Getting atomic cluster of E3!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #From E3, subatomic
    try:
        entityListRaw = api.getCluster(testEntityID3, 1)
        entityClusterJSON2 = api.getClusterJSON(testEntityID3, 1)
        entityList2 = []
        for entityNode in entityListRaw["nodes"]:
            entityList2.append(entityNode['id'])
        if str(testEntityID6) not in entityList2:
            testResult = "False"
            errorMsg = ('%E6 should be in subatomic link cluster of E3, but is not!\n' %errorMsg)  
        if len(entityList2) != 2: 
            testResult = "False"
            errorMsg = ('%E3 should have 2 members in its subatomic link cluster - itself and 1 sibling, but it has %s members!\n' %(errorMsg, len(entityList1)))      
    except Exception as e:
        testResult = "False"
        errorMsg = ('Getting atomic cluster of E3!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #From E5, atomic
    try:
        entityListRaw = api.getCluster(testEntityID5)
        entityClusterJSON3 = api.getClusterJSON(testEntityID5)
        entityList3 = []
        for entityNode in entityListRaw["nodes"]:
            entityList3.append(entityNode['id'])
        if str(theSingleton) not in entityList3:
            testResult = "False"
            errorMsg = ('%Examples.MemeA4 should be in atomic link cluster of E5, but is not!\n' %errorMsg)
        if len(entityList3) != 2: 
            testResult = "False"
            errorMsg = ('%E5 should 2 members in its atomic link cluster, itself and the Examples.MemeA4 singleton, but the cluster has %s members!\n' %(errorMsg, len(entityList1)))      
    except Exception as e:
        testResult = "False"
        errorMsg = ('Getting atomic cluster of E5!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #From E5, subatomic
    try:
        entityListRaw = api.getCluster(testEntityID5, 1)
        entityClusterJSON4 = api.getClusterJSON(testEntityID5, 1)
        entityList4 = []
        for entityNode in entityListRaw["nodes"]:
            entityList4.append(entityNode['id'])
        if len(entityList4) != 1: 
            testResult = "False"
            errorMsg = ('%E5 should be alone in its atomic link cluster, but the cluster has %s members!\n' %(errorMsg, len(entityList1)))      
    except Exception as e:
        testResult = "False"
        errorMsg = ('Getting atomic cluster of E5!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    testcase = "getClusterMembers()"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet




def testPropertyChangeEvent():
    """
        Create an entity from PropertyChangeEvent.PropChangeTest. 
            It starts with:
            propA = 11  ( has an event script.  Returns a hash "<oldVal> <newVal>" )
            propB = xyz ( has an event script.  Returns the entiry UUID)
            propC = abc ( no SES)
        
        1 - Alter its prop A to an allowed value.  Verify the value of the return.
        2 - Alter its prop A a second time (to an allowed value) and verify.
        3 - Alter prop B and check that the returned UUID is correct.
        4 - Alter prop C to a disallowed value.  Verify that return is None
    """
    method = moduleName + '.' + 'testPropertyChangeEvent'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create 5 entities of type Graphyne.Generic and get the Examples.MemeA4 singleton as well.  
    #Chain them together: E1 >> E2 >> E3 >> E4 >> Examples.MemeA4 << E5
    try:
        theEntity = Graph.api.createEntityFromMeme("PropertyChangeEvent.PropChangeTest")
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error creating entities!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #Alter its prop A to an allowed value.  Verify the value of the return.
    try:
        expectedReturnValue = "11 12"
        returnValue = api.setEntityPropertyValue(theEntity, "propA", 12)
        if returnValue != expectedReturnValue: 
            testResult = "False"
            errorMsg = ('%sSetting the value of propA from 11 to 12 should return "%s" in the return value of the property change event.  "%s returned" !\n' %(errorMsg, expectedReturnValue, returnValue))
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error setting value of propA!  Traceback = %s' % (e) )
        errata.append(errorMsg)
      
    #Alter its prop A a second time (to an allowed value) and verify.
    try:
        expectedReturnValue = "12 15"
        returnValue = api.setEntityPropertyValue(theEntity, "propA", 15)
        if returnValue != expectedReturnValue: 
            testResult = "False"
            errorMsg = ('%sSetting the value of propA from 12 to 15 should return "%s" in the return value of the property change event.  "%s returned" !\n' %(errorMsg, expectedReturnValue, returnValue))
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error setting value of propA!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #Alter prop B and check that the returned UUID is correct.
    try:
        returnValue = api.setEntityPropertyValue(theEntity, "propB", 'abc')
        if returnValue != str(theEntity): 
            testResult = "False"
            errorMsg = ('%sSetting the value of propB should return "%s" in the return value of the property change event.  "%s returned" !\n' %(errorMsg, theEntity, returnValue))
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error setting value of propA!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #Alter prop C to a disallowed value.  Verify that return is None
    try:
        returnValue = api.setEntityPropertyValue(theEntity, "propC", 'xyz')
        if returnValue != None: 
            testResult = "False"
            errorMsg = ('%sSetting the value of propB should return "%s" in the return value of the property change event.  "%s returned" !\n' %(errorMsg, None, returnValue))
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error setting value of propA!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    testcase = "propertyChangeEvent()"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet



def testLinkEvent():
    """
        Create two entities from LinkEvent.LinkChangeTest. 
        Greate three generic entities
        
        1 - Link the a LinkEvent.LinkChangeTest entitiy with a generic one, with LinkChangeTest as the source
        2 - Break the link
        3 - Link the two with LinkChangeTest as the target
        
        4 - Link the two generics
        5 - Break the link
        
        Create two generic entities
        
        6 - Link the twoLinkEvent.LinkChangeTest entities
        7 - Break the link
    """
    method = moduleName + '.' + 'testLinkEvent'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create two entities from LinkEvent.LinkChangeTest. 
    #Greate three generic entities
    try:
        linkChangeTest0 = Graph.api.createEntityFromMeme("LinkEvent.LinkChangeTest")
        linkChangeTest1 = Graph.api.createEntityFromMeme("LinkEvent.LinkChangeTest")
        genEntity0 = Graph.api.createEntity()
        genEntity1 = Graph.api.createEntity()
        genEntity2 = Graph.api.createEntity()
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error creating entities!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #1 - Link the a LinkEvent.LinkChangeTest entitiy with a generic one, with LinkChangeTest as the source
    try:
        expectedReturnValue10 = "Added %s as link source for %s" %(linkChangeTest0, genEntity0)
        returnArray = api.addEntityLink(linkChangeTest0, genEntity0)
        if returnArray[0] != expectedReturnValue10: 
            testResult = "False"
            errorMsg = '%sAdding link to LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, expectedReturnValue10, returnArray[0])
        if returnArray[1] is not None: 
            testResult = "False"
            errorMsg = '%sAdding link to LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, None, returnArray[1])
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error adding link!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #2 - Break the link
    try:
        expectedReturnValue20 = "Removed %s as link source for %s" %(linkChangeTest0, genEntity0)
        returnArray = api.removeEntityLink(linkChangeTest0, genEntity0)
        if returnArray[0] != expectedReturnValue20: 
            testResult = "False"
            errorMsg = '%sRemoving link to LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, expectedReturnValue20, returnArray[0])
        if returnArray[1] is not None: 
            testResult = "False"
            errorMsg = '%sRemoving link to LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, None, returnArray[1])
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error removing link!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #3 - Link the two with LinkChangeTest as the target
    try:
        expectedReturnValue30 = "Added %s as link target for %s" %(linkChangeTest0, genEntity0)
        returnArray = api.addEntityLink(genEntity0, linkChangeTest0)
        if returnArray[1] != expectedReturnValue30: 
            testResult = "False"
            errorMsg = '%sAdding link to LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, expectedReturnValue30, returnArray[0])
        if returnArray[0] is not None: 
            testResult = "False"
            errorMsg = '%sAdding link to LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, None, returnArray[1])
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error adding link!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #4 - Link two generics
    try:
        returnArray = api.addEntityLink(genEntity1, genEntity2)
        if returnArray[0] is not None: 
            testResult = "False"
            errorMsg = '%sAdding link to generic entity should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, None, returnArray[0])
        if returnArray[1] is not None: 
            testResult = "False"
            errorMsg = '%sAdding link to generic entity should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, None, returnArray[1])
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error adding link!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
        
    #5 - Break the link
    try:
        returnArray = api.removeEntityLink(genEntity1, genEntity1)
        if returnArray[0] is not None: 
            testResult = "False"
            errorMsg = '%Removing link from generic entity should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, None, returnArray[0])
        if returnArray[1] is not None: 
            testResult = "False"
            errorMsg = '%Removing link from generic entity should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, None, returnArray[1])
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error removing link!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #6 - Link the twoLinkEvent.LinkChangeTest entities
    try:
        expectedReturnValue60 = "Added %s as link source for %s" %(linkChangeTest0, linkChangeTest1)
        expectedReturnValue61 = "Added %s as link target for %s" %(linkChangeTest1, linkChangeTest0)
        returnArray = api.addEntityLink(linkChangeTest0, linkChangeTest1)
        if returnArray[0] != expectedReturnValue60: 
            testResult = "False"
            errorMsg = '%sAdding link to LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, expectedReturnValue60, returnArray[0])
        if returnArray[1] != expectedReturnValue61: 
            testResult = "False"
            errorMsg = '%sAdding link to LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, expectedReturnValue61, returnArray[1])
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error adding link!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    #6 - remove the link
    try:
        expectedReturnValue70 = "Removed %s as link source for %s" %(linkChangeTest0, linkChangeTest1)
        expectedReturnValue71 = "Removed %s as link target for %s" %(linkChangeTest1, linkChangeTest0)
        returnArray = api.removeEntityLink(linkChangeTest0, linkChangeTest1)
        if returnArray[0] != expectedReturnValue70: 
            testResult = "False"
            errorMsg = '%Removing link from LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, expectedReturnValue70, returnArray[0])
        if returnArray[1] != expectedReturnValue71: 
            testResult = "False"
            errorMsg = '%sRemoving link from LinkEvent.LinkChangeTest should return "%s" in the return value [0] of the link added event.  "%s returned" !\n' %(errorMsg, expectedReturnValue71, returnArray[1])
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error removing link!  Traceback = %s' % (e) )
        errata.append(errorMsg)
        
    testcase = "testLinkEvent()"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet



def testBrokenEvents():
    """
        This method tests the SES event handling of broken scripts
        
        The first series of tests (execute) runs with a SES script that:
            1- causes an uncaught KeyError exception
            2- causes the same KeyError exception, but catches and actively raises it (as an exception)
            3 - The SES script class has no execute() method 
            
        The second series of tests (propertyChanged) runs with a SES script that:
            1- causes an uncaught KeyError exception
            2- causes the same KeyError exception, but catches and actively raises it (as an exception)
            
        The third series of tests (linkAdd) runs with a SES script that:
            1- causes an uncaught KeyError exception
            2- causes the same KeyError exception, but catches and actively raises it (as an exception)
            
        The fourth series of tests (linkRemove) runs with a SES script that:
            1- causes an uncaught KeyError exception
            2- causes the same KeyError exception, but catches and actively raises it (as an exception)
         
    """
    method = moduleName + '.' + 'testBrokenEvents'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create two entities from LinkEvent.LinkChangeTest. 
    #Greate three generic entities
    try:
        entity0 = Graph.api.createEntityFromMeme("EventFailure.BrokenLinkChangeTest")
        entity1 = Graph.api.createEntityFromMeme("EventFailure.ThrowsLinkChangeTest")
        entity2 = Graph.api.createEntityFromMeme("EventFailure.MalformedEvent")
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error creating entities!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #execute for all.
    try:
        unusedReturnvalue = api.evaluateEntity(entity0)
        
        #yes, in this testcase, valid tests throw exceptions
        testResult = "False"
        errorMsg = ('Error.  execute event for EventFailure.BrokenLinkChangeTest should raise an Exceptions.ScriptError exception, but did not!')
        errata.append(errorMsg)
    except Exceptions.EventScriptFailure as e:
        pass
    except Exception as e:
        testResult = "False"
        erorMessage = ('Error.  execute event for EventFailure.BrokenLinkChangeTest should raise an Exceptions.ScriptError exception, but did not!')
        fullerror = sys.exc_info()
        errorMsg = str(fullerror[1])
        tb = sys.exc_info()[2]
        erorMessage = "%s  Traceback = %s %s" %(erorMessage, errorMsg, tb)
        errata.append(erorMessage)  
    try:
        unusedReturnvalue = api.evaluateEntity(entity1)
        testResult = "False"
        errorMsg = ('Error.  execute event for EventFailure.ThrowsLinkChangeTest should raise an exception, but did not!')
        errata.append(errorMsg)
    except Exceptions.EventScriptFailure as e:
        pass
    except Exception as e:
        testResult = "False"
        erorMessage = ('Error.  execute event for EventFailure.BrokenLinkChangeTest should raise an Exceptions.ScriptError exception, but did not!')
        fullerror = sys.exc_info()
        errorMsg = str(fullerror[1])
        tb = sys.exc_info()[2]
        erorMessage = "%s  Traceback = %s %s" %(erorMessage, errorMsg, tb)
        errata.append(erorMessage) 
    try:
        unusedReturnvalue = api.evaluateEntity(entity2)
        testResult = "False"
        errorMsg = ('Error.  execute event for EventFailure.MalformedEvent should raise an exception, but did not!')
        errata.append(errorMsg)
    except Exceptions.EventScriptFailure as e:
        pass
    except Exception as e:
        testResult = "False"
        erorMessage = ('Error.  execute event for EventFailure.BrokenLinkChangeTest should raise an Exceptions.ScriptError exception, but did not!')
        fullerror = sys.exc_info()
        errorMsg = str(fullerror[1])
        tb = sys.exc_info()[2]
        erorMessage = "%s  Traceback = %s %s" %(erorMessage, errorMsg, tb)
        errata.append(erorMessage)  

    #propertyChanged.
    try:
        unusedReturnvalue = api.setEntityPropertyValue(entity0, "propB", "abc")
        
        #yes, in this testcase, valid tests throw exceptions
        testResult = "False"
        errorMsg = ('Error.  propertyChanged event for EventFailure.BrokenLinkChangeTest should raise an exception, but did not!')
        errata.append(errorMsg)
    except Exceptions.EventScriptFailure as e:
        pass
    except Exception as e:
        testResult = "False"
        erorMessage = ('Error.  execute event for EventFailure.BrokenLinkChangeTest should raise an Exceptions.ScriptError exception, but did not!')
        fullerror = sys.exc_info()
        errorMsg = str(fullerror[1])
        tb = sys.exc_info()[2]
        erorMessage = "%s  Traceback = %s %s" %(erorMessage, errorMsg, tb)
        errata.append(erorMessage)   
    try:
        unusedReturnvalue = api.setEntityPropertyValue(entity1, "propB", "abc")
        testResult = "False"
        errorMsg = ('Error.  propertyChanged event for EventFailure.ThrowsLinkChangeTest should raise an exception, but did not!')
        errata.append(errorMsg)
    except Exceptions.EventScriptFailure as e:
        pass
    except Exception as e:
        testResult = "False"
        erorMessage = ('Error.  execute event for EventFailure.BrokenLinkChangeTest should raise an Exceptions.ScriptError exception, but did not!')
        fullerror = sys.exc_info()
        errorMsg = str(fullerror[1])
        tb = sys.exc_info()[2]
        erorMessage = "%s  Traceback = %s %s" %(erorMessage, errorMsg, tb)
        errata.append(erorMessage) 

    #linkAdd
    try:
        unusedReturnvalue = api.addEntityLink(entity0, entity1)
        
        #yes, in this testcase, valid tests throw exceptions
        testResult = "False"
        errorMsg = ('Error.  linkAdd event for EventFailure.BrokenLinkChangeTest should raise an exception, but did not!')
        errata.append(errorMsg)
    except Exceptions.EventScriptFailure as e:
        pass
    except Exception as e:
        testResult = "False"
        erorMessage = ('Error.  execute event for EventFailure.BrokenLinkChangeTest should raise an Exceptions.ScriptError exception, but did not!')
        fullerror = sys.exc_info()
        errorMsg = str(fullerror[1])
        tb = sys.exc_info()[2]
        erorMessage = "%s  Traceback = %s %s" %(erorMessage, errorMsg, tb)
        errata.append(erorMessage)  

    #linkRemove
    try:
        unusedReturnvalue = api.removeEntityLink(entity0, entity1)
        
        #yes, in this testcase, valid tests throw exceptions
        testResult = "False"
        errorMsg = ('Error.  linkRemove event for EventFailure.BrokenLinkChangeTest should raise an exception, but did not!')
        errata.append(errorMsg)
    except Exceptions.EventScriptFailure as e:
        pass
    except Exception as e:
        testResult = "False"
        erorMessage = ('Error.  execute event for EventFailure.BrokenLinkChangeTest should raise an Exceptions.ScriptError exception, but did not!')
        fullerror = sys.exc_info()
        errorMsg = str(fullerror[1])
        erorMessage = "%s  Traceback = %s" %(erorMessage, errorMsg)
        tb = sys.exc_info()[2]
        #raise Exceptions.EventScriptFailure(errorMsg).with_traceback(tb)
        errata.append(erorMessage)  
        
    testcase = "testLinkEvent()"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet


def testInitializeEvent():
    """
        Create one entity from EventInitRemove.InitRemoveEventTest. 
        Greate three generic entities
        
        1 - Check that it has an AProp property and its value is 'Hello'
        
        The meme has no proeprties, but the initialize event script adds the AProp property
    """
    method = moduleName + '.' + 'testInitializeEvent'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create two entities from LinkEvent.LinkChangeTest. 
    #Greate three generic entities
    try:
        theEntity = Graph.api.createEntityFromMeme("EventInitRemove.InitRemoveEventTest")
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error creating entity!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #1 - Link the a LinkEvent.LinkChangeTest entitiy with a generic one, with LinkChangeTest as the source
    try:
        retrunValue = api.getEntityPropertyValue(theEntity, "AProp")
        if retrunValue != "Hello": 
            testResult = "False"
            errorMsg = 'The initialize event script, EventInitRemove.OnInitialize, should add a property called AProp to EventInitRemove.InitRemoveEventTest and its value should be "Hello".  It is actually "%s" !\n' %(retrunValue)
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error in initialze event script!  Traceback = %s' % (e) )
        errata.append(errorMsg)

        
    testcase = "testInitializeEvent()"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet


def testRemoveEvent():
    """
        Locate the EventInitRemove.InitRemoveEventTest entity created in testInitializeEvent(). (it should be singular) 
        Delete it
        
        1 - Check that delete script return value is 'Hello World'
        
        The meme has no proeprties, but the initialize event script adds the AProp property
    """
    method = moduleName + '.' + 'testInitializeEvent'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])

    resultSet = []
    errata = []
    testResult = "True"
    expectedResult = "True"
    errorMsg = ""
    
    #Create two entities from LinkEvent.LinkChangeTest. 
    #Greate three generic entities
    try:
        theEntities = Graph.api.getEntitiesByMemeType("EventInitRemove.InitRemoveEventTest")
        if len(theEntities) != 1: 
            testResult = "False"
            errorMsg = 'One EventInitRemove.InitRemoveEventTest entity was created in the graph, during testInitializeEvent().  There can be only one!  There are actually %s ' %(len(theEntities))
        else:
            theEntity = theEntities[0]
    except Exception as e:
        testResult = "False"
        errorMsg = ('Error locating entity!  Traceback = %s' % (e) )
        errata.append(errorMsg)

    #1 - Link the a LinkEvent.LinkChangeTest entitiy with a generic one, with LinkChangeTest as the source
    try:
        destroyReturn = api.destroyEntity(theEntity)
        if destroyReturn != "Hello World": 
            testResult = "False"
            errorMsg = 'The terminate event script, EventInitRemove.OnDelete, should return "Hello World".  It actually returned "%s" !\n' %(destroyReturn)

    except Exception as e:
        testResult = "False"
        errorMsg = ('Error in terminate event script!  Traceback = %s' % (e) )
        errata.append(errorMsg)

        
    testcase = "testRemoveEvent()"
    
    results = [1, testcase, testResult, expectedResult, errata]
    resultSet.append(results)
    
    Graph.logQ.put( [logType , logLevel.INFO , method , "Finished testcase %s" %(1)])
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return resultSet
   


######################
#End Test Block
#####################


def getResultPercentage(resultSet):
    #results = [n, testcase, allTrueResult, expectedResult, errata]
    totalTests = len(resultSet)
    if totalTests == 0:
        return 0
    else:
        partialResult = 0
        if totalTests > 0:
            for test in resultSet:
                try:
                    if test[2].upper() == test[3].upper():
                        partialResult = partialResult + 1
                except Exception as e:
                    print(e)
        pp = partialResult/totalTests
        resultPercentage = pp * 100
        return int(resultPercentage)


def publishResults(testReports, css, fileName, titleText):
    #testReport = {"resultSet" : resultSet, "validationTime" : validationTime, "persistence" : persistence.__name__} 
    #resultSet = [u"Condition (Remote Child)", copy.deepcopy(testSetData), testSetPercentage])

    "Every report repeats exactly the same result sets, so we need only count onece"
    testCaseCount = 0
    exampleTestReport = testReports[0]
    exampleResultSet = exampleTestReport["resultSet"]
    for testScenario in exampleResultSet:
        testCaseCount = testCaseCount + len(testScenario[2])
        
    #Totals for time and number of test cases
    numReports = len(testReports)
    totalTCCount = testCaseCount * numReports
    totalTCTime = 0.0
    for countedTestReport in testReports:
        totalTCTime = totalTCTime + countedTestReport["validationTime"] 
        
    # Create the minidom document
    doc = minidom.Document()
    
    # Create the <html> base element
    html = doc.createElement("html")
        
    # Create the <head> element
    head = doc.createElement("head")
    style = doc.createElement("style")
    defaultCSS = doc.createTextNode(css)
    style.appendChild(defaultCSS)
    title = doc.createElement("title")
    titleTextNode = doc.createTextNode(titleText)
    title.appendChild(titleTextNode)
    head.appendChild(style)
    head.appendChild(title)
        
    body = doc.createElement("body")
    h1 = doc.createElement("h1")
    h1Text = doc.createTextNode(titleText)
    h1.appendChild(h1Text)
    body.appendChild(h1)
    h2 = doc.createElement("h2")
    h2Text = doc.createTextNode("%s regression tests over %s persistence types in in %.1f seconds:  %s" %(totalTCCount, numReports, totalTCTime, ctime()))
    h2.appendChild(h2Text)
    body.appendChild(h2)
    h3 = doc.createElement("h2")
    h3Text = doc.createTextNode("Entity Count at start of tests:  %s" %(exampleTestReport["entityCount"]))
    h3.appendChild(h3Text)
    body.appendChild(h3)
    
    
    """
        The Master table wraps all the result sets.
        masterTableHeader contains all of the overview blocks
        masterTableBody contains all of the detail elements
    """  
    masterTable = doc.createElement("table")
    masterTableHeader = doc.createElement("table")
    masterTableBody = doc.createElement("table")
    
    for testReport in testReports:
        masterTableHeaderRow = doc.createElement("tr")
        masterTableBodyRow = doc.createElement("tr")
        
        localValTime = testReport["validationTime"]
        localPersistenceName = testReport["persistence"]
        resultSet = testReport["resultSet"]
        profileName = testReport["profileName"]
    
        #Module Overview
        numberOfColumns = 1
        numberOfModules = len(resultSet)
        if numberOfModules > 6:
            numberOfColumns = 2
        if numberOfModules > 12:
            numberOfColumns = 3
        if numberOfModules > 18:
            numberOfColumns = 4
        if numberOfModules > 24:
            numberOfColumns = 5
        rowsPerColumn = numberOfModules//numberOfColumns + 1
    
        listPosition = 0
        icTable = doc.createElement("table")
        
        icTableHead= doc.createElement("thead")
        icTableHeadText = doc.createTextNode("%s, %s: %.1f seconds" %(profileName, localPersistenceName, localValTime) )
        icTableHead.appendChild(icTableHeadText)
        icTableHead.setAttribute("class", "tableheader")
        icTable.appendChild(icTableHead)
        
        icTableFoot= doc.createElement("tfoot")
        icTableFootText = doc.createTextNode("Problem test case sets are detailed in tables below" )
        icTableFoot.appendChild(icTableFootText)
        icTable.appendChild(icTableFoot)
        
        icTableRow = doc.createElement("tr")
        
        for unusedI in range(0, numberOfColumns):
            bigCell = doc.createElement("td")
            nestedTable = doc.createElement("table")
            
            #Header
            headers = ["", "Tests", "Valid"]
            nestedTableHeaderRow = doc.createElement("tr")
            for headerElement in headers:
                nestedCell = doc.createElement("th")
                nestedCellText = doc.createTextNode("%s" %headerElement)
                nestedCell.appendChild(nestedCellText)
                nestedTableHeaderRow.appendChild(nestedCell)
                #nestedTableHeaderRow.setAttribute("class", "tableHeaderRow")
                nestedTable.appendChild(nestedTableHeaderRow)  
                      
            for dummyJ in range(0, rowsPerColumn):
                currPos = listPosition
                listPosition = listPosition + 1
                if listPosition <= numberOfModules:
                    try:
                        moduleReport = resultSet[currPos]
                        
                        #Write Data Row To Table
                        row = doc.createElement("tr")
                        
                        #Module Name is first cell
                        cell = doc.createElement("td")
                        cellText = doc.createTextNode("%s" %moduleReport[0])
                        hyperlinkNode = doc.createElement("a")
                        hyperlinkNode.setAttribute("href", "#%s%s" %(moduleReport[0], localPersistenceName)) 
                        hyperlinkNode.appendChild(cellText)
                        cell.appendChild(hyperlinkNode)
                        if moduleReport[1] < 100:
                            row.setAttribute("class", "badOverviewRow")
                        else:
                            row.setAttribute("class", "goodOverviewRow")                   
                        row.appendChild(cell) 
    
                        rowData = [len(moduleReport[2]), "%s %%" %moduleReport[1]]
                        for dataEntry in rowData:
                            percentCell = doc.createElement("td")
                            percentCellText = doc.createTextNode("%s" %dataEntry)
                            percentCell.appendChild(percentCellText)
                            row.appendChild(percentCell)
                        nestedTable.appendChild(row)
                    except:
                        pass
                else:
                    row = doc.createElement("tr")
                    cell = doc.createElement("td")
                    cellText = doc.createTextNode("")
                    cell.appendChild(cellText)
                    row.appendChild(cellText)
                    nestedTable.appendChild(row)
            nestedTable.setAttribute("class", "subdivision")
            bigCell.appendChild(nestedTable) 
            
            icTableRow.appendChild(bigCell)
            icTableDiv = doc.createElement("div")
            icTableDiv.setAttribute("class", "vAlignment")
            icTableDiv.appendChild(icTableRow) 
            icTable.appendChild(icTableDiv)
            
        #Add some blank spave before icTable
        frontSpacer = doc.createElement("div")
        frontSpacer.setAttribute("class", "vBlankSpace")
        frontSpacer.appendChild(icTable)
        
        masterTableDiv = doc.createElement("div")
        masterTableDiv.setAttribute("class", "vAlignment")
        masterTableDiv.appendChild(frontSpacer) 
        masterTableHeaderRow.appendChild(masterTableDiv)
        masterTableHeader.appendChild(masterTableHeaderRow)
                
            
        #Individual Data Sets
        for testSet in resultSet:
            
            #first, build up the "outer" table header, which has the header
            idHash = "%s%s" %(testSet[0], localPersistenceName)
            oTable = doc.createElement("table")
            oTable.setAttribute("style", "border-style:solid")
            tableHeader= doc.createElement("thead")
            tableHeaderText = doc.createTextNode("%s (%s)" %(testSet[0], localPersistenceName) )
            tableAnchor = doc.createElement("a")
            tableAnchor.setAttribute("id", idHash)
            tableAnchor.appendChild(tableHeaderText)
            tableHeader.appendChild(tableAnchor)
            tableHeader.setAttribute("class", "tableheader")
            oTable.appendChild(tableHeader)
            oTableRow = doc.createElement("tr")
            oTableContainer = doc.createElement("td")
    
            #Inner Table         
            table = doc.createElement("table")
            headers = ["#", "Test Case", "Result", "Expected Result", "Notes"]
            tableHeaderRow = doc.createElement("tr")
            for headerEntry in headers:
                cell = doc.createElement("th")
                cellText = doc.createTextNode("%s" %headerEntry)
                cell.appendChild(cellText)
                cell.setAttribute("class", "tableHeaderRow")
                tableHeaderRow.appendChild(cell)
            table.appendChild(tableHeaderRow)
            
            for fullTestRow in testSet[2]:
                #fullTestRow = [n, testcase, allTrueResult, expectedResult, errata]
                test = [fullTestRow[0], fullTestRow[1], fullTestRow[2], fullTestRow[3]]
                tableRow = doc.createElement("tr")
                for dataEntry in test:
                    cell = doc.createElement("td")
                    cellText = doc.createTextNode("%s" %dataEntry)
                    cell.appendChild(cellText)
                    cell.setAttribute("class", "detailsCell")
                    tableRow.appendChild(cell)
                    try:
                        if test[2].upper() != test[3].upper():
                            #then mark the whole row as red
                            tableRow.setAttribute("class", "badDRow")
                        else:
                            tableRow.setAttribute("class", "goodDRow")
                    except:
                        cell = doc.createElement("td")
                        cellText = doc.createTextNode("Please check Testcase code: actual test result = %s, expected = %s" %(test[2], test[3]))
                        cell.appendChild(cellText)
                        cell.setAttribute("class", "detailsCell")
                        tableRow.appendChild(cell) 
                        tableRow.setAttribute("class", "badDRow")                   
    
                errataCell = doc.createElement("td")
                if type(fullTestRow[4]) == type([]):
                    filteredErrata = Graph.filterListDuplicates(fullTestRow[4])
                    for bulletpointElement in filteredErrata:
                        
                        paragraph = doc.createElement("p")
                        pText = doc.createTextNode("%s" %bulletpointElement)
                        paragraph.appendChild(pText)
                        errataCell.appendChild(paragraph)
                        tableRow.appendChild(cell)
                else:
                    filteredErrata = Graph.filterListDuplicates(fullTestRow[4])
                    paragraph = doc.createElement("p")
                    pText = doc.createTextNode("%s" %filteredErrata)
                    paragraph.appendChild(pText)
                    #rowValidityCell.appendChild(paragraph)
                    errataCell.appendChild(paragraph)
                tableRow.appendChild(errataCell)
                table.appendChild(tableRow)
            oTableContainer.appendChild(table)
            oTableRow.appendChild(oTableContainer)
            oTable.appendChild(oTableRow)
            
            #Add some blank spave before any tables
            tableSpacer = doc.createElement("div")
            tableSpacer.setAttribute("class", "vBlankSpace")
            tableSpacer.appendChild(oTable)
            
            masterTableDivL = doc.createElement("div")
            masterTableDivL.setAttribute("class", "vAlignment")
            masterTableDivL.appendChild(tableSpacer) 
            masterTableBodyRow.appendChild(masterTableDivL)
            masterTableBody.appendChild(masterTableBodyRow)

    masterTable.appendChild(masterTableHeader)
    masterTable.appendChild(masterTableBody)
    body.appendChild(masterTable)
    html.appendChild(head)
    html.appendChild(body)
    doc.appendChild(html)
        
    fileStream = doc.toprettyxml(indent = "    ")
    logRoot =  expanduser("~")
    logDir = os.path.join(logRoot, "Graphyne")
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    resultFileLoc = os.path.join(logDir, fileName)
    fileObject = open(resultFileLoc, "w", encoding="utf-8")
    #fileObject.write(Fileutils.smart_str(fileStream))
    fileObject.write(fileStream)
    fileObject.close()
        


def usage():
    print(__doc__)

    
def runTests(css):
    global testImplicit
    method = moduleName + '.' + 'main'
    Graph.logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    
    #Make sure that we have a script facade available
    global api
    api = Graph.api.getAPI()
    
    # A line to prevent pydev from complaining about unused variables
    dummyIgnoreThis = str(api)
    
    # a helper item for debugging whther or not a particular entity is in the repo
    debugHelperIDs = api.getAllEntities()
    for debugHelperID in debugHelperIDs:
        try:
            debugHelperMemeType = api.getEntityMemeType(debugHelperID)
            entityList.append([str(debugHelperID), debugHelperMemeType])
        except Exception as unusedE:
            #This exception is normally left as a pass.  If you need to debug the preceeding code, then uncomment the block below.
            #  The exception is called 'unusedE', so that Pydev will ignore the unused variable
            
            #errorMessage = "debugHelperMemeType warning in Smoketest.Runtests.  Traceback = %s" %unusedE
            #Graph.logQ.put( [logType , logLevel.WARNING , method , errorMessage])
            pass

    #test
    resultSet = []

    print("Meta Meme Properties")
    testSetData = testMetaMemeProperty()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Meta Meme Properties", testSetPercentage, copy.deepcopy(testSetData)])
    
    print("Meta Meme Singleton")
    testSetData = testMetaMemeSingleton()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Meta Meme Singleton", testSetPercentage, copy.deepcopy(testSetData)])
    
    print("Meta Meme Switch")
    testSetData = testMetaMemeSwitch()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Meta Meme Switch", testSetPercentage, copy.deepcopy(testSetData)])

    print("Meta Meme Enhancements")
    testSetData = testMetaMemeEnhancements()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Meta Meme Enhancements", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testMemeValidity()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Meme Validity", testSetPercentage, copy.deepcopy(testSetData)])

    testSetData = testEntityPhase1()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 1", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testEntityPhase1_1()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 1.1", testSetPercentage, copy.deepcopy(testSetData)])

    testSetData = testEntityPhase2()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 2", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testEntityPhase2_1()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 2.1", testSetPercentage, copy.deepcopy(testSetData)])

    testSetData = testEntityPhase3()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 3", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testEntityPhase3_1()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 3.1", testSetPercentage, copy.deepcopy(testSetData)])

    testSetData = testEntityPhase4()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 4", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testEntityPhase4_1()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 4.1", testSetPercentage, copy.deepcopy(testSetData)])

    testSetData = testEntityPhase1('testEntityPhase5', 'Entity_Phase5.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 5", testSetPercentage, copy.deepcopy(testSetData)])

    testSetData = testEntityPhase1_1('testEntityPhase5.1', 'Entity_Phase5.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 5.1", testSetPercentage, copy.deepcopy(testSetData)])

    testSetData = testEntityPhase6()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 6", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testEntityPhase6_1()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 6.1", testSetPercentage, copy.deepcopy(testSetData)])

    testSetData = testEntityPhase7()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 7", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testLinkCounterpartsByMetaMemeType()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 7.1", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testEntityPhase2('testEntityPhase8', 'Entity_Phase8.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 8", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testEntityPhase2_1('testEntityPhase8_1', 'Entity_Phase8.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 8.1", testSetPercentage, copy.deepcopy(testSetData)])
        
    testSetData = testEntityPhase9()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 9", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testEntityPhase10()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 10", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Repeats 7, but with directional references
    testSetData = testEntityPhase7('testEntityPhase11', "Entity_Phase11.atest")
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Phase 11", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Repeats 7, but with directionasl references filters
    testSetData = testTraverseParams()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Traverse Params", testSetPercentage, copy.deepcopy(testSetData)])
    
    #NumericValue.atest
    testSetData = testNumericValue('NumericValue.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["NumericValue", testSetPercentage, copy.deepcopy(testSetData)])
    
    if (testImplicit == True):
        print("Implicit Memes")
        testSetData = testImplicitMeme()
        testSetPercentage = getResultPercentage(testSetData)
        resultSet.append(["Implicit Meme", testSetPercentage, copy.deepcopy(testSetData)])
    else:
        print("No Persistence:  Skipping Implicit Memes")
    
    print("Conditions")
    testSetData = testCondition('ConditionSimple.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Condition (Simple)", testSetPercentage, copy.deepcopy(testSetData)])
    
    #ConditionSet.atest
    testSetData = testCondition('ConditionSet.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Condition (Set)", testSetPercentage, copy.deepcopy(testSetData)])
    
    # Script Conditions
    testSetData = testCondition('ConditionScript.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Condition (Script)", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Child conditions in remote packages
    testSetData = testCondition('ConditionRemotePackage.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Condition (Remote Child)", testSetPercentage, copy.deepcopy(testSetData)])
    
    #String and Numeric Conditions with Agent Attributes
    testSetData = testAACondition('ConditionAA.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Condition (Agent Attributes)", testSetPercentage, copy.deepcopy(testSetData)])
    
    #String and Numeric Conditions with Multi Agent Attributes
    testSetData = testAACondition('ConditionMAA.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Condition (Multi Agent Attributes)", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Creating source metamemes via the script facade
    testSetData = testSourceCreateMeme('SourceCreateMeme.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Editor Meme Creation", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Set a source meme property via the script facade
    testSetData = testSourceProperty('SourceProperty.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Editor Meme Property Set", testSetPercentage, copy.deepcopy(testSetData)])

    #Delete a source meme property via the script facade
    testSetData = testSourcePropertyRemove('SourceProperty.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Editor Meme Property Remove", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Add a member meme via the script facade
    testSetData = testSourceMember('SourceMember.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Editor Member Meme Add", testSetPercentage, copy.deepcopy(testSetData)])

    #Remove a member meme via the script facade
    testSetData = testSourceMemberRemove('SourceMember.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Editor Member Meme Remove", testSetPercentage, copy.deepcopy(testSetData)])

    #Add an enhancement via the script facade
    testSetData = testSourceEnhancement('SourceEnhancement.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Editor Enhancement Add", testSetPercentage, copy.deepcopy(testSetData)])

    #Remove an enhancement via the script facade
    testSetData = testSourceEnhancementRemove('SourceEnhancement.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Editor Enhancement Remove", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Set the singleton flag via the script facade
    testSetData = testSourceSingletonSet('SourceCreateMeme.atest')
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Editor Singleton Setting", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Create a Generic entity and check to see that it's meme is Graphyne.Generic
    testSetData = testGeneric()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Generic Entity", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Test Entity Deletion
    testSetData = testDeleteEntity()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Entity Deletion", testSetPercentage, copy.deepcopy(testSetData)])
    
    #Atomic and subatomic links
    testSetData = testSubatomicLinks()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Subatomic Links", testSetPercentage, copy.deepcopy(testSetData)])
    
    #getting the cluster member list
    testSetData = testGetClusterMembers()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Cluster Member List", testSetPercentage, copy.deepcopy(testSetData)])
    
    testSetData = testGetHasCounterpartsByType()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Has Counterparts by Type", testSetPercentage, copy.deepcopy(testSetData)])   
    
    testSetData = testGetEntityMetaMemeType()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["API method testGetEntityMetaMemeType", testSetPercentage, copy.deepcopy(testSetData)])    
      
    testSetData = testInstallExecutor()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["API method testInstallExecutor", testSetPercentage, copy.deepcopy(testSetData)])  

    #getting the cluster dictionary
    testSetData = testGetCluster()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Cluster", testSetPercentage, copy.deepcopy(testSetData)])
    
    #testRevertEntity
    testSetData = testRevertEntity()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["API Method revertEntity", testSetPercentage, copy.deepcopy(testSetData)])
    
    #testPropertyChangeEvent
    testSetData = testPropertyChangeEvent()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Property Change Event", testSetPercentage, copy.deepcopy(testSetData)])
    
    #testLinkEvent
    testSetData = testLinkEvent()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Link Event", testSetPercentage, copy.deepcopy(testSetData)])
    
    #testBrokenEvents
    testSetData = testBrokenEvents()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Broken Event", testSetPercentage, copy.deepcopy(testSetData)])
    
    #testLinkEvent
    testSetData = testInitializeEvent()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Initialize Event", testSetPercentage, copy.deepcopy(testSetData)])
    
    #testBrokenEvents
    testSetData = testRemoveEvent()
    testSetPercentage = getResultPercentage(testSetData)
    resultSet.append(["Remove Event", testSetPercentage, copy.deepcopy(testSetData)])

    #endTime = time.time()
    #validationTime = endTime - startTime     
    #publishResults(resultSet, validationTime, css)
    return resultSet
    #Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    



def smokeTestSet(persistence, lLevel, css, profileName, persistenceArg = None, persistenceType = None, resetDatabase = False, createTestDatabase = False, scaleFactor = 0):
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
        
    scaleFactor = Scale factor (S).  Given N non-singleton memes, N*S "ballast" entities will be created in the DB before starting the test suite.  This allows us
        to use larger datasets to test scalability (at least with regards to entity repository size)
        
        *If persistenceType is None (no persistence, then this is ignored and won't throw any InconsistentPersistenceArchitecture exceptions)
    '''
    global testImplicit
    print(("\nStarting Graphyne Smoke Test: %s") %(persistence.__name__))
    print(("...%s: Engine Start") %(persistence.__name__))
    
    #Only test implicit memes in the case that we are using persistence
    if persistenceType is None:
        testImplicit = False
        
    #Don't validate the repo when we are performance testing
    if scaleFactor < 1:
        validateOnLoad = True
    else:
        validateOnLoad = False
    
    time.sleep(10.0)

    installFilePath = os.path.dirname(__file__)
    testRepo = os.path.join(installFilePath, "Config", "Test", "TestRepository")
    #mainAngRepo = os.path.join(os.environ['ANGELA_HOME'], "RMLRepository") 
    try:
        Graph.startLogger(lLevel)
        Graph.startDB([testRepo], persistenceType, persistenceArg, True, resetDatabase, True, validateOnLoad)
    except Exception as e:
        print(("Graph not started.  Traceback = %s" %e))
        raise e 
    print(("...Engine Started: %s") %persistence.__name__)
    
    time.sleep(30.0)
    print(("...%s: Engine Started") %(persistence.__name__))
    
    #If scaleFactor > 0, then we are also testing performance
    if (scaleFactor > 0):
        print("Performance Test: ...Creating Content")
        for unusedj in range(1, scaleFactor):
            for moduleID in Graph.templateRepository.modules.keys():
                if moduleID != "BrokenExamples":
                    #The module BrokenExamples contaons mmemes that are deliberately malformed.  Don't beother with these
                    module = Graph.templateRepository.modules[moduleID]
                    for listing in module:
                        template = Graph.templateRepository.resolveTemplateAbsolutely(listing[1])
                        if template.className == "Meme":
                            if template.isSingleton != True:
                                try:
                                    unusedEntityID = Graph.api.createEntityFromMeme(template.path.fullTemplatePath)
                                except Exception as e:
                                    pass
        print("Performance Test: Finished Creating Content")
    # /Scale Factor'
    
    entityCount = Graph.countEntities()

    
    startTime = time.time()
    try:
        resultSet = runTests(css)   
    except Exception as e:
        print(("test run problem.  Traceback = %s" %e))
        raise e 
    endTime = time.time()
    validationTime = endTime - startTime
    testReport = {"resultSet" : resultSet, "validationTime" : validationTime, "persistence" : persistence.__name__, "profileName" : profileName, "entityCount" : entityCount}     
    #publishResults(resultSet, validationTime, css)
    
    print(("...%s: Test run finished.  Waiting 30 seconds for log thread to catch up before starting shutdown") %(persistence.__name__))
    time.sleep(30.0)
    
    print(("...%s: Engine Stop (%s)") %(persistence.__name__, profileName)) 
    Graph.stopLogger()
    print(("...%s: Engine Stopped (%s)") %(persistence.__name__, profileName))   
    return testReport 

  
    
if __name__ == "__main__":
    print("\nStarting Graphyne Smoke Test")
    parser = argparse.ArgumentParser(description="Graphyne Smoke Test")
    parser.add_argument("-l", "--logl", type=str, help="|String| Graphyne's log level during the validation run.  \n    Options are (in increasing order of verbosity) 'warning', 'info' and 'debug'.  \n    Default is 'warning'")
    parser.add_argument("-r", "--resetdb", type=str, help="|String| Reset the esisting persistence DB  This defaults to true and is only ever relevant when Graphyne is using relational database persistence.")
    parser.add_argument("-d", "--dbtype", type=str, help="|String| The database type to be used.  If --dbtype is a relational database, it will also determine which flavor of SQL syntax to use.\n    Possible options are 'none', 'sqlite', 'mssql' and 'hana'.  \n    Default is 'none'")
    parser.add_argument("-c", "--dbtcon", type=str, help="|String| The database connection string (if a relational DB) or filename (if SQLite).\n    'none' - no persistence.  This is the default value\n    'memory' - Use SQLite in in-memory mode (connection = ':memory:')  None persistence defaults to memory id SQlite is used\n    '<valid filename>' - Use SQLite, with that file as the database\n    <filename with .sqlite as extension, but no file> - Use SQLite and create that file to use as the DB file\n    <anything else> - Presume that it is a pyodbc connection string")
    args = parser.parse_args()
    
    
    lLevel = Graph.logLevel.WARNING
    if args.logl:
        if args.logl == "info":
            lLevel = Graph.logLevel.INFO
            print("\n  -- log level = 'info'")
        elif args.logl == "debug":
            lLevel = Graph.logLevel.DEBUG
            print("\n  -- log level = 'debug'")
        elif args.logl == "warning":
            pass
        else:
            print("Invalid log level %s!  Permitted valies of --logl are 'warning', 'info' and 'debug'!" %args.logl)
            sys.exit()
    
    persistenceType = None
    if args.dbtype:
        if (args.dbtype is None) or (args.dbtype == 'none'):
            pass
        elif (args.dbtype == 'sqlite') or (args.dbtype == 'mssql') or (args.dbtype == 'hana'):
            persistenceType = args.dbtype
            print("\n  -- using persistence type %s" %args.dbtype)
        else:
            print("Invalid persistence type %s!  Permitted valies of --dbtype are 'none', 'sqlite', 'mssql' and 'hana'!" %args.logl)
            sys.exit()
            
    dbConnectionString = None
    if args.dbtcon:
        if (args.dbtcon is None) or (args.dbtcon == 'none'):
            if persistenceType is None:
                print("\n  -- Using in-memory persistence (no connection required)")
            elif persistenceType == 'sqlite':
                dbConnectionString = 'memory'
                print("\n  -- Using sqlite persistence with connection = :memory:")
            else:
                print("\n  -- Persistence type %s requires a valid database connection.  Please provide a --dbtcon argument!" %persistenceType)
                sys.exit()
        elif args.dbtcon == 'memory':
            if persistenceType is None:
                #memory is a valid alternative to none with no persistence
                print("\n  -- Using in-memory persistence (no connection required)")
            elif persistenceType == 'sqlite':
                dbConnectionString = args.dbtcon
                print("\n  -- Using sqlite persistence with connection = :memory:")
            else:
                print("\n  -- Persistence type %s requires a valid database connection.  Please provide a --dbtcon argument!" %persistenceType)
                sys.exit()
        else:
            dbConnectionString = args.dbtcon
            if persistenceType == 'sqlite':
                if dbConnectionString.endswith(".sqlite"):
                    print("\n  -- Using sqlite persistence with file %s" %dbConnectionString)
                else:
                    print("\n  -- Using sqlite persistence with invalid filename %s.  It must end with the .sqlite extension" %dbConnectionString)
                    sys.exit()
            else:
                print("\n  -- Using persistence type %s with connection = %s" %(args.dbtype, args.dbtcon))
    
    resetDatabase = True    
    if args.resetdb:
        if args.logl.lower() == "false":
            resetDatabase = False
    
    print(("   ...params: log level = %s, db driver = %s, connection string = %s" %(lLevel, persistenceType, dbConnectionString)))
    
    testReport = None
    css = Fileutils.defaultCSS()
    try:
        if persistenceType is None:
            from Graphyne.DatabaseDrivers import NonPersistent as persistenceModule1
            testReport = smokeTestSet(persistenceModule1, lLevel, css, "No-Persistence", dbConnectionString, persistenceType, resetDatabase, True)
        elif ((persistenceType == "sqlite") and (dbConnectionString== "memory")):
            from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModule2
            testReport = smokeTestSet(persistenceModule2, lLevel, css, "sqllite", dbConnectionString, persistenceType, resetDatabase, True)
        elif persistenceType == "sqlite":
            from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModule4
            testReport = smokeTestSet(persistenceModule4, lLevel, css, "sqllite", dbConnectionString, persistenceType, resetDatabase)
        else:
            from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModul3
            testReport = smokeTestSet(persistenceModul3, lLevel, css, persistenceType, dbConnectionString, persistenceType, resetDatabase)
    except Exception as e:
            from Graphyne.DatabaseDrivers import RelationalDatabase as persistenceModul32
            testReport = smokeTestSet(persistenceModul32, lLevel, css, persistenceType, dbConnectionString, persistenceType, resetDatabase)

    titleText = "Graphyne Smoke Test Suite - Results"
    publishResults([testReport], css, "GraphyneTestResult.html", titleText)