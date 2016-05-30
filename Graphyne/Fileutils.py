"""
   Fileutils.py: A collection of file utilities for Graphyne
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'


import types
import re
import sys
import os
import zipfile
import codecs
import importlib
from xml.dom import minidom

def ensureDirectory(targetDir):
    '''Endure that targetDir exists, by creating whatever part of the tree is required '''
    firstGoodAncestor = targetDir
    badAncestors = []
    while not os.access(firstGoodAncestor, os.F_OK):
        tempTuple = os.path.split(firstGoodAncestor)
        firstGoodAncestor = tempTuple[0]
        badAncestors.insert(1, tempTuple[1])
        
    for badAncestor in badAncestors:
        targetDir = os.path.join(firstGoodAncestor, badAncestor)
        print(("creating %s" %targetDir))
        os.mkdir(targetDir)
        
    
def getModuleFromResolvedPath(fullModuleName):
    try:
        # 2to3 delta
        #x = __import__(fullModuleName)
        #for fragment in fullModuleName.split('.')[1:]:
        #    x = getattr(x, fragment)
        x = importlib.import_module(fullModuleName)
        return x
    except ImportError:
        fullerror = sys.exc_info()
        errorID = str(fullerror[0])
        errorMsg = str(fullerror[1])
        pathlist = []
        for aDir in sys.path:
            pathlist.append(aDir)
        errorMessage = "Unable to resolve module at path %s.  module not in sys.path [ %s ].  Nested Traceback = %s:%s" %(fullModuleName, pathlist, errorID, errorMsg)
        raise ImportError(errorMessage)
    except Exception as e:
        unused_errorMsg = "unable to resolve module at path %s" %fullModuleName
        #debug
        for aDir in sys.path:
            print(aDir)
        #/debug
        raise e



def listFromFile(listFileName):
    listFile = open ( listFileName )
    returnList = listFile.readlines()
    listFile.close() 		
    return returnList
    
    
def getCodePageFromFile(fileURI):
    return "utf-8"


# A recursive examiner for package subdirectories
def walkDirectory(workingDir, packagePath):
    #Go through the subdirectory and load the files up 
    #method = moduleName + '.' + 'walkDirectory'
    
    if packagePath is None:
        #Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Branch is directly off the root'])
        pass
        
    pathSet = {}  # A dict object containing all modules.  Key = module path.  Data = filedata
    dirList = os.listdir(workingDir)
    #Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Child dirs of package path %s ' % packagePath])
    for dummyDir in dirList:
        #Graph.logQ.put( [logType , logLevel.DEBUG , method , '... %s ' % dummyDir])
        pass
        
    for dirEntity in dirList:
        #Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Examining %s' % dirEntity])
        trimmedfile = re.split('\.', dirEntity)
        if packagePath is not None:
            localPackagePath = packagePath + '.' + trimmedfile[0]
        else:
            localPackagePath = trimmedfile
        
        fileName = os.path.join(workingDir, dirEntity)
        #Graph.logQ.put( [logType , logLevel.DEBUG , method , 'package path = %s' % localPackagePath])
        #Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Examining %s' % fileName])
        #logging.logger.logDebug( method, 'Examining %s' % fileName)
        fileData = {}
        if (os.path.isdir(fileName)) and (re.search( '.', localPackagePath) is None):
            # ensuring that there are no dots in localPackagePath is a workaround to prevent
            #   the engine from choking on repositories that are in versioning repositories, such as svn
            #Graph.logQ.put( [logType , logLevel.DEBUG , method , '%s is a directory' % fileName])
            pathSubSet = walkDirectory(fileName, localPackagePath)
            pathSet.update(pathSubSet)
        elif re.search( '.py', fileName) is not None:
            #Graph.logQ.put( [logType , logLevel.DEBUG , method , '%s is a python file' % fileName])
            pass
        elif re.search( '.xml', fileName) is not None:
            #Graph.logQ.put( [logType , logLevel.DEBUG , method , '%s is an xml file' % fileName])
            codepage = getCodePageFromFile(fileName)
            fileObj = codecs.open( fileName, "r", codepage )
            fileStream = fileObj.read() # Returns a Unicode string from the UTF-8 bytes in the file   
            fileData[fileStream] = codepage
            pathSet[localPackagePath] = fileData
        else:
            #Graph.logQ.put( [logType , logLevel.DEBUG , method , '%s is not a directory, xml or python file and will be ignored' % fileName])
            pass
    #Graph.logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return pathSet


def walkRepository(dataLocation, pathSet, dynamicPackage = None):
    '''
        Walk through the file hierarchy of the Schema Repository given at <dataLocation> and return 
    '''
   
    #Go through the condition repository directory and load the files up
    packageList = os.listdir(dataLocation)
    for package in packageList:
        #Graph.logQ.put( [logType , logLevel.DEBUG , method , 'Examining %s' % package])
        fileName = os.path.join(dataLocation, package)
        fileData = {}
        fileStream = None
        trimmedPackage = re.split('\.', package)
        packagePath = trimmedPackage[0]
        #packages will be zip files.  Free modules wll not be
        try:
            z = zipfile.ZipFile(fileName)
            for currFile in z.namelist():
                trimmedfile = re.split('\.', currFile)
                localPackagePath = packagePath + '.' + trimmedfile[0]
                try:
                    if re.search( '.py', currFile) is not None:
                        pass
                    elif re.search( '.xml', currFile) is not None:
                        codepage = getCodePageFromFile(currFile)
                        fileObj = z.read(currFile)
                        fileStream = str(fileObj, codepage)
                        fileData[fileStream] = codepage
                        pathSet[localPackagePath] = fileData
                    else:
                        pass
                except Exception as e:
                    raise e
        except:
            # if the file is not a zip, then we'll get this exception
            if os.path.isdir(fileName):
                pathSubSet = walkDirectory(fileName, packagePath)
                pathSet.update(pathSubSet)
            elif re.search( '.xml', fileName) is not None:
                codepage = getCodePageFromFile(fileName)
                fileObj = codecs.open( fileName, "r", codepage )
                fileStream = fileObj.read() # Returns a Unicode string from the UTF-8 bytes in the file 
                fileData[fileStream] = codepage
                pathSet[packagePath] = fileData
            else:
                pass
    return pathSet




def defaultCSS():
    ''' A default CSS stylesheet  for formatting HTML generated by Test Utilities'''
    subdivision = "table.subdivision = {border-style:solid}"
    tableheader = "thead.tableheader {font-size:1.35em;font-weight:bolder}"
    badOVCell = "td.badOVCell {background-color:LightPink}"
    goodOVCell = "td.goodOVCell {background-color:LightGreen}"
    tableHeaderRow = "th.tableHeaderRow {text-align:center;padding-right:50px}"
    badDRow = "tr.badDRow {background-color:LightPink;color:black;font-weight:bold;padding-right:50px;padding-left:10px;padding-top:10px;text-align:top}"
    goodDRow = "tr.goodDRow {background-color:white;color:black;padding-right:50px;padding-left:10px;padding-top:10px;text-align:top}"
    badOverviewRow = "tr.badOverviewRow {background-color:LightPink;color:black;font-weight:bold;padding-right:10px;padding-left:10px;padding-top:10px;text-align:top}"
    goodOverviewRow = "tr.goodOverviewRow {background-color:LightGreen;color:black;padding-right:10px;padding-left:10px;padding-top:10px;text-align:top}"
    detailsCell = "td.detailsCell {padding-right:50px;padding-left:10px;padding-top:10px;text-align:top;border-style:solid}}"
    vBlankSpace = "div.vBlankSpace {padding-top:100px}"
    hBlankSpace = "div.hBlankSpace {padding-left:100px}"
    vAlignment = "div.vAlignment {margin-top:10px}"
    
    defaultCSS = "<!--\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n-->" %(subdivision, tableheader, badOVCell, goodOVCell, badDRow, goodDRow, badOverviewRow, goodOverviewRow, tableHeaderRow, detailsCell, vBlankSpace, hBlankSpace, vAlignment)
    return defaultCSS



    
def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Copied from django.utils.encoding to remove a dependency on Django 
        and allow Graphyne to be ported to python 3.0
    
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (type(None), int)):
        return s
    if isinstance(s, Promise):
        return str(s).encode(encoding, errors)
    elif not isinstance(s, str):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print- itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return str(s).encode(encoding, errors)
    elif isinstance(s, str):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s
    
    
class Promise(object):
    """
    Copied from django.utils.encoding to remove a dependency on Django 
        and allow Graphyne to be ported to python 3.0 .  Looks like an interface,
        but smart_str needs it.     
    
    This is just a base class for the proxy class created in
    the closure of the lazy function. It can be used to recognize
    promises in code.
    """
    pass

