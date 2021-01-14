"""
   Graph.py: Core Graph Plumbing for Graphyne.
"""
from ast import Str
from uuid import UUID

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'


from xml.dom import minidom
import uuid
import decimal
import copy
import re
import threading
import sys
import os
import queue
import functools
import platform
import json
import time
from os.path import expanduser

#remote debugger support for pydev
#import pydevd

class GraphyneTemplate(object):
    
    def getTemplateType(self):
        return None    


class EntityPropertyType(object):
    String = 0
    Integer = 1
    Decimal = 2
    Boolean = 3
    List = 4


class EntityActiveState(object):
    ACTIVE = 0
    DEPRICATED = 1
    ALL = 2    
    

class LinkDirectionType(object):
    BIDIRECTIONAL = 0
    OUTBOUND = 1
    INBOUND = 2

class LinkType(object):
    ATOMIC = 0
    SUBATOMIC = 1
    ALIAS = 2 
    
    
class LinkAttributeOperatorType(object):
    EQUAL = 0
    EQUALORGREATER = 1
    EQUALORLESS = 2
    GREATER = 3
    LESS = 4
    NOTEQUAL = 5
    IN = 6
    NOTIN = 7
    
    
class StateEventType(object):
    INIT = 0
    EXECUTE = 1
    TERMINATE = 2
    LINKADDED =3
    LINKREMOVED = 4
    PROPERTYCHANGED = 5
    
    

class StartupState(object):
    def __init__(self):
        self.TEMPLATES_FINISHED_LOADING = 0
        self.ACTIONS_INDEXED = 1
        self.REGISTRAR_READY = 2
        self.AE_READY_TO_SERVE = 3
        
        

class LogLevel(object):
    ''' Java style class to designate constants. ERROR = 0, WARNING = 1, INFO = 2 and ALL = -1.  '''
    def __init__(self):
        self.ERROR = 0
        self.WARNING = 1
        self.ADMIN = 2
        self.INFO = 3
        self.DEBUG = 4 
        
        
class LogType(object):
    ''' Java style class to designate constants. ERROR = 0, WARNING = 1, INFO = 2 and ALL = -1.  '''
    def __init__(self):
        self.ENGINE = 0
        self.CONTENT = 1
        
        
class Queues(object):
        
    def syndicate(self, streamData):
        #syndicate all data to the load queues
        for loadQKey in self.__dict__.keys(): 
            try:
                loadQ = self.__getattribute__(loadQKey)
                loadQ.put(streamData)
            except:
                pass       
            
             

entityPropTypes = EntityPropertyType()
entityActiveStates = EntityActiveState()  
moduleName = 'Graph'
serverLanguage = 'en' 
logTypes =  LogType()
global logType 
global linkTypes
global validateOnLoad
logType = logTypes.ENGINE
logLevel = LogLevel()
linkTypes = LinkType()
validateOnLoad = True
startupState = StartupState()
renderStageStimuli = []
logQ = queue.Queue()
templateQueues = []

global loggingService
loggingService = None


from .DatabaseDrivers import SQLDictionary
from Graphyne import Exceptions
from Graphyne import Condition
from Graphyne import Fileutils
#import PluginFacade



#databases.  The runtime and design persistences may not be the same
global persistenceType
global persistenceDB
global dbConnection
global sqlSyntax
global createTestData
persistenceType = None
persistenceDB = None
dbConnection = None
sqlSyntax = None 
createTestData = False

#Flag indicating to other modules that the Graph has finished initializing the schema into it's repo
readyToServe = False
            
class TemplateRepository(object):
    """ packages - A catalog of the relative paths of a package. 
        Each package is a key.
        Each value is a 2d array
         [0] is relative path (relativeTemplatePath)
         [1] is absolute template path (fullTemplatePath)
        
    modules - A catalog of the templates of a module. 
        Each module is a key.
        Each value is a 2d array
         [0] is relative path (templateName)
         [1] is absolute template path (fullTemplatePath)
         
    templates - A catalog of the templates. 
        Each template path (fullTemplatePath) is a key.
        Each value is an templatePath template""" 
        
    className = "TemplateRepository"    
    
    def __init__(self):
        self.lock = threading.RLock()
        self.packages = {}        
        self.modules = {}
        self.templates = {}
        
        
    # registers an TemplatePath template in the catalog     
    def catalogTemplate(self, templatePath, template):
        #method = moduleName + '.' +  self.className + '.catalogTemplatePaths'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        #occasionally, dodgy templates won't have templates
        try:
            unusedTest = templatePath.fullTemplatePath
        except:
            raise Exceptions.TemplatePathError()

        try:
            #If a template is already cataloged at this path, we can just refresh the fullTemplatePath entry
            assert templatePath.fullTemplatePath in self.templates
        except AssertionError:
            #Packages
            """pathList = [templatePath.relativeTemplatePath, templatePath.fullTemplatePath]
            try:
                templateList = self.packages[templatePath.packagePath]
                templateList.append(pathList)
                self.packages[templatePath.packagePath] = templateList
                #logQ.put( [logType , logLevel.DEBUG , method , 'Added %s to template repository under package %s' % (templatePath.relativeTemplatePath, templatePath.packagePath)])
            except:
                # the package is not registered
                templateList = []
                templateList.append(pathList)
                self.packages[templatePath.packagePath] = templateList
                #logQ.put( [logType , logLevel.DEBUG , method , 'Added %s to template repository under package %s' % (templatePath.relativeTemplatePath, templatePath.packagePath)])
            """    
            #Modules
            pathList = [templatePath.templateName, templatePath.fullTemplatePath]
            try:
                templateList = self.modules[templatePath.modulePath]
                templateList.append(pathList)
                self.modules[templatePath.modulePath] = templateList
                #logQ.put( [logType , logLevel.DEBUG , method , 'Added %s to template repository under module %s' % (templatePath.templateName, templatePath.modulePath)])
            except KeyError:
                # the package is not registered
                templateList = []
                templateList.append(pathList)
                self.modules[templatePath.modulePath] = templateList
                #logQ.put( [logType , logLevel.DEBUG , method , 'Added %s to template repository under module %s' % (templatePath.templateName, templatePath.modulePath)])
            except Exception:
                fullerror = sys.exc_info()
                errorID = str(fullerror[0])
                errorMsg = str(fullerror[1])
                tb = sys.exc_info()[2]
                exceptionMsg = "Unable to catalog template %s, Nested Traceback = %s: %s" %(templatePath.fullTemplatePath, errorID, errorMsg)
                raise ValueError(exceptionMsg).with_traceback(tb)
            
        self.templates[templatePath.fullTemplatePath] = template
        #logQ.put( [logType , logLevel.DEBUG , method , 'Added %s under entry %s to template repository template list' % (template, templatePath.fullTemplatePath)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    def resolveTemplate(self, callingTemplate, calledTemplate, noWarningOnFail = True):
        #method = moduleName + '.' +  self.className + '.resolveTemplate'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        #logQ.put( [logType , logLevel.DEBUG , method , 'Resolving template path of %s as called from %s' % (calledTemplate, callingTemplate.fullTemplatePath)])
        
        resolvedTemplate = None
        resolvedTemplatePath = None
        
        try:
            assert calledTemplate in self.templates
            resolvedTemplatePath = calledTemplate
            resolvedTemplate = self.templates[resolvedTemplatePath]
        except AssertionError:
            try:
    
                # if there is more than one dot, we have three or more segments in the called template
                #    This means that we have an absolute path, with the last two meing module and template name
                # If there is one dot, then we have two segments
                #    This means that we have a relative path to a template in the same package as the calling template
                # If there are no dots, then we have only one segment
                #    This means that we are looking for a template within the same module as the calling template
                
                splitTemplatePath = calledTemplate.rsplit('.')
                dotOccurances = []
                try:
                    if len(splitTemplatePath) > 1:
                        n = 1
                        nMax = len(splitTemplatePath) - 1
                        pathPrefix = str(splitTemplatePath[0])
                        while n < nMax:
                            pathPrefix = pathPrefix + '.' +str(splitTemplatePath[n])
                            n = n+1
                        pathSuffix = str(splitTemplatePath[nMax])
                        dotOccurances.append(pathPrefix)
                        dotOccurances.append(pathSuffix)
                    else:
                        dotOccurances.append(calledTemplate)
                except:
                    self.moduleName = str(splitTemplatePath[0])
                
                if len(dotOccurances) > 1:
                    # fully resolved path
                    #logQ.put( [logType , logLevel.DEBUG , method , '%s is already a fully resolved path.  No transformation needed' % (calledTemplate)])
                    resolvedTemplatePath = calledTemplate
                    '''elif len(dotOccurances) > 1:
                    # relative path
                    # look in the packagepath list (of callingTemplate.packagePath) for the absolute path
                    #logQ.put( [logType , logLevel.DEBUG , method , "%s seems to be relative to %s's package.  Trying to resolve" % (calledTemplate, callingTemplate.fullTemplatePath)])
                    try:
                        pathList = self.modules[callingTemplate.packagePath]
                        for path in pathList:
                            if calledTemplate == path[0]:
                                #logQ.put( [logType , logLevel.DEBUG , method , "Relative Path %s == %s  :: Found %s in %s's path list" % (calledTemplate, path[0], calledTemplate, callingTemplate.packagePath)])
                                resolvedTemplatePath = path[1]
                            else: 
                                #logQ.put( [logType , logLevel.DEBUG , method , "Relative Path %s != %s" % (calledTemplate, path[0])])  
                    except:
                        #This happens if the calling template and called templates are both free modules 
                        #    AND the reference to the called template is fully resolved.
                        resolvedTemplatePath = calledTemplate '''
                                     
                else:
                    # relative path
                    # look in the module path list (of callingTemplate.modulePath) for the absolute path
                    #logQ.put( [logType , logLevel.DEBUG , method , "%s seems to be relative to %s's module.  Trying to resolve" % (calledTemplate, callingTemplate.fullTemplatePath)])
                    pathList = self.modules[callingTemplate.modulePath]
                    for path in pathList:
                        if calledTemplate == path[0]:
                            #logQ.put( [logType , logLevel.DEBUG , method , "Template Name %s == %s  :: Found %s in %s's path list" % (calledTemplate, path[0], calledTemplate, callingTemplate.modulePath)])
                            resolvedTemplatePath = path[1]
                        else:
                            #logQ.put( [logType , logLevel.DEBUG , method , "Template Name %s != %s" % (calledTemplate, path[0])])
                            pass
        
                #logQ.put( [logType , logLevel.DEBUG , method , 'Resolved path of %s == %s' % (calledTemplate, resolvedTemplatePath)])
                try:
                    resolvedTemplate = self.templates[resolvedTemplatePath]
                except Exception:
                    fullerror = sys.exc_info()
                    errorID = str(fullerror[0])
                    errorMsg = str(fullerror[1])
                    tb = sys.exc_info()[2]
                    exception = "Unable to resolve template path %s, Nested Traceback = %s: %s" %(resolvedTemplatePath, errorID, errorMsg)

                    #debug
                    #if resolvedTemplatePath is None:
                        #self.resolveTemplate(callingTemplate, calledTemplate, noWarningOnFail)
                    #/debug
                    '''
                    for path in self.templates:
                        if path == resolvedTemplatePath:
                            #logQ.put( [logType , logLevel.DEBUG , method , "----- %s == %s" % (resolvedTemplatePath, path)])
                            resolvedTemplatePath = path[1]
                        else: 
                            #logQ.put( [logType , logLevel.DEBUG , method , "----- %s != %s" % (resolvedTemplatePath, path)])
                            pass 
                    logQ.put( [logType , logLevel.WARNING , method , exception])
                    logQ.put( [logType , logLevel.DEBUG , method , method + u' with errors!'])
                    '''
                    raise Exceptions.TemplatePathError(exception).with_traceback(tb)
            
            except Exception:
                
                # If noWarningOnFail is set to true, then the calling method considers a None type 
                #    return acceptable and there is no need to clutter up the log files with warnings.
                #    A good example is when seraching for template paths using wildcards
                #failLogLevel = logLevel.WARNING
                #if noWarningOnFail == True:
                #    failLogLevel = logLevel.DEBUG
                    
                #Build up a full java or C# style stacktrace, so that devs can track down errors in script modules within repositories
                fullerror = sys.exc_info()
                errorID = str(fullerror[0])
                errorMsg = str(fullerror[1])
                tb = sys.exc_info()[2]
                exception = "Unable to resolve template path %s, Nested Traceback = %s: %s" %(resolvedTemplatePath,errorID, errorMsg)
                #logQ.put( [logType , logLevel.DEBUG , method , "self.templates == %s" % (self.templates)])
                for path in self.templates:
                    if path == resolvedTemplatePath:
                        #logQ.put( [logType , logLevel.DEBUG , method , "----- %s == %s" % (resolvedTemplatePath, path)])
                        resolvedTemplatePath = path[1]
                    else: 
                        #logQ.put( [logType , logLevel.DEBUG , method , "----- %s != %s" % (resolvedTemplatePath, path)])
                        pass  
                raise Exceptions.TemplatePathError(exception).with_traceback(tb)
                   

        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return resolvedTemplate
    
    
    def resolveTemplatePath(self, callingTemplate, calledTemplate, noWarningOnFail = True):
        """
            resolveTemplate(), but return ONLY the fully resolved template path string
        """
        #method = moduleName + '.' +  self.className + '.resolveTemplatePath'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        try:
            targetTemplate = self.resolveTemplate(callingTemplate, calledTemplate, noWarningOnFail)
            return targetTemplate.path.fullTemplatePath
        except Exceptions.TemplatePathError as e:
            raise e 
        #logQ.put( [logType , logLevel.DEBUG , method , "exitong"])

    
    
    
    def resolveTemplateAbsolutely(self, calledTemplate):
        method = moduleName + '.' +  self.className + '.resolveTemplateAbsolutely'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        #logQ.put( [logType , logLevel.DEBUG , method , 'Resolving template path of %s from absolute reference' % (calledTemplate)])
        
        resolvedTemplate = None
        try:
            resolvedTemplate = self.templates[calledTemplate]
        except Exception:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]

            exception = "Resolved template path %s has no entry in the template repository.  Nested Traceback = %s: %s" %(calledTemplate, errorID, errorMsg)
            #logQ.put( [logType , logLevel.DEBUG , method , "self.templates == %s" % (self.templates)])
            for path in self.templates:
                if path == calledTemplate:
                    #logQ.put( [logType , logLevel.DEBUG , method , "----- %s == %s" % (calledTemplate, path)])
                    calledTemplate = path[1]
                else: 
                    #logQ.put( [logType , logLevel.DEBUG , method , "----- %s != %s" % (calledTemplate, path)])
                    pass  
            logQ.put( [logType , logLevel.WARNING , method , exception])
            #logQ.put( [logType , logLevel.DEBUG , method , method + u' with errors!'])
            raise Exceptions.TemplatePathError(exception).with_traceback(tb)
            

        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return resolvedTemplate    
    

class TemplatePath(object):
    className = "TemplatePath"
    
    def __init__(self, modulePath, templateName, extension = None):
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        #logQ.put( [logType , logLevel.DEBUG , method , 'Building paths for template %s at %s' % (templateName, modulePath)])
        self.packagePath = None          # Path of the package that the template resides in
        self.modulePath = modulePath    # The full path of the module
        self.moduleName = None           # The path of the module relative to it's parent package.  I.E Module Name
        self.templateName = templateName     # The name of the template within it's module
        self.fullTemplatePath = None       # Full path of template
        #self.relativeTemplatePath = None   # path of template relative to ts package
        self.extension = extension          # Used when assigning a path to a data structure within a template, such as properties of metamemes

        uModulePath = str(modulePath) 
        uTemplateName = str(templateName)
        
        #We've been having problems with relative paths when the source template is in a deeper heirarchy than
        #    the target template.  A workaround is to disable relative heirarchies and enforce a strategy of either
        #    giving the template path to another template in the same module, OR enforcing that the full template
        #    path is given.
        splitTemplateName = templateName.rsplit('.')
        if len(splitTemplateName) > 1:
            self.fullTemplatePath = templateName
        else:
            #If the module path has a dot in it, then it is the child of a package
            #  If it has no dot, then it is a free module
            #trailingDot = re.compile('$\.')
            #trimmedModulePath = re.split(trailingDot, modulePath)
            trimmedModulePath = modulePath.rsplit('.')
            #logQ.put( [logType , logLevel.DEBUG , method , 'Template %s has trimmed module path %s' % (templateName, trimmedModulePath)])
            try:
                if len(trimmedModulePath) > 1:
                    n = 1
                    nMax = len(trimmedModulePath) - 1
                    self.packagePath = str(trimmedModulePath[0])
                    while n < nMax:
                        self.packagePath = self.packagePath + '.' +str(trimmedModulePath[n])
                        n = n+1
                    self.moduleName = str(trimmedModulePath[nMax])
                else:
                    self.moduleName = modulePath
            except:
                self.moduleName = str(trimmedModulePath[0])
            self.fullTemplatePath = uModulePath + '.' + uTemplateName
        #self.relativeTemplatePath = self.moduleName + u'.' + templateName
        #logQ.put( [logType , logLevel.DEBUG , method , 'Paths for template %s = %s' % (templateName, self.__dict__)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        

class EnhancementIndex(object):
    ''' All of the template enhancement relationships'''
    className = "EnhancementIndex"
    
    def __init__(self):
        self.enhancementLists = {}


    def addEnhancement(self, enhancingPath, enhancedPath):
        '''  Add an enhancement to the list of enhancements in the catalog '''
        method = moduleName + '.' +  self.className + '.addEnhancement'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        try:
            enhancementList = self.enhancementLists[enhancedPath]
            enhancementList.append(enhancingPath)
            newEnhancementList = filterListDuplicates(enhancementList)
            self.enhancementLists[enhancedPath] = newEnhancementList
        except:
            # key error.  No enhancement yet registered
            enhancementList = [enhancingPath]
            self.enhancementLists[enhancedPath] = enhancementList
        logQ.put( [logType , logLevel.INFO , method , "Template %s is now enhanced by %s." %(enhancedPath, enhancingPath)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
    def removeEnhancement(self, enhancingPath, enhancedPath):
        '''  Remove an enhancement from the list of enhancements in the catalog '''
        method = moduleName + '.' +  self.className + '.removeEnhancement'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        try:
            enhancementList = self.enhancementLists[enhancedPath]
            found = False
            newList = []
            for enhancement in enhancementList:
                if enhancement != enhancingPath:
                    newList.append(enhancement)
                else:
                    found = True
            self.enhancementLists[enhancedPath] = newList
            if found == True:
                logQ.put( [logType , logLevel.INFO , method , "Template %s has had its enhancement from %s severed." %(enhancedPath, enhancingPath)])        
            else:
                logQ.put( [logType , logLevel.INFO , method , "Template %s is not enhanced by %s." %(enhancedPath, enhancingPath)])
        except:
            # key error.  No enhancement yet registered.  Nothing to do.
            logQ.put( [logType , logLevel.INFO , method , "Template %s has no enhancements.  Request to remove %s from its enhancement is moot" %(enhancedPath, enhancingPath)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
    def getEnhancements(self, enhancedPath):
        '''  Add an enhancement to the list of enhancements in the catalog '''
        #method = moduleName + '.' +  self.className + '.getEnhancements'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        returnList = []
        try:
            returnList = self.enhancementLists[enhancedPath]
        except:
            pass
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnList
       



 


#Globals
global templateRepository
global entityRepository
global linkRepository
templateRepository = TemplateRepository()  
sourceTemplateRepository = TemplateRepository()
#entityRepository = EntityRepository()
#linkRepository = LinkRepository()
tempRepository = TemplateRepository() # remporary repo for bootstrapping
enhancementIndex = EnhancementIndex()
linkDirectionTypes = LinkDirectionType()
linkAttributeOperatorTypes = LinkAttributeOperatorType()



class TraverseParameter(object):
    operator = None
    parameter = None
    value = None
    
    def __init__(self, statement):
        
        splitEQ = statement.rpartition("=")
        splitGT = statement.rpartition("<")
        splitLT = statement.rpartition(">")
        splitNE = statement.rpartition("!=")
        splitEL = statement.rpartition(">=")
        splitEG = statement.rpartition("<=")
        splitNI = statement.rpartition("><")
        splitIN = statement.rpartition("<>")
        
        if (len(splitNE[0]) > 0):
            self.operator = linkAttributeOperatorTypes.NOTEQUAL
            self.parameter = splitNE[0].strip()
            self.value = splitNE[2].strip()
        elif (len(splitEL[0]) > 0):
            self.operator = linkAttributeOperatorTypes.EQUALORLESS
            self.parameter = splitEL[0].strip()
            self.value = splitEL[2].strip()
        elif (len(splitEG[0]) > 0):
            self.operator = linkAttributeOperatorTypes.EQUALORGREATER
            self.parameter = splitEG[0].strip()
            self.value = splitEG[2].strip()
        elif (len(splitIN[0]) > 0):
            self.operator = linkAttributeOperatorTypes.IN
            self.parameter = splitIN[0].strip()
            self.value = splitIN[2].strip()
        elif (len(splitNI[0]) > 0):
            self.operator = linkAttributeOperatorTypes.NOTIN
            self.parameter = splitNI[0].strip()
            self.value = splitNI[2].strip()
        elif (len(splitIN[0]) > 0):
            self.operator = linkAttributeOperatorTypes.IN
            self.parameter = splitNI[0].strip()
            self.value = splitNI[2].strip()
        elif (len(splitGT[0]) > 0):
            self.operator = linkAttributeOperatorTypes.GREATER
            self.parameter = splitGT[0].strip()
            self.value = splitGT[2].strip()
        elif (len(splitLT[0]) > 0):
            self.operator = linkAttributeOperatorTypes.LESS
            self.parameter = splitLT[0].strip()
            self.value = splitLT[2].strip()
        elif (len(splitEQ[0]) > 0):
            self.operator = linkAttributeOperatorTypes.EQUAL
            self.parameter = splitEQ[0].strip()
            self.value = splitEQ[2].strip()
        else:
            #If there is no operator, then operator == None. 
            self.operator = None
            self.parameter = statement.strip()
    
    
    



class ImplicitMemeRelationship(object):
    className = "ImplicitMemeMasterData"
    
    def __init__(self, table, childColumn, parentColumn, path, backReferenceColumn = None):
        '''
            Voodoo Alert!
            We are going to make use a hybrid template path to get to the implicit meme.  If there are n hops to traverse from parent to child (and n > 1),
            then the hops from 0 to n-1 will go via the metameme path.  The last hop will be via meme path.  This reflects that facts that:
            
            A) in the metameme definition of the forward reference, we know the metameme of the child, but because the meme definition (in xml) is actually 
            a metameme stub, we don't yet know the corresponding meme as it is defined in the relational database table.  
            
            B) we may also not be in possession of the meme template path needed to traverse from parent to child as the in-between hops may themselves
            be implicit.
            
            This is why the designer is instructed to maintain the full metameme template (traverse) path from the parent to child in the traversePath attribute
            of the BackReference and ForwardReference elements.
        '''
        method = moduleName + '.' +  self.className + '.__init__'
        try:
            partitionSequence = '::'
            splitPath = path.rpartition(partitionSequence)
            self.path = splitPath[0]
            self.endEfectorMetaMeme = splitPath[2]
        except Exception as e:
            logQ.put( [logType , logLevel.WARNING , method , "Failed to parse implicit meme reference path %s for %s reference to %s in implicit meme table %s-  Traceback = %s" %(path, parentColumn, childColumn, table, e)])
            self.path = ''
            self.endEfectorMetaMeme = ''           
        self.parentColumn = parentColumn
        self.childColumn = childColumn
        self.table = table
        self.backReferenceColumn = backReferenceColumn
        


class ImplicitMemeMasterData(object):
    className = "ImplicitMemeMasterData"
    properties = {}
    forwardReferences = [] 
    backReferences = [] 
    primaryKeyColumn = None
    table = None    
    
    def __init__(self, table, primaryKeyColumn):
        self.primaryKeyColumn = primaryKeyColumn
        self.table = table
        self.properties = {}
        self.forwardReferences = [] 
        self.backReferences = [] 
        
    def addForwardReference(self, implicitMemeRelationship):
        self.forwardReferences.append(implicitMemeRelationship)
        
    def addBackReference(self, implicitMemeRelationship):
        self.backReferences.append(implicitMemeRelationship)
        
    def addImplicitProperty(self, propertyID, columnID):
        self.properties[propertyID] = columnID
        
        


class MetaMeme(object):        
    className = "MetaMeme"
    
    def __init__(self, path, isSwitch, extends, enhances, properties, memberMetaMemes, isSingleton = False, isAssemblyRoot = False):
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.path = path
        self.isSwitch = isSwitch
        self.extends = extends
        self.enhances = enhances
        self.aliases = []
        self.properties = properties
        self.memberMetaMemes = memberMetaMemes
        self.isSingleton = isSingleton
        self.isAssemblyRoot = isAssemblyRoot
        self.isImplicit = False
        self.isCloneable = False
        self.implicitMemeMasterData = None
        
        self.memberMetaMemes.update(memberMetaMemes)

        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    def setImplicit(self, implicitMemeMasterData):
        #If implicit memes are not relevant in the no-persistence scenario
        global persistenceType
        if persistenceType != "none":
            self.implicitMemeMasterData = implicitMemeMasterData
            self.isImplicit = True
        
        
    def setCloneable(self, isCloneable = False):
        self.isCloneable = isCloneable
        
    
    
    def getProperty(self, propertyFullName):
        method = moduleName + '.' +  self.className + '.getProperty'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        #logQ.put( [logType , logLevel.DEBUG , method , "Trying to find property %s in Metameme %s" %(propertyFullName, self.path.fullTemplatePath)])
        returnProp = None
        
        #First, split off part after the last dot. 
        uPropName = str(propertyFullName)
        splitName = uPropName.rpartition('.') 
        propertyName = splitName[2]
        
        if splitName[0] != '':
            # The property is in another metameme.  Go fetch it from the repository
            #logQ.put( [logType , logLevel.DEBUG , method , "Property is supposed to be in member Metameme %s.  Trying to resolve" %(splitName[0])])
            memberMMName = splitName[0]
            memeberMMProp = splitName[2]
            try:
                #logQ.put( [logType , logLevel.DEBUG , method , "Continuing search for %s at a lower level.  Trying to retrieve %s from member metameme %s" %(propertyName, memeberMMProp, memberMMName)])
                memberMM = self.getMemberMetaMeme(memberMMName)
                returnProp = memberMM.getProperty(memeberMMProp)
            except Exception as e:
                logQ.put( [logType , logLevel.WARNING , method , "Failed to retrieve property %s from member metameme %s.  Traceback = %s" %(memeberMMProp, memberMMName, e)])
        else:
            #logQ.put( [logType , logLevel.DEBUG , method , "Property is supposed to be in Metameme itself (and not a member metameme).  Trying to resolve"])
            for propertyKey in self.properties.keys():
                templateProperty = self.properties[propertyKey]
                if templateProperty.name == propertyName:
                    #logQ.put( [logType , logLevel.DEBUG , method , "Metameme property %s == %s" %(property.name, splitName[2])])
                    returnProp = templateProperty
                else:
                    #logQ.put( [logType , logLevel.DEBUG , method , "Metameme property %s != %s" %(property.name, splitName[2])])
                    pass

        if returnProp is not None:
            #logQ.put( [logType , logLevel.DEBUG , method , "Metameme %s templateProperty %s found: %s" %(propertyName, propertyName, returnProp.__dict__)])
            pass
        else:
            errorMessage = "Metameme %s property %s not found" %(self.path.fullTemplatePath, propertyName)
            logQ.put( [logType , logLevel.WARNING , method , errorMessage])
            raise Exceptions.MetaMemePropertyNotDefinedError(errorMessage)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnProp

    
    
    def getMemberMetaMeme(self, memberMMName):
        """ siphon off the leftmost template path in a chained path and resolve it.
            If the leftmost one is the only one, then resolve that path to a template and return it.
            If it does not, call the template's getMemberMetaMeme() method.  """
        method = moduleName + '.' +  self.className + '.getMemberMetaMeme'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        returnMM = None
        partitionSequence = '::'
        splitMetaMemePath = []
        try:
            splitMetaMemePath = memberMMName.partition(partitionSequence)
            childMM = templateRepository.resolveTemplate(self.path, splitMetaMemePath[0])
        
            #First things first.  Make sure that our membership path has not veered off course 
            #    and that childMM is a valid member metameme of self.
            try:
                assert childMM.path.fullTemplatePath in self.memberMetaMemes
                if splitMetaMemePath[2] != '':
                    #we have not reached the end of the membership path yet.  Continue to march.
                    #logQ.put( [logType , logLevel.DEBUG , method , "%s is an antecedent of the desired member metameme.  Following the remainder of the membership path %s" %(childMM.path.fullTemplatePath, splitMetaMemePath[2])])
                    returnMM = childMM.getMemberMetaMeme(splitMetaMemePath[2])
                else:
                    #single path, meaning that the member mm is the last stop in the membership path.  Our journey is over
                    #logQ.put( [logType , logLevel.DEBUG , method , "%s is desired metameme." %(childMM.path.fullTemplatePath)])
                    returnMM = childMM
            except AssertionError:
                errorMsg = "Can't retrieve member metameme %s from metameme %s as it is not registered as a member." %(childMM.path.fullTemplatePath, self.path.fullTemplatePath)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            except Exception as e:
                errorMsg = "Failed to retrieve member metameme %s from metameme %s.  Traceback = %s" %(childMM.path.fullTemplatePath, self.path.fullTemplatePath, e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
        except Exceptions.TemplatePathError as e:
            logQ.put( [logType , logLevel.ERROR , method , "Unbable to resolve ember metameme %s.  Traceback = %s" %(childMM.path.fullTemplatePath, e)])
        except Exception as e:
            logQ.put( [logType , logLevel.ERROR , method , "Unable to partition member metameme path into current and child node segments.  Traceback = %s" %(e)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnMM


    def mergeExtensions(self):
        ''' merge everything that this metameme extends.
        Note!  This is an expensive method, but I currently have neither the time, nor the mathematical skills to
        create an elegant and lightweight alternative to crawling the remo n^2 times and  repeatedly duplicating merges.
        Patches are welcome!'''
        
        method = moduleName + '.' +  self.className + '.extend'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        #First, collect all ancestors into a list
        extendUs = self.collectAncestors()
        
        for mergeMe in extendUs:
            try:
                self.merge(mergeMe)
            except Exception as e:
                errorMsg = "Metameme %s can't extend %s, %s" %(self.path.fullTemplatePath, mergeMe, e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
                    
        
    def merge(self, toBeMergedPath):
        ''' merged toBeMerged into self '''
        method = moduleName + '.' +  self.className + '.merge'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        toBeMerged = None
        
        try:
            toBeMerged = tempRepository.resolveTemplate(self.path, toBeMergedPath)
        except Exception as e:
            errorMsg = "Problem resolving extended metameme %s from %s.  Traceback = %s" %(toBeMergedPath, self.path.fullTemplatePath, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.TemplatePathError(errorMsg)

        # ignore circular extensions
        if toBeMerged.path.fullTemplatePath == self.path.fullTemplatePath:
            return
        
        
        # extending a switch always makes us a switch
        if toBeMerged.isSwitch == True:
            self.isSwitch = True
            
        # ditto with singletons
        if toBeMerged.isSingleton == True:
            self.isSingleton = True
        
        self.aliases.append(toBeMerged.path)    
        self.aliases.extend(toBeMerged.aliases)
        self.aliases = filterListDuplicates(self.aliases)       
                
        self.enhances.extend(toBeMerged.enhances)
        self.enhances = filterListDuplicates(self.enhances)         
        
        self.aliases.extend(toBeMerged.aliases)
        self.aliases = filterListDuplicates(self.aliases)         
                
        for propertyKey in toBeMerged.properties.keys():
            try:
                # do nothing if we actually find a key with the same name in the merge metameme
                # if A extends B.  Any property declarations of the same name override B's
                mergeProp = self.properties[propertyKey]
            except:
                # Property not overridden
                mergeProp = toBeMerged.properties[propertyKey]
                self.properties[propertyKey] = mergeProp
                
        for memberMetaMemeKey in toBeMerged.memberMetaMemes.keys():
            try:
                # do nothing if we actually find a key with the same name in the merge metameme
                # if A extends B.  Any member declarations of the same name override B's
                mergeMember = self.memberMetaMemes[memberMetaMemeKey]
            except:
                # Property not overridden
                mergeMember = toBeMerged.memberMetaMemes[memberMetaMemeKey]
                self.memberMetaMemes[memberMetaMemeKey] = mergeMember

        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
       
        
    def validateMembers(self, memberDict, memePath):
        ''' 1 - Check to see that the member memes of the meme (memePath) are all created from metamemes that are 
                    member metamemes of self.
            2 - Check to ensure that the cardinality of all member metamemes is observed '''
        method = moduleName + '.' +  self.className + '.validateMembers'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        isValid = True
        validationIssues = []
        
        memberMetaMemeCount = {} #keep track of the total counts of the various metamemes
        
        #first iterate over the member metamemes and create a little occurrence tracker
        #After reviewing membership, we'll report any violated cardinality in the log.
        for memeberMetaMemeKey in self.memberMetaMemes.keys():
            memeberMetaMeme = self.memberMetaMemes[memeberMetaMemeKey]
            
            # CardinalityList is
            #    [min, max, total # of occurrences across all distinct members]                
            cardinalityList = [memeberMetaMeme.min, memeberMetaMeme.max, 0]
            memberMetaMemeCount[memeberMetaMemeKey] = cardinalityList

               
        #per distinct membermeme in the meme being validated, build the cardinality lists
        #    If allDesctinctMembers flag is set, there may each member must be unique
        memberMMList = []
        for memeberMemePath in memberDict.keys():
            memeberMemeOcc = int(memberDict[memeberMemePath])
            try:
                # first get the member meme that the dict refers to
                memberMeme = templateRepository.resolveTemplate(memePath, memeberMemePath)
                try:
                    #naturally, that meme should have a registered metameme
                    member = memberMeme.getParentMetaMeme()
                    memberMMList.append(member.path.fullTemplatePath)
                    try:
                        # THAT metameme should also me a member metameme of this one
                        #  If so, then we increment the total number of occurrences to account for this distinct member
                        oldCardinalityList = []
                        extensionParents = []
                        try:
                            assert member.path.fullTemplatePath in memberMetaMemeCount
                            oldCardinalityList = memberMetaMemeCount[member.path.fullTemplatePath]
                        except AssertionError:                           
                            #This assertion error might be falsely triggered, if the member meme is from a metameme that extends the original
                            for extending in member.extends:
                                try:
                                    assert extending in memberMetaMemeCount
                                    oldCardinalityList = memberMetaMemeCount[extending]
                                    extensionParents.append(extending)
                                except AssertionError: 
                                    pass
                            for extending in member.enhances:
                                try:
                                    assert extending in memberMetaMemeCount
                                    oldCardinalityList = memberMetaMemeCount[extending]
                                    extensionParents.append(extending)
                                except AssertionError: 
                                    pass
                                
                            #Hopefully extensionParents includes exactly one entry.  If it is zero, then we failed the 
                            #    cardinality test outright.  If it is greater than 1, we have a ambiguous cardinality.
                            if len(extensionParents) == 1:
                                pass  #everything ok so far.  Pass the cardinality along
                            elif len(extensionParents) > 1:
                                errorMsg = "Meme %s claims metameme %s has %s as member metameme, but %s extends or enhances multiple members from the member keys, %s" % (memePath.fullTemplatePath, self.path.fullTemplatePath, member.path.fullTemplatePath, member.path.fullTemplatePath, list(extensionParents))
                                raise Exceptions.MemeMembershipValidationError(errorMsg)
                            else:
                                errorMsg = "Meme %s claims metameme %s has %s as member metameme, but it not is among the former's member metameme keys: %s" % (memePath.fullTemplatePath, self.path.fullTemplatePath, member.path.fullTemplatePath, list(memberMetaMemeCount.keys()))
                                raise Exceptions.MemeMembershipValidationError(errorMsg)
                        totalOcc = oldCardinalityList[2]
                        totalOcc = totalOcc + memeberMemeOcc
                        cardinalityList = [oldCardinalityList[0], oldCardinalityList[1], totalOcc]
                        
                        memberMetaMemeCount[member.path.fullTemplatePath] = cardinalityList
                        if len(extensionParents) == 1:
                            #For purposes of tracking cardinality, also use the parent as a key
                            memberMetaMemeCount[extensionParents[0]] = cardinalityList
                        
                        #Raises exception if member is not actually a member metameme of self
                        if len(extensionParents) == 0:
                            memeberMetaMeme = self.memberMetaMemes[member.path.fullTemplatePath]
                        else:
                            memeberMetaMeme = self.memberMetaMemes[extensionParents[0]]
                        
                        #lastly, if the allDesctinctMembers flag is set, then memeberMemeOcc must be < 2
                        #    Even if the members are not distinct, they still have to be within cardinality.
                        if (memeberMetaMeme.allDesctinctMembers == True) and (memeberMemeOcc > 1):
                            exception = "Meme %s has member %s that occurs %s times, but allDesctinctMembers is set." % (memePath.fullTemplatePath, member.path.fullTemplatePath, memeberMemeOcc)
                            raise Exceptions.MemeMembershipValidationError(exception)
                    except Exceptions.MemeMembershipValidationError as e:
                        logQ.put( [logType , logLevel.WARNING , method , e])
                        validationIssues.append(e)
                        isValid = False
                    except KeyError as e:
                        exception = "Meme %s claims metameme %s has %s as member metameme, but it is not in the repository" % (memePath.fullTemplatePath, self.path.fullTemplatePath, member.path.fullTemplatePath)
                        logQ.put( [logType , logLevel.WARNING , method , exception])
                        validationIssues.append(exception)
                        isValid = False
                    except Exception as e:
                        exception = "Meme %s falsely claims metameme %s has %s as member metameme" % (memePath.fullTemplatePath, self.path.fullTemplatePath, member.path.fullTemplatePath)
                        logQ.put( [logType , logLevel.WARNING , method , exception])
                        validationIssues.append(exception)
                        isValid = False
                except Exceptions.MemeMembershipValidationError as e:
                    raise Exceptions.MemeMembershipValidationError(e)
                except AttributeError as e:
                    exception = "Invalid Membership!  Meme %s claims metameme %s as a member.  Memes can only have memes as members!" % (memePath.fullTemplatePath, memberMeme.path.fullTemplatePath)
                    logQ.put( [logType , logLevel.WARNING , method , exception])                        
                    raise Exceptions.MemeMembershipValidationError(exception)
                except Exception as e:
                    raise e
            except Exception as e:
                isValid = False
                exception = "Meme %s validation problem.  Traceback = %s" %(memeberMemePath, e)
                validationIssues.append(exception)
                logQ.put( [logType , logLevel.WARNING , method , exception])


        #A bit of explanation justifying the second iteration over memberDict is in order.
        #    On thre first pass, there are multiple members of the same metameme type, it won't be possible
        #    to properly validate the cardinality.  By waiting making a second pass, we can be sure that
        #    the values of the cardinality lists are aggregated on a per metameme, rather than meme basis
        for memeberMemePath in memberDict.keys():
            try:
                memberMeme = templateRepository.resolveTemplate(memePath, memeberMemePath)
                #naturally, that meme should have a registered metameme
                member = memberMeme.getParentMetaMeme()
                memberMMList.append(member.path.fullTemplatePath)
                assert member.path.fullTemplatePath in memberMetaMemeCount
                cardinalityList = memberMetaMemeCount[member.path.fullTemplatePath]
                if cardinalityList[2] > cardinalityList[1]:
                    exception = "Meme %s validation problem.  Too many members of type %s. occurs %s, when the max allowed is %s." %(memePath.fullTemplatePath, member.path.fullTemplatePath, cardinalityList[2], cardinalityList[1])
                    raise Exceptions.MemeMembershipValidationError(exception)
                elif cardinalityList[2] < cardinalityList[0]:
                    exception = "Meme %s validation problem.  Too few members of type %s. occurs %s, when the min allowed is %s." %(memePath.fullTemplatePath, member.path.fullTemplatePath, cardinalityList[2], cardinalityList[0])
                    raise Exceptions.MemeMembershipValidationError(exception)
            except AssertionError:
                #This is a reiteration of the assert on the last iteration over the member dict.
                #  If the assert will have failed here, it will have failed earlier and we don't need to
                #  clutter up the logs with duplicate warnings.  The assert is just to prevent the dict
                #  access from throwning an irrelevant exception
                pass
            except Exceptions.MemeMembershipValidationError as e:
                logQ.put( [logType , logLevel.WARNING , method , e])
                validationIssues.append(e)
                isValid = False
            except Exception:
                # Again, as with the assertion, this should have already turned up.  This operation is an abbreviated pass
                #  through the ember dict and all operations here have already been tried.
                pass

        # If self is a switch, then memes constructed from it it may only have 0 or 1 member types.
        if self.isSwitch == True:
            usedMMList = []
            for memeberMemePath in memberDict.keys():
                memberMeme = templateRepository.resolveTemplate(memePath, memeberMemePath)
                member = memberMeme.getParentMetaMeme()
                usedMMList.append(member.path.fullTemplatePath)
            usedMMList = filterListDuplicates(usedMMList)
            numberOfTypes = 0 #the total number of types
            for memberPath in usedMMList:
                numberOfTypes = numberOfTypes + 1
            if numberOfTypes > 1:
                exception = "Meme %s validation problem.  Too many types.  Only one allowed with switches." %(memePath)
                validationIssues.append(exception)
                logQ.put( [logType , logLevel.WARNING , method , exception])
                isValid = False 
        
        # Check to make sure that the total member count per type falls within the cardinality
        #  If self is a switch and the meme has only one member, we still need to ensure that type fits the cardinality
        if (self.isSwitch == False) or (numberOfTypes == 0):     
            for memberPath in memberMetaMemeCount.keys():
                cardinalityList = memberMetaMemeCount[memberPath]
                if self.isSwitch == False:
                    if cardinalityList[2] > cardinalityList[1]:
                        isValid = False
                        exception = "Meme %s validation problem.  Too many members of type %s. occurs %s, when the max allowed is %s." %(memePath.fullTemplatePath, memberPath, cardinalityList[2], cardinalityList[1])
                        validationIssues.append(exception)
                        logQ.put( [logType , logLevel.WARNING , method , exception]) 
                    elif (cardinalityList[2] < cardinalityList[0]):
                        isValid = False
                        exception = "Meme %s validation problem.  Too few members of type %s. occurs %s, when the min allowed is %s." %(memePath.fullTemplatePath, memberPath, cardinalityList[2], cardinalityList[0])
                        validationIssues.append(exception)
                        logQ.put( [logType , logLevel.WARNING , method , exception])
        elif numberOfTypes == 1:
            # In this case, switch is true, so we have a switch metameme and a meme with one member type Memes built from 
            #    switches may only one of the members declared in the metameme and we don't want failures triggered by other 
            #    metamemes.  Use usedMMList instead of iterating across memberMetaMemeCount
            cardinalityList = memberMetaMemeCount[usedMMList[0]]
            if self.isSwitch == False:
                if cardinalityList[2] > cardinalityList[1]:
                    isValid = False
                    exception = "Meme %s validation problem.  Too many members of type %s. occurs %s, when the max allowed is %s." %(memePath, memberPath, cardinalityList[2], cardinalityList[1])
                    validationIssues.append(exception)
                    logQ.put( [logType , logLevel.WARNING , method , exception])
                elif (cardinalityList[2] < cardinalityList[0]):
                    isValid = False
                    exception = "Meme %s validation problem.  Too few members of type %s. occurs %s, when the min allowed is %s." %(memePath, memberPath, cardinalityList[2], cardinalityList[0])
                    validationIssues.append(exception)
                    logQ.put( [logType , logLevel.WARNING , method , exception])

        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return [isValid, validationIssues]
    
    

    def collectMemes(self):
        ''' Find all the memes in the repository with self as parent metameme'''
        #method = moduleName + '.' +  self.className + '.collectMemes'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        memes = []

        for testMemePath in templateRepository.templates:
            # Yes, we ARE iterating across all the templates in the repo.  Hence this method being expensive
            #iterate over the extension list and see if we have a match
            #logQ.put( [logType , logLevel.DEBUG , method , "checking to see if %s is a child meme of %s" %(testMemePath, self.path.fullTemplatePath)])
            try:
                testMeme = templateRepository.resolveTemplateAbsolutely(testMemePath)
                if testMeme.metaMeme == self.path.fullTemplatePath:
                    memes.append(testMemePath)
            except:
                #trying this on anything other than a meme will result in an exception, 
                #    which gives a quick and dirty, albiet hackish, way of filtering for memes 
                pass
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return memes
    
    

    def collectEnhancements(self):
        ''' Find all of the metamemes enhanced by self, or ancestors of self.
            Then call collectExtensions() on each of them to compile a list of all metamemes enhanced by self'''
        #method = moduleName + '.' +  self.className + '.collectEnhancements'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        enhancementList = self.collectEnhancementsFromAncestors()
        enhancementExtensionsList = []
        
        for enhancement in enhancementList:
            enhancementMM = templateRepository.resolveTemplate(self.path, enhancement)
            enhancementExtensionsFrag = enhancementMM.collectExtensions()
            enhancementExtensionsList.extend(enhancementExtensionsFrag)
            
        enhancementList.extend(enhancementExtensionsList)
        
        enhancementList = filterListDuplicates(enhancementList)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return enhancementList
    
    
    
    def collectEnhancementsFromAncestors(self):
        ''' Find all of the metamemes enhanced by self, or ancestors of self.
            Then call collectExtensions() on each of them to compile a list of all metamemes enhanced by self'''
        method = moduleName + '.' +  self.className + '.collectEnhancementsFromAncestors'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        enhancementList = []
        
        #iterate over the enhancement list and see if we have a match
        for enhancement in self.enhances:
            #logQ.put( [logType , logLevel.DEBUG , method , "testing enhancement %s against %s" %(enhancement, self.path.fullTemplatePath)])
            try:
                testMM = templateRepository.resolveTemplate(self.path, enhancement)
                enhancementList.append(testMM.path.fullTemplatePath)
            except Exception as e:
                logQ.put( [logType , logLevel.WARNING , method , "Unable to catalog declared enhancement %s in %s.  Traceback = %s" %(enhancement, self.path.fullTemplatePath, e)])
        
        # Now kick it up a level.  This will recursively find ALL of self's enhancements        
        for extension in self.extends:
            try:
                extendsMetaMeme = templateRepository.resolveTemplate(self.path, extension)
                enhancementListFrag = extendsMetaMeme.collectEnhancements()
                enhancementList.extend(enhancementListFrag)
            except Exception as e:
                logQ.put( [logType , logLevel.WARNING , method , "Unable to catalog enhancements in parent metameme %s of %s.  Traceback = %s" %(extension, self.path.fullTemplatePath, e)])
                #debug
                #extendsMetaMeme = templateRepository.resolveTemplate(self.path, extension)
                #enhancementListFrag = extendsMetaMeme.collectEnhancements()
                #enhancementList.extend(enhancementListFrag)
                
        enhancementList = filterListDuplicates(enhancementList)        
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return enhancementList
    
    
    
    def collectExtensions(self):
        ''' The problem:  A enhances B.  C extends B and D extends C.
            By virtue of inheritance, A enhances C and D.  This method is for that use case.
            
            self is the poverbial B.  Method finds everything that extends B
            
            This method looks at all of the memes that extend self and recursively checks them, looking for further extensions.
            This method is VERY computationally expensive!  
            We save a bit of wieght by insisting that ancestor already be a fully resolved metameme.'''
        method = moduleName + '.' +  self.className + '.collectExtensions'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        extensions = []

        for testMetaMemeID in templateRepository.templates:
            # Yes, we ARE iterating across all the templates in the repo.  Hence this method being expensive
            #iterate over the extension list and see if we have a match
            #logQ.put( [logType , logLevel.DEBUG , method , "checking to see if %s, is among the metamemes that extend %s" %(testMetaMemeID, self.path.fullTemplatePath)])
            testMetaMeme = templateRepository.resolveTemplateAbsolutely(testMetaMemeID)
            try:
                for extension in testMetaMeme.extends:
                    try:
                        extensionMM = templateRepository.resolveTemplate(testMetaMeme.path, extension)
                        if extensionMM.path.fullTemplatePath == self.path.fullTemplatePath:
                            #logQ.put( [logType , logLevel.DEBUG , method , "%s == %s" %(extensionMM.path.fullTemplatePath, self.path.fullTemplatePath)])
                            extensions.append(testMetaMeme.path.fullTemplatePath)
                            furtherExtensions = testMetaMeme.collectExtensions()
                            extensions.extend(furtherExtensions)
                        else:
                            #logQ.put( [logType , logLevel.DEBUG , method , "%s != %s" %(extensionMM.path.fullTemplatePath, self.path.fullTemplatePath)])
                            pass
                    except Exception as e:
                        logQ.put( [logType , logLevel.WARNING , method , "%s has invalid extends declaration %s.  Traceback = %s" %(testMetaMeme.path.fullTemplatePath, extension, e)])
            except:
                #only meta memes have an extends attribute
                pass
        extensions = filterListDuplicates(extensions) 
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return extensions
    
    
    
    def collectAncestors(self):
        """
            This method will search across all extension trees and find the templates that they in turn extend.
            Given the metameme toBeSearched, this method will return all fully resolved template paths of the extensions
        """
        method = moduleName + '.' +  self.className + '.collectAncestors'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        allExtensions = []
        for extends in self.extends:
            try:
                toBeMerged = tempRepository.resolveTemplate(self.path, extends)
                allExtensions.append(toBeMerged.path.fullTemplatePath)
                toBeMergedExtensions = toBeMerged.collectAncestors()
                allExtensions.extend(toBeMergedExtensions)
            except Exception as e:
                logQ.put( [logType , logLevel.WARNING , method , "%s has invalid extends declaration %s.  Traceback = %s" %(self.path.fullTemplatePath, extends, e)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return allExtensions
            
            
    
    
    def getTemplateType(self):
        return "MetaMeme"
    
    
    def testTaxonomy(self, templatePath):
        """
            Performs a boolean true/false test to see if the full tamplate path of self, or any ancestor
                matches the tested path.  Useful for indexing actions and stimuli.
        """
        #method = moduleName + '.' +  self.className + '.testMetaMemeType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        fullMetaMemeTypeList = []
        fullMetaMemeTypeList.append(self.path.fullTemplatePath)
        ancestors = self.collectAncestors()
        fullMetaMemeTypeList.extend(ancestors)
        
        returnResult = False
        if templatePath in fullMetaMemeTypeList:
            returnResult = True
        
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnResult
        
    
    


            
            




class MemberMetaMeme(object):
    className = "MemberMetaMeme"
    
    def __init__(self, memPath, minVal, maxVal, lt = linkTypes.ATOMIC, allDesctinctMembers = False):
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.memberPath = memPath
        
        self.min = minVal
        self.max = maxVal
        self.allDesctinctMembers = allDesctinctMembers
        self.lt = lt
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"]) 
        
    def validateMemberIsMetaMeme(self, parentMetaMeme):
        '''Ensure that the member metameme is indeed a metameme '''
        method = moduleName + '.' +  self.className + '.validateMemberIsMetaMeme'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        returnVal = False
        try:
            memberMetameme = tempRepository.resolveTemplate(parentMetaMeme.path, self.memberPath.fullTemplatePath)
            if type(memberMetameme) == "MetaMeme":
                returnVal = False
        except:
            logQ.put( [logType , logLevel.WARNING, method , "Metameme %s claims non-existant %s as member metameme" %(parentMetaMeme.path.fullTemplatePath, self.memberPath.fullTemplatePath)])#
    
        return returnVal
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"]) 
        
        
 
 
class PropertyDefinition(object):
    className = "PropertyDefinition"

    def __init__(self, name, propertyType, restMin, restMax, restList, constrained):
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.name = name
        self.propertyType = propertyType
        self.restMin = restMin
        self.restMax = restMax
        self.restList = restList
        self.constrained = constrained
        self.propError = []
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"]) 
        
        
    def setValue(self, newValue, autoCap = True):
        """  An abstract method that is not actually used by the MetaMeme property, 
            but is used by the meme and entity property classes. 
            If autoCap == True, then any value outside the bounds will automatically locked to the bounds.
            Otherwise, the change will fail.  """
        method = moduleName + '.' +  self.className + '.setValue'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        propValue = None
        if self.propertyType == 'decimal':
            #logQ.put( [logType , logLevel.DEBUG, method , "Attempting to set decimal property %s to %s" %(self.name, newValue)])
            try:
                propValue = decimal.Decimal(newValue)
                if self.constrained is True:
                    if self.restMin is not None:
                        if propValue < self.restMin:
                            if autoCap == True:
                                propValue = self.restMin
                                errorMsg = "Unable to assign value %s to constrained decimal property %s.  Proposed new value is less than the minimum value %s and will be capped at %s" % (newValue, self.name, self.restMin, self.restMin)
                                try:
                                    self.propError.append(errorMsg) # property has this list, but not propertydefinition
                                except: pass #ignore if called on propertydefinition
                                logQ.put( [logType , logLevel.WARNING, method , errorMsg])   
                            else:
                                exception = "Unable to assign value %s to constrained decimal property %s.  Proposed new value is less than the minimum value %s." % (newValue, self.name, self.restMin)
                                logQ.put( [logType , logLevel.WARNING, method , exception])
                                raise Exceptions.EntityPropertyValueOutOfBoundsError(exception)  
                    if self.restMax is not None:
                        if propValue > self.restMax:
                            if autoCap == True:
                                propValue = self.restMax
                                errorMsg = "Unable to assign value %s to constrained decimal property %s.  Proposed new value is greater than the maximum value %s and will be capped at %s" % (newValue, self.name, self.restMax, self.restMax)
                                try:
                                    self.propError.append(errorMsg) # property has this list, but not propertydefinition
                                except: pass #ignore if called on propertydefinition
                                logQ.put( [logType , logLevel.WARNING, method , errorMsg])
                            else:
                                exception = "Unable to assign value %s to constrained decimal property %s.  Proposed new value is greater than the maximum value %s." % (newValue, self.name, self.restMax)
                                logQ.put( [logType , logLevel.WARNING, method , exception])
                                raise Exceptions.EntityPropertyValueOutOfBoundsError(exception)
                    if (self.restList is not None) and (len(self.restList) > 0):
                        if propValue not in self.restList:
                            exception = "Unable to assign value %s to constrained decimal property %s.  Proposed new value is not one of the following allowed discreet values %s." % (newValue, self.name, self.restList)
                            logQ.put( [logType , logLevel.WARNING, method , exception])
                            raise Exceptions.EntityPropertyValueOutOfBoundsError(exception)   
            except Exceptions.EntityPropertyValueOutOfBoundsError as e:
                logQ.put( [logType , logLevel.WARNING, method , "EntityPropertyValueOutOfBoundsError assigning value %s to decimal property %s.  Traceback = %s" %(propValue, self.name, e)])
                raise Exceptions.EntityPropertyValueTypeError(e)
            except Exception as e:
                exception = "Unable to assign value %s to decimal property %s.  Traceback = %s" % (newValue, self.name, e)
                logQ.put( [logType , logLevel.WARNING, method , exception])
                raise Exceptions.EntityPropertyValueTypeError(exception)
        elif self.propertyType == 'boolean':
            #logQ.put( [logType , logLevel.DEBUG, method , "Attempting to set boolean property %s to %s" %(self.name, newValue)])
            try:
                propValueI = 0
                if (newValue == 'true') or (newValue == 'true'):
                    propValueI = 1
                elif (newValue == 'false') or (newValue == 'false'):
                    propValueI = 0
                else:
                    propValueI = int(newValue)
                if (propValueI > 1) or (propValueI < 0):
                    exception = "Unable to assign value %s to constrained decimal property %s.  Proposed new value is greater than the maximum value %s." % (newValue, self.name, self.restMax)
                    logQ.put( [logType , logLevel.WARNING, method , exception])
                    raise Exceptions.EntityPropertyValueTypeError(exception)
                else:
                    propValue = bool(propValueI)
            except Exceptions.EntityPropertyValueTypeError as e:
                raise e
            except Exception as e:
                exception = "Unable to assign value %s to boolean property %s.  Traceback = %s" % (newValue, self.name, e)
                raise e
        elif self.propertyType == 'integer':
            #logQ.put( [logType , logLevel.DEBUG, method , "Attempting to set integer property %s to %s" %(self.name, newValue)])
            try:
                propValue = int(newValue)
                if self.constrained == True:
                    if self.restMin is not None:
                        if propValue < self.restMin:
                            if autoCap == True:
                                propValue = self.restMin
                                logQ.put( [logType , logLevel.WARNING, method , "Unable to assign value %s to constrained integer property %s.  Proposed new value is less than the minimum value %s and will be capped at %s" % (newValue, self.name, self.restMin, self.restMin)])   
                            else:
                                exception = "Unable to assign value %s to constrained integer property %s.  Proposed new value is less than the minimum value %s." % (newValue, self.name, self.restMin)
                                logQ.put( [logType , logLevel.WARNING, method , exception])
                                raise Exceptions.EntityPropertyValueOutOfBoundsError(exception)  
                    if self.restMax is not None:
                        if propValue > self.restMax:
                            if autoCap == True:
                                propValue = self.restMax
                                logQ.put( [logType , logLevel.WARNING, method , "Unable to assign value %s to constrained integer property %s.  Proposed new value is greater than the maximum value %s and will be capped at %s" % (newValue, self.name, self.restMax, self.restMax)])
                            else:
                                exception = "Unable to assign value %s to constrained integer property %s.  Proposed new value is greater than the maximum value %s." % (newValue, self.name, self.restMax)
                                logQ.put( [logType , logLevel.WARNING, method , exception])
                                raise Exceptions.EntityPropertyValueOutOfBoundsError(exception)
                    if (self.restList is not None) and  (len(self.restList) > 0):
                        if propValue not in self.restList:
                            #Auto cap does not work for lists
                            exception = "Unable to assign value %s to constrained integer property %s.  Proposed new value is not one of the following allowed discreet values %s." % (newValue, self.name, self.restList)
                            logQ.put( [logType , logLevel.WARNING, method , exception])
                            raise Exceptions.EntityPropertyValueOutOfBoundsError(exception)  
            except Exceptions.EntityPropertyValueOutOfBoundsError as e:
                logQ.put( [logType , logLevel.WARNING, method , "EntityPropertyValueOutOfBoundsError assigning value %s to decimal property %s.  Traceback = %s" %(propValue, self.name, e)])
                raise Exceptions.EntityPropertyValueTypeError(e)
            except Exception as e:
                exception = "Unable to assign value %s to integer property %s.  Traceback = %s" % (newValue, self.name, e)
                logQ.put( [logType , logLevel.WARNING, method , exception])
                raise Exceptions.EntityPropertyValueTypeError(exception)
        else:
            #logQ.put( [logType , logLevel.DEBUG, method , "Attempting to set string property %s to %s" %(self.name, newValue)])
            propValue = newValue
            
        self.value = propValue
        #logQ.put( [logType , logLevel.DEBUG, method , "Property %s set to %s" %(self.name, self.value)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        


class PropertyRestrictionDecimal(object): 
    className = "PropertyRestrictionDecimal"
    
    def __init__(self, path, minVal = None, maxVal = None):
        method = moduleName + '.' +  self.className + '.initialize'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.path = path
        
        #Set self.min
        if minVal is None:
            self.min = None
        elif minVal == "":
            self.min = None
        else:
            try:
                self.min = decimal.Decimal(minVal)
            except:
                self.min = None
                logQ.put( [logType , logLevel.WARNING , method , "Decimal Property Restriction %s being initialized with min value %s that can't be cast to decimal.  Initializing as 'None'" % (path.fullTemplatePath, minVal)])
                
        #Set self.maxVal
        if maxVal is None:
            self.max = None
        elif maxVal == "":
            self.max = None
        else:
            try:
                self.max = decimal.Decimal(maxVal)
            except:
                self.max = None
                logQ.put( [logType , logLevel.WARNING , method , "Decimal Property Restriction %s being initialized with max value %s that can't be cast to decimal.  Initializing as 'None' (infinity)" % (path.fullTemplatePath, maxVal)])

        #logQ.put( [logType , logLevel.DEBUG , method , "Restriction %s: min = %s, max = %s" %(path.fullTemplatePath, self.min, self.max)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])    



class PropertyRestrictionInteger(object): 
    className = "PropertyRestrictionInteger"
    
    def __init__(self, path, minVal = None, maxVal = None):
        method = moduleName + '.' +  self.className + '.initialize'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.path = path
        
        #Set self.min
        if minVal is not None:
            try:
                self.min = int(minVal)
            except:
                self.min = 0
                logQ.put( [logType , logLevel.WARNING , method , "Integer Property Restriction %s being initialized with min value %s that is not an integer.  Initializing as 0" % (path.fullTemplatePath, minVal)])
        else:
            self.min = None
                            
        if maxVal is not None:
            try:
                self.max = int(maxVal)
            except:
                self.max = None
                logQ.put( [logType , logLevel.WARNING , method , "Integer Property Restriction %s being initialized with max value %s that is not an integer.  Initializing as 'None' (infinity)" % (path.fullTemplatePath, minVal)])
        else:
            self.max = None
               
        #logQ.put( [logType , logLevel.DEBUG , method , "Restriction %s: min = %s, max = %s" %(path.fullTemplatePath, self.min, self.max)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
        
class PropertyRestrictionList(object): 
    className = "PropertyRestrictionList"
    
    def __init__(self, path, values = []):
        #method = moduleName + '.' +  self.className + '.initialize'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.path = path
        self.values = values
        #logQ.put( [logType , logLevel.DEBUG , method , "Restriction %s: list = %s" %(path.fullTemplatePath, self.values)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])    
    
    
    

class Taxonomy(object):
    className = "Taxonomy"
    
    def __init__(self, taxonomyString):
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.fullPath = taxonomyString
        dot = re.compile(r'\.')
        self.splitPath = re.split(dot, taxonomyString)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])



class Property(PropertyDefinition):
    className = "Property"
    
    def __init__(self, metaMemeProperty, propValue):
        method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.name = metaMemeProperty.name
        self.propertyType = metaMemeProperty.propertyType
        self.constrained = metaMemeProperty.constrained
        self.restMin = metaMemeProperty.restMin
        self.restMax = metaMemeProperty.restMax
        self.restList = metaMemeProperty.restList
        self.propError = []
        
        try:
            self.setValue(propValue, False) 
        except Exceptions.EntityPropertyValueOutOfBoundsError as e:
            logQ.put( [logType , logLevel.WARNING , method , "Property %s validation problem.  Traceback = %s" %(metaMemeProperty.name, e)])
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting - (with warnings)"])
        except Exceptions.EntityPropertyValueTypeError as e:
            logQ.put( [logType , logLevel.WARNING , method , "Property %s validation problem.  Traceback = %s" %(metaMemeProperty.name, e)])
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting - (with warnings)"])
        except Exception as e:
            logQ.put( [logType , logLevel.WARNING , method , "Property %s validation problem.  Traceback = %s" %(metaMemeProperty.name, e)])
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting - (with warnings)"])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    def validate(self, memeID):
        #method = moduleName + '.' +  self.className + '.validate'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        isValid = True
        
        try:
            if self.value is None:
                isValid = False 
            elif (self.propertyType == 'decimal') or (self.propertyType == 'integer'):
                if self.restMax is not None:
                    if self.value > self.restMax:
                        isValid = False
                        exception = "Out of bounds numeric property %s.  Max = %s.  Value = %s" % (self.name, self.restMax, self.value)
                        self.propError.append(exception)
                if self.restMin is not None:
                    if self.value < self.restMin:
                        isValid = False
                        exception = "Out of bounds numeric property %s.  Min = %s.  Value = %s" % (self.name, self.restMin, self.value)
                        self.propError.append(exception)
            elif self.propertyType == 'boolean':
                if (self.value > 1) or (self.value < 0):  
                    exception = "Out of bounds boolean property %s.  Value %s is not boolean" % (self.name, self.value)
                    self.propError.append(exception)
                    isValid = False
            
            if len(self.restList) >= 1:
                if self.value not in self.restList:
                    isValid = False   
                    exception = "Out of bounds list property %s.  Value %s is not among list of valid values %s " % (self.name, self.value, self.restList)
                    self.propError.append(exception)            
        except Exception:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            exception = "Property %s of meme %s has no value property.  Likely reason is that restriction constraints were violated during intiialization.  Nested traceback = %s, %s : %s" % (self.name, memeID, errorID, errorMsg, tb)
            self.propError.append(exception)
            isValid = False
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return isValid
            
        


class SourceMeme(object):     
    """ 
    self.path = the template path
    self.metaMeme = the path of the parent metameme
    self.memberMemes = dict
        key  = memberID (the path of the member)
        value = occurrence (how many distinct times) 
    self.properties = dict
        key  = name (property name)
        value = occurrence (a Property object) 
    """   
 
    className = "sourceMeme"
            
    def __init__(self, path, metaMeme, localPath = None):
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.sourceMemeLock = threading.RLock()
        self.path = path
        self.localPath = localPath
        self.metaMeme = metaMeme
        self.memberMemes = {}
        self.properties = {}
        self.implicitReferences = {}    #The key is always the meme of the last hop.  The value is the metameme path required to traverse to hop n-1
        self.clones = []                #The clones is a list of the cloneable members
        self.enhances = {}
        self.tags = {}
        self.isSingleton = False
        self.invalidProps = {}
        self.entityUUID = None
        self.inactive = False
        self.validationErrors = []  #for validation errors that are discoverable at initial load, but lost later; such as Exceptions.DisallowedCloneError
        sourceTemplateRepository.catalogTemplate(self.path, self)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    
    
    #memberMemes, properties, enhances, tags, isSingleton, invalidProps = []):

    def setProperty(self, propName, propValueStr, propType = "string"):
        """
            Changes a meme property value.
            If the property is being added to a Generic Meme, then a PropertyDefinition is dynamically generated.
            string, list, integer, boolean, decimal
        """
        method = moduleName + '.' +  self.className + '.setProperty'
        try:
            metaMemeProperty = self.metaMeme.getProperty(propName)
            templateProperty = Property(metaMemeProperty, propValueStr)
            self.properties[propName] = templateProperty
        except Exceptions.MemePropertyValueOutOfBoundsError as e:
            logQ.put( [logType , logLevel.WARNING , method , e])
            self.invalidProps[propName] = e
            raise e
        except Exceptions.MemePropertyValueTypeError as e:
            logQ.put( [logType , logLevel.WARNING , method , e])
            self.invalidProps[propName] = e
            raise e
        except Exceptions.MemePropertyValueError as e:
            logQ.put( [logType , logLevel.WARNING , method , e]) 
            self.invalidProps[propName] = e  
            raise e   
        except Exceptions.MetaMemePropertyNotDefinedError as e:  
            if self.metaMeme.path.fullTemplatePath == "Graphyne.GenericMetaMeme":
                #Generic memes are allowed to add properties not in the metameme
                validPropTypes = ['string', 'list', 'integer', 'boolean', 'decimal']
                if propType not in validPropTypes:
                    errorMessage = "False property type %s" %propType
                    raise  Exceptions.MemePropertyValueTypeError(errorMessage)
                else:
                    dynamicProperty = PropertyDefinition(propName, propType, None, None, [], False)
                    templateProperty = Property(dynamicProperty, propValueStr)
                    self.properties[propName] = templateProperty
            else:
                propError = "Meme %s has property %s, but it is not a property of parent metameme %s.  Traceback = %s" % (self.path.fullTemplatePath, propName, self.metaMeme.path.fullTemplatePath, e)
                logQ.put( [logType , logLevel.WARNING , method , propError])
                self.invalidProps[propName] = propError
                
                tb = sys.exc_info()[2]
                raise Exceptions.MemePropertyValidationError(propError).with_traceback(tb)        
        except Exception as e:
            #OOPS!  Meme has a property that is not in the metameme
            propError = "Unknown problem with Meme %s and property %s, from parent metameme %s.  Traceback = %s" % (self.path.fullTemplatePath, propName, self.metaMeme.path.fullTemplatePath, e)
            logQ.put( [logType , logLevel.WARNING , method , propError])
            self.invalidProps[propName] = propError
            
            tb = sys.exc_info()[2]
            raise Exceptions.MemePropertyValidationError(propError).with_traceback(tb)

    def removeProperty(self, propName):
        method = moduleName + '.' +  self.className + '.removeProperty'
        try:
            del self.properties[propName]
        except Exception as e:
            exceptionMsg = "Problem removing property %s from meme %s.  Traceback = %s" %(propName, self.path.fullTemplatePath, e)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])    
            raise Exceptions.MemePropertyValidationError(exceptionMsg)   
        

    def addMemberMeme(self, memberID, occurrence, lt = linkTypes.ATOMIC):
        method = moduleName + '.' +  self.className + '.addMemberMeme'
        try:
            self.memberMemes[memberID] = (occurrence, lt)
            #debug
            #dummyString = "why is the implicit meme not a reerence?"
            #/debug
        except:
            exceptionMsg = "Can't add member %s (occurrence = %s) to meme %s" %(memberID, occurrence, self.path.fullTemplatePath)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])
            raise Exceptions.MemeMembershipValidationError(exceptionMsg)            
        
        
    def removeMemberMeme(self, memberID):
        method = moduleName + '.' +  self.className + '.removeMemberMeme'
        try:
            del self.memberMemes[memberID]
        except:
            exceptionMsg = "Meme %s does not have member %s" %(self.path.fullTemplatePath, memberID)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])
            raise Exceptions.MemeMembershipValidationError(exceptionMsg)
        
        
    def swapImplicitReference(self, newMemeID, oldMemeTemplateID, modulePath = None):
        ''' Exchange a member reference from <oldMemeID> with <newMemeID>  '''
        method = moduleName + '.' +  self.className + '.swapImplicitReference'
        try:
            #irst try using only the template ID.  It might be a local reference
            occurrence = self.implicitReferences[oldMemeTemplateID]
            del self.implicitReferences[oldMemeTemplateID]
            self.implicitReferences[newMemeID] = occurrence
        except KeyError:
            try:
                fullPath = None
                if modulePath is None:
                    fullPath = "%s.%s" %(self.path.modulePath, oldMemeTemplateID)
                else:
                    fullPath = "%s.%s" %(modulePath, oldMemeTemplateID)
                occurrence = self.implicitReferences[fullPath]
                del self.implicitReferences[fullPath]
                self.implicitReferences[newMemeID] = occurrence
            except Exception as e:
                raise e
        except Exception as e:
            exceptionMsg = "Error while trying to swap meme %s's implicit reference %s for %s" %(self.path.fullTemplatePath, oldMemeTemplateID, newMemeID)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])
            self.validationErrors.append(Exceptions.MemeMembershipValidationError(exceptionMsg))
        
        
        
    def addImplicitMemberMemes(self, soureMemeList, endEffector = None, traversePath = '', hierarchyRootNode = False):
        '''
            Concerts the implicitReferences into concrete member memes.
            soureMemeList = The entire source meme list (this method is intended to be called before self.compile() is called on all Source Memes at bootstrap)
            endEffector = the MemeID to be added.  If this method is called with it, it means that self is the descedent of another implicit meme (A), which is more than one hop from the end effector (B)
            traversePath = the remaining traverse path to get from A to B.  Self is a waypoint hop.  I None, then there are no remaining hops to reach B and we'll be attaching B to self.
            hierarchyRootNode = a boolean, indicating whether we are at the root of a hierarchy of implicit memes.  
            
            or adding self's own implicit memes:
            Step 1: Sort the implicitReferences members by the length of the metameme traverse path (number of hops)
            Step 2: By traverse path length, add the references as proper member metamemes
        '''
        method = moduleName + '.' +  self.className + '.addImplicitMemberMemes'
        
        if self.metaMeme.isImplicit == True:
  
            ''' We may be in a nested call or not.  In any case FIRST start off by converting the implicit memes o self to explicit.  
                Then aterwards, continue processing any additional implicit memes from an antescedent in the hierarchy.
            '''
            
            #debug
            #if (u"ImplicitMemes.HasChildPhase2" in self.path.fullTemplatePath) or (u"ImplicitMemes.SecondMiddleNodeHop" in self.path.fullTemplatePath):
            #    pass
            #/debug
            
            #Step 1
            partitionSequence = '::'
            traverseCountSortedReferences = {}
            for implicitReferenceKey in self.implicitReferences.keys():
                splitMetaMemePath = []
                count = 0
                implicitReferencePath = self.implicitReferences[implicitReferenceKey]
                if (len(implicitReferencePath) > 0) and implicitReferencePath is not None:
                    try:
                        splitMetaMemePath = implicitReferencePath.split(partitionSequence)
                        [a for a in splitMetaMemePath if a != '::']
                        count = len(splitMetaMemePath)
                    except:
                        pass
                if count in traverseCountSortedReferences:
                    #tcsrDictEntry = traverseCountSortedReferences[count]
                    #tcsrDictEntry.append(implicitReferenceKey)
                    #traverseCountSortedReferences[count] = tcsrDictEntry
                    traverseCountSortedReferences[count].append(implicitReferenceKey)
                else:
                    traverseCountSortedReferences[count] = [implicitReferenceKey]
                    
            #Step 2
            traverseHops = list(traverseCountSortedReferences.keys())
            traverseHops.sort() #to ensure that we start with hopcount = 0 and work outward
            for hopCount in traverseHops:
                currentimplicitReferenceList = traverseCountSortedReferences[hopCount]
                for hopMember in currentimplicitReferenceList:
                    #Remove hopMember from self.implicitReferences, in case we get circular references
                    hopTraversePath = self.implicitReferences[hopMember]
        
                    try:
                        del self.implicitReferences[hopMember]
                    except KeyError:
                        pass
                    
                    if hopCount < 1:
                        #nothing to do, add the member
                        self.addMemberMeme(hopMember, 1)
                    else:
                        ''' voodoo alert!
                            We have a template path with at least one hop, but we don't know exactly how many.
                            We do know that we have this struture: [A].[B], which is [metameme of next member].[o to n nested metamememe members]
                            So first, we pull A off, leaving [B], which may be empty.  
                            I'm sure there is some clever and unreadable regex statement that can do this in one line.'''
                        nextMetaMeme = None
                        continuedTraverse = ''
                        abSplit = hopTraversePath.split('::', 1) #[A]
                        nextMetaMeme = abSplit[0]
                        if len(abSplit) > 1:
                            continuedTraverse = abSplit[1] #[B]
                            
                        for sourceMeme in soureMemeList:
                            if sourceMeme.metaMeme.isImplicit == True:
                                if (sourceMeme.metaMeme.path.fullTemplatePath == nextMetaMeme):
                                    #'inflate' the implicit meme reerences on the clild, but only if it is a member of self
                                    for traverseNodeCandidate in self.memberMemes.keys():
                                        '''
                                            There is potential for a bug here.  We can't guarantee that traverseNodeCandidate uses the full template path, instead of its localName.
                                            Therefore we have to check against both.  BUT... if self.memberMemes has two or more members with the same localName, but coming from
                                            diferent modules, then me might be installing the member onto the wrong member.  By requiring the entire implicit meme hierarchy to be
                                            from the same module, we can sidestep this as a workaround.
                                        '''
                                        if (traverseNodeCandidate == sourceMeme.path.fullTemplatePath) or (traverseNodeCandidate == sourceMeme.path.templateName):
                                            try:
                                                sourceMeme.addImplicitMemberMemes(soureMemeList, hopMember, continuedTraverse)
                                            except Exceptions.MemeMembershipValidationError as e:
                                                em = "Implicit Meme Reference %s on meme %s is broken.  Nested Traceback = %s" %(hopTraversePath, self.path.fullTemplatePath,e)
                                                logQ.put( [logType , logLevel.WARNING , method ,em])
                                                raise Exceptions.MemeMembershipValidationError(em)
                                            except Exception as e:
                                                pass
                                                #debug
                                                #sourceMeme.addImplicitMemberMemes(soureMemeList, hopMember, continuedTraverse)
                                                #/debug
                                
            #Now that we done handling self's own implicit members, continue handling the antescedent mount request
            if (self.metaMeme.isImplicit == True) or (self.metaMeme.isCloneable == True):
                if hierarchyRootNode == False:
                    if traversePath != '':
                        #Clearly, this is not our irst pass through
                        if endEffector is None:
                            errorMsg = "Traverse Path of meme %s is empty, but there is not end effector!" %(self.path.fullTemplatePath)
                            logQ.put( [logType , logLevel.WARNING , method ,errorMsg])
                            raise Exceptions.MemeMembershipValidationError(errorMsg)  
                        else:
                            #we have both an end effector and a non empty traversePath
                            splitTraverse = traversePath.partition('::')                
                            found = False
                            for sourceMeme in soureMemeList:
                                if sourceMeme.metaMeme.isImplicit == True:
                                    if (sourceMeme.metaMeme.path.fullTemplatePath == splitTraverse[0]):
                                        found = True
                                        for nextMember in self.memberMemes:
                                            #Remember our requirement that the entire implicit meme hierarchy be in the same module?  Yeah, places like the next line are why.
                                            if ((sourceMeme.path.fullTemplatePath == nextMember) or (sourceMeme.path.templateName == nextMember)):
                                                if splitTraverse[1] == '':
                                                    # we have one hop.  What we need to do is match up which of self's children shares the same metameme as hopTraversePath and pass it on 
                                                    try:
                                                        sourceMeme.addImplicitMemberMemes(soureMemeList, endEffector) 
                                                    except Exceptions.MemeMembershipValidationError as e:
                                                        errorMsg = "Nested Exception while adding implicit member memes to %s child member %s.  Nested Traceback = %s" %(sourceMeme.path.fullTemplatePath, self.path.fullTemplatePath, e)
                                                        self.validationErrors.append(Exceptions.MemeMembershipValidationError(errorMsg))
                                                        logQ.put( [logType , logLevel.WARNING , method ,errorMsg])
                                                else:
                                                    try:
                                                        sourceMeme.addImplicitMemberMemes(soureMemeList, endEffector, splitTraverse[2])
                                                    except Exceptions.MemeMembershipValidationError as e:
                                                        errorMsg = "Nested Exception while adding implicit member memes to %s child member %s.  Nested Traceback = %s" %(self.path.fullTemplatePath, splitTraverse[0], e)
                                                        self.validationErrors.append(Exceptions.MemeMembershipValidationError(errorMsg))
                                                        logQ.put( [logType , logLevel.WARNING , method ,errorMsg])
                            if found == False:
                                e = "Expected to find %s among the members of %s.  %s is a waypoint hop in an implicit meme reference." %(splitTraverse[0], self.path.fullTemplatePath, self.path.fullTemplatePath)
                                self.validationErrors.append(Exceptions.MemeMembershipValidationError(e))
                                logQ.put( [logType , logLevel.WARNING , method ,e])
                    elif endEffector is not None:
                        #nothing to do, add the member
                        self.addMemberMeme(endEffector, 1)
                    else:
                        #this is not our irst pass through, but we have only the end eector left to handle
                        errorMsg = "Traverse Path of meme %s is empty, but there is not end effector!" %(self.path.fullTemplatePath)
                        self.validationErrors.append(Exceptions.MemeMembershipValidationError(errorMsg))
                        logQ.put( [logType , logLevel.WARNING , method ,errorMsg])

    
    def addEnhancement(self, memeID):
        method = moduleName + '.' +  self.className + '.addEnhancement'
        try:
            self.enhances[memeID] = memeID
            enhancementIndex.addEnhancement(self.path.fullTemplatePath, memeID)
            return True 
        except Exception as e:
            exceptionMsg = "Problem adding enhancement %s to meme %s.  Traceback = %s" %(memeID, self.path.fullTemplatePath, e)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])
            raise Exceptions.EnhancementError(exceptionMsg)    
        
    def removeEnhancement(self, memeID):
        method = moduleName + '.' +  self.className + '.removeEnhancement'
        try:
            del self.enhances[memeID]
            enhancementIndex.removeEnhancement(self.path.fullTemplatePath, memeID)
        except:
            exceptionMsg = "Meme %s does not enhance %s" %(self.path.fullTemplatePath, memeID)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])
            raise Exceptions.EnhancementError(exceptionMsg)
    
    
    def addTag(self, tag):
        method = moduleName + '.' +  self.className + '.addTag'
        try:
            self.tags[tag] = tag
            return True
        except Exception as e:
            exceptionMsg = "Problem adding tag %s to meme %s.  Traceback = %s" %(tag, self.path.fullTemplatePath, e)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])
            raise Exceptions.TagError()
        
        
    def removeTag(self, tag):
        method = moduleName + '.' +  self.className + '.removeTag'
        try:
            del self.tags[tag]
        except:
            exceptionMsg = "Meme %s does not have %s as tag" %(self.path.fullTemplatePath, tag)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])
            raise Exceptions.TagError()
            
            
    def setSingleton(self, isSingleton):
        method = moduleName + '.' +  self.className + '.setSingleton'
        try:
            self.isSingleton = isSingleton
            return True
        except Exception as e:
            exceptionMsg = "Problem setting singleton status of meme %s to %s.  Traceback = %s" %(self.path.fullTemplatePath, isSingleton, e)
            logQ.put( [logType , logLevel.WARNING , method , exceptionMsg])
            raise Exceptions.NonInstantiatedSingletonError()
        
            
            
    def compile(self, validate = True, instantiateSingletons = True):
        method = moduleName + '.' +  self.className + '.compile'
        #meme = Meme(path, metaMeme.path.fullTemplatePath, memberMemes, memeProperties, enhances, tags, isSingleton, invalidProps)
        validationResults = []
        enhancesList = []
        
        for enhancesListKey in self.enhances.keys():
            enhancesList.append(enhancesListKey)

        #debug
        #if u"ImplicitMemes" in self.path.fullTemplatePath:
        #    pass
        #/debug
            
        try:
            meme = Meme(self.path, self.metaMeme.path.fullTemplatePath, self.memberMemes, self.properties, enhancesList, self.tags, self.isSingleton, self.invalidProps)
            meme.inherentInvalidity.extend(self.validationErrors)
        except Exception as e:
            errorMessage = "Meme %s can't be created.  Traceback =%s" %(self.path.fullTemplatePath, e)   
            logQ.put( [logType , logLevel.WARNING , method ,errorMessage]) 
            
        try:
            #if the meme already exists at that location, then replace it and force an automerge
            assert self.path.fullTemplatePath in templateRepository.templates
            #alreadyExists = templateRepository.resolveTemplateAbsolutely(self.path.fullTemplatePath)
            templateRepository.templates[self.path.fullTemplatePath] = meme
            '''if alreadyExists.isSingleton == True:
                if alreadyExists.entityUUID is not None:
                    oldUUID = alreadyExists.entityUUID
                    if meme.isSingleton == True:
                        
                        logQ.put( [logType , logLevel.INFO , method ,"Meme %s is a singleton and will be instantiated" %(meme.path.fullTemplatePath)])
                        try:
                            #the old entity fall out of scope and get garbage collected.
                            # Re-use the old UUID and no not recreate any links.  Keep the old link network
                            entityID = meme.getEntityFromMeme(copy.deepcopy(oldUUID), True)
                            entity = entityRepository.indexByID[entityID]
                            entity.initialize()
                        except Exception as e:
                            errorMsg = "Meme %s is a singleton, but can't be instantiated.  Old entity destroyed.  Traceback = %s" %(meme.path.fullTemplatePath, e) 
                            entityDestroyer = destroyEntity()
                            entityDestroyer.execute([oldUUID])
                            logQ.put( [logType , logLevel.WARNING , method ,errorMsg])
                            raise Exception(errorMsg)
                    else:
                        errorMsg = "Meme %s is not a singleton, older version was.  Old entity destroyed and not replaced." %(meme.path.fullTemplatePath) 
                        entityDestroyer = destroyEntity()
                        entityDestroyer.execute([oldUUID])
                        logQ.put( [logType , logLevel.WARNING , method ,errorMsg])    
                        raise Exception(errorMsg)                                               
                else:
                    #is a singleton, but has not yet been instantiated
                    pass
                '''
            #validate = True
        except AssertionError:
            #Now it is perfectly possible to get this exception
            templateRepository.catalogTemplate(self.path, meme)            
        except Exception as e:
            #Now it is perfectly possible to get this exception
            errorMsg = "Encountered problem updating meme %s" %self.path.fullTemplatePath
            logQ.put( [logType , logLevel.WARNING , method ,errorMsg])

            
        if validate == True:
            validationResults = meme.validate([])
            
        return validationResults             
            
        
        


class Meme(object):     
    """ 
    self.path = the template path
    self.metaMeme = the path of the parent metameme
    self.memberMemes = dict
        key  = memberID (the path of the member)
        value = occurrence (how many distinct times) 
    self.properties = dict
        key  = name (property name)
        value = occurrence (a Property object) 
    """   
 
    className = "Meme"
    
    def __init__(self, path, metaMeme, memberMemes, properties, enhances, tags, isSingleton, invalidProps = []):
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.path = path
        self.metaMeme = metaMeme
        self.memberMemes = memberMemes
        self.properties = properties
        self.enhances = enhances
        self.tags = tags
        self.invalidProps = invalidProps
        self.entityUUID = None
        self.inactive = False
        self.inherentInvalidity = []
        
        metaMemeObject = templateRepository.resolveTemplateAbsolutely(metaMeme)
        if (metaMemeObject.isSingleton == True) or (isSingleton == True):
            self.isSingleton = True
        else:
            self.isSingleton = False 
            
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        

    def catalogEnhancements(self):
        ''' Walk through the enhances  '''
        for enhancedPath in self.enhances:
            fullEnhancedPath = templateRepository.resolveTemplate(self.path.fullTemplatePath, enhancedPath)
            enhancementIndex.addEnhancement(self.path.fullTemplatePath, fullEnhancedPath)

        
    def validate(self, memberExcludeList = []):
        ''' validate the meme's members against its metameme.  
            Properties are validated when read in as part of the getMemesFromFile() method 
            
            memberExcludeList is used to prevent infintie loops caused by memes recursively 
                validating one another '''
        method = moduleName + '.' +  self.className + '.validate'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        errorReport = []
        
        clonedMEL = copy.deepcopy(memberExcludeList)
        self.memberExcludeList = clonedMEL
        self.memberExcludeList.append(self.path.fullTemplatePath)
        isValid = False
        
        #debug
        #if (u"ImplicitMemes.HasChild" in self.path.fullTemplatePath) or (u"ImplicitMemes.MiddleNode" in self.path.fullTemplatePath):
        #    pass
        #/debug
        
        try:
            parentMetaMeme = templateRepository.resolveTemplate(self.path, self.metaMeme)
            
            #Meme members are stored in unresolved form.  When validating, we'll have to pass the full template paths
            resolvedMembers = {}
            unresolvedMember = False
            for unresolvedMemberMeme in self.memberMemes.keys():
                memeberMemeOcc = self.memberMemes[unresolvedMemberMeme][0]
                try:
                    resolvedMemberMetaMeme = templateRepository.resolveTemplate(self.path, unresolvedMemberMeme)
                    resolvedMembers[resolvedMemberMetaMeme.path.fullTemplatePath] = memeberMemeOcc
                except Exception as e:
                    errorMessage = "Problem resolving %s's member MetaMeme %s.  Traceback = %s" %(self.path.fullTemplatePath, unresolvedMemberMeme, e)
                    errorReport.append(errorMessage)
                    unresolvedMember = True
                    logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                    #debug
                    resolvedMemberMetaMeme = templateRepository.resolveTemplate(self.path, unresolvedMemberMeme)
            membersValidReport = parentMetaMeme.validateMembers(resolvedMembers, self.path)
            membersValid = membersValidReport[0]
            errorReport.extend(membersValidReport[1])
            
            # now make sure that all of the members are also valid
            for resolvedMemberMemeKey in resolvedMembers.keys():
                try:
                    resolvedMemberMeme = templateRepository.resolveTemplateAbsolutely(resolvedMemberMemeKey)
                    if resolvedMemberMemeKey not in memberExcludeList:
                        try:
                            memberValidRep = resolvedMemberMeme.validate(self.memberExcludeList)
                            memberValid = memberValidRep[0] 
                            if memberValid == False:
                                try:
                                    exception = "Meme %s is invalid because member meme %s is invalid.  Ivalidity is inherited from members.!" %(self.path.fullTemplatePath, resolvedMemberMemeKey)
                                    logQ.put( [logType , logLevel.WARNING , method , exception])
                                    membersValid = False
                                    errorReport.append(exception)
                                    errorReport.append(memberValidRep[1])
                                    
                                except Exception as e:
                                    exception = "Meme %s is invalid!  Traceback = %e" %(self.path.fullTemplatePath, e)
                                    logQ.put( [logType , logLevel.WARNING , method , exception])
                        except Exception as e:
                            exception = "Meme %s is invalid!  Traceback = %e" %(self.path.fullTemplatePath, e)
                            logQ.put( [logType , logLevel.WARNING , method , exception])
                            
                    elif resolvedMemberMeme.isSingleton == True:
                        # skip validating this member if it is a singleton and has already been 
                        #  validated by another meme in the assembly.  This is prone to happening in
                        #  highly re-used memes, such as Memetic.Script; especially in the context
                        #  of Angela's condition sets
                        logMessage = "Meme %s shares a link to singleton meme %s with another meme in its assembly." %(self.path.fullTemplatePath, resolvedMemberMemeKey)
                        logQ.put( [logType , logLevel.INFO , method , logMessage])
                    else:
                        # Houston, we have a problem!  A designer has created a recursive linking of members.  
                        #    DO NOT ALLOW THIS MONSTROSITY TO BE INSTANTIATED!
                        exception = "Meme %s is invalid because of a circular membership reference via meme %s.  Meme flagged as inactive!" %(self.path.fullTemplatePath, resolvedMemberMemeKey)
                        logQ.put( [logType , logLevel.WARNING , method , exception])
                        membersValid = False
                        errorReport.append(exception)
                        errorReport.append(memberExcludeList)
                        self.inactive = True
                except Exception as e:
                    exception = "Meme %s is invalid!  Traceback = %e" %(self.path.fullTemplatePath, e)
                    logQ.put( [logType , logLevel.WARNING , method , exception])
            
            
            
            propertiesValid = True
            propertyErrors = []
            # Validate the properties in the meme against their metamemes
            for propertyName in self.properties.keys():
                templateProperty = self.properties[propertyName]
                propertyValid = templateProperty.validate(self.path.fullTemplatePath)
                if propertyValid != True:
                    propertiesValid = False
                for propertyError in templateProperty.propError:
                    logMessage = "Meme Validation Error in %s.  %s" %(self.path.fullTemplatePath, propertyError)
                    propertiesValid = False
                    propertyErrors.append(propertyError)
                    logQ.put( [logType , logLevel.WARNING , method , logMessage])
            
            #A meme designer might have created a meme with an "orphaned" property;  one for which no metameme prop definition exists
            #    Such properties generate an exception at load time and fail to create a property.
            #    This snippet of code riminds us of the props that were not created because of this
            #    Such properties are also invalid props.
            for invalidProp in self.invalidProps:
                reason = None
                try:
                    reason = self.invalidProps[invalidProp]
                except Exception as e:
                    reason = e
                exception = "Meme %s has invalid property %s that was never created in repository.  Reason = %s" %(self.path.fullTemplatePath, invalidProp, reason)
                logQ.put( [logType , logLevel.WARNING , method , exception])
                propertyErrors.append(exception)
                propertiesValid = False
            errorReport.extend(propertyErrors)
            if len(errorReport) > 0:
                errorMsg = "Meme %s has orphaned properties: %s" %errorReport
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                
                
    
            #Enhanced memes are stored in unresolved form.  When validating, we'll have to pass the full template paths
            enhancementsValid = True
            enhancementErrors = []
            enhancableMemesInRepo = self.collectEnhanceableMemes()
            for unresolvedEnhancement in self.enhances:
                resolvedEnhancement = templateRepository.resolveTemplate(self.path, unresolvedEnhancement)
                if resolvedEnhancement.path.fullTemplatePath not in enhancableMemesInRepo:
                    enError = "Meme %s has claims to enhance meme %s, but there is no metameme enhancement path" %(self.path.fullTemplatePath, resolvedEnhancement.path.fullTemplatePath)
                    logQ.put( [logType , logLevel.WARNING , method , enError])
                    enhancementErrors.append(enError)
                    enhancementsValid = False
                    
            #make sure that if this metameme is enhanced by multiple memes, that they each have their own individual metameme
            iAmValidlyEnhanced = True
            enhancedByList = self.collectMemesThatEnhanceSelf()
            enhancedByMemesList = {}
            for enhancedBy in enhancedByList:
                enhancedByMeme = templateRepository.resolveTemplateAbsolutely(enhancedBy)
                enhancedByMM = enhancedByMeme.metaMeme
                try:
                    assert enhancedByMM not in enhancedByMemesList
                    enhancedByMemesList[enhancedByMM] = 'X'
                except AssertionError:
                    enError = "Meme %s is enhanced by multiple memes derived from metameme %s" % (self.path.fullTemplatePath, enhancedByMM)
                    logQ.put( [logType , logLevel.WARNING , method , enError])
                    enhancementErrors.append(enError)
                    iAmValidlyEnhanced = False
                    
            errorReport.extend(enhancementErrors)
                    
            #Since we just took the trouble run collectMemesThatEnhanceSelf, 
            #    it is very expensive and we'll need that info again at entity creation,
            #    catalog it in the Engine's enhancement index
            if iAmValidlyEnhanced == True:
                enhancementIndex.enhancementLists[self.path.fullTemplatePath] = enhancedByList
            
              
            if (membersValid == True) and\
                (propertiesValid == True) and\
                (enhancementsValid == True) and\
                (iAmValidlyEnhanced == True) and\
                (unresolvedMember == False):
                isValid = True
            else:
                logQ.put( [logType , logLevel.WARNING , method , "Meme %s does not validate!" %(self.path.fullTemplatePath)])
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        except TypeError as e:
            errorMsg = "Error validating meme %s.  Traceback = %s" %(self.path.fullTemplatePath, e)
        except Exception as e:
            errorMsg = "Error validating meme %s.  Traceback = %s" %(self.path.fullTemplatePath, e)

        for inherentError in self.inherentInvalidity:
            errorReport.append(inherentError.message)
            
        #At this point, we  are likely to have nested lists and duplicates.  Flatten it
        filteredErrata = []
        for errorEntry in errorReport:
            if type(errorEntry) == type([]):
                errorEntry = filterListDuplicates(errorEntry)
                for errorSubEntry in errorEntry:
                    filteredErrata.append(errorSubEntry)
            else:
                filteredErrata.append(errorEntry)
        cleanErrorReport = filterListDuplicates(filteredErrata)
           
        #del(memberExcludeList)
        #del(self.memberExcludeList)
        return [isValid, cleanErrorReport]
    
    
    
    def getEntityFromMeme(self, masterEntity = None, noMembers = False, passedUUID = None):
        ''' create a new entity from the meme.
            parentEntity is used if entity's parent is a member meme and this entity is being created 
            as a result of the other entity. When a new entity is created, entities are also created
            from all member memes, with the new entity as parent.'
            
            If the new member is a singleton and the entity had been created, then just return that UUID
            
            If noMembers is false, then entities from the meme's members will be created and the entities linked
            
            If passedUUID is not None, then the passed value will be attached to the Entity.  This is used where
            the entity is being restored from persistence on engine start.
            
            If restoreState is True, then when we instantiate the entity, we'll have to read the properties from
            persistence, rather than from the meme.
        '''
        method = moduleName + '.' +  self.className + '.getEntityFromMeme'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        returnUUID = None
        if (self.entityUUID is not None) and (passedUUID is None):
            returnUUID = self.entityUUID
        else:
            try:
                entity = Entity(self, masterEntity, noMembers, passedUUID)
                
                #If passedUUID is not None, then we already have the entity in persistence and are siply rebuilding it in memory
                if passedUUID is None:
                    entityRepository.addEntity(entity)
                else:
                    entityRepository.addEntityToIndex(entity)
                    
                returnUUID = entity.uuid
                if self.isSingleton == True:
                    self.entityUUID = returnUUID
            except Exception as e:
                #debug
                entity = Entity(self, masterEntity, noMembers, passedUUID)
                entityRepository.addEntity(entity)

                #/debug
                logQ.put( [logType , logLevel.WARNING , method , "Unable to instantiate meme %s!  Traceback = %s" %(self.path.fullTemplatePath, e)])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnUUID
    
    
    def getIsAssemblyRoot(self):
        ''' check and see if the metameme involved is an assembly root '''
        #method = moduleName + '.' +  self.className + '.getIsAssemblyRoot'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        isAssemblyRoot = False
        parentMM = self.getParentMetaMeme()
        if parentMM.isAssemblyRoot == True:
            isAssemblyRoot = True
        elif self.isSingleton == True:
            isAssemblyRoot = True
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return isAssemblyRoot       
       
        
        
    def getParentMetaMeme(self):
        ''' get the metameme against which this meme is created '''
        method = moduleName + '.' +  self.className + '.getParentMetaMeme'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        memeberMeme = None
        try:
            memeberMeme = templateRepository.resolveTemplate(self.path, self.metaMeme)
        except:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            exception = "Parent metameme %s of meme %s has no entry in the template repository.  Nested Traceback = %s: %s" % (self.metaMeme, self.path.fullTemplatePath, errorID, errorMsg)
            logQ.put( [logType , logLevel.WARNING , method , exception])
            raise Exceptions.TemplatePathError(exception).with_traceback(tb)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return memeberMeme   
    
    
    
    def collectEnhanceableMemes(self):
        ''' Find all the memes in the repository that self can enhance'''
        #method = moduleName + '.' +  self.className + '.collectMemes'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        parentMM = self.getParentMetaMeme()
        
        enhancableMMs = parentMM.collectEnhancements()
        enhancableMemes = []

        for metaMemeID in enhancableMMs:
            metaMeme = templateRepository.resolveTemplate(self.path, metaMemeID)
            enhancableMemesFrag = metaMeme.collectMemes()
            enhancableMemes.extend(enhancableMemesFrag)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return enhancableMemes 
    
    
    def collectMemesThatEnhanceSelf(self):
        ''' Find all the memes in the repository that enhance self'''
        #method = moduleName + '.' +  self.className + '.collectMemesThatEnhanceSelf'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])

        enhanceList = []
        
        for testMemePath in templateRepository.templates:
            # Yes, we ARE iterating across all the templates in the repo.  Hence this method being expensive
            #iterate over the enhancement list and see if we have a match to self
            try:
                testMeme = templateRepository.resolveTemplateAbsolutely(testMemePath)
                assert "metaMeme" in testMeme.__dict__
                for enhancesID in testMeme.enhances:
                    enhances = templateRepository.resolveTemplate(testMeme.path, enhancesID)
                    if enhances.path.fullTemplatePath == self.path.fullTemplatePath:
                        enhanceList.append(testMeme.path.fullTemplatePath)
            except AssertionError:
                #trying test = testMeme.metaMeme on anything other than a meme will result in an exception, 
                #    which gives a quick and dirty, albiet hackish, way of filtering for memes 
                pass
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return enhanceList 
    
    

    def getTemplateType(self):
        return "Meme"
    
    def testTaxonomy(self, templatePath):
        """
            Performs a boolean true/false test to see if the full tamplate path of self, or any ancestor
                matches the tested path.  Useful for indexing actions and stimuli.
        """
        #method = moduleName + '.' +  self.className + '.testMetaMemeType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        metaMeme = templateRepository.resolveTemplate(self.path, self.metaMeme)
        returnResult = metaMeme.testTaxonomy(templatePath)
        
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnResult        
    
    

class EntityProperty(PropertyDefinition):
    className = "EntityProperty"
    
    def __init__(self, name, value, propertyType, constrained = False, restMin = None, restMax = None, restList = None, memePath = None):
        method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.name = name
        self.propertyType = propertyType
        self.constrained = constrained
        self.restMin = restMin
        self.restMax = restMax
        self.restList = restList
        self.memePath = memePath        
        try:
            self.setValue(value)
        except Exceptions.EntityPropertyValueOutOfBoundsError as e:
            logQ.put( [logType , logLevel.WARNING , method , "Entity property %s validation problem." %(memePath)])
            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)
        except Exceptions.EntityPropertyValueTypeError as e:
            logQ.put( [logType , logLevel.WARNING , method , "Entity property %s validation problem." %(memePath)])
            raise Exceptions.EntityPropertyValueTypeError(e)
        except Exception as e:
            logQ.put( [logType , logLevel.WARNING , method , "Entity property %s validation problem." %(memePath)])
            logQ.put( [logType , logLevel.WARNING, method , e])

        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        



class Entity(object):
    """  The runtime instances of memes. """  
    
    def __init__(self, parentMeme, masterEntity = None, noMembers = False, passedUUID = None):
        """ Initialization of entities
        
        NOTE!!!  An entity is not fuly initialized until initialize() is run and the 
            state script callable objects (if any) have been set up.  The createEntityFromMeme.execute()
            method (which is used by the script facade) does this automatically.  If you are creating
            an entity manually (as the Meme.__init__() method does when initing a singleton meme), then
            you will have to manually execute initialize().  The reason for this two stage initialization 
            is to allow members in composites to be indexed in the entity repository.
            
        If we are restoring an Entity from persistence, then passedUUID will not be none and restoreState
            will not be false when self.initialize() is called.  In this case, we use the passed UUID value 
            and will have to bootstrap self's properties dictionary from the persistence, rather than from 
            the meme.
            
        oF passedUUID is not None, then noMembers is always True, as we are simply restoring prexisting 
            entities.  If the constructor is called with noMembers = false and passedUUID not None, we'll
            reset noMembers to True
        """
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        #debug
        #print("Creating: %s" %parentMeme.path.fullTemplatePath)
        #/debug
        global entityRepository
        
        self.className = "Entity"
        self.depricated = False
        self.memePath = parentMeme.path
        self.metaMeme = parentMeme.metaMeme
        self.tags = []
        self.properties = {}
        self.propertyChangeEvents = {}
        self.isInitialized = False
        self.initScript = None
        self.execScript = None
        self.terminateScript = None
        
        restore = False
        
        #Defining the UUID
        if passedUUID is not None:
            perparedUUIDFormat = '{%s}' % passedUUID
            self.uuid = uuid.UUID(perparedUUIDFormat)
            noMembers = True
            restore = True
        else:
            self.uuid = uuid.uuid1()
        
        memeIsAssemblyRoot = parentMeme.getIsAssemblyRoot()
        if (masterEntity == None) and (memeIsAssemblyRoot == True):
            masterEntity = self.uuid
            
        #Add the initial DB insertion here
        #If passedUUID is not None, then we are recreating the entity fro persisted data.  There is no need to try an insertion, as the
        #    entity is already in the database and if we do, then trying to insert on a nexisting primary key will generate an error
        try:
            if passedUUID is None:
                entityRepository.addEntityProvisional(self.uuid, masterEntity, self.depricated, parentMeme.path.fullTemplatePath, parentMeme.metaMeme)
        except Exception as e:
            raise e
        
        #Beyond initializing the parent meme path and uuid, even the parent meme is treated as an enhancement
        try:
            self.mergeEnhancement(parentMeme, masterEntity, noMembers, restore) 
        except Exception as e:
            raise e
        
        #self.entityLock = threading.RLock()
        
        # Now apply any actual enhancements
        try:
            enhancements = enhancementIndex.getEnhancements(parentMeme.path.fullTemplatePath)
            for enhancingMemeID in enhancements:
                enhancingMeme = templateRepository.resolveTemplateAbsolutely(enhancingMemeID)
                self.mergeEnhancement(enhancingMeme, masterEntity, noMembers, restore)
        except Exception as e:
            raise e
        
        #Restoring properties from the database at engine startup
        try:
            if restore is True:
                allPropertyTuples = entityRepository.getAllEntityProperties(self.uuid)
                for propertyTuple in allPropertyTuples:
                    #debug
                    #if (propertyTuple[2] == 2) and (propertyTuple[1] == 55.5):
                    #    localPT = entityRepository.getAllEntityProperties(self.uuid)
                    #/debug
                    newprop = EntityProperty(propertyTuple[0], propertyTuple[1], propertyTuple[2], propertyTuple[3], propertyTuple[4], propertyTuple[5], propertyTuple[6], propertyTuple[7])
                    self.properties[propertyTuple[0]] = newprop
                    self.propertyChangeEvents[propertyTuple[0]] = None
        except Exception as e:
            raise e
            
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])



    def setThreadable(self):
        self.entityLock = threading.RLock()
        
        
    def getThreadable(self):
        try:
            if self.__getattribute__('entityLock') is not None: 
                return True
        except AttributeError: 
            return False


    def execute(self, params):
        returnVal = None
        try:
            returnVal = self.execScript.execute(params[1])
        except Exception as e:
            errorMsg = "Script error on execute method of %s entity %s.  Traceback = %s" %(self.memePath, self.uuid, e)
            raise Exceptions.ScriptError(errorMsg)
        return returnVal
    
    
    def initialize(self, restoreState = False):
        """
            restoreState has two functions during initialization, and affects how properties and members are handled.  The
            actual processing is handled in the self.mergeEnhancement() method   
            
            properties - If restoreState is False, then we read properties from the meme and post them into persistence.
                If restoreState is True, then we ignore the meme's default properties and read from persistence.
                
            members - If restoreState is tTrie, then this will also act as a NoMembers flag on mergeenhancement
        """
        method = moduleName + '.' +  self.className + '.initialize'
        #The final step in entity creation is to initialize the callable objects related to the state event script
        # events.  Then execute the init script (if any) contained in the StateEventScript.Script.Script

        # a singleton that has previously been initialized.  No need in duplicating the work
        if self.isInitialized == True:
            return

        # The script entity is special in that is is non-executable and is only ever linked to by an SES meme.
        #    Therefore, we should skip initializing it
        if self.metaMeme.rfind("Graphyne.DNA.Script") != -1:
            return
        
        #SES Handling
        #If an entity is to have event scripts, then it will have SES enetities as schildren.  The goal of
        #  the following code block is to collect the scripts associated with these SES entities and install
        #  them onto the 'parent' entity. 
        #This may seem counterintuitive, but we don't install event scripts on SES entities, but rather 
        #    on their child 'script' entities.  This is because although graphyne currently supports only
        #    python scripts, we want to be future-proofe and leave open the possibility of having additional
        #    scripting options in the future.
        #ConditionXXX entities have special handling and are ignored here.  
        conditionMetaMemes = ['Graphyne.Condition.ConditionSet', 'Graphyne.Condition.ConditionString', 'Graphyne.Condition.ConditionNumeric']
        if self.metaMeme in conditionMetaMemes:
            parentConditionIDList = self.getLinkedEntitiesByMetaMemeType("Graphyne.Condition.Condition", linkTypes.SUBATOMIC)
            for parentConditionIDListItem in parentConditionIDList:
                parentConditionID = parentConditionIDListItem
            if self.metaMeme == "Graphyne.Condition.ConditionSet":
                childConditions = self.getLinkedEntitiesByMetaMemeType("Graphyne.Condition.ConditionSetChildren::Graphyne.Condition.Condition", None)

            operator = Condition.getOperatorFromConditionEntity(parentConditionID)
            path = api.getEntityMemeType(parentConditionID)
            newCondition = None
            if self.metaMeme  == "Graphyne.Condition.ConditionSet":
                newCondition = Condition.ConditionSet(parentConditionID, path, operator, childConditions)
            else:
                #determine the paths and argument types    
                try:
                    currArgumentType = Condition.getArgumentTypeFromConditionEntity(parentConditionID)
                    argumentPaths = Condition.getArgumentsFromConditionEntity(parentConditionID)
                except Exception as e:
                    #Build up a full java or C# style stacktrace, so that devs can track down errors in script modules within repositories
                    fullerror = sys.exc_info()
                    errorID = str(fullerror[0])
                    errorMsg = str(fullerror[1])
                    tb = sys.exc_info()[2]
                    ex = "Failed to initialize entity %s, of type %s. Nested Traceback = %s: %s" %(self.uuid, self.memePath.fullTemplatePath, errorID, errorMsg)
                    logQ.put( [logType , logLevel.WARNING , method , ex])
                    raise Exceptions.EntityInitializationError(ex).with_traceback(tb)
                
                if currArgumentType == Condition.argumentType.MULTI_ATTRIBUTE:
                    if self.metaMeme == 'Graphyne.Condition.ConditionString':
                        #conditionContainerUUID, name, operator, subjectArgumentPath, argumentTag1, objectArgumentPath, argumentTag2
                        newCondition = Condition.ConditionStringMultiA(parentConditionID, path, operator, argumentPaths)
                    elif self.metaMeme == 'Graphyne.Condition.ConditionNumeric':
                        newCondition = Condition.ConditionNumericMultiA(parentConditionID, path, operator, argumentPaths)
                elif currArgumentType == Condition.argumentType.ATTRIBUTE:
                    values = Condition.getTestValuesFromConditionEntity(parentConditionID)
                    if self.metaMeme == 'Graphyne.Condition.ConditionString':
                        #totdo - crash here
                        newCondition = Condition.ConditionStringAAA(parentConditionID, path, operator, argumentPaths, values)
                    elif self.metaMeme == 'Graphyne.Condition.ConditionNumeric':
                        newCondition = Condition.ConditionNumericAAA(parentConditionID, path, operator, argumentPaths, values)
                else:
                    values = Condition.getTestValuesFromConditionEntity(parentConditionID)
                    if self.metaMeme == 'Graphyne.Condition.ConditionString':
                        values = Condition.getTestValuesFromConditionEntity(parentConditionID)
                        newCondition = Condition.ConditionStringSimple(parentConditionID, path, operator, argumentPaths, values)
                    elif self.metaMeme == 'Graphyne.Condition.ConditionNumeric':
                        memberUUIDs = api.getLinkCounterpartsByMetaMemeType(parentConditionID, "**::Graphyne.Numeric.Formula", None)
                        newCondition = Condition.ConditionNumericSimple(parentConditionID, path, operator, argumentPaths, memberUUIDs)
            
            api.installPythonExecutor(parentConditionID, newCondition)
            
            uuidAsStr = str(parentConditionID)
            logStatement = "Added executor object to %s condition %s" %(path, uuidAsStr)
            api.writeLog(logStatement)
        
            #  Event installation of Conditions other script conditions.  Conditions are two tiered, with a 
            #    condition entity as parent for a xxxCondition entity, which in turn has the SES child.  
            #ConditionSet
            listOfSetConditions = self.getLinkedEntitiesByMetaMemeType(">>Graphyne.Condition.ConditionSet", None)
            for setConditionUUID in listOfSetConditions:
                childConditions = api.getLinkCounterpartsByMetaMemeType(setConditionUUID, ">>Graphyne.Condition.ConditionSetChildren::Graphyne.Condition.Condition", None)
    
            conditionType = None
            try:
                memberUUIDs = self.getLinkedEntitiesByMetaMemeType(">>Graphyne.Condition.ConditionSet", None)
                if len(memberUUIDs) < 1:
                    memberUUIDs = self.getLinkedEntitiesByMetaMemeType(">>Graphyne.Condition.ConditionString", None)
                if len(memberUUIDs) < 1:
                    memberUUIDs = self.getLinkedEntitiesByMetaMemeType(">>Graphyne.Condition.ConditionNumeric", None)
                for conditionToTestUUID in memberUUIDs:
                    #There should be exactly ONE member.  Condition is a switch
                    conditionType = api.getEntityMetaMemeType(conditionToTestUUID)
                
                if conditionType is not None:
                    if conditionType != "Graphyne.Condition.ConditionScript":
                        #Operators are not relevant for script conditions
                        operator = Condition.getOperatorFromConditionEntity(self.uuid)
        
                    newCondition = None
                    if conditionType == "Graphyne.Condition.ConditionSet":
                        newCondition = Condition.ConditionSet(self.uuid, self.memePath.fullTemplatePath, operator, childConditions)
                    else:
                        #determine the paths and argument types    
                        
                        currArgumentType = Condition.getArgumentTypeFromConditionEntity(self.uuid)
                        argumentPaths = Condition.getArgumentsFromConditionEntity(self.uuid)
                        
                        if currArgumentType == Condition.argumentType.MULTI_ATTRIBUTE:
                            if conditionType == 'Graphyne.Condition.ConditionString':
                                #self.uuid, name, operator, subjectArgumentPath, argumentTag1, objectArgumentPath, argumentTag2
                                newCondition = Condition.ConditionStringMultiA(self.uuid, self.memePath.fullTemplatePath, operator, argumentPaths)
                            elif conditionType == 'Graphyne.Condition.ConditionNumeric':
                                newCondition = Condition.ConditionNumericMultiA(self.uuid, self.memePath.fullTemplatePath, operator, argumentPaths)
                        elif currArgumentType == Condition.argumentType.ATTRIBUTE:
                            values = Condition.getTestValuesFromConditionEntity(self.uuid)
                            if conditionType == 'Graphyne.Condition.ConditionString':
                                #totdo - crash here
                                newCondition = Condition.ConditionStringAAA(self.uuid, self.memePath.fullTemplatePath, operator, argumentPaths, values)
                            elif conditionType == 'Graphyne.Condition.ConditionNumeric':
                                newCondition = Condition.ConditionNumericAAA(self.uuid, self.memePath.fullTemplatePath, operator, argumentPaths, values)
                        else:
                            values = Condition.getTestValuesFromConditionEntity(self.uuid)
                            if conditionType == 'Graphyne.Condition.ConditionString':
                                values = Condition.getTestValuesFromConditionEntity(self.uuid)
                                newCondition = Condition.ConditionStringSimple(self.uuid, self.memePath.fullTemplatePath, operator, argumentPaths, values)
                            elif conditionType == 'Graphyne.Condition.ConditionNumeric':
                                memberUUIDs = api.getLinkCounterpartsByMetaMemeType(self.uuid, "**::Numeric.Formula")
                                newCondition = Condition.ConditionNumericSimple(self.uuid, self.memePath.fullTemplatePath, operator, argumentPaths, memberUUIDs)
                        
                        self.installExecutorObject(newCondition)
                        uuidAsStr = str(self.uuid)
                        logStatement = "Added executor object to %s condition %s" %(self.memePath.fullTemplatePath, uuidAsStr)
                        api.writeLog(logStatement)
            except Exception as e:
                unusedDebugCatch = "me"
        else:
            #Install SES scripts
            sesEntities = self.getLinkedEntitiesByMetaMemeType('Graphyne.DNA.StateEventScript', None)
            
            #this block is for Script conditions.  They function as normal SES evaluate events, but whereas 
            #    the callable object (script) is normally installed onto the parent of Graphyne.DNA.StateEventScript 
            #    (which in this case is Graphyne.Condition.ConditionScript), it is instead called on the grandparent, 
            #    which in this case is Graphyne.Condition.Condition entity
            if self.metaMeme == 'Graphyne.Condition.Condition':
                sesEntities = self.getLinkedEntitiesByMetaMemeType('Graphyne.Condition.ConditionScript::Graphyne.DNA.StateEventScript', None)
                
            for sesEntityUUID in sesEntities:
                sesEntity = entityRepository.getEntity(sesEntityUUID)
                propertyID = None
                try:
                    state = sesEntity.getPropertyValue('State')
                    try:
                        propertyID = sesEntity.getPropertyValue('PropertyID')
                    except Exception as e:
                        pass #getPropertyValue() throws an exception if the property is not present.  Ignore this exception
                    scriptEntities = sesEntity.getLinkedEntitiesByMetaMemeType('Graphyne.DNA.Script', None)
                    for scriptEntityUUID in scriptEntities:
                        scriptEntity = entityRepository.getEntity(scriptEntityUUID)
                        scriptLocation = scriptEntity.getPropertyValue('Script')
                        scriptLanguage = scriptEntity.getPropertyValue('Language')
                        self.setStateEventScript(scriptLocation, scriptLanguage, state, propertyID)
                except Exceptions.StateEventScriptInitError as e:
                    raise e
                except Exception as e:
                    #Build up a full java or C# style stacktrace, so that devs can track down errors in script modules within repositories
                    fullerror = sys.exc_info()
                    errorID = str(fullerror[0])
                    errorMsg = str(fullerror[1])
                    tb = sys.exc_info()[2]
                    ex = "Failed to initialize Graphyne.StateEventScript entity %s, child of %s entity %s. Nested Traceback = %s: %s" %(sesEntity.memePath.fullTemplatePath, self.memePath.fullTemplatePath, self.uuid, errorID, errorMsg)
                    logQ.put( [logType , logLevel.WARNING , method , ex])
                    raise Exceptions.EntityInitializationError(ex).with_traceback(tb)
                
        initParams = {} #the params dict for the initi event is empty   
        if self.initScript is not None:
            try:
                self.initScript.execute(self.uuid, initParams)
            except Exception as e:
                errorMsg = "Error executing the initialization state event script of entity %s from meme %s" %(self.uuid, self.memePath.fullTemplatePath)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                #For debugging
                #self.initScript.execute(self.uuid, initParams)
        self.isInitialized = True     
                

        
       
    def mergeEnhancement(self, parentMeme, masterEntity, noMembers = False, restore = False):
        """ 
            Merge the properties and member of an enhancement meme into the entity being created.
            
            If noMembers is True, then we don't create the members of the current meme.  E.g. we
                don't want to create members when we are running a restore from DB at engine startup
                
            If restore is True, then the current entity is being restored from the database and 
                we don't want to either create members (they already exist) or set the properties,
                as property state exists in the DB tables and may not be the same as initial.
        """
        method = moduleName + '.' +  self.className + '.mergeEnhancement'
        global linkRepository
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        self.tags.extend(parentMeme.tags)
        self.tags = filterListDuplicates(self.tags)

        if noMembers == False:
            for memberMemeKey in parentMeme.memberMemes.keys():
                occurs = parentMeme.memberMemes[memberMemeKey][0]  #memermeme is a tuple with coocurence count at position 0 and linkType at position 1
                lnkTyp = parentMeme.memberMemes[memberMemeKey][1]
                if lnkTyp == 1:
                    unusedCatch = "me"
                member = templateRepository.resolveTemplate(parentMeme.path, memberMemeKey)
                n = 1
                while n <= int(occurs):
                    try:
                        n = n+1
                        childEntityID = member.getEntityFromMeme(masterEntity)
                        
                        #Now flag both entities as being linked
                        #All child entities created in this method have membership type = SUBATOMIC
                        #Don't bother locking the child for now as the public does not know about it yet
                        #memberID1, memberID2, membershipType, keyLink = None, masterEntity = None
                        #ToDo: cataloging of links is currently paremeter-less
                        #linkRepository.catalogLink(self.uuid, childEntityID, linkTypes.SUBATOMIC, {}, masterEntity)
                        linkRepository.catalogLink(self.uuid, childEntityID, lnkTyp, {}, masterEntity)
                    except Exception as e:
                        errprMsg = "Problem instantiating child meme of %s.  Entity initialization aborted!  Traceback = %s" %(parentMeme.path.fullTemplatePath, e)
                        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
                        #debug
                        #childEntityID = member.getEntityFromMeme(masterEntity)
                        #linkRepository.catalogLink(self.uuid, childEntityID, linkTypes.SUBATOMIC, {}, masterEntity)
                        print(errprMsg)
                        break
        
        if restore == False:
            for memePropKey in parentMeme.properties.keys():
                memeProperty = parentMeme.properties[memePropKey]
                
                try:
                    #We really don't need to be storing entity property types as unicide strings!
                    if memeProperty.propertyType == "integer":
                        self.addIntegerProperty(memeProperty.name, memeProperty.value, memeProperty.constrained, memeProperty.restMin, memeProperty.restMax, memeProperty.restList, parentMeme.path)
                    elif memeProperty.propertyType == "boolean":
                        #need to add a boolean function
                        self.addBooleanProperty(memeProperty.name, memeProperty.value, memeProperty.constrained, memeProperty.restMin, memeProperty.restMax, memeProperty.restList, parentMeme.path)
                        #newProp = EntityProperty(memeProperty.name, memeProperty.value, entityPropTypes.Boolean, memeProperty.constrained, memeProperty.restMin, memeProperty.restMax, memeProperty.restList, parentMeme.path)
                        #self.properties[memeProperty.name] =  newProp
                    elif memeProperty.propertyType == "decimal":
                        self.addDecimalProperty(memeProperty.name, memeProperty.value, memeProperty.constrained, memeProperty.restMin, memeProperty.restMax, memeProperty.restList, parentMeme.path)
                    elif memeProperty.propertyType == "list":
                        self.addListProperty(memeProperty.name, memeProperty.value, memeProperty.constrained, memeProperty.restMin, memeProperty.restMax, memeProperty.restList, parentMeme.path)
                    else:
                        self.addStringProperty(memeProperty.name, memeProperty.value, memeProperty.constrained, memeProperty.restMin, memeProperty.restMax, memeProperty.restList, parentMeme.path)
                except Exception as e:
                    errprMsg = "Unable to create property %s on %s entity %s.  Traceback = %s" %(memeProperty.name,parentMeme.path.fullTemplatePath, self.uuid, e)
                    logQ.put( [logType , logLevel.WARNING , method , errprMsg])

        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        

    
    def revertPropertyValues(self, drillDown = False):
        """ Reset property values to their original values as defined in the parent meme(s).  
        It does not affect custom properties or properties from depricated memes"""
        #method = moduleName + '.' +  self.className + '.revertPropertyValues'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])

        for propertyKey in self.properties.keys():
            prop = self.properties[propertyKey]
            if prop.memePath is not None:
                meme = templateRepository.resolveTemplateAbsolutely(self.memePath.fullTemplatePath)
                memeProperty = meme.properties[propertyKey]
                prop.value = memeProperty.value
                                        
                #First check the parent meme for the property
                #for memePropertyName in entityMeme.properties.iterkeys():
                    #if memePropertyName == propertyKey:
                        #memeProperty = entityMeme.properties[memePropertyName]
                        #prop.value = memeProperty.value
                        #updated = True
                
                # # if we did not find the property in that meme, check the other memes
                '''if updated == False:
                    enhancingMemesList = enhancementIndex.getEnhancements(self.memePath)
                    for enhancingMemeID in enhancingMemesList:
                        if updated == False:
                            enhancingMeme = templateRepository.resolveTemplateAbsolutely(enhancingMemeID)
                            for memePropertyName in enhancingMeme.properties.iterkeys():
                                if memePropertyName == propertyKey:
                                    memeProperty = entityMeme.properties[memePropertyName]
                                    prop.value = memeProperty.value
                                    updated = True
                '''

        if drillDown == True:
            links = linkRepository.getCounterparts(self.uuid) 
            for memberEntityID in links:
                try:
                    member = entityRepository.getEntity(memberEntityID)
                    member.entityLock.acquire(True)
                    try:
                        member.member.revertPropertyValues(True)
                    finally: member.entityLock.release()
                except: pass
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    def removeAllCustomProperties(self, drillDown = True):
        """ Remove all properties that do not come from a meme"""
        #method = moduleName + '.' +  self.className + '.removeAllCustomProperties'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        deleteList = []
        for propertyKey in self.properties.keys():
            templateProperty = self.properties[propertyKey]
            if templateProperty.memePath is None:
                #if it has no memePath, then it is a custom property
                deleteList.append(propertyKey)
        for delPath in deleteList:
            del self.properties[delPath]
            if delPath in self.propertyChangeEvents:
                del self.propertyChangeEvents[delPath]
            
        if drillDown == True:
            links = linkRepository.getCounterparts(self.uuid)
            for memberEntityID in links:
                try:
                    member = entityRepository.getEntity(memberEntityID)
                    member.entityLock.acquire(True)
                    try:
                        member.removeAllCustomProperties(True)
                    finally: member.entityLock.release()
                except: pass
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
        
    
    def getHasLinkedEntityByMemeType(self, meme, splitMetaMemePath = None, linkType = 0):
        """  """
        #method = moduleName + '.' +  self.className + '.getHasLinkedEntityByMemeType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        hasMember = False
        try:
            findList = self.getLinkedEntitiesByMemeType(meme, splitMetaMemePath, linkType)
            if len(findList) > 0:
                hasMember = True
        except:
            pass
        #memberToFind = entityRepository.getEntity(uuid)
        #for memberEntityEntry in self.memberEntities:
            #memberEntityID = memberEntityEntry[0]
            #member = entityRepository.getEntity(memberEntityID)
            #if member.memePath == meme.path.fullTemplatePath:
                #hasMember = True
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return hasMember
        
        
    #Todo - add getCounterparts params to method call
    def getAreEntitiesLinked(self, uuid, memBershipType = 0, ):
        """  """
        #method = moduleName + '.' +  self.className + '.getAreEntitiesLinked'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        hasMember = False
        members = linkRepository.getCounterparts(self.uuid, linkDirectionTypes.BIDIRECTIONAL, [], [], memBershipType)
        if uuid in members:
            hasMember = True
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return hasMember   
        
        
    def getIsSingleton(self):
        """  """
        #method = moduleName + '.' +  self.className + '.getIsSingleton'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        parentMeme = templateRepository.resolveTemplateAbsolutely(self.memePath.fullTemplatePath)
        isSingleton = parentMeme.isSingleton
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return isSingleton




    def getLinkIDs(self):
        """ Get all of the UUIDs for all links involving this entity"""
        #method = moduleName + '.' +  self.className + '.getLinkIDs'
        filteredLinkList = []
        try:
            sourceID = self.uuid
            filteredLinkList = linkRepository.getAllLinks(sourceID)
            #filteredLinkTuples= linkRepository.getAllLinks(sourceID)
            #for filteredLinkTuple in filteredLinkTuples:
            #    filteredLinkList.append(filteredLinkTuple[0])
        except Exception as e:
            unusedDummy = e #dummy variable declaration to prevent false alarm pydev warnings when debug statement is commented out
            #logQ.put( [logType , logLevel.DEBUG , method , "Failure getting link IDs.  Traceback = %s" %e])
            pass
            
        return filteredLinkList



    def getLinkedEntitiesByMemeType(self, memePath, splitMetaMemePath = None, linkType = 0):
        """ Find the member entities at the end of the Member Path.
        May be called with a composite path (e.g. Inventory.Inventory::Loot.GoldCoin) in meme
        or may be called with an explicitly regression split member path (which is a list)
        
        examples:
        entities = self.getMemberEntiesByType('Inventory.Inventory::Loot.GoldCoin')
        entities = self.getMemberEntiesByType(None, ['Inventory.Inventory', 'Loot.GoldCoin'])
        """
        #method = moduleName + '.' +  self.className + '.getLinkedEntitiesByMemeType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        returnMembers = self.getLinkedEntitiesByTemplateType(memePath, True, linkType, False, [], True, None)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnMembers
        
    
    def getLinkedEntitiesByMetaMemeType(self, metaMemePath, linkType = 0, returnUniqueValuesOnly = True):
        """ Find the member entities at the end of the Member Path.
        May be called with a composite path (e.g. Inventory.Inventory::Loot.GoldCoin) in meme
        or may be called with an explicitly regression split member path (which is a list)
        
        examples:
        entities = self.getMemberEntiesByType('Inventory.Inventory::Loot.GoldCoin')
        entities = self.getMemberEntiesByType(None, ['Inventory.Inventory', 'Loot.GoldCoin'])
        """
        #method = moduleName + '.' +  self.className + '.getLinkedEntitiesByMetaMemeType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        returnMembers = self.getLinkedEntitiesByTemplateType(metaMemePath, False, linkType, False, [], returnUniqueValuesOnly, None)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnMembers
    
    
    
    
    def buildClusterMemberMetadata(self, rawCluster):
        """
            This is a method for refining the raw entity member data into metadata
        """
        clusterMetadata = {}
        for rawClusterEntry in rawCluster:
            dictKey = getUUIDAsString(rawClusterEntry[1])
            clusterMetadata[dictKey] = [rawClusterEntry[2], rawClusterEntry[3]]
        return clusterMetadata
    


    def getClusterMembers(self, linkType= 0, crossSingletons = False, excludeLinks = []):
        """ 
            This method wraps getEntityCluster and then returns only the UUIDS of the members of the cluster
        """
        #method = moduleName + '.' +  self.className + '.getLinkedEntitiesByTemplateType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])

        entireCluster = self.getEntityCluster(linkType, crossSingletons, excludeLinks)
        clusterMetaData = self.buildClusterMemberMetadata(entireCluster)
        
        #buildClusterMemberMetadata returns the UUIDs as strings, because UUIDs can't be used for indexing dicts.
        #  This method returns UUID objects however
        returnMembersStrings = clusterMetaData.keys()
        returnMembers = []
        for returnMembersString in returnMembersStrings:
            idAsUUID = uuid.UUID(returnMembersString)
            returnMembers.append(idAsUUID)
        return returnMembers
    
    
    
    
    
    def getEntityCluster(self, linkType = 0, crossSingletons = False, excludeLinks = []):
        """ This is a method is a close relative of getLinkedEntitiesByTemplateType.  It is used for finding 
        associated (linked) entities and their meme types.  Like getLinkedEntitiesByTemplateType, it parses the
            link path and follows each step of the path in turn by a recursive call.  
            
        Where it differs is that it is not searching for a specific meme type, but instead double wildcards itself all
            the way through the assembly network; returning everything that self is linked to, no matter how remotely  
            
            linkTypes - the entity link type
            
            crossSingletons - if this is false, the recursion will stop at any singletons
            
            The method id not intended to be called directly, but is instead wrapped by helper functions (getClusterMembers and 
                getCluster) that refine the results.
        """
        #method = moduleName + '.' +  self.className + '.getLinkedEntitiesByTemplateType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])

        returnMembers = []
        
        try:
            members = linkRepository.getCounterparts(self.uuid, linkDirectionTypes.BIDIRECTIONAL, [], [], linkType, excludeLinks)
            newExcludeLinks = self.getLinkIDs()
            excludeLinks.extend(newExcludeLinks)
            
        
            for memberEntityID in members:
                member = entityRepository.getEntity(memberEntityID)
                isSingleton = member.getIsSingleton()
                
                if isSingleton == True:
                    position = 2  #Singleton
                else:
                    position = 1  #Not the origin entity and not a singleton
                
                returnMembers.append([self.uuid, member.uuid, member.memePath.fullTemplatePath, member.metaMeme, position])
                if (isSingleton == False) or (crossSingletons == True):
                    partialRet = member.getEntityCluster(linkType, crossSingletons, excludeLinks)
                    returnMembers.extend(partialRet)                      

        except Exception as e:
            unusedDummy = e #dummy variable declaration to prevent false alarm pydev warnings when debug statement is commented out
            #logQ.put( [logType , logLevel.DEBUG , method , "Failure getting overview.  Traceback = %s" %e])
            pass
                                        
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnMembers




    def getTraverseFilters(self, filterStatement, isNode = True):
        #Find the paremeters
        linkParams = []
        nodeParams = []
                
        #Peel off the parameter filters from filterStatement
        #reInnerParentheses = re.compile("\('([^']+)', '([^']+)'\)")
        #reOuterParentheses  = re.compile("\((.+)\)")
        #reInnerBrackets = re.compile("\[([^]]*)\]")
        #reOPMatches = reOuterParentheses.search(filterStatement)
        #reIBMatches = reInnerBrackets.search(filterStatement)
        reParenthesis = re.compile(r"\(.+?\)")
        reBrackets = re.compile(r"\[.+?\]")
        allParenthesis = reParenthesis.findall(filterStatement)
        allBrackets = reBrackets.findall(filterStatement)
        
        for reP in allParenthesis:
            reStripParentheses  = re.compile(r"\((.+)\)")
            reOPMatches = reStripParentheses.search(reP)
            reOPMatch = reOPMatches.groups(1)
            innerLinkParams, innerNodeParams = self.getTraverseFilters(reOPMatch[0])
            linkParams.extend(innerLinkParams)
            nodeParams.extend(innerNodeParams)

        for reB in allBrackets:
            reStripBrackets  = re.compile(r"\[([^]]*)\]")
            reIBMatches = reStripBrackets.search(reB)            
            reIBMatch = reIBMatches.groups(1)
            innerLinkParams, innerNodeParams = self.getTraverseFilters(reIBMatch[0], False)
            linkParams.extend(innerLinkParams)
            nodeParams.extend(innerNodeParams)
        
        #I we have no brackets or parenthesis, then we must be in the 'inner sanctum of the 'filter statement
        if (len(allParenthesis) < 1) and (len(allBrackets) < 1):
            tp = TraverseParameter(filterStatement.strip())
            if tp.operator is not None:
                if isNode == True:
                    nodeParams.append(tp)
                else:
                    linkParams.append(tp)
        
        return linkParams, nodeParams
    



    def getTraverseReport(self, splitPath, isMeme, linkType = 0, excludeLinks = [], returnUniqueValuesOnly = True, excludeCluster = []):
        """
            This method is an aid for designers troubleshooting traverse paths, or anyone simply asking 'what lies
            along the path'.  It is very similar to getLinkedEntitiesByTemplateType, but works in some subtle and
            substantially different ways.  Instead of delivering the uuid of an entity at the end effector of the 
            traverse path, it delivers a report of what is along that path and what the nearest neighbors are of 
            every hop.
            
            The format is very similar to the results of getClusterJSON, so that it can readily be drawn using charting tools
            
            Returns a python dict corresponding to the following JSON example
            {
              "nodes": [
                {"id": "Myriel", "group": 1},
                {"id": "Napoleon", "group": 1}
              ],
              "links": [
                {"source": "Napoleon", "target": "Myriel", "value": 1},
                {"source": "Mlle.Baptistine", "target": "Myriel", "value": 8}
              ]
            }
        """
        method = moduleName + '.' +  self.className + '.getTraverseReport'
        timestamp = time.time()
        
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        #no traverse reports for traverse pathgs with wildcards
        if "*" in splitPath:
            ex = "Traverse path %s contains a wildcard (* or **).  It is not possible to create a traverse report for wildcard paths" %splitPath
            raise Exceptions.TemplatePathError(ex)
        
        selfUUIDAsStr = str(self.uuid)
        if excludeCluster is not None:
            excludeCluster.append(selfUUIDAsStr)
        excludeLinks.append(selfUUIDAsStr)
        
        try:
            traverseOrder = {}
            traverseNeighbors = {}
            traverseLinks = []
            runningPath = ''

            #start by building the root node portion (index = "0") of the report
            rootMeme = self.memePath.fullTemplatePath
            rootMetaMeme = self.metaMeme
            rootMemberList = linkRepository.getCounterparts(self.uuid, linkDirectionTypes.BIDIRECTIONAL, [], [], linkType, excludeLinks)
            memberListInbound = linkRepository.getCounterparts(self.uuid, linkDirectionTypes.INBOUND, [], [], linkType, excludeLinks)      
            
            for memID in rootMemberList:
                sMemID = str(memID)
                if memID in memberListInbound:
                    traverseLinks.append({"source": sMemID, "target": selfUUIDAsStr, "value": 1})
                else:
                    traverseLinks.append({"source": selfUUIDAsStr, "target": sMemID, "value": 1})
                rootMember = entityRepository.getEntity(memID)
                memMeme = rootMember.memePath.fullTemplatePath
                memMetaMeme = rootMember.metaMeme
                traverseNeighbors[sMemID] = {"id" : sMemID, "meme" : memMeme, "metaMeme" : memMetaMeme, "position" : "-1"}

            traverseOrder[selfUUIDAsStr] = {"id" : selfUUIDAsStr, "meme" : rootMeme, "metaMeme" : rootMetaMeme, "position" : timestamp} 
            
            #Build up the list of traverse paths
            forwardTraverseJoin = '>>'
            backwardTraverseJoin = '<<'
            polydirectionalTraverseJoin = '::'
            
            if len(splitPath) > 0:
                #pathTraversed == True
            #while (pathTraversed == False):
                #Start by determining whether ot not the we have a leading direction indicator.  
                #If so, then set the direction to search for currPath and then remove the leading linkdir
                soughtPathDirection = linkDirectionTypes.BIDIRECTIONAL #by default
                if splitPath.startswith(forwardTraverseJoin) == True:
                    soughtPathDirection = linkDirectionTypes.OUTBOUND
                    splitPath = splitPath[2:]
                elif splitPath.startswith(backwardTraverseJoin) == True:
                    soughtPathDirection = linkDirectionTypes.INBOUND
                    splitPath = splitPath[2:]
                elif splitPath.startswith(polydirectionalTraverseJoin) == True:
                    splitPath = splitPath[2:]
            
                #determine which traverse direction we have in splitPath
                partitionSequence = polydirectionalTraverseJoin
                lowestIndex = -1
                forwardIndex = -1
                reverseIndex = -1
                polydirectionalIndex = -1
                try:
                    forwardIndex = splitPath.index('>>')
                except: pass
                try:
                    reverseIndex = splitPath.index('<<')
                except: pass
                try:
                    polydirectionalIndex = splitPath.index('::')
                    lowestIndex = polydirectionalIndex
                except: pass
                if (forwardIndex > -1):
                    if (forwardIndex < lowestIndex) or\
                        ((forwardIndex > lowestIndex) and (lowestIndex < 0)):
                        lowestIndex = forwardIndex
                        partitionSequence = forwardTraverseJoin
                if ((reverseIndex > -1) or (reverseIndex == 0)):
                    if (reverseIndex < lowestIndex) or\
                        ((reverseIndex > lowestIndex) and (lowestIndex < 0)):  
                        lowestIndex = reverseIndex
                        partitionSequence = backwardTraverseJoin
                        
                        
                #If forcedContinue is true, we don't bother splitting the path as there was a double wildcard in the recursion history
                #    somewhere.  We'll just accept splitPath as it is.  
                repartitionedSplitPath = splitPath.partition(partitionSequence)
                runningPath = "%s%s%s" %(runningPath, partitionSequence, repartitionedSplitPath[0])
                if ((len(repartitionedSplitPath[2]) > 0) and (len(repartitionedSplitPath[1]) > 0)):
                    splitPath = "%s%s" %(repartitionedSplitPath[1], repartitionedSplitPath[2])
                else:
                    splitPath = repartitionedSplitPath[2]
                currentPathFragment = repartitionedSplitPath[0]
                    
                        
                #Peel off the parameter filters from currentPathFragment
                linkParams, nodeParams = self.getTraverseFilters(currentPathFragment)
                reOuterParentheses  = re.compile(r"\((.+)\)")
                reInnerBrackets = re.compile(r"\[([^]]*)\]")
        
                #strip of the bits inside parenthesis and brackets
                currentPathFragment = re.sub(reOuterParentheses, '', currentPathFragment)
                currentPathFragment = re.sub(reInnerBrackets, '', currentPathFragment)
                    
                try:
                    if (currentPathFragment is not None) and (len(currentPathFragment) > 0):
                        if isMeme == True:
                            try:
                                soughtPath = templateRepository.resolveTemplate(self.memePath, currentPathFragment, True)
                            except Exceptions.TemplatePathError as e:
                                errorMsg = "Failed to resolve path relative to %s.  Nested Traceback = %s" %(self.memePath, e)
                                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                                raise e                         
                        else:
                            #We only the fullPemplatePath attribute of the entity, not the actual path pointer
                            metaMeme = templateRepository.resolveTemplateAbsolutely(self.metaMeme)
                            soughtPath = templateRepository.resolveTemplate(metaMeme.path, currentPathFragment, True)
                except Exception as e:
                    errorMsg = "Failed to resolve path relative to %s.  Nested Traceback = %s" %(self.memePath, e)
                    logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                    raise e            
        
                try:
                    #linkDirectionTypes.BIDIRECTIONAL, '', None, linkAttributeOperatorTypes.EQUAL
                    members = linkRepository.getCounterparts(self.uuid, soughtPathDirection, linkParams, nodeParams, linkType, excludeLinks)
                    
                    if excludeCluster is not None:
                        #we need to make sure that we don't backtrack, so filter the exclude list
                        memberSet = set(members)
                        excludeSet = set(excludeCluster)
                        memberSet.difference_update(excludeSet)
                        members = list(memberSet)
                
                    for memberEntityID in members:
                        member = entityRepository.getEntity(memberEntityID)
                        if ((isMeme == True) and\
                            (str(memberEntityID) not in excludeLinks) and\
                            (member.memePath.fullTemplatePath == soughtPath.path.fullTemplatePath)) or (member.metaMeme == soughtPath.path.fullTemplatePath):
                            if len(splitPath) > 0:
                                partialLinks, partialNodes, partialTraverseOrder = member.getTraverseReport(splitPath, isMeme, linkType, excludeLinks, returnUniqueValuesOnly, excludeCluster)
                                traverseLinks.extend(partialLinks) 
                                traverseOrder.update(partialTraverseOrder)
                                traverseNeighbors.update(partialNodes)
                            else:
                                partialLinks, partialNodes, partialTraverseOrder = member.getTraverseReport("", isMeme, linkType, excludeLinks, returnUniqueValuesOnly, excludeCluster)
                                traverseLinks.extend(partialLinks) 
                                traverseOrder.update(partialTraverseOrder)
                                traverseNeighbors.update(partialNodes)
                
                except KeyError as e:
                    #self.getLinkedEntitiesByTemplateType(oldSplitPath, isMeme, linkType, forcedContinue, excludeLinks, returnUniqueValuesOnly, excludeCluster)
                    pass
                except Exception as e:
                    #logQ.put( [logType , logLevel.DEBUG , method , "Failure getting linked entities.  Traceback = %s" %e])
                    pass
                                                
        except Exception as e:
            ex = "Function getHasLinkedEntityByMemeType failed.  Traceback = %s" %e
            #raise Exceptions.ScriptError(ex)
        return traverseLinks, traverseNeighbors, traverseOrder


    #Todo - update the method with the getCounterparts
    def getLinkedEntitiesByTemplateType(self, splitPath, isMeme, linkType = 0, forcedContinue = False, excludeLinks = [], returnUniqueValuesOnly = True, excludeCluster = []):
        """ This is a critically important method for finding associated (linked) entities.  It parses the
            link path and follows each step of the path in turn by a recursive call.  
            
            It also handles single star and double star wildcards.
            * (single star) - is a one step wildcard.  The recursive call will be made on every counterpart of the current step.
                Use this wildard if you know how many steps are required to get to a particular entity, but not the intermediate
                templates (meme or metameme).
            ** (double star) - this is a multistep wildcard.  The recursive call will be made as many times as needed to get to
                the first entity that matches the pattern after the double star.  E.g. '**::SomeTemplate' would result in
                recursive calls to scour entity links until 'SomeTemplate' is found. 
                
            path - the link path (in link path syntax) of sought entity's meme or metameme.
            
            isMeme - this boolean determines whether we compare the memePath or metaMeme properties of the entities
            
            linkTypes - the entity link type
            
            maxDOS - the allowed number of degrees and it is decrimented with every recursive call.  It is a hackish way of 
                preventing endless loops with circular link patterns.  Later, a better method will be needed.
                
            
            forcedContinue - If a double wildcard turns up in currentPathFragment (see below), then we have a wildcard search
                with an unknown number of degrees of seperation.  If this is true, we'll pass the recursion to every link 
                with a forced continue until we get our entity
                
            returnUniqueValuesOnly - I set to True, this method will filter returnlist duplicates.
            
            excludeCluster - This is an option for increasing performance on traverses; at the potential cost of fidelity.  
                If this paramter is a list and not None, whenerver we traverse entity 1+n in a cluster, we can never cross
                back over an entity that we already traversed.
        """
        method = moduleName + '.' +  self.className + '.getLinkedEntitiesByTemplateType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        selfUUIDAsStr = str(self.uuid)
        if excludeCluster is not None:
            excludeCluster.append(selfUUIDAsStr)
        
        #Debug aid- Only used for logging in the event of a KeyError exception
        oldSplitPath = copy.deepcopy(splitPath)

        returnMembers = []
        soughtPath = None
        currentPathFragment = None
        
        forwardTraverseJoin = '>>'
        backwardTraverseJoin = '<<'
        polydirectionalTraverseJoin = '::'
        
        #Start by determining whether ot not the we have a leading direction indicator.  
        #If so, then set the direction to search for currPath and then remove the leading linkdir
        soughtPathDirection = linkDirectionTypes.BIDIRECTIONAL #by default
        if splitPath.startswith(forwardTraverseJoin) == True:
            soughtPathDirection = linkDirectionTypes.OUTBOUND
            splitPath = splitPath[2:]
        elif splitPath.startswith(backwardTraverseJoin) == True:
            soughtPathDirection = linkDirectionTypes.INBOUND
            splitPath = splitPath[2:]
        elif splitPath.startswith(polydirectionalTraverseJoin) == True:
            splitPath = splitPath[2:]
    
        #determine which traverse direction we have in splitPath
        partitionSequence = polydirectionalTraverseJoin
        lowestIndex = -1
        forwardIndex = -1
        reverseIndex = -1
        polydirectionalIndex = -1
        try:
            forwardIndex = splitPath.index('>>')
        except: pass
        try:
            reverseIndex = splitPath.index('<<')
        except: pass
        try:
            polydirectionalIndex = splitPath.index('::')
            lowestIndex = polydirectionalIndex
        except: pass
        if (forwardIndex > -1):
            if (forwardIndex < lowestIndex) or\
                ((forwardIndex > lowestIndex) and (lowestIndex < 0)):
                lowestIndex = forwardIndex
                partitionSequence = forwardTraverseJoin
        if ((reverseIndex > -1) or (reverseIndex == 0)):
            if (reverseIndex < lowestIndex) or\
                ((reverseIndex > lowestIndex) and (lowestIndex < 0)):  
                lowestIndex = reverseIndex
                partitionSequence = backwardTraverseJoin
                
                
        #If forcedContinue is true, we don't bother splitting the path as there was a double wildcard in the recursion history
        #    somewhere.  We'll just accept splitPath as it is.  
        if forcedContinue == False:
            repartitionedSplitPath = splitPath.partition(partitionSequence)
            currentPathFragment = repartitionedSplitPath[0]
            if ((len(repartitionedSplitPath[2]) > 0) and (len(repartitionedSplitPath[1]) > 0)):
                splitPath = "%s%s" %(repartitionedSplitPath[1], repartitionedSplitPath[2])
            else:
                splitPath = repartitionedSplitPath[2]
                
        #Peel off the parameter filters from currentPathFragment
        linkParams, nodeParams = self.getTraverseFilters(currentPathFragment)
        reOuterParentheses  = re.compile(r"\((.+)\)")
        reInnerBrackets = re.compile(r"\[([^]]*)\]")

        #strip of the bits inside parenthesis and brackets
        currentPathFragment = re.sub(reOuterParentheses, '', currentPathFragment)
        currentPathFragment = re.sub(reInnerBrackets, '', currentPathFragment)
            
        # If currentPathFragment is a double wildcard, turn on forcedContinue    
        if currentPathFragment == "**":
            forcedContinue = True
        
        # If currentPathFragment is a wildcard, don't bother trying to resolve soughtPath as we're not trying to resolve
        #    anything in this step.  Soughtpath is the template path of the next child in the link tree.  
        # If currentPathFragment is a single wildcard, then we will examine all children on this step.
        # If forcedContinue is True, then we are trying to resolve a soughtPath in any case because we don't know how many
        #    degrees of seperation we have.
        # If we lead with a unidirectional directional relationship, handle appropriately (see below)  
        if (forcedContinue == True) or (currentPathFragment != "*"):
            try:
                if isMeme == True:
                    try:
                        soughtPath = templateRepository.resolveTemplate(self.memePath, currentPathFragment, True)
                    except Exceptions.TemplatePathError as e:
                        if forcedContinue == False:
                            errorMsg = "Failed to resolve path relative to %s.  Nested Traceback = %s" %(self.memePath, e)
                            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                            raise e                         
                else:
                    #We only the fullPemplatePath attribute of the entity, not the actual path pointer
                    metaMeme = templateRepository.resolveTemplateAbsolutely(self.metaMeme)
                    soughtPath = templateRepository.resolveTemplate(metaMeme.path, currentPathFragment, True)
            except Exception as e:
                if forcedContinue == False:
                    errorMsg = "Failed to resolve path relative to %s.  Nested Traceback = %s" %(self.memePath, e)
                    logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                    raise e            

        try:
            #linkDirectionTypes.BIDIRECTIONAL, '', None, linkAttributeOperatorTypes.EQUAL
            members = linkRepository.getCounterparts(self.uuid, soughtPathDirection, linkParams, nodeParams, linkType, excludeLinks)
            
            if excludeCluster is not None:
                #we need to make sure that we don't backtrack, so filter the exclude list
                memberSet = set(members)
                excludeSet = set(excludeCluster)
                memberSet.difference_update(excludeSet)
                members = list(memberSet)
            
            if (oldSplitPath == "*") and (splitPath == ""):
                #We have a wildcard end effector on the traverse path.  Just return members and be done with it
                returnMembers = members
            else:
                newExcludeLinks = self.getLinkIDs()
                excludeLinks.extend(newExcludeLinks)
            
                for memberEntityID in members:
                    member = entityRepository.getEntity(memberEntityID)
                    isSingleton = member.getIsSingleton()
                    if soughtPath is not None:
                        #we are searching for a specific template
                        if ((isMeme == True) and (member.memePath.fullTemplatePath == soughtPath.path.fullTemplatePath)) or\
                            (member.metaMeme == soughtPath.path.fullTemplatePath):
                            if len(splitPath) > 0:
                                #splitPath, isMeme, linkType = 0, forcedContinue = False, excludeLinks = []
                                partialRet = member.getLinkedEntitiesByTemplateType(splitPath, isMeme, linkType, False, excludeLinks, returnUniqueValuesOnly, excludeCluster)
                                returnMembers.extend(partialRet)
                            else:
                                returnMembers.append(member.uuid)   
                        if (forcedContinue == True) and (isSingleton == False):
                            partialRet = member.getLinkedEntitiesByTemplateType(splitPath, isMeme, linkType, forcedContinue, excludeLinks, returnUniqueValuesOnly, excludeCluster)
                            returnMembers.extend(partialRet)                      
                    else:
                        #currentPathFragment is a wildcard.  Therefore soughtPath is None 
                        #    In ths case, we follow ALL the rabbit holes looking for our next hit, but with forcedContinue turned off
                        partialRet = member.getLinkedEntitiesByTemplateType(splitPath, isMeme, linkType, False, excludeLinks, returnUniqueValuesOnly, excludeCluster)
                        returnMembers.extend(partialRet)
        
        except KeyError as e:
            #self.getLinkedEntitiesByTemplateType(oldSplitPath, isMeme, linkType, forcedContinue, excludeLinks, returnUniqueValuesOnly, excludeCluster)
            pass
        except Exception as e:
            #logQ.put( [logType , logLevel.DEBUG , method , "Failure getting linked entities.  Traceback = %s" %e])
            pass
                                        
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        if returnUniqueValuesOnly == True:
            streamlinedReturnMembers = filterListDuplicates(returnMembers)
            return streamlinedReturnMembers
        else:
            return returnMembers
        


    #Todo - propogate the method additions to the script acade
    def getLinkedEntityByMemeTag(self, tag, memBershipType = 0, direction = linkDirectionTypes.BIDIRECTIONAL):
        """  """
        #method = moduleName + '.' +  self.className + '.getMemberEntiesByType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        returnMembers = []
        members = linkRepository.getCounterparts(self.uuid, direction, '', None, linkAttributeOperatorTypes.EQUAL, memBershipType)
        for memberEntityID in members:
            member = entityRepository.getEntity(memberEntityID)
            member = entityRepository.getEntity(uuid)
            for entityTag in member.tags:
                if entityTag == tag:
                    returnMembers.append(member.uuid)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnMembers
        
        
    def addDecimalProperty(self, name, value, constrained = None, restMin = None, restMax = None, restList = None, memePath = None):
        """ A method for adding ad hoc properties after entity creation """
        #method = moduleName + '.' +  self.className + '.addIntegerProperty'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        if self.getHasProperty(name) != True:
            decValue = decimal.Decimal(value)  
            newprop = EntityProperty(name, decValue, entityPropTypes.Decimal, constrained, restMin, restMax, restList, memePath)
            self.properties[name] = newprop 
            
            #If self is not archived in an Entity table pickle column
            global entityRepository
            if self.getThreadable() == True: 
                entityRepository.addEntityDecimalProperty(self.uuid, name, value, memePath, restMin, restMax, restList)
                             
        else:
            try:
                assert name not in self.properties
            except AssertionError:
                e = "Property %s already exists in %s entity %s" %(name, self.memePath, self.uuid)
                #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with errors"])
                raise Exceptions.EntityPropertyDuplicateError(e) 
        
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])


    def addIntegerProperty(self, name, value, constrained = None, restMin = None, restMax = None, restList = None, memePath = None):
        """ A method for adding ad hoc properties after entity creation """
        #method = moduleName + '.' +  self.className + '.addIntegerProperty'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        if self.getHasProperty(name) != True:
            intValue = int(value)  
            newprop = EntityProperty(name, intValue, entityPropTypes.Integer, constrained, restMin, restMax, restList, memePath)
            self.properties[name] = newprop 
            
            #If self is not archived in an Entity table pickle column
            global entityRepository
            if self.getThreadable() == True:  
                entityRepository.addEntityIntegerProperty(self.uuid, name, value, memePath, restMin, restMax, restList)             
        else:
            e = "Property %s already exists in %s entity %s" %(name, self.memePath, self.uuid)
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with errors"])
            raise Exceptions.EntityPropertyDuplicateError(e)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    def addListProperty(self, name, value, constrained = None, restMin = None, restMax = None, restList = None, memePath = None):
        """ A method for adding ad hoc properties after entity creation """
        #method = moduleName + '.' +  self.className + '.addIntegerProperty'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        if self.getHasProperty(name) != True:
            try:
                valList = []
                unicodeString = ''
                asciiString = ''
                try:
                    #if propValue is a string, parse it on commas
                    if type(value) == type(asciiString):
                        partitionSequence = ','
                        preValues = value.partition(partitionSequence)
                        stripper = {}
                        for valueElement in preValues:
                            stripper[valueElement] = valueElement
                        del stripper[partitionSequence]
                        value = []
                        for stripperVal in stripper.keys():
                            value.append(stripperVal)
                    elif type(value) == type(unicodeString):
                        partitionSequence = ','
                        preValues = value.partition(partitionSequence)
                        stripper = {}
                        for valueElement in preValues:
                            stripper[valueElement] = valueElement
                        del stripper[partitionSequence]
                        value = []
                        for stripperVal in stripper.keys():
                            value.append(stripperVal)
                except: pass # propValue is not a string
                for val in value:
                    if len(val) > 0:
                        valList.append(val)
                newprop = EntityProperty(name, value, entityPropTypes.List, constrained, restMin, restMax, restList, memePath)
                self.properties[name] = newprop 
                
                """
                deprecated, todo - delete
                #If self is not archived in an Entity table pickle column
                global entityRepository
                if self.getThreadable() == True:  
                    entityRepository.addEntityLinkProperty(self.uuid, name, value, memePath)
                """
            except Exception as e:
                e = "List Property %s can't be added to %s entity %s.  Proposed value %s is not iterable.  Traceback = %s" %(name, self.memePath, self.uuid, value, e)
                #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with error"])
                raise Exceptions.EntityPropertyValueTypeError(e)            
        else:
            try:
                assert name not in self.properties
            except AssertionError:
                e = "Property %s already exists in %s entity %s" %(name, self.memePath, self.uuid)
                #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with errors"])
                raise Exceptions.EntityPropertyDuplicateError(e)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])

        
    def addStringProperty(self, name, value, constrained = None, restMin = None, restMax = None, restList = None, memePath = None):
        """ A method for adding ad hoc properties after entity creation """
        #method = moduleName + '.' +  self.className + '.addStringProperty'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        if self.getHasProperty(name) != True:
            stringValue = str(value) 
            newprop = EntityProperty(name, stringValue, entityPropTypes.String, constrained, restMin, restMax, restList, memePath)
            self.properties[name] = newprop 
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])   
            
            #If self is not archived in an Entity table pickle column
            global entityRepository
            if self.getThreadable() == True:  
                entityRepository.addEntityStringProperty(self.uuid, name, value, memePath, restList)      
        else:
            try:
                assert name not in self.properties
            except AssertionError:
                e = "Property %s already exists in %s entity %s" %(name, self.memePath, self.uuid)
                #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with errors"])
                raise Exceptions.EntityPropertyDuplicateError(e)


    def addBooleanProperty(self, name, value, constrained = None, restMin = None, restMax = None, restList = None, memePath = None):
        """ A method for adding ad hoc properties after entity creation """
        #method = moduleName + '.' +  self.className + '.addBooleanProperty'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        if self.getHasProperty(name) != True:
            try:
                boolValue = bool(value)  
                newprop = EntityProperty(name, boolValue, entityPropTypes.Boolean, constrained, restMin, restMax, restList, memePath)
                self.properties[name] = newprop
                
                #If self is not archived in an Entity table pickle column
                global entityRepository
                if self.getThreadable() == True: 
                    entityRepository.addEntityBooleanProperty(self.uuid, name, value, memePath)
            except:
                e = "Can't add boolean property %s to %s entity %s.  Unable to cast %s to boolean" %(name, self.memePath, self.uuid, value)
                #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with errors"])
                raise ValueError(e)          
        else:
            try:
                assert name not in self.properties
            except AssertionError:
                e = "Property %s already exists in %s entity %s" %(name, self.memePath, self.uuid)
                #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with errors"])
                raise Exceptions.EntityPropertyDuplicateError(e)
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    def getHasProperty(self, fullPropPath):
        """  Test whether self has the prescribed property 
        The rightmost segment in the rightmost path will be the sought after property.
        The leftmost segment in the leftmost path *might* be the metameme name of the entity  
        """
        #method = moduleName + '.' +  self.className + '.getHasProperty'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        hasProperty = False
        partitionSequence = '.'
        splitPropPath = fullPropPath.rpartition(partitionSequence)
        
        #Just peel off the very last entry after the last dot.  It is our property name
        if splitPropPath[0] == '':
            try:
                assert fullPropPath in self.properties
                hasProperty = True 
            except AssertionError:
                pass
        else:
            #if there is a tuple and an entry for splitPropPath[2], then we can find the entity
            #    associated with splitPropPath[0]
            memberEntityIDList = self.getLinkedEntitiesByMemeType(splitPropPath[0], None, None) 
            for memberEntityID in memberEntityIDList:
                memberEntity = entityRepository.getEntity(memberEntityID)
                try:
                    assert splitPropPath[2] in memberEntity.properties
                    hasProperty = True
                except AssertionError:
                    pass 
              
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return hasProperty


    def getPropertyType(self, fullPropPath):
        """ returns the value of propertyName.  Returns None if it does not exist """
        #method = moduleName + '.' +  self.className + '.getPropertyValue'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        returnType = ""
        
        partitionSequence = '.'
        splitPropPath = fullPropPath.rpartition(partitionSequence)
        
        prop = None
        #Just peel off the very last entry after the last dot.  It is our property name
        if splitPropPath[0] == '':
            prop = self.properties[fullPropPath] 
        else:
            #if there is a tuple and an entry for splitPropPath[2], then we can find the entity
            #    associated with splitPropPath[0]
            memberEntityIDList = self.getLinkedEntitiesByMemeType(splitPropPath[0], None, None)
            for memberEntityID in memberEntityIDList:
                memberEntity = entityRepository.getEntity(memberEntityID)
                try:
                    prop = memberEntity.properties[splitPropPath[2]]
                except:
                    pass

        try:
            if prop.propertyType == entityPropTypes.String:
                returnType = "String"
            elif prop.propertyType == entityPropTypes.Integer:
                returnType = "Integer"
            elif prop.propertyType == entityPropTypes.Decimal:
                returnType = "Decimal"
            elif prop.propertyType == entityPropTypes.Boolean:
                returnType = "Boolean"
            else:
                returnType = "List"
        except:
            None
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnType
        
        
    def getPropertyValue(self, fullPropPath):
        """ returns the value of propertyName.  Returns None if it does not exist """
        #method = moduleName + '.' +  self.className + '.getPropertyValue'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        value = None
        partitionSequence = '.'
        splitPropPath = fullPropPath.rpartition(partitionSequence)
        
        prop = None
        #Just peel off the very last entry after the last dot.  It is our property name
        if splitPropPath[0] == '':
            if fullPropPath in self.properties:
                prop = self.properties[fullPropPath] 
                try:
                    value = prop.value
                except:
                    value = None
            else:
                errorMsg = "Entity %s of type %s was asked to provide the value of property '%s', but it has no such property" %(self.uuid, self.memePath.fullTemplatePath, fullPropPath)
                raise Exceptions.EntityPropertyMissingValueError(errorMsg)
        else:
            #if there is a tuple and an entry for splitPropPath[2], then we can find the entity
            #    associated with splitPropPath[0]
            memberEntityIDList = self.getLinkedEntitiesByMemeType(splitPropPath[0], None, None)
            for memberEntityID in memberEntityIDList:
                memberEntity = entityRepository.getEntity(memberEntityID)
                try:
                    prop = memberEntity.properties[splitPropPath[2]]
                except:
                    pass
                       
            try:
                value = prop.value
            except:
                pass
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return value
        
        
    def setPropertyValue(self, fullPropPath, value):
        """ Sets the value of an existing property.
        Cast the proposed value to the correct type.  If that can't be done, raise an exception
        If the property does not exist, create it as a string instead of failing """
        method = moduleName + '.' +  self.className + '.setPropertyValue'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        
        partitionSequence = '.'
        splitPropPath = fullPropPath.rpartition(partitionSequence)
        
        #Just peel off the very last entry after the last dot.  It is our property name
        proposedNewValue = []
        if splitPropPath[0] != '':
            targetEntityIDList = self.getLinkedEntitiesByMemeType(splitPropPath[0], None, None)
            for targetEntityID in targetEntityIDList:
                targetEntity = entityRepository.getEntity(targetEntityID)
                returnValue = targetEntity.setPropertyValue(splitPropPath[2], value)
        else:
            if self.getHasProperty(fullPropPath) != True:
                self.addStringProperty(fullPropPath, value)
                templateProperty = self.properties[fullPropPath]
            else:
                templateProperty = self.properties[fullPropPath]
                
            if templateProperty.propertyType == entityPropTypes.List:
                try:
                    for val in value:
                        proposedNewValue.append(val)
                except:
                    proposedNewValue.append(value)
            else:
                try:
                    if templateProperty.propertyType == entityPropTypes.String:
                        if type(value) == 'unicode':
                            proposedNewValue.append(value)
                        else:
                            proposedNewValue.append(str(value))
                    elif templateProperty.propertyType == entityPropTypes.Decimal:
                        proposedNewValue.append(decimal.Decimal(value))
                    elif templateProperty.propertyType == entityPropTypes.Integer:
                        proposedNewValue.append(int(value))   
                    elif templateProperty.propertyType == entityPropTypes.Boolean:
                        prop = False
                        if value.lower() == 'true':
                            prop = True
                        else:
                            try:
                                prop = bool(value)
                            except:
                                prop = False
                        proposedNewValue.append(prop)
                except:
                    e = e = "Can't set value of %s entity %s property %s to %s.  Wrong Type" %(self.memePath, self.uuid, templateProperty.name, value)
                    #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with error"])
                    raise Exceptions.EntityPropertyValueTypeError(e)             
                    
            if (templateProperty.constrained == True) and (templateProperty.propertyType != entityPropTypes.Boolean):
                # test the constraints
                if (templateProperty.restList is not None) and (len(templateProperty.restList) > 0):
                    allInList = True
                    bogusValues = []
                    for propVal in proposedNewValue:
                        inList = False
                        for restriction in templateProperty.restList:
                            if restriction == propVal:
                                inList = True
                        if inList == False:
                            allInList = False
                            bogusValues.append(propVal)
                    if allInList == False:
                        e = "Can't set value of %s entity %s property %s to %s.  It is a constrained property and the following values violate the constraint: %s" %(self.memePath, self.uuid, fullPropPath, value, bogusValues)
                        #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with error"])
                        raise Exceptions.EntityPropertyValueOutOfBoundsError(e)
                else:
                    if templateProperty.restMax is not None:
                        if templateProperty.restMax < proposedNewValue[0]:
                            e = "Can't set value of %s entity %s property %s to %s.  It is a constrained property and new value is greater than the allowed max of %s" %(self.memePath, self.uuid, templateProperty.name, value, templateProperty.restMax)
                            #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with error"])
                            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)   
                    if templateProperty.restMin is not None:
                        if templateProperty.restMin > proposedNewValue[0]:
                            e = "Can't set value of %s entity %s property %s to %s.  It is a constrained property and new value is less than the allowed min of %s" %(self.memePath, self.uuid, templateProperty.name, value, templateProperty.restMin)
                            #logQ.put( [logType , logLevel.DEBUG , method , "exiting - with error"])
                            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)  
                
            # if we can cast the value and no exceptions have been raised due to constraints,
            #    then go ahead and set the value
            # If it is not a list, then property.value will have a length of 0 or 1, depending on whether it has a value or not
            oldValue = copy.copy(templateProperty.value)  #When firing propertyChanged events, we pass both the old and new values
            stringID = "%s" %self.uuid
            params = {'oldVal' : oldValue, 'entityID' : stringID}
            returnValue = None
            if templateProperty.propertyType == entityPropTypes.List:
                try:
                    params['newVal'] = proposedNewValue
                    if fullPropPath in self.propertyChangeEvents:
                        ses = self.propertyChangeEvents[fullPropPath]
                        returnValue = ses.execute(self.uuid, params)
                        unusedCatch = "me"
                except Exception as e:
                    templateProperty.value = []
                    fullerror = sys.exc_info()
                    errorID = str(fullerror[0])
                    errorMsg = str(fullerror[1])
                    tb = sys.exc_info()[2]
                    try:
                        scriptLoc = getScriptLocation(params[0], "propertyChanged")
                    except Exception as e:
                        innerFullerror = sys.exc_info()
                        innerErrorMsg = str(innerFullerror[1])
                        scriptLoc = "UNKNOWN LOCATION ((%s))" %innerErrorMsg                       
                    errorMessage = "EventScriptFailure!  Entity of type %s experienced an error while trying to execute script at %s during propertyChanged event."  %(self.memePath.fullTemplatePath, scriptLoc)
                    errorMessage = "%s  Nested Traceback %s: %s" %(errorMessage, errorID, errorMsg)
                    logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                    raise Exceptions.EventScriptFailure(errorMessage).with_traceback(tb)
            else:
                try:
                    templateProperty.value = proposedNewValue[0]
                    params['newVal'] = proposedNewValue[0]
                    if fullPropPath in self.propertyChangeEvents:
                        ses = self.propertyChangeEvents[fullPropPath]
                        returnValue = ses.execute(self.uuid, params)
                        unusedCatch = "me"
                except Exception as e:
                    templateProperty.value = []
                    fullerror = sys.exc_info()
                    errorID = str(fullerror[0])
                    errorMsg = str(fullerror[1])
                    tb = sys.exc_info()[2]
                    try:
                        scriptLoc = getScriptLocation(params[0], "propertyChanged")
                    except Exception as e:
                        innerFullerror = sys.exc_info()
                        innerErrorMsg = str(innerFullerror[1])
                        scriptLoc = "UNKNOWN LOCATION ((%s))" %innerErrorMsg                         
                    errorMessage = "EventScriptFailure!  Entity of type %s experienced an error while trying to execute script at %s during propertyChanged event."  %(self.memePath.fullTemplatePath, scriptLoc)
                    errorMessage = "%s  Nested Traceback %s: %s" %(errorMessage, errorID, errorMsg)
                    logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                    raise Exceptions.EventScriptFailure(errorMessage).with_traceback(tb)
            return returnValue
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        

    def setStateEventScript(self, scriptLocation, scriptLanguage = "python", state = "execute", propertyID = None):
        """ Set the state event callable object on self.
        scriptLocation = The classpath of the callable object
        scriptLanguage = at the moment, only Python is supported
        Sate = One of the valid values for the restriction Memetic.StateEventType 
        propertyID = If the state is propertyChanged, then the property ID should be passed.
        """
        method = moduleName + '.' +  self.className + '.setStateEventScript'
        logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        if scriptLanguage == "python":
            splitClasspath = scriptLocation.rpartition(".")
            mName = splitClasspath[0]
            cName = splitClasspath[2]
            try:
                mod = Fileutils.getModuleFromResolvedPath(mName)
                tmpClass = getattr(mod, cName)
                function = tmpClass()
                if state == "initialize":
                    self.initScript = function
                elif state == "execute":    
                    self.execScript = function
                elif state == "terminate":    
                    self.terminateScript = function   
                elif state == "linkAdd":    
                    self.linkAdd = function 
                elif state == "linkRemove":    
                    self.linkRemove = function 
                elif state == "propertyChanged":    
                    if propertyID is not None:
                        function.setState(propertyID)
                        self.propertyChangeEvents[propertyID] = function  
                    else:
                        errorMessage = "%s entity unable to initialize propertyChanged state event script %s.%s, as no property has been assigned."  %(self.memePath, mName, cName)
                        raise Exceptions.StateEventScriptInitError(errorMessage)
            except Exception:
                #Build up a full java or C# style stacktrace, so that devs can track down errors in script modules within repositories
                fullerror = sys.exc_info()
                errorID = str(fullerror[0])
                errorMsg = str(fullerror[1])
                tb = sys.exc_info()[2]
                raise Exceptions.StateEventScriptInitError("%s entity unable to aquire state event script %s in module %s.  Nested Traceback %s: %s" %(self.memePath.fullTemplatePath, cName, mName, errorID, errorMsg)).with_traceback(tb)

        else:
            #Note - If any script language is added, this will need to be updated
            ex = "Unsupported script language declaration %s for script at %s" %(scriptLanguage, scriptLocation)
            logQ.put( [logType , logLevel.WARNING , method , ex])
            raise Exceptions.StateEventScriptInitError(ex)
        logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    def installExecutorObject(self, callableObject):
        """ Directly install the self.execScript callable object.
        Useful when the callable object must be initialized and prepared in some way before being executed 
        """    
        method = moduleName + '.' +  self.className + '.installExecutorObject'
        logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        try:
            #assert callable(callableObject)
            self.execScript = callableObject
        except:
            logQ.put( [logType , logLevel.WARNING , method , "Unable to install callable object in entity of type %s" %(self.memePath)]) 
        logQ.put( [logType , logLevel.DEBUG , method , "exiting"])    
        
                
        
    def removeProperty(self, templateProperty):
        """ if the property exists, remove it """
        global persistenceType
        #method = moduleName + '.' +  self.className + '.removeProperty'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        if self.getHasProperty(templateProperty) == True:
            del self.properties[templateProperty]
            
        if (persistenceType != "none"): 
            #if we are using persistence, then we need to make sure that the archive entity also get's the property removed    
            if self.getThreadable() == True: 
                #Then tell the repo to remove the table records and update the archive entity
                entityRepository.removeProperty(self.uuid, templateProperty)
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])

        
        




########################
# Start Script handlers
########################

class createEntityFromMeme(object):
    #createEntityFromMeme params = [entityUUID, runtimeVariables, ActionID, Subject, Controller, supressInit]
    #five params: memePath, ActionID = None, Subject = None, Controller = None, supressInit = False
    def execute(self, params):
        try:
            meme = templateRepository.resolveTemplateAbsolutely(params[0])
            entityID = meme.getEntityFromMeme()
            entity = entityRepository.getEntity(entityID)
            #entity.entityLock.acquire(True)
            
            try:
                #todo - wtf?  params[4]?
                if params[4] == False:
                    entity.initialize()
            except Exceptions.StateEventScriptInitError as e:
                raise e
            except Exception as e:
                ex = "Unable to init entity %s of type %s.  Traceback = %s" %(entityID, entity.memePath.fullTemplatePath, e)
                #debug
                #entity.isInitialized = False
                #entity.initialize()
                '''
                try:
                    meme = templateRepository.resolveTemplateAbsolutely(params[0])
                    entityID = meme.getEntityFromMeme()
                    entity = entityRepository.getEntity(entityID)
                    entity.entityLock.acquire(True)
                    
                    try:
                        #todo - wtf?  params[4]?
                        if params[4] == False:
                            entity.initialize()
                    except Exception as e:
                        pass
                except Exception as e:
                    pass
                '''
                raise Exceptions.ScriptError(ex)
    
            return entityID
        except Exception as e:
            raise e


    
    
class execStateEventScript(object):
    ''' A useful function for editors that wish to test state event scripts for entities '''
    #one params: entityUUID, stateEvenScriptID, params
    def execute(self, params, supressInit = False):
        param = params[0]
        entityClass = getEntity()
        entity = entityClass.execute([param])
        
        returnVal = None # by default, we assume that the script is not present

        entity.entityLock.acquire(True)
        
        try:
            testMe = False
            if (params[1] == 0):
                try:
                    if entity.initScript is not None: testMe = True
                except: return returnVal #no init script installed
                if testMe == True:
                    entity.initialize()
                    returnVal = True
            elif (params[1] == 1):
                try:
                    if entity.execScript is not None: testMe = True
                except: return returnVal #no init script installed
                if testMe == True:
                    returnVal = entity.execScript.execute(params)
            elif (params[1] == 2):
                try:
                    if entity.terminateScript is not None: testMe = True
                except: return returnVal #no terminate script installed
                if testMe == True:
                    returnVal = entity.terminateScript.execute(params)
            else:
                errorMsg = "%s is not a valid state event script ID"
                raise Exceptions.ScriptError(errorMsg)
        except Exception as e:
            ses = None
            try:
                ses = params[1]
            except:
                pass
            ex = "Unable to execute state event script %s on entity %s of type %s.  Traceback = %s" %(ses, entity.uuid, entity.memePath.fullTemplatePath, e)
            raise Exceptions.ScriptError(ex)
        finally:
            entity.entityLock.release()
        return returnVal
    

class getIsMemeSingleton(object):
    ''' One params: full template path'''
    def execute(self, params):
        isSingleton = False
        try:
            meme = templateRepository.resolveTemplateAbsolutely(params[0])
            if meme is not None:
                isSingleton = meme.isSingleton
        except Exception as e:
            ex = "Function getIsMemeSingleton failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return isSingleton


class getMemeExists(object):
    ''' One params: full template path'''
    def execute(self, params):
        exists = False
        try:
            meme = templateRepository.resolveTemplateAbsolutely(params[0])
            if meme is not None:
                exists = True
        except Exception as e:
            ex = "Function getMemeExists failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return exists
    
    
    
class addEntityDecimalProperty(object):
    ''' Three params: entity, name, value'''
    def execute(self, params):
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.addDecimalProperty(params[1], params[2])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function addEntityDecimalProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None


class addEntityIntegerProperty(object):
    ''' Three params: entity, name, value'''
    def execute(self, params):
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.addIntegerProperty(params[1], params[2])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function addEntityIntegerProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None


class addEntityListProperty(object):
    ''' Three params: entity, name, value'''
    def execute(self, params):
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.addListProperty(params[1], params[2])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function addEntityListProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None
    

class addEntityStringProperty(object):
    ''' Three params: entity, name, value'''
    def execute(self, params):
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.addStringProperty(params[1], params[2])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function addEntityStringProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None
    
    
class addEntityBooleanProperty(object):
    ''' Three params: entity, name, value'''
    def execute(self, params):
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.addBooleanProperty(params[1], params[2])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function addEntityBooleanProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None


class addEntityTaxonomy(object):
    def execute(self, params):
        #ToDo -
        return None

class addEntityLink(object):
    ''' Three params: entityUUID1, entityUUID2, linkAttributes = {}, linkType = linkTypes.ATOMIC'''
    #ToDo: add paremeter dict as param[3]
    def execute(self, params):
        method = moduleName + '.' +  'addEntityLink' + '.execute'
        returnArray = []
        try:
            entity0 = entityRepository.getEntity(params[0])
            entity1 = entityRepository.getEntity(params[1])
            if (entity0.depricated != True) and (entity1.depricated != True):
                entity0.entityLock.acquire(True)
                entity1.entityLock.acquire(True)
                try:
                    linkRepository.catalogLink(params[0], params[1], params[3], params[2])
                    
                    #Fire Link Event for both entity0 and entity1, if one exists
                    linkParams = {"sourceEntityID" : params[0], "targetEntityID" : params[1], "membershipType" : params[3], "linkAttributes": params[2]}
                    if hasattr(entity0, 'linkAdd'):
                        try:
                            sesScriptReturn = entity0.linkAdd.execute(params[0], linkParams)
                            returnArray.append(sesScriptReturn)
                        except Exception as e:
                            fullerror = sys.exc_info()
                            errorID = str(fullerror[0])
                            errorMsg = str(fullerror[1])
                            tb = sys.exc_info()[2]
                            try:
                                scriptLoc = getScriptLocation(params[0], "linkAdd")
                            except Exception as e:
                                innerFullerror = sys.exc_info()
                                innerErrorMsg = str(innerFullerror[1])
                                scriptLoc = "UNKNOWN LOCATION ((%s))" %innerErrorMsg 
                            errorMessage = "EventScriptFailure!  Entity of type %s experienced an error while trying to execute script at %s during linkAdd event."  %(entity0.memePath.fullTemplatePath, scriptLoc)
                            errorMessage = "%s  Entity is source.  Membership type = %s.  linkAttributes = %s" %(errorMessage, params[3], params[2])
                            errorMessage = "%s  Nested Traceback %s: %s" %(errorMessage, errorID, errorMsg)
                            logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                            raise Exceptions.EventScriptFailure(errorMessage).with_traceback(tb)
                    else:
                        returnArray.append(None)
                    if hasattr(entity1, 'linkAdd'):
                        try:
                            sesScriptReturn = entity1.linkAdd.execute(params[1], linkParams)
                            returnArray.append(sesScriptReturn)
                        except Exception as e:
                            fullerror = sys.exc_info()
                            errorID = str(fullerror[0])
                            errorMsg = str(fullerror[1])
                            tb = sys.exc_info()[2]
                            try:
                                scriptLoc = getScriptLocation(params[1], "linkAdd")
                            except Exception as e:
                                innerFullerror = sys.exc_info()
                                innerErrorMsg = str(innerFullerror[1])
                                scriptLoc = "UNKNOWN LOCATION ((%s))" %innerErrorMsg 
                            errorMessage = "EventScriptFailure!  Entity of type %s experienced an error while trying to execute script at %s during linkAdd event."  %(entity0.memePath.fullTemplatePath, scriptLoc)
                            errorMessage = "%s  Entity is target.  Membership type = %s.  linkAttributes = %s" %(errorMessage, params[3], params[2])
                            errorMessage = "%s  Nested Traceback %s: %s" %(errorMessage, errorID, errorMsg)
                            logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                            raise Exceptions.EventScriptFailure(errorMessage).with_traceback(tb)
                    else:
                        returnArray.append(None) 
                except Exceptions.EventScriptFailure as e:
                    raise e      
                except Exception as e:
                    raise e                
                finally:
                    entity0.entityLock.release()
                    entity1.entityLock.release()
            elif (entity0.depricated == True) and (entity1.depricated == True):
                ex = "Both reference source entity %s and source entity %s have been archived and are no longer available" %(params[0], params[1])
                raise Exceptions.EntityLinkFailureError(ex)               
            elif entity0.depricated == True:
                ex = "Reference source entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.EntityLinkFailureError(ex)
            else:
                ex = "Reference target entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.EntityLinkFailureError(ex)
        except Exceptions.EventScriptFailure as e:
            raise e
        except Exception as e:
            ex = "Function addEntityLink failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return returnArray
    


class destroyEntity(object):
    ''' Two params: entity, drillDown (optional, default True)'''
    def execute(self, params):
        method = moduleName + '.' +  'destroyEntity' + '.execute'
        global entityRepository
        
        drillDown = True
        if len(params) == 2:
            drillDown = params[1]
        try:
            returnData = None
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entityID = "%s" %entity.uuid
                    if hasattr(entity, 'terminateScript'):
                        if entity.terminateScript is not None:
                            try:
                                returnData = entity.terminateScript.execute(entity.uuid, {})
                            except Exception as e:
                                fullerror = sys.exc_info()
                                errorID = str(fullerror[0])
                                errorMsg = str(fullerror[1])
                                tb = sys.exc_info()[2]
                                try:
                                    scriptLoc = getScriptLocation(entityID, "terminateScript")
                                except Exception as e:
                                    innerFullerror = sys.exc_info()
                                    innerErrorMsg = str(innerFullerror[1])
                                    scriptLoc = "UNKNOWN LOCATION ((%s))" %innerErrorMsg 
                                errorMessage = "EventScriptFailure!  Entity of type %s experienced an error while trying to execute script at %s during destroyEntity event."  %(entity.memePath.fullTemplatePath, scriptLoc)
                                errorMessage = "%s  Nested Traceback %s: %s" %(errorMessage, errorID, errorMsg)
                                logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                                raise Exceptions.EventScriptFailure(errorMessage).with_traceback(tb)
                    
                    nearestNeighbors = api.getLinkCounterpartsByType(params[0], "*")
                    
                    # depricate the entity
                    entity.depricated = True

                    for nearestNeighbor in nearestNeighbors:
                        # Dirty Hack Alert!
                        # This is a bit clumsy and wastes clock cycles, trying to remove links that may not even be there.
                        #  Trying to remove non-existant links raises an exception and we just bury them with a pass.
                        #  To fix it, we need to seperate the methods in the persistence driver modules into a discovery phase,
                        #    which determines which links to delete and a seperated link deletion phase.
                        #  #PossiblePreformanceIssue
                        try:
                            api.removeEntityLink(params[0], nearestNeighbor)
                        except IndexError as e:
                            pass
                        except Exception as e:
                            raise e
                        
                        try:
                            api.removeEntityLink(nearestNeighbor, params[1])
                        except IndexError as e:
                            pass
                        except Exception as e:
                            raise e
                    
                    if drillDown == True:
                        #Do the same for the children
                        if hasattr(entity, 'memberEntities'):
                            for memberEntityEntry in entity.memberEntities:
                                memberEntityID = memberEntityEntry[0]
                                destroyer = destroyEntity()
                                destroyer.execute([memberEntityID, True])
                    
                    entity.entityLock.release()
                    entityRepository.removeEntity(params[0])            
                except Exception as e:
                    raise e                


            else:
                ex = "Entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.ScriptError(ex)
            return returnData
        except Exception as e:
            ex = "Function destroyEntity failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)


class getAllEntitiesByTag(object):
    ''' Three params: entity, uuid, zone.
        zone is optional'''
    def execute(self, params):
        entities = []
        zone = None
        try:
            zone = params[2]
        except: pass
        try:
            entities = entityRepository.getEntitiesByTag(params[2], zone)
        except Exception as e:
            ex = "Function getAllEntitiesByTag failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return entities
    


class getAllEntitiesByTaxonomy(object):
    def execute(self, params):
        try:
            entities = entityRepository.getEntitiesByMetaMemeType(params[0])
            return entities
        except KeyError as e:
            singletonTester = getIsMemeSingleton()
            isSingleton = singletonTester.execute([params[0]])
            if isSingleton == True:
                entityFactory = createEntityFromMeme()
                entityID = entityFactory.execute(params)
                entity = entityRepository.getEntity(entityID)
                return entity
            else:
                raise e
        except Exception as e:
            raise e  


class getEntitiesByMemeType(object):
    def execute(self, params):
        try:
            entities = entityRepository.getEntitiesByType(params[0])
            return entities
        except KeyError as e:
            singletonTester = getIsMemeSingleton()
            isSingleton = singletonTester.execute([params[0]])
            if isSingleton == True:
                entityFactory = createEntityFromMeme()
                entityID = entityFactory.execute(params)
                entity = entityRepository.getEntity(entityID)
                return entity
            else:
                raise e
        except Exception as e:
            raise e 

class getEntitiesByMetaMemeType(object):
    ''' One Param - Metameme Type as fully resolved string '''
    def execute(self, params):
        try:
            entities = entityRepository.getEntitiesByMetaMemeType(params[0])
            return entities
        except Exceptions.TemplatePathError as e:
            raise e
        except Exception as e:
            raise e    
    
    

class getEntity(object):
    def execute(self, params):
        try:
            entity = entityRepository.getEntity(params[0])
            return entity
        except KeyError as ko:
            try:
                singletonTester = getIsMemeSingleton()
                isSingleton = singletonTester.execute([params[0]])
                if isSingleton == True:
                    entityFactory = createEntityFromMeme()
                    entityID = entityFactory.execute(params)
                    entity = entityRepository.getEntity(entityID)
                    return entity
                else:
                    raise ko
            except Exceptions.ScriptError as e:
                raise Exceptions.NoSuchEntityError()
            except Exception as e:
                raise e
        except Exceptions.ScriptError as e:
            raise e
        except Exception as e:
            raise e
        
        
        
class getAllEntities(object):
    def execute(self):
        global entityRepository
        try:
            entities = entityRepository.getAllEntities()
            return entities
        except Exception as e:
            raise e
                
            
    
    
class getEntityMemeType(object):
    def execute(self, params):
        global entityRepository
        entity = entityRepository.getEntity(params[0])
        memeType = entity.memePath.fullTemplatePath
        return memeType
    
    
class getEntityMetaMemeType(object):
    def execute(self, params):
        entity = entityRepository.getEntity(params[0])
        return entity.metaMeme
    
    
class getMemeMetaMemeType(object):
    def execute(self, params):
        templateRepository.resolveTemplateAbsolutely(params[0])
        entity = entityRepository.getEntity(params[0])
        return entity.metaMeme



class getEntityHasProperty(object):
    ''' Two params: entity, property'''
    def execute(self, params):
        hasMProperty = False
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    hasMProperty = entity.getHasProperty(params[1])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        
        except Exception as e:
            ex = "Function getEntityHasProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return hasMProperty
    

class getEntityPropertyType(object):
    ''' Two params: entity, property'''
    def execute(self, params):
        returnVal = None
        #try:
        entity = entityRepository.getEntity(params[0])
        if entity.depricated != True:
            entity.entityLock.acquire(True)
            try:
                returnVal = entity.getPropertyType(params[1])
            except Exception as e:
                raise e                
            finally:
                entity.entityLock.release()
        else:
            ex = "Entity %s has been archived and is no longer available" %params[0]
            raise Exceptions.ScriptError(ex)
        
        #except Exception as e:
            #ex = "Function getEntityPropertyType failed.  Traceback = %s" %e
            #raise Exceptions.ScriptError(ex)
        return returnVal
    

class getEntityPropertyValue(object):
    ''' Two params: entity, property'''
    def execute(self, params):
        returnVal = None
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    returnVal = entity.getPropertyValue(params[1])
                except Exceptions.EntityPropertyMissingValueError as e:
                    raise e
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        
        except Exception as e:
            fullerror = sys.exc_info()
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            try:
                entity = entityRepository.getEntity(params[0])
                ex = "Function getEntityPropertyValue failed. on entitty of type %s.  Details: (%s, %s, %s, %s, %s).  Traceback = %s" %(entity.memePath.fullTemplatePath, params[0], params[1], params[2], params[3], params[4], errorMsg)
            except Exception as e:
                ex = "Function getEntityPropertyValue failed. on entitty of unknown type.  Details: (%s, %s, %s, %s, %s) .  Possible reason is that entity is not in repository.  Traceback = %s" %(params[0], params[1], params[2], params[3], params[4], errorMsg)   
            raise Exceptions.ScriptError(ex).with_traceback(tb)
        return returnVal
    
    
class getHasCounterpartsByType(object):
    # getLinkCounterpartsByMetaMemeType(self, meme):
    ''' Three params: entity, memePath, linkType'''
    def execute(self, params):
        getLinkCounterpartsByTypeObject = getLinkCounterpartsByType()
        getList = getLinkCounterpartsByTypeObject.execute(params)
        if len(getList) == 0:
            return False
        else:
            return True
        
        
class getHasCounterpartsByMetaMemeType(object):
    # getMemberEntiesByType(self, meme):
    ''' Three params: entity, memePath, linkType'''
    def execute(self, params):
        getLinkCounterpartsByMMTypeObject = getLinkCounterpartsByType()
        getList = getLinkCounterpartsByMMTypeObject.execute(params)
        if len(getList) == 0:
            return False
        else:
            return True
        

class getLinkCounterpartsByType(object):
    # getMemberEntiesByType(self, meme):
    ''' Four params: 
            entity
            memePath
            linkType
            traverseFilters
    '''
    def execute(self, params):
        counterparts = []
        try:
            entity = entityRepository.getEntity(params[0])
            
            linkType = params[2]
            if (params[2] != linkTypes.ALIAS) and (params[2] != linkTypes.ATOMIC) and (params[2] != linkTypes.SUBATOMIC):
                linkType = None
                
            returnUniqueValuesOnly = True
            clusterExcludeList = []
            try:
                clusterExcludeList = params[3]
            except: pass
                
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    isMeme = True
                    try:
                        #This param will be provided when this call is originating in getHasCounterpartsByType
                        isMeme = params[4]
                    except: pass
                    
                    counterparts = entity.getLinkedEntitiesByTemplateType(params[1], isMeme, linkType, False, [], returnUniqueValuesOnly, clusterExcludeList)
                except Exception as e:
                        raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function getHasLinkedEntityByMemeType failed.  Traceback = %s" %e
            #raise Exceptions.ScriptError(ex)
        return counterparts

    
    
class getLinkCounterpartsByMetaMemeType(object):
    # getMemberEntiesByType(self, meme):
    ''' Four params: entity, metaMemePath, linkType, returnUniqueValuesOnly'''
    def execute(self, params):
        counterparts = []
        try:
            entity = entityRepository.getEntity(params[0])
            
            linkType = params[2]
            if (params[2] != linkTypes.ALIAS) and (params[2] != linkTypes.ATOMIC) and (params[2] != linkTypes.SUBATOMIC):
                linkType = None
                
            returnUniqueValuesOnly = True
            try:
                returnUniqueValuesOnly = params[3]
            except: pass
                
            if entity.depricated != True:
                try:
                    entity.entityLock.acquire(True)
                    counterparts = entity.getLinkedEntitiesByMetaMemeType(params[1], linkType, returnUniqueValuesOnly)
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function getHasLinkedEntityByMemeType failed.  Traceback = %s" %e
            #raise Exceptions.ScriptError(ex)
        return counterparts
    


class getTraverseReport(object):
    # getTraverseReport(self, splitPath, isMeme, lthLevel = 0, linkType = 0, excludeLinks = [], returnUniqueValuesOnly = True, excludeCluster = [])(self, meme):
    ''' Four params: 
            entity
            memePath
            linkType
            traverseFilters
    '''
    def execute(self, params):
        counterparts = []
        try:
            entity = entityRepository.getEntity(params[0])
            
            linkType = params[3]
            if (params[3] != linkTypes.ALIAS) and (params[3] != linkTypes.ATOMIC) and (params[3] != linkTypes.SUBATOMIC):
                linkType = None
                
            returnUniqueValuesOnly = True
                
            clusterExcludeList = []
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    isMeme = True
                    try:
                        #This param will be provided when this call is originating in getHasCounterpartsByType
                        isMeme = params[2]
                    except: pass
                    traverseLinks, traverseNeighbors, traverseOrder = entity.getTraverseReport(params[1], isMeme, linkType, [], returnUniqueValuesOnly, clusterExcludeList)
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function getHasLinkedEntityByMemeType failed.  Traceback = %s" %e
            #raise Exceptions.ScriptError(ex)
        return traverseLinks, traverseNeighbors, traverseOrder    


class getHasCounterpartsByTag(object):
    # getMemberEntiesByType(self, meme):
    ''' Three params: entity, memePath, linkType'''
    def execute(self, params):
        getList = getLinkCounterpartsByTag(params)
        if len(getList) == 0:
            return False
        else:
            return True
    

#Todo - add paremeter for link direction    
class getLinkCounterpartsByTag(object):
    # getMemberEntiesByType(self, meme):
    ''' Three params: entity, memePath, linkType, direction'''
    #linkDirectionTypes.BIDIRECTIONAL, '', None, linkAttributeOperatorTypes.EQUAL
    def execute(self, params):
        counterparts = []
        try:
            entity = entityRepository.getEntity(params[0])
            
            linkType = params[2]
            if (params[2] != linkTypes.ALIAS) and (params[2] != linkTypes.ATOMIC) and (params[2] != linkTypes.SUBATOMIC):
                linkType = None
                
            if len(params) < 4:
                direction = linkDirectionTypes.BIDIRECTIONAL
                
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    linkList = linkRepository.getCounterparts(params[0], direction, '', None, linkAttributeOperatorTypes.EQUAL, linkType)
                    for friendUUID in linkList:
                        friend = entityRepository.getEntity(friendUUID)
                        if params[1] in friend.tags:
                            counterparts.append(friendUUID)
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.ScriptError(ex)
        
        except Exception as e:
            ex = "Function getLinkCounterpartsByTag failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return counterparts




class getAreEntitiesLinked(object):
    #getAreEntitiesLinked(self, uuid):
    ''' Two params: entity, memePath'''
    def execute(self, params):
        hasMembers = False
        try:
            entity = entityRepository.getEntity(params[1])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    hasMembers = entity.getAreEntitiesLinked(params[2])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.ScriptError(ex)
        
        except Exception as e:
            ex = "Function getAreEntitiesLinked failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return hasMembers

class getIsEntitySingleton(object):
    #getIsSingleton
    ''' One param: entity'''
    def execute(self, params):
        isSingleton = False
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    isSingleton = entity.getIsSingleton()
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        
        except Exception as e:
            ex = "Function getIsEntitySingleton failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return isSingleton
    

class getIsEntityTaxonomyExact(object):
    def execute(self, params):
        return None

class getIsEntityTaxonomyGeneralization(object):
    def execute(self, params):
        return None



class getIsEntityTaxonomySpecialization(object):
    def execute(self, params):
        return None



class getLinkedEntityByMemeTag(object):
    #getMemberEntiesByTag(self, tag):
    ''' Three params: entity, tag, membership type = 0'''
    def execute(self, params):
        members = []
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    members = entity.getLinkedEntityByMemeTag(params[1], params[2])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function getLinkedEntityByMemeTag failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return members
    

    

class getMemberEnties(object):
    ''' One param: entityUUID'''
    #getMemberEnties(self, uuid):
    def execute(self, params):
        returnEntities = None
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    returnEntities = entity.getMemberEnties()
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[1]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function getMemberEnties failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return returnEntities
    

class instantiateEntity(object):
    def execute(self, params):
        #ToDo - 
        return None
    
    
    
class removeAllCustomPropertiesFromEntity(object):
    """ Remove all properties that do not come from a meme"""
    #removeAllCustomProperties(self, drillDown = True):
    def execute(self, params):
        drillDown = True
        if len(params) == 2:
            drillDown = params[1]
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.removeAllCustomProperties(drillDown)
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function removeAllCustomPropertiesFromEntity failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None
    

    
#Todo - add parameterization for link
class removeEntityLink(object):
    """ Two params: MemberUUID1, MemberUUID2"""
    def execute(self, params):
        method = moduleName + '.' +  'addEntityLink' + '.execute'
        returnArray = []
        try:
            linkRepository.removeLink(params[0], params[1])
            
            #Fire Link Event for both entity0 and entity1, if one exists
            entity0 = entityRepository.getEntity(params[0])
            entity1 = entityRepository.getEntity(params[1])
            linkParams = {"sourceEntityID" : params[0], "targetEntityID" : params[1]}
            if hasattr(entity0, 'linkRemove'):
                try:
                    sesScriptReturn = entity0.linkRemove.execute(params[0], linkParams)
                    returnArray.append(sesScriptReturn)
                except Exception as e:
                    try:
                        scriptLoc = getScriptLocation(params[0], "linkRemove")
                    except Exception as e:
                        innerFullerror = sys.exc_info()
                        innerErrorMsg = str(innerFullerror[1])
                        scriptLoc = "UNKNOWN LOCATION ((%s))" %innerErrorMsg 
                    fullerror = sys.exc_info()
                    errorID = str(fullerror[0])
                    errorMsg = str(fullerror[1])
                    tb = sys.exc_info()[2]
                    errorMessage = "EventScriptFailure!  Entity of type %s experienced an error while trying to execute script at %s during linkRemove event."  %(entity0.memePath.fullTemplatePath, scriptLoc)
                    errorMessage = "%s  Entity is source." %(errorMessage)
                    errorMessage = "%s  Nested Traceback %s: %s" %(errorMessage, errorID, errorMsg)
                    logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                    raise Exceptions.EventScriptFailure(errorMessage).with_traceback(tb)
            else:
                returnArray.append(None)
            if hasattr(entity1, 'linkRemove'):
                try:
                    sesScriptReturn = entity1.linkRemove.execute(params[1], linkParams)
                    returnArray.append(sesScriptReturn)
                except Exception as e:
                    try:
                        scriptLoc = getScriptLocation(params[1], "linkRemove")
                    except Exception as e:
                        innerFullerror = sys.exc_info()
                        innerErrorMsg = str(innerFullerror[1])
                        scriptLoc = "UNKNOWN LOCATION ((%s))" %innerErrorMsg 
                    fullerror = sys.exc_info()
                    errorID = str(fullerror[0])
                    errorMsg = str(fullerror[1])
                    tb = sys.exc_info()[2]
                    errorMessage = "EventScriptFailure!  Entity of type %s experienced an error while trying to execute script at %s during linkRemove event."  %(entity0.memePath.fullTemplatePath, scriptLoc)
                    errorMessage = "%s  Entity is target." %(errorMessage)
                    errorMessage = "%s  Nested Traceback %s: %s" %(errorMessage, errorID, errorMsg)
                    logQ.put( [logType , logLevel.WARNING , method , errorMessage])
                    raise Exceptions.EventScriptFailure(errorMessage).with_traceback(tb)
            else:
                returnArray.append(None)
        except Exceptions.EventScriptFailure as e:
            raise e
        except Exception as e:
            ex = "Function removeMemberEntity failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return returnArray


#Todo - add parameterization for link
#Todo - add the getCounterparts parameters
class removeAllCounterpartsOfType(object):
    #removeAllCounterpartsOfType(self, memeID, drillDown = True):
    def execute(self, params):
        try:
            linkType = None
            try:
                if (params[2] == 0) or (params[2] == 1) or (params[2] == 2):
                    linkType = params[2]
            except:
                pass
            counterparts = linkRepository.getCounterparts(params[0], linkDirectionTypes.BIDIRECTIONAL, [], [], linkType)
            for counterpart in counterparts:
                counterpartEntity = entityRepository.getEntity(params[0])
                if params[2] == counterpartEntity.memePath.fullTemplatePath:
                    linkRepository.removeLink(params[0], counterpart)
        except Exception as e:
            ex = "Function removeAllCounterpartsOfType failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None



#Todo - add parameterization for link
#Todo - add the getCounterparts parameters
class removeAllCounterpartsOfTag(object):
    #removeAllMemberEntitiesWithTag(self, tag, drillDown = True):
    def execute(self, params):
        try:
            linkType = None
            try:
                if (params[2] == 0) or (params[2] == 1) or (params[2] == 2):
                    linkType = params[1]
            except:
                pass
            counterparts = linkRepository.getCounterparts(params[0], linkDirectionTypes.BIDIRECTIONAL, [], [], linkType)
            for counterpart in counterparts:
                counterpartEntity = entityRepository.getEntity(params[0])
                if params[2] in counterpartEntity.tags:
                    linkRepository.removeLink(params[0], counterpart)
        except Exception as e:
            ex = "Function removeAllMemberEntitiesOfTag failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None


class removeEntityProperty(object):
    ''' entityID, templateProperty, drilldown '''
    def execute(self, params):
        try:
            templateProperty = params[1]
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.removeProperty(templateProperty)
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function removeEntityProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None

class removeEntityTaxonomy(object):
    def execute(self, params):
        return None

    
    
    
class evaluateEntity(object):
    def execute(self, uuidVal, params):
        returnVal = None
        try:
            #Evaluate entity is called with five params: 
            #    entityUUID, runtimeVariables, ActionID = None, Subject = None, Controller = None, supressInit = False
            #It must in turn call getEntity.execute(), which has also has four params in a different layout.  
            #    The runtimeVariables at position 1 is stripped out
            retreiveParams = []
            retreiveParams.append(params["entityID"])
            retreiveParams.append(params["actionID"])
            retreiveParams.append(params["subjectID"])
            retreiveParams.append(params["objectID"])
            retreiveParams.append(params["supressInit"])
            
            entityClass = getEntity() 
            entity = entityClass.execute(retreiveParams)
            if entity.depricated != True:
                if entity.execScript is not None:
                    #No need to aquire the lock on the entity, only on the exec object
                    #entity.entityLock.acquire(True)
                    entity.execScript.entityLock.acquire(True)
                    try:
                        #Do proper exception handling
                        returnVal = entity.execScript.execute(uuidVal, params)
                    except Exception as e:
                        fullerror = sys.exc_info()
                        errorID = str(fullerror[0])
                        errorMsg = str(fullerror[1])
                        tb = sys.exc_info()[2]
                        try:
                            scriptLoc = type(entity.execScript)
                        except Exception as e:
                            innerFullerror = sys.exc_info()
                            innerErrorMsg = str(innerFullerror[1])
                            scriptLoc = "UNKNOWN SCRIPT CLASS ((%s))" %innerErrorMsg
                        errorMessage = "EventScriptFailure!  Entity of type %s experienced an error while trying to execute script %s during evaluate event."  %(entity.memePath.fullTemplatePath, scriptLoc)
                        errorMessage = "%s  Entity is target." %(errorMessage)
                        errorMessage = "%s  Nested Traceback %s: %s" %(errorMessage, errorID, errorMsg)
                        logQ.put( [logType , logLevel.WARNING , "Graph.EvaluateEntity.execute" , errorMessage])
                        raise Exceptions.EventScriptFailure(errorMessage).with_traceback(tb)                
                    finally:
                        entity.execScript.entityLock.release()
                        #entity.entityLock.release()
                else:
                    ex = "%s Entity %s has no executor script installed." %(entity.memePath.fullTemplatePath, uuidVal)
                    raise Exceptions.ScriptError(ex)                    
            else:
                ex = "%s Entity %s is depricated" %(entity.memePath, uuidVal)
                raise Exceptions.ScriptError(ex)
        except Exceptions.EventScriptFailure as e:
            raise e
        except TypeError as e:
            fullerror = sys.exc_info()
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            raisedErrorMessage = "Function evaluateEntity failed.  %s" %errorMsg
            raise Exceptions.ScriptError(raisedErrorMessage).with_traceback(tb)
        except AttributeError as e:
            em = "Entity %s has no execute script!"  %params[0]
            fullerror = sys.exc_info()
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            raisedErrorMessage = "Function evaluateEntity failed.  %s.  %s" %(errorMsg, em)
            raise Exceptions.ScriptError(raisedErrorMessage).with_traceback(tb)
        except Exception as e:
            fullerror = sys.exc_info()
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            raisedErrorMessage = "Function evaluateEntity failed.  %s" %errorMsg
            raise Exceptions.ScriptError(raisedErrorMessage).with_traceback(tb)
        return returnVal




class revertEntity(object):
    """ Reset property values to their original values as defined in the parent meme(s)
           and removes custom properties.
    Two params: entity, drilldown (optional)'''"""
    # revertPropertyValues(self, drillDown = False)
    def execute(self, params):
        drillDown = False
        try:
            if len(params) == 2:
                drillDown = params[1]
        except: pass
        
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.revertPropertyValues(drillDown)
                    entity.removeAllCustomProperties(drillDown)
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function addEntityDecimalProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None
    
    
    
class revertEntityPropertyValues(object):
    """ Reset property values to their original values as defined in the parent meme(s).  
    It does not affect custom properties or properties from depricated memes.
    Two params: entity, drilldown (optional)'''"""
    # revertPropertyValues(self, drillDown = False)
    def execute(self, params):
        drillDown = False
        try:
            if len(params) == 2:
                drillDown = params[1]
        except: pass
        
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.revertPropertyValues(drillDown)
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exception as e:
            ex = "Function addEntityDecimalProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None
    

class setEntityPropertyValue(object):
    ''' Three params: entity, name, value'''
    def execute(self, params):
        returnValue = None
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    returnValue = entity.setPropertyValue(params[1], params[2])
                except Exceptions.EventScriptFailure as e:
                    raise e
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exceptions.EventScriptFailure as e:
            raise e
        except Exceptions.EntityPropertyValueTypeError as e:
            raise Exceptions.EntityPropertyValueTypeError(e)
        except Exceptions.EntityPropertyValueOutOfBoundsError as e:
            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)
        except Exception as e:
            ex = "Function addEntityDecimalProperty failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return returnValue
    
    
    
class setStateEventScript(object):
    ''' Two params: entity, script'''
    def execute(self, params):
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.setStateEventScript(params[1])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exceptions.EntityPropertyValueTypeError as e:
            raise Exceptions.EntityPropertyValueTypeError(e)
        except Exceptions.EntityPropertyValueOutOfBoundsError as e:
            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)
        except Exception as e:
            ex = "Function setExecScript failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None
    
    
class installPythonExecutor(object):
    ''' two params - the entity and the callable object '''
    def execute(self, params):
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    entity.installExecutorObject(params[1])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exceptions.EntityPropertyValueTypeError as e:
            raise Exceptions.EntityPropertyValueTypeError(e)
        except Exceptions.EntityPropertyValueOutOfBoundsError as e:
            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)
        except Exception as e:
            ex = "Function setExecScript failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return None 
    
    
class getChildMemes(object):
    def execute(self, params):
        return []
    
class getParentMemes(object):
    def execute(self, params):
        return []
    
class getChildMetaMemes(object):
    def execute(self, params):
        return []
    
class getParentMetaMemes(object):
    #param[0] = meme ID
    def execute(self, params):
        meme = templateRepository.resolveTemplateAbsolutely(params[0])
        return meme.metaMeme
    
class getExtendingMetamemes (object):
    #MetaMeme.collectExtensions
    #param[0] = meme ID
    def execute(self, params):
        meme = templateRepository.resolveTemplateAbsolutely(params[0])
        extendingMetaMemes =  meme.collectExtensions()
        return extendingMetaMemes
    
class getTaxonomy(object):
    #param[0] = meme ID
    def execute(self, params):
        fullTypeList = []
        meme = templateRepository.resolveTemplateAbsolutely(params[0])
        metameme = templateRepository.resolveTemplateAbsolutely(meme.metaMeme)
        fullTypeList.append(meme.metaMeme)
        extendingMetaMemes =  metameme.collectExtensions()
        fullTypeList.extend(extendingMetaMemes)
        return fullTypeList

class getHasTaxonomy(object):
    #params[0] = meme ID
    #params[1] = metameme path
    def execute(self, params):
        meme = templateRepository.resolveTemplateAbsolutely(params[0])
        isMetaMemeType = meme.testTaxonomy(params[1])
        return isMetaMemeType

    
class getEnhancingMetamemes (object):
    #MetaMeme.collectEnhancements
    def execute(self, params):
        return []    
    
class getEnhancedMetamemes (object):
    #MetaMeme.collectEnhancements
    def execute(self, params):
        return []    
    
    
class getEnhanceableMemes (object):
    #Meme.collectEnhanceableMemes
    def execute(self, params):
        return []    
    
class getEnhancedMemes (object):
    def execute(self, params):
        return []   
    
class getEnhancingMemes (object):
    #MetaMeme.collectMemesThatEnhanceSelf
    def execute(self, params):
        return []   
    
class hotLoadTemplate (object):
    #MetaMeme.collectMemesThatEnhanceSelf
    def execute(self, params):
        return True 
    
class getClusterMembers (object):
    ''' Three params - entity UUID, link types, halt on singleton'''
    def execute(self, params):
        bigList = []
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                entity.entityLock.acquire(True)
                try:
                    bigList = entity.getClusterMembers(params[1], params[2], [])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exceptions.EntityPropertyValueTypeError as e:
            raise Exceptions.EntityPropertyValueTypeError(e)
        except Exceptions.EntityPropertyValueOutOfBoundsError as e:
            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)
        except Exception as e:
            ex = "Function getClusterMembers failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        return bigList 



class getCluster(object):
    ''' Three params - entity UUID, link types, halt on singleton
    
        Returns a python dict corresponding to the following JSON example
        {
          "nodes": [
            {"id": "Myriel", "group": 1},
            {"id": "Napoleon", "group": 1}
          ],
          "links": [
            {"source": "Napoleon", "target": "Myriel", "value": 1},
            {"source": "Mlle.Baptistine", "target": "Myriel", "value": 8}
          ]
        }
    '''
    def execute(self, params):
        nodesDict = {}  
        nodes = []
        links = []
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                selfMeme = api.getEntityMemeType(params[0])
                selfMetaMeme = api.getEntityMetaMemeType(params[0])
                
                entityString = getUUIDAsString(params[0])
                nodeData = {"id": entityString, "meme": selfMeme, "metaMeme": selfMetaMeme, "position" : 0}
                nodesDict[entityString] = nodeData
                
                entity.entityLock.acquire(True)
                try:
                    #bigList = entity.getClusterMembers(params[1], params[2], [])
                    entireCluster = entity.getEntityCluster(params[1], params[2], [])
                    
                    # Each entry in bigList looks like [start.uuid, end.uuid, member.memePath.fullTemplatePath, member.metaMeme]
                    for bigListEntry in entireCluster:
                        sourceID = getUUIDAsString(bigListEntry[0])
                        targetID = getUUIDAsString(bigListEntry[1])
                        linkdata ={"source": sourceID, "target": targetID, "value": 1}
                        links.append(linkdata)
                        
                        #We add the node data into a dict, to ensure that each node comes up exactly once
                        nodeData = {"id": targetID, "meme": bigListEntry[2], "metaMeme": bigListEntry[3], "position" : bigListEntry[4]}
                        nodesDict[targetID] = nodeData
                    for nodesDictKey in nodesDict.keys():
                        nodes.append(nodesDict[nodesDictKey])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exceptions.EntityPropertyValueTypeError as e:
            raise Exceptions.EntityPropertyValueTypeError(e)
        except Exceptions.EntityPropertyValueOutOfBoundsError as e:
            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)
        except Exception as e:
            ex = "Function getClusterMembers failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        cluster = {"nodes": nodes, "links": links}
        return cluster
    
    
    
    
class getClusterJSON(object):
    ''' Four params - entity UUID, link types, halt on singleton
    
        Returns a python dict corresponding to the following JSON example
        {
          "nodes": [
            {"id": "Myriel", "group": 1},
            {"id": "Napoleon", "group": 1}
          ],
          "links": [
            {"source": "Napoleon", "target": "Myriel", "value": 1},
            {"source": "Mlle.Baptistine", "target": "Myriel", "value": 8}
          ]
        }
    '''
    def execute(self, params):
        nodesDict = {}  
        nodes = []
        links = []
        try:
            entity = entityRepository.getEntity(params[0])
            if entity.depricated != True:
                selfMeme = api.getEntityMemeType(params[0])
                selfMetaMeme = api.getEntityMetaMemeType(params[0])
                
                entityString = getUUIDAsString(params[0])
                nodeData = {"id": entityString, "meme": selfMeme, "metaMeme": selfMetaMeme}
                nodesDict[entityString] = nodeData
                
                entity.entityLock.acquire(True)
                try:
                    #bigList = entity.getClusterMembers(params[1], params[2], [])
                    entireCluster = entity.getEntityCluster(params[1], params[2], [])
                    
                    # Each entry in bigList looks like [start.uuid, end.uuid, member.memePath.fullTemplatePath, member.metaMeme]
                    for bigListEntry in entireCluster:
                        sourceID = getUUIDAsString(bigListEntry[0])
                        targetID = getUUIDAsString(bigListEntry[1])
                        linkdata ={"source": sourceID, "target": targetID, "value": 1}
                        links.append(linkdata)
                        
                        #We add the node data into a dict, to ensure that each node comes up exactly once
                        nodeData = {"id": targetID, "meme": bigListEntry[2], "metaMeme": bigListEntry[3], "position" : bigListEntry[4]}
                        nodesDict[targetID] = nodeData
                    for nodesDictKey in nodesDict.keys():
                        nodes.append(nodesDict[nodesDictKey])
                except Exception as e:
                    raise e                
                finally:
                    entity.entityLock.release()
            else:
                ex = "Entity %s has been archived and is no longer available" %params[0]
                raise Exceptions.ScriptError(ex)
        except Exceptions.EntityPropertyValueTypeError as e:
            raise Exceptions.EntityPropertyValueTypeError(e)
        except Exceptions.EntityPropertyValueOutOfBoundsError as e:
            raise Exceptions.EntityPropertyValueOutOfBoundsError(e)
        except Exception as e:
            ex = "Function getClusterMembers failed.  Traceback = %s" %e
            raise Exceptions.ScriptError(ex)
        cluster = {"nodes": nodes, "links": links}
        clusterJSON = json.dumps(cluster)
        return clusterJSON
    
    
    
class sourceMemeCreate (object):
    ''' Three params - modulePath, memeName, metamemePath'''
    className = "sourceMemeCreate"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceTemplateRepository.lock.acquire(True)
            path = TemplatePath(params[0], params[1])
            metaMeme = templateRepository.resolveTemplate(path, params[2])
            meme = SourceMeme(path, metaMeme)
            try:
                templateRepository.lock.acquire(True)
                sourceTemplateRepository.catalogTemplate(meme.path, meme)
                validationResults = meme.compile(True, False)
            except Exception as e:
                fullerror = sys.exc_info()
                errorID = str(fullerror[0])
                nestEerrorMsg = str(fullerror[1])
                errorMsg = "Error while trying to create compile meme %s,   Nested Traceback = %s: %s" %(path.fullTemplatePath, errorID, nestEerrorMsg)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Source Meme Creation Failed.  Traceback = %s" %e
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceTemplateRepository.lock.release()
        return {"memeID" : meme.path.fullTemplatePath, "ValidationResults" : validationResults}
        


    
class sourceMemePropertySet (object):
    '''Three params - sourceMeme.path.fullTemplatePath, propName, propValueStr'''
    className = "sourceMemePropertySet"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                sourceMeme.setProperty(params[1], params[2])
                validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't set meme %s property %s to %s.  Traceback = %s" %(params[0], params[1], params[2], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.sourceMemeLock.release()
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults}   
    
    
class sourceMemePropertyRemove (object):
    '''Three params - sourceMeme.path.fullTemplatePath, propName'''
    className = "sourceMemePropertyRemove"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            try:
                sourceMeme.sourceMemeLock.acquire(True)
                try:
                    templateRepository.lock.acquire(True)
                    sourceMeme.removeProperty(params[1])
                    validationResults = sourceMeme.compile(True, False)
                except Exception as e:
                    errorMsg = "Can't remove meme %s property %s.  Traceback = %s" %(params[0], params[1], e)
                    logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                    raise Exceptions.SourceMemeManipulationError(errorMsg)
                finally:
                    templateRepository.lock.release()
            except Exceptions.SourceMemeManipulationError as e:
                raise e
            except Exception as e:
                errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.ScriptError(errorMsg)
            finally:
                sourceMeme.sourceMemeLock.release()
        except Exceptions.ScriptError as e:
            raise e
        except Exception as e:
            raise e
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults}   
    
    

class sourceMemeMemberAdd (object):
    '''Three params - sourceMeme.path.fullTemplatePath, memberID, occurrence'''
    className = "sourceMemeMemberAdd"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                count = int(params[2])
                lt = int(params[3])
                templateRepository.lock.acquire(True)
                sourceMeme.addMemberMeme(params[1], count, lt)
                validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't add member %s to meme %s.  Traceback = %s" %(params[1], params[0], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.sourceMemeLock.release()
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults}   
    
    
    
class sourceMemeMemberRemove (object):
    '''Two params - sourceMeme.path.fullTemplatePath, memberID'''
    className = "sourceMemeMemberRemove"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                sourceMeme.removeMemberMeme(params[1])
                validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't remove member %s from meme %s.  Traceback = %s" %(params[1], params[0], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.sourceMemeLock.release()
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults} 
    



class sourceMemeEnhancementAdd (object):
    '''Two params - sourceMeme.path.fullTemplatePath, memeID'''
    className = "sourceMemeEnhancementAdd"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                sourceMeme.addEnhancement(params[1])
                validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't set meme %s to enhance %s.  Traceback = %s" %(params[0], params[1], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.sourceMemeLock.release()
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults} 
    
    
    
class sourceMemeEnhancementRemove (object):
    '''Two params - sourceMeme.path.fullTemplatePath, memeID'''
    className = "sourceMemeEnhancementRemove"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                sourceMeme.removeEnhancement(params[1])
                validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't set meme %s to no longer enhance %s.  Traceback = %s" %(params[0], params[1], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.sourceMemeLock.release()
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults} 
    
    
    
class sourceMemeTagAdd (object):
    '''Two params - sourceMeme.path.fullTemplatePath, tag'''
    className = "sourceMemeTagAdd"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                sourceMeme.addTag(params[1])
                validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't add tag %s to meme %s.  Traceback = %s" %(params[0], params[1], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.sourceMemeLock.release()
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults} 
    
    
    
class sourceMemeTagRemove (object):
    '''Two params - sourceMeme.path.fullTemplatePath, tag'''
    className = "sourceMemeTagRemove"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                sourceMeme.removeTag(params[1])
                validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't remove tag %s from meme %s.  Traceback = %s" %(params[0], params[1], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.sourceMemeLock.release()
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults} 
    
    
    
class sourceMemeSetSingleton (object):
    '''Two params - sourceMeme.path.fullTemplatePath, isSingleton'''
    className = "sourceMemeSetSingleton"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                sourceMeme.setSingleton(params[1])
                validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't set singleton status on meme %s.  Traceback = %s" %(params[0], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise e
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.sourceMemeLock.release()
        return {"memeID" : sourceMeme.path.fullTemplatePath, "ValidationResults" : validationResults} 



class sourceMemeCompile (object):
    ''' Two params - fullTemplatePath, validate = True
        This method will re-deploy the entire repository and then validate the chosen meme.
        Use sparingly, as it is a resource hog
    '''
    className = "sourceMemeCompile"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                validationResults = sourceMeme.compile(params[1], False)
            except Exception as e:
                errorMsg = "Source Meme %s Compilation Failed.  Traceback = %s" %(params[0], e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Encountered problem while trying to aquire lock on meme %s.  Traceback = %s" %(params[0], e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.entityLock.release()
        return validationResults        
    
    
    
class sourceMemeValidate (object):
    ''' One param - fullTemplatePath
        This method will re-deploy the entire repository and then validate the chosen meme.
        Use sparingly, as it is a resource hog
    '''
    className = "sourceMemeValidate"
    
    def execute(self, params):
        method = moduleName + '.' +  self.className + '.execute'
        validationResults = []
        try:
            sourceMeme = sourceTemplateRepository.resolveTemplateAbsolutely(params[0])
            sourceMeme.sourceMemeLock.acquire(True)
            try:
                templateRepository.lock.acquire(True)
                try:
                    deployedMeme = templateRepository.resolveTemplateAbsolutely(sourceMeme.path.fullTemplatePath)
                    validationResults = deployedMeme.validate([])
                except Exception as e:
                    errMsg = "Unable to validate compiled meme %s.  It is probably uncompiled.  Traceback = %s" %(sourceMeme.path.fullTemplatePath, e)
                    nextTryMsg = "Now trying to compile source meme %s before retrying validation" %sourceMeme.path.fullTemplatePath
                    logQ.put( [logType , logLevel.INFO , method , errMsg]) 
                    logQ.put( [logType , logLevel.INFO , method , nextTryMsg])
                    validationResults = sourceMeme.compile(True, False)
            except Exception as e:
                errorMsg = "Can't validate meme %s.  Traceback = %s" %(sourceMeme.path.fullTemplatePath, e)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.SourceMemeManipulationError(errorMsg)
            finally:
                templateRepository.lock.release()
        except Exceptions.SourceMemeManipulationError as e:
            raise e
        except Exception as e:
            errorMsg = "Can't validate meme %s.  Traceback = %s" %(sourceMeme.path.fullTemplatePath, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            raise Exceptions.ScriptError(errorMsg)
        finally:
            sourceMeme.entityLock.release()
        return validationResults
    
    
class MapBroker(object):
        
    def execute(self, mapFunction, paramSet, argumentMap = []):

        #we're going to pass argumentMap in a map() and don't need it broken up.  Hence this little hack
        argumentMapParams = []
        for unused in paramSet:
            argumentMapParams.append(argumentMap)

        mappedValues = list(map(mapFunction, paramSet, argumentMapParams))
        return mappedValues 
    
    
    
class ReduceBroker(object):
            
    def execute(self, reduceFunction, paramSet):  
        returnResult = functools.reduce(reduceFunction, paramSet)
        return returnResult 
  
     
   
########################
#End Script Handlers
######################### 


def countEntities():
    global entityRepository
    return len(entityRepository.indexByID)


def startLogger(lLevel = logLevel.WARNING, codePage = "utf-8", overwrite = True, logDir = None):
    """
        Start the internal logging service.  This is not needed if Graphyne is started with an external log Queue
    """
    #Ensure logging
    from . import Logger
    try:
        global loggingService
        tmpClass = getattr(Logger, 'Logger')
        loggingService = tmpClass()
        loggingService.initialize(lLevel, codePage, logDir, overwrite)
        #loggingService = Logger.Logger(lLevel, codePage, logDir, overwrite)
        #loggingService.initialize(lLevel, codePage, logDir, overwrite = True)
        logQ.put( [logType , logLevel.ADMIN , "Graph.initialize" , "starting %s" %loggingService.__class__])
        print("starting Graphyne Internal Logging Service")
        loggingService.start()
    except Exception as e:
        print(("Failed to start Graphyne Internal Logging Service.  Traceback = %s" %(e)))
        logQ.put( [logType , logLevel.ERROR , "Graph.initialize" , "Failed to start Logger.  Traceback = %s" %( e)])
            
            
            
def stopLogger():
    """
        Stop the internal logging service.  The internal logging service is a seperate thread.  
    """
    try:
        global loggingService
        print("stopping Graphyne Internal Logging Service")
        loggingService.join(30.0) #the timeout is because the join sometimes hangs in multiprocess usage
    except Exception:
        pass
    
    
def startDB(repoLocations=[], flaggedPersistenceType=None , persistenceArg=None, useDefaultSchema=False, resetDatabase=False, createTestDatabase=False, validate=True):
    ''' Initialization of restrictions, meta-memes and memes.
            Sequentially empty the restrictionQueue, metamemeQueue and memeQueue,
            loading the relevant template types as found in each queue.
        Restrictions must be loaded before metamemes.
        Metamemes must be loaded before memes.
        
        Parameters:
            repoLocations = a list of all of the filesystem location that that compose the repository.
            useDefaultSchema.  I True, then load the 'default schema' of Graphyne
            flaggedPersistenceType = The type of database used by the persistence engine.  This is used to determine which flavor of SQL syntax to use.
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
            resetDatabase - If it is set to True and a database already exists (e.g. when using sqlite with a file, or any other kind of relational database
                with preexisting data, then the DB tables will be cleared.
            createTestDatabase = a flag for creating regression test data.  This flag is only to be used for regression testing the graph and even then, only if the test 
                database does not already exist. 

                *If persistenceType is None (no persistence, then this is ignored and won't throw any InconsistentPersistenceArchitecture exceptions)
         
    '''
    method = moduleName + '.' + 'initialize'

    global entityRepository
    global linkRepository  
    global persistenceType
    global persistenceDB 
    global dbConnection
    global sqlSyntax
    global validateOnLoad
    
    validateOnLoad = validate
    
    persistenceType = "none"
    if flaggedPersistenceType is None:
        flaggedPersistenceType = "none"
    elif flaggedPersistenceType == "":
        flaggedPersistenceType = "none"
    persistenceType = flaggedPersistenceType
    
    #Get All Repositories
    objectMap = {}
    for repoLocation in repoLocations:
        sys.path.append(repoLocation)
        objectMap = Fileutils.walkRepository(repoLocation, objectMap)
    
    if useDefaultSchema is True:
        #installFilePath = os.path.dirname(Fileutils.__file__)
        #schemaPath = os.path.join(installFilePath, "Schema")
        #sys.path.append(schemaPath)
        #Voodoo alert!
        #  The 'default' schema is in the same directory as Graph.py
        #  Since we don't know where it is in the filesystem, we need to find out where we are installed first.
        #  1 - Import a module from within the Graphyne package.
        #    We have already imported Exceptions.py, so we'll look for its location
        #  2 - Fetch the dirname of this module.
        #    This will be the "Repository" location and will contain the Memetic package
        try:
            childDirectory = os.path.dirname(Exceptions.__file__)
            parentDirectory = os.path.split(childDirectory)
            objectMap = Fileutils.walkRepository(parentDirectory[0], objectMap)
        except Exception as e:
            errorMessage = "Error: useDefaultSchema is set to true, but default package (Memetic) can't be bootstrapped.  Please install it and ensure that it is in the PYTHONPATH.  Traceback = %s" %e
            print(errorMessage)
            raise Exceptions.TemplatePathError(errorMessage)
    
    #syndicate all data to the load queues
    toBeIndexed = []
    restrictions = []
    metamemes = []
    sourceMemes = []
    memes = []
    for packagePath in objectMap.keys():
        try:
            fileData = objectMap[packagePath]
            for fileStream in fileData.keys():
                codepage = fileData[fileStream]
                toBeIndexed = [fileStream, codepage, packagePath]
    
            #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
            
            #catalog the restrictions in the restriction queue
            #logQ.put( [logType , logLevel.DEBUG , method , "making pass %s on restriction load queue" %(nth)])
            #logQ.put( [logType , logLevel.DEBUG , method , "Trying to pop item from queue %s" %self.restLoadQ])
            logQ.put( [logType , logLevel.INFO , method , "Loading restrictions from module %s" %(toBeIndexed[2])])
            if len(toBeIndexed) > 2:
                try:
                    restrictionsFrag = getRestrictionsFromFile(toBeIndexed[0], toBeIndexed[1], toBeIndexed[2])
                    restrictions.extend(restrictionsFrag)
                    logQ.put( [logType , logLevel.INFO, method , "Loaded %s restrictions from module %s" %(len(restrictionsFrag), toBeIndexed[2])])
                except Exception as e:
                    logQ.put( [logType , logLevel.ERROR , method , "Indexing failure for restrictions in module %s.  Traceback = %s" %(toBeIndexed[2], e)])
                    logQ.put( [logType , logLevel.INFO, method , "Loaded 0 restrictions from module %s" %(toBeIndexed[2])])
                    restrictionsFrag = getRestrictionsFromFile(toBeIndexed[0], toBeIndexed[1], toBeIndexed[2])
                    restrictions.extend(restrictionsFrag)
                    logQ.put( [logType , logLevel.INFO, method , "Loaded %s restrictions from module %s" %(len(restrictionsFrag), toBeIndexed[2])])
    
            else:
                logQ.put( [logType , logLevel.ERROR , method , "Load queue item does not fit format: %s" %toBeIndexed])     
        except Exception as e:
            logQ.put( [logType , logLevel.ERROR , method , "Error while loading restriction from file %s.  Traceback = %s" %(toBeIndexed, e)])
    #finished loading restrictions
    #logQ.put( [logType , logLevel.DEBUG , method , 'Finished loading restrictions from XML in queue.  Restriction Queue now empty.']) 

        
    #Repeat for metamemes
    for packagePath in objectMap.keys(): 
        try:
            fileData = objectMap[packagePath]
            for fileStream in fileData.keys():
                codepage = fileData[fileStream]
                toBeIndexed = [fileStream, codepage, packagePath]
            #logQ.put( [logType , logLevel.DEBUG , method , "making pass %s on metameme load queue" %(nth)])
            #logQ.put( [logType , logLevel.DEBUG , method , "Trying to pop item from metameme queue %s" %self.mmLoadQ])
            logQ.put( [logType , logLevel.INFO , method , "Loading metamemes from module %s" %(toBeIndexed[2])])
            if len(toBeIndexed) > 2:
                try:
                    metamemesFrag = getMetaMemesFromFile(toBeIndexed[0], toBeIndexed[1], toBeIndexed[2])
                    metamemes.extend(metamemesFrag)
                    logQ.put( [logType , logLevel.INFO, method , "Loaded %s metamemes from module %s" %(len(metamemesFrag), toBeIndexed[2])])
                except Exception as e:
                    logQ.put( [logType , logLevel.ERROR , method , "Indexing failure for metamemes in module %s.  Traceback = %s" %(toBeIndexed[2], e)])
                    logQ.put( [logType , logLevel.INFO, method , "Loaded 0 metamemes from module %s" %(toBeIndexed[2])])
            else:
                logQ.put( [logType , logLevel.ERROR , method , "Load queue item does not fit format: %s" %toBeIndexed])
        except Exception as e:
            logQ.put( [logType , logLevel.ERROR , method , "Error while loading metamemes from file %s.  Traceback = %s" %(toBeIndexed, e)])
    #Before Continuing, create a Generic Metameme
    gPath = TemplatePath("Graphyne", "GenericMetaMeme")
    gmetaMeme = MetaMeme(gPath, False, [], ["Graphyne.GenericMetaMeme"], {}, {}, False)
    metamemes.append(gmetaMeme)

    #Before we can load the memes, we have to catalog the metamemes
    for metameme in metamemes:
        try:
            tempRepository.catalogTemplate(metameme.path, metameme)
        except Exception as e:
            errorMsg = "Problem pre-cataloging metameme %s.  Traceback = %s" %(metameme.path.fullTemplatePath, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
    for metameme in metamemes:
        try:
            metameme.mergeExtensions()
        except Exception as e:
            errorMsg = "Problem extending metameme %s list: %s.  Traceback = %s" %(metameme.path.fullTemplatePath, metameme.extends, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
    for metameme in metamemes:
        try:
            templateRepository.catalogTemplate(metameme.path, metameme) 
        except Exception as e:
            errorMsg = "Problem cataloging metameme %s.  Traceback = %s" %(metameme.path.fullTemplatePath, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
    #Finished loading metamemes
    #logQ.put( [logType , logLevel.DEBUG , method , 'Finished loading meta-memes from XML in queue.  Metameme Queue now empty.']) 

    #Before we can start instantiating any entities (or catalog implicit memes) - including singletnns and pre-archived entities - we need to start the repo
    #Initialize Entity Repository    
    if persistenceType == "none":
        #"none" - no persistence
        print("Warning!  No persistence declared.  Deaulting to in-memory transient persistentce")
        logQ.put( [logType , logLevel.WARNING , method , "Warning!  No persistence declared.  Deaulting to in-memory transient persistentce"])
        from .DatabaseDrivers import NonPersistent as persistenceNone
        #persistenceNone.initialize(api, repoLocations, logQ, persistenceArg)
        persistenceNone.initialize(api, templateRepository, logQ, persistenceArg)
        entityRepository = persistenceNone.entityRepository
        linkRepository = persistenceNone.linkRepository
    elif persistenceType == "sqlite":
        if persistenceArg is None:
            persistenceArg = "memory"
        try:
            if persistenceArg == "memory":
                #"memory" - Use SQLite in in-memory mode (connection = ":memory:")
                from .DatabaseDrivers import RelationalDatabase  as persistenceMemory
                import sqlite3 as dbDriverMemory
                persistenceDB = dbDriverMemory
                sqlSyntax = SQLDictionary.SyntaxDefSQLite()
                dbConnection = persistenceDB.connect(":memory:")
                #persistenceMemory.initialize(api, repoLocations, logQ, persistenceArg, dbConnection)
                persistenceMemory.initialize(api, templateRepository, logQ, persistenceArg, dbConnection)
                persistenceMemory.setSyntax(sqlSyntax)
                persistenceMemory.ensureDatabase() 
                if createTestDatabase == True:
                    #if we are testing, then ensure that we have a cleab DB
                    sqlSyntax.createTestDB(dbConnection)
                    global createTestData
                    createTestData = createTestDatabase
                entityRepository = persistenceMemory.entityRepository
                linkRepository = persistenceMemory.linkRepository
            elif ((persistenceArg.endswith(".sqlite") == True) and (os.path.isfile(persistenceArg) == True)):
                #"<valid filename with .sqlite as extension>" - Use SQLite, with that file as the database
                from .DatabaseDrivers import RelationalDatabase as persistenceExisting
                import sqlite3 as dbDriverExisting
                persistenceDB = dbDriverExisting
                sqlSyntax = SQLDictionary.SyntaxDefSQLite()
                dbConnection = persistenceDB.connect(persistenceArg)
                #persistenceExisting.initialize(api, repoLocations, logQ, persistenceArg, dbConnection)
                persistenceExisting.initialize(api, templateRepository, logQ, persistenceArg, dbConnection)
                persistenceExisting.setSyntax(sqlSyntax)
                entityRepository = persistenceExisting.entityRepository
                linkRepository = persistenceExisting.linkRepository
            elif ((persistenceArg.endswith(".sqlite") == True) and (os.path.isfile(persistenceArg) == False)):
                #"<filename with .sqlite as extension, but no file>" - Use SQLite and create that file to use as the DB file
                
                #  If only a filename is passed, then we default to using the log directory.
                #  If a path is passed and we are running on a Windows system, then use that path
                #  If a path is passed and we are on a *nix system, then the passed path is relative to <usr>
                dbLoc = None
                basename = os.path.basename(persistenceArg)
                if (basename == persistenceArg):
                    #only the filename itself was passed
                    userDir =  expanduser("~")
                    dbLoc = os.path.join(userDir, "Graphyne", persistenceArg)
                elif (platform.system() == 'Windows'):
                    dbLoc = persistenceArg
                else:
                    userDir =  expanduser("~")
                    dbLoc = os.path.join(userDir, persistenceArg)                    
                
                from .DatabaseDrivers import RelationalDatabase as persistenceNew
                import sqlite3 as dbDriverNew
                persistenceDB = dbDriverNew
                sqlSyntax = SQLDictionary.SyntaxDefSQLite()
                dbConnection = persistenceDB.connect(dbLoc)
                #persistenceNew.initialize(api, repoLocations, logQ, persistenceArg, dbConnection)
                persistenceNew.initialize(api, templateRepository, logQ, persistenceArg, dbConnection, resetDatabase, False)
                persistenceNew.setSyntax(sqlSyntax)
                persistenceNew.ensureDatabase() 
                entityRepository = persistenceNew.entityRepository
                linkRepository = persistenceNew.linkRepository
            else:
                raise Exceptions.InconsistentPersistenceArchitecture(persistenceType, persistenceArg)   
        except Exception as e:
            raise Exceptions.InconsistentPersistenceArchitecture(persistenceType, persistenceArg, e)
    elif persistenceType == "mssql":
        if persistenceArg is None:
            throwMe = Exceptions.InconsistentPersistenceArchitecture(persistenceType, persistenceArg)
            raise throwMe
        else:
            try:
                from .DatabaseDrivers import RelationalDatabase as persistenceMSSQL
                import pyodbc as dbDriverMSSQL
                persistenceDB = dbDriverMSSQL
                sqlSyntax = SQLDictionary.SyntaxDefMSSQL()
                dbConnection = dbDriverMSSQL.connect(persistenceArg)
                persistenceMSSQL.setSyntax(sqlSyntax)
                persistenceMSSQL.initialize(api, repoLocations, logQ, persistenceArg, dbConnection, resetDatabase)
                entityRepository = persistenceMSSQL.entityRepository
                linkRepository = persistenceMSSQL.linkRepository
            except Exception as e:
                throwMe = Exceptions.InconsistentPersistenceArchitecture(persistenceType, persistenceArg, e)
                raise throwMe
    else:           
        #"<anything else>" - Presume that it is a pyodbc connection string
        pass 
    #/Initialize Entity Repository


    # Load the memes
    for packagePath in objectMap.keys():
        try:
            fileData = objectMap[packagePath]
            for fileStream in fileData.keys():
                codepage = fileData[fileStream]
                toBeIndexed = [fileStream, codepage, packagePath]                
            #logQ.put( [logType , logLevel.DEBUG , method , "making pass %s on meme load queue" %(nth)])
            #logQ.put( [logType , logLevel.DEBUG , method , "Trying to pop item from meme queue %s" %self.mLoadQ])
            
            logQ.put( [logType , logLevel.INFO, method , "Loading memes from module %s" %(toBeIndexed[2])])
            if len(toBeIndexed) > 2:
                try:
                    memesFrag = getMemesFromFile(persistenceDB, toBeIndexed[0], toBeIndexed[1], toBeIndexed[2])
                    sourceMemes.extend(memesFrag)
                    logQ.put( [logType , logLevel.INFO, method , "Loaded %s memes from module %s" %(len(memesFrag), toBeIndexed[2])])
                except Exceptions.InconsistentPersistenceArchitecture as e:
                    raise e
                except Exception as e:
                    logQ.put( [logType , logLevel.ERROR , method , "Indexing failure for memes in module %s.  Traceback = %s" %(toBeIndexed[2], e)])
                    logQ.put( [logType , logLevel.INFO, method , "Loaded 0 memes from module %s" %(toBeIndexed[2])])
            else:
                logQ.put( [logType , logLevel.ERROR , method , "Load queue item does not fit format: %s" %toBeIndexed])
        #except Exceptions.ScriptError as e:
            #errorMsg = "Error loading memes from %s.  Please check structure of source file.  Traceback = %s" %(self.mLoadQ, e)
            #logQ.put( [logType , logLevel.WARNING , method , errorMsg])
        except Exception as e:
            logQ.put( [logType , logLevel.ERROR , method , "Error while loading memes from file %s.  Traceback = %s" %(toBeIndexed, e)])
    #/Loading from file
    
    #lets duplicate the clonables and add them to the list
    logQ.put( [logType , logLevel.INFO , method ,"Cloning cloneable memes"])
    sourceMemesExtended = getSourceMemesExtension(sourceMemes, sourceMemes)
    sourceMemes = sourceMemesExtended
    
    #Before Compiling, just as we created a generic metameme, we'll now create a generic, hardcoded Graphyne.Generic meme
    gMetaMeme = templateRepository.resolveTemplateAbsolutely("Graphyne.GenericMetaMeme")
    gPath = TemplatePath("Graphyne", "Generic")
    gMeme = SourceMeme(gPath, gMetaMeme)  
    sourceMemes.append(gMeme)
    
    logQ.put( [logType , logLevel.INFO , method ,"Transforming implicit meme references to explicit ones"])
    for sourceMeme in sourceMemes:
        if sourceMeme.metaMeme.isImplicit == True:
            #Make sure that all implicit references are turned into explicit members
            try:
                sourceMeme.addImplicitMemberMemes(sourceMemes, None, '', True)
                #debug
                #if (u"ImplicitMemes.HasChild" in sourceMeme.path.fullTemplatePath) or (u"ImplicitMemes.MiddleNode" in sourceMeme.path.fullTemplatePath):
                #    pass
                #/debug
            except Exceptions.MemeMembershipValidationError as e:
                logQ.put( [logType , logLevel.WARNING , method ,e])
            except Exception as e:
                errorMsg = "Error while transforming implicit references into concrete membership on meme %s. Traceback = %s" %(sourceMeme.path.templateName, e)
                logQ.put( [logType , logLevel.WARNING , method ,errorMsg])
                
    logQ.put( [logType , logLevel.INFO , method ,"Starting Meme Archiving"])      
    for sourceMeme in sourceMemes:          
        #Compile them
        #debug
        #if (u"ImplicitMemes.HasChild" in sourceMeme.path.fullTemplatePath) or (u"ImplicitMemes.MiddleNode" in sourceMeme.path.fullTemplatePath):
        #    pass
        #/debug
        unused_createMeme = sourceMeme.compile(False, False)   #Compile returns a validation report.  Ignore it
        memes.append(templateRepository.resolveTemplateAbsolutely(sourceMeme.path.fullTemplatePath)) 
    
    if validateOnLoad == True:  
        logQ.put( [logType , logLevel.INFO , method ,"ValidateOnLoad is set to 'true' in AngelaMasterConfiguration.xml"])   
        logQ.put( [logType , logLevel.INFO , method ,"Starting Meme Validation"])    
        for sourceMeme in memes:
            #Validate the new meme, but don't actually do anything with the report.
            #    This just puts any errors with the memes in the engine log.
            unused_justDoIt = sourceMeme.validate([])
        logQ.put( [logType , logLevel.INFO , method ,"Finished Meme Validation"])
    else:
        logQ.put( [logType , logLevel.INFO , method ,"ValidateOnLoad is set to 'false' in AngelaMasterConfiguration.xml.  No auto validation will be performed"])

    #Refactor memes with aubatomic links
    #Previously, when reading the memes in, we could not determine which children had subatomic links.
    #   This information is defined in the metameme only and when reading a meme from its file, it is not possible
    #   to fully resolve child meme links, as they may have the local name only in the xml file.  
    #At this stage however, we have our metamemes and memes in the template repository and can fully resolve child memes.
    #    This allows us to finally determine which ones should be subatomic
    for sourceMeme in memes:
        memeToBeUpdated = templateRepository.templates[sourceMeme.path.fullTemplatePath]
        for memberMemeKey in memeToBeUpdated.memberMemes.keys():
            occurs = memeToBeUpdated.memberMemes[memberMemeKey][0]  #memermeme is a tuple with coocurence count at position 0 and linkType at position 1
            sourceMetaMeme = templateRepository.templates[memeToBeUpdated.metaMeme]
            try:
                memberPath = templateRepository.resolveTemplatePath(sourceMeme.path.fullTemplatePath, memberMemeKey)
                memberMeme = templateRepository.templates[memberPath]
                membership = sourceMetaMeme.memberMetaMemes[memberMeme.metaMeme]
                if membership.lt == linkTypes.SUBATOMIC:  
                    memeToBeUpdated.memberMemes[memberMemeKey] = (occurs, linkTypes.SUBATOMIC)
                    templateRepository.templates[sourceMeme.path.fullTemplatePath] = memeToBeUpdated
                    unusedCatch = "me"
            except:
                pass
    
    
    #Restore entities from persistence
    entityTupleList = entityRepository.getAllArchivedEntities(0)
    for entityTuple in entityTupleList:
        #entityTuple[] = uuid, meme, metameme
        try:
            #convert the master entity ID to a string
            perparedUUIDFormat = '{%s}' % entityTuple[3]
            masterEntityID = uuid.UUID(perparedUUIDFormat)
            
            #Rebuild the entity
            meme = templateRepository.resolveTemplateAbsolutely(entityTuple[1])
            entityID = meme.getEntityFromMeme(masterEntityID, False, entityTuple[0])
            entity = entityRepository.getEntity(entityID)
        except Exception as e:
            raise e
    for entityTuple in entityTupleList:    
        try:
            entity.initialize()
        except Exception as e:
            raise e

        
    #now, we should make sure that all singleton memes are instantiated.
    logQ.put( [logType , logLevel.INFO , method ,"Instantiating singleton memes"])
    for meme in memes:
        try:
            if meme.isSingleton == True:
                logQ.put( [logType , logLevel.INFO , method ,"Meme %s is a singleton and will be instantiated" %(meme.path.fullTemplatePath)])
                try:
                    entityID = meme.getEntityFromMeme()
                except Exception as e:
                    logQ.put( [logType , logLevel.WARNING , method ,"Meme %s is a singleton, but can't be instantiated.  Traceback = %s" %(meme.path.fullTemplatePath, e)])
                    print("Meme %s is a singleton, but can't be instantiated.  Traceback = %s" %(meme.path.fullTemplatePath, e))                        
        except Exception as e:
            logQ.put( [logType , logLevel.WARNING , method ,"Meme %s is a singleton, but can't be instantiated.  Traceback = %s" %(meme.path.fullTemplatePath, e)])
            print("Meme %s is a singleton, but can't be instantiated.  Traceback = %s" %(meme.path.fullTemplatePath, e))
            #try:
                #entityID = meme.getEntityFromMeme()
                #singletonEntityList.append(entityID)
            #except:
                #pass
    
    #Lastly, iterate over any already created entities (singletons and members) and 
    #    make sure that they have their scripts intialized
    entityList = api.getAllEntities()
    logQ.put( [logType , logLevel.INFO , method , "Instantiating %s enities." %(len(entityList))])
    for entityID in entityList:
        try:
            entity = entityRepository.getEntity(entityID)
            try:
                entity.initialize()
            except Exception as e:
                # if a new initialization is throwing an exception, the following statement can be uncommented to try debugging it
                #entity.initialize()
                
                #Build up a full java or C# style stacktrace, so that devs can track down errors in script modules within repositories
                fullerror = sys.exc_info()
                errorID = str(fullerror[0])
                nestEerrorMsg = str(fullerror[1])
                tb = sys.exc_info()[2]
                errorMsg = "Failed to initialize entity of type %s.  Nested Traceback = %s: %s" %(entity.memePath.fullTemplatePath, errorID, nestEerrorMsg)
                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                raise Exceptions.EntityInitializationError(errorMsg).with_traceback(tb)
        except Exceptions.EntityInitializationError as e:
            #Error already logged
            pass
        except Exception as e:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            nestEerrorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            errorMsg = "Failed to initialize entity %s of unknown type.  It seems not to be in the repository.  Nested Traceback = %s: %s" %(entityID, errorID, nestEerrorMsg)
            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
            #debug
            #entity = entityRepository.getEntity(entityID)
            #/debug
    
    #We are now ready to serve
    global readyToServe
    readyToServe = True        
    #logQ.put( [logType , logLevel.DEBUG , method , 'Finished loading memes from XML in queue.  Meme Queue now empty.']) 
    #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])


    

def getUUIDAsString(uuidToParse):
    #ensure that the uuid given as a parameter is in unicode format
    try:
        testStr = 'x'
        testUnicode = 'x'

        if type(uuidToParse) == type(testStr):
            uuidAsString = str(uuidToParse)
            return uuidAsString
        elif type(uuidToParse) == type(testUnicode):
            #nothing to do
            return uuidToParse
        else:
            #2to3 change location
            #stringURN = uuidToParse.get_urn()
            stringURN = uuidToParse.urn
            partStringURN = stringURN.rpartition(":")
            uuidAsString = partStringURN[2]
            return uuidAsString
    except Exception as e:
        return "Traceback = %s" %e  



def getRestrictionsFromFile(xmlData, codepage, modulePath):
    ''' Given a file containing n PropertyRestriction elements, return a dict containing all restrictins.  
    This intended to run once, at server intiialization '''
    #method = moduleName + '.getRestrictionsFromFile'
    #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    
    #Parse the condition file in a unicode friendly manner
    #logQ.put( [logType , logLevel.DEBUG , method , "module name = %s, codepage = %s" %(modulePath, codepage)])
    fileXML = minidom.parseString(xmlData.encode( codepage ))
    if fileXML == None:
        raise Exceptions.EmptyFileError
    
    restrictions = []

    for restrictionElement in fileXML.getElementsByTagName("PropertyRestriction"):
        strName = restrictionElement.getAttribute("id")
        path = TemplatePath(modulePath, strName)

        #logQ.put( [logType , logLevel.DEBUG , method , "Building PropertyRestriction %s" %(strName)])
        
        for restrictionMMIElement in restrictionElement.getElementsByTagName("RestrictionMinMaxInteger"):
            minVal = None
            maxVal = None   
            try:
                minStr = restrictionMMIElement.getAttribute("restrictionMin")
                minVal = int(minStr)
            except: pass
            try:
                maxStr = restrictionMMIElement.getAttribute("restrictionMax")
                maxVal = int(maxStr)
            except: pass
            restriction = PropertyRestrictionInteger(path, minVal, maxVal)
            restrictions.append(restriction)
            
        for restrictionMMDElement in restrictionElement.getElementsByTagName("RestrictionMinMaxDecimal"):
            minVal = None
            maxVal = None   
            try:
                minStr = restrictionMMDElement.getAttribute("restrictionMin")
                minVal = decimal.Decimal(minStr) 
            except: pass
            try:
                maxStr = restrictionMMDElement.getAttribute("restrictionMax")
                maxVal = decimal.Decimal(maxStr)
            except: pass
            restriction = PropertyRestrictionDecimal(path, minVal, maxVal)
            restrictions.append(restriction)
            
        restrictionList = []    
        for restrictionValElement in restrictionElement.getElementsByTagName("RestrictionValueString"):
            restrictionEntry = restrictionValElement.firstChild.data
            restrictionList.append(restrictionEntry)
        for restrictionValElement in restrictionElement.getElementsByTagName("RestrictionValueInteger"):
            restrictionEntryStr = restrictionValElement.firstChild.data
            restrictionEntry = int(restrictionEntryStr)
            restrictionList.append(restrictionEntry)
        for restrictionValElement in restrictionElement.getElementsByTagName("RestrictionValueDecimal"):
            restrictionEntryStr = restrictionValElement.firstChild.data
            restrictionEntry = decimal.Decimal(restrictionEntryStr)
            restrictionList.append(restrictionEntry)

        if restrictionList.__len__() > 0:
            restriction = PropertyRestrictionList(path, restrictionList)
            restrictions.append(restriction)
        #except Exception as e:
            #logQ.put( [logType , logLevel.WARNING , method ,  u"Internationalized Descriptor %s encountered error while loading from file %s!" % (strName, path.fullTemplatePath) ])
            #logQ.put( [logType , logLevel.WARNING , method ,  "Traceback = %s \n" %e])
            #raise Exceptions.UndefinedUUIDError
        
        #add the restrictions from the file to the repository    
        for restriction in restrictions:
            templateRepository.catalogTemplate(restriction.path, restriction)
            
    #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return restrictions

      


def getMetaMemesFromFile(xmlData, codepage, modulePath):
    ''' Given a file containing one or more meta memes, return a dict containing all metamemes.  
    This intended to run once, at server intiialization '''
    method = moduleName + '.getMetaMemesFromFile'
    #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    
    #Parse the condition file in a unicode friendly manner
    fileXML = minidom.parseString(xmlData.encode( codepage ))
    if fileXML == None:
        raise Exceptions.EmptyFileError
    
    metaMemes = []
    
    for metaMemeElement in fileXML.getElementsByTagName("MetaMeme"):
        
        strName = metaMemeElement.getAttribute("id")
        path = TemplatePath(modulePath, strName)
        #logQ.put( [logType , logLevel.DEBUG , method , "loading metameme id %s at path %s" %(strName, path.fullTemplatePath)])
        
        isSwitch = False
        try: 
            isSwitchStr = metaMemeElement.getAttribute("switch")
            if isSwitchStr == "true":
                isSwitch = True
        except: pass
        
        isSingleton = False
        try:
            isSingletonStr = metaMemeElement.getAttribute("singleton")
            if isSingletonStr == "true":
                isSingleton = True
        except: pass
        
        isCloneable = False
        try:
            isCloneableStr = metaMemeElement.getAttribute("dynamic")
            if isCloneableStr == "cloneable":
                isCloneable = True
        except: pass
        
        extends = []
        for extendsElement in metaMemeElement.getElementsByTagName("MetaMemeExtensions"):
            for idElement in extendsElement.getElementsByTagName("MetaMemeID"):
                mmID = idElement.firstChild.data
                extends.append(mmID)
                
        
        enhances = []
        for modifiesElement in metaMemeElement.getElementsByTagName("MetaMemeEnhancements"):
            for idElement in modifiesElement.getElementsByTagName("MetaMemeID"):
                mmID = idElement.firstChild.data
                enhances.append(mmID)
        
        memberMetaMemes = {}
        for memberMetaMemeElement in metaMemeElement.getElementsByTagName("MemberMetaMeme"):
            strName = memberMetaMemeElement.getAttribute("reference")
            memPath = TemplatePath(modulePath, strName)
         
            cardMin = 0
            try: 
                minStr = memberMetaMemeElement.getAttribute("min")
                cardMin = int(minStr)
            except: pass
            
            # Let's default the maximum number of member on unbound to the high end for a 16 bit signed int.
            #    We can alsways go back later and come up with a cleaner implementation when someone needs an 
            #    object with > 32k members 
            cardMax = 32767 
            try: 
                maxStr = memberMetaMemeElement.getAttribute("max")
                cardMax = int(maxStr)
            except: pass
            
            lt = 0
            memberMetaMeme = MemberMetaMeme(memPath, cardMin, cardMax, lt)
            memberMetaMemes[memPath.fullTemplatePath] = memberMetaMeme
            
                
        properties = {}
        for propertyElement in metaMemeElement.getElementsByTagName("MetaMemeProperty"):
            name = propertyElement.getAttribute("name")
            propertyType = propertyElement.getAttribute("type")
            restType = None
            try:
                restType = propertyElement.getAttribute("restriction")
            except:
                pass
            constrained = False
            try:
                constrainedStr = propertyElement.getAttribute("constrained")
                #Presumably the xsd definition is not being used while parsing the xml file
                #    and the xs:boolean restriction on the 'constrained' attribute means nothing
                if constrainedStr == 'true':
                    constrained = True
            except:
                pass
            
            #Resolve Restrictions.  Since restrictions are loaded before metamemes, we can resolve the restrictions right away
            restMin = None
            restMax = None
            restList = [] 
            if (restType is not None) and (len(restType) > 1):
                #logQ.put( [logType , logLevel.DEBUG , method , "...resolving restriction %s for prop %s" %(restType, name)])
                try:
                    restriction = templateRepository.resolveTemplate(path, restType)
                    restrictionType = restriction.className
                    if restrictionType.find('PropertyRestrictionDecimal') >= 0:
                        restMin = restriction.min
                        restMax = restriction.max
                    elif restrictionType.find('PropertyRestrictionInteger') >= 0:
                        restMin = restriction.min
                        restMax = restriction.max
                    elif restrictionType.find('PropertyRestrictionList') >= 0:
                        restList = restriction.values
                except Exception as e:
                    logQ.put( [logType , logLevel.ERROR , method , "Can't properly resolve restriction %s for prop %s.  Traceback = %s" %(restType, name, e)])
            else:
                constrained = False
                #logQ.put( [logType , logLevel.DEBUG , method , "... prop %s has no restrictions" %(name)])
            templateProperty = PropertyDefinition(name, propertyType, restMin, restMax, restList, constrained)
            properties[name] = templateProperty

            #logQ.put( [logType , logLevel.DEBUG , method , "Building MetaMeme %s, property %s, of type %s with restriction %s" %(strName, name, propertyType, restType)])
            
        #first, create the metameme
        metaMeme = MetaMeme(path, isSwitch, extends, enhances, properties, memberMetaMemes, isSingleton)
        
        #dynamic metamemes
        metaMeme.setCloneable(isCloneable)

        #If we have an ImplicitMemeMasterData element, we should add the appropriate objects to the metameme object
        for implicitElement in metaMemeElement.getElementsByTagName("ImplicitMemeMasterData"):
            implicitMemeMasterData = None
            table = implicitElement.getAttribute("table")
            primaryKeyColumn = implicitElement.getAttribute("primaryKeyColumn")
            implicitMemeMasterData = ImplicitMemeMasterData(table, primaryKeyColumn)
            i2 = copy.deepcopy(implicitMemeMasterData) #this line is a worksround, because Python infuriantingly is re-using the same copy implicitMemeMasterData and we end up accumulating the property references for ALL impolicit memes
            
            for propertySourceElement in implicitElement.getElementsByTagName("PropertySource"):
                propertyID = primaryKeyColumn = propertySourceElement.getAttribute("property")
                columnID = primaryKeyColumn = propertySourceElement.getAttribute("column")
                i2.addImplicitProperty(propertyID, columnID)
                
            for forwardReferenceElement in implicitElement.getElementsByTagName("ForwardReference"):
                table = forwardReferenceElement.getAttribute("table")
                childColumn = forwardReferenceElement.getAttribute("childColumn")
                parentColumn = forwardReferenceElement.getAttribute("parentColumn")
                traversePath = forwardReferenceElement.getAttribute("traversePath")
                implicitMemeRelationship = ImplicitMemeRelationship(table, childColumn, parentColumn, traversePath)
                i2.addForwardReference(implicitMemeRelationship)
                
            for backReferenceElement in implicitElement.getElementsByTagName("BackReference"):
                table = backReferenceElement.getAttribute("table")
                childColumn = backReferenceElement.getAttribute("childColumn")
                parentColumn = backReferenceElement.getAttribute("parentColumn")
                traversePath = backReferenceElement.getAttribute("traversePath")
                backRefColumn = None
                try:
                    backRefColumn = backReferenceElement.getAttribute("backReferenceColumn")
                except: pass
                implicitMemeRelationship = ImplicitMemeRelationship(table, childColumn, parentColumn, traversePath, backRefColumn)
                i2.addBackReference(implicitMemeRelationship)
            
            if implicitMemeMasterData is not None:
                metaMeme.setImplicit(i2)
            
        #We're finished.  Add it to the metememes list
        metaMemes.append(metaMeme)            
    #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return metaMemes



def getMemesFromFile(dbConnectionString, xmlData, codePage, modulePath):
    '''  The filename is a nismomer:  this method gets the memes from a file AND fetches any corresponding metadata from a relational database 
        Given a file containing one or more memes, return a list containing all memes.  This intended to run once, at server intiialization '''
    method = moduleName + '.getMemesFromFile'
    global dbConnection
    global persistenceDB
    global persistenceType
    global sqlSyntax
    #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
    
    #Parse the condition file in a unicode friendly manner
    fileXML = minidom.parseString(xmlData.encode( codePage ))
    if fileXML == None:
        raise Exceptions.EmptyFileError

    memes = []
    debugMemes = {}

    try:
       
        for memeElement in fileXML.getElementsByTagName("Meme"):
        
            memesToBeCreated = []
            
            isImplicitMeme = False
            try:
                isImplicitMemeStr = memeElement.getAttribute("implicitMeme")
                if isImplicitMemeStr == "true":
                    isImplicitMeme = True
            except:
                pass
            
            metamemeAsStr = memeElement.getAttribute("metameme")
            
            #If it is an implicit meme, we need the metameme, to get the table connection info to build the meme list
            #   Otherwise, we need the meme path to get the metameme.  ;-)
            metaMeme = None
            path = None
            try:
                strName = memeElement.getAttribute("id")
                #debug
                if "Landmark1" in strName:
                    pass
                #/debug
                path = TemplatePath(modulePath, strName)
                try:
                    metaMeme = templateRepository.resolveTemplate(path, metamemeAsStr)
                except: #try resolving absolutely
                    metaMeme = templateRepository.resolveTemplateAbsolutely(metamemeAsStr)
            except Exception as e:
                raise e
                    
            if isImplicitMeme == True:
                if persistenceDB is None:
                    raise Exceptions.UndefinedPersistenceError()
                try:
                    #Set the SQL Syntax
                    global sqlSyntax
                    try:
                        #selectStatement = sqlSyntax.selectMemesFromMetamameTable
                        selectStatement = "SELECT %s FROM %s" %(metaMeme.implicitMemeMasterData.primaryKeyColumn, metaMeme.implicitMemeMasterData.table)
                    except:
                        raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectMemesFromMetamameTable, as sqlSyntax has not been defined")
                    cursor = dbConnection.cursor()
                    cursor.execute(selectStatement) #table name can't be parameterized
                    #cursor.execute(selectStatement, (metaMeme.implicitMemeMasterData.primaryKeyColumn, metaMeme.implicitMemeMasterData.table, ))
                    for row in cursor:
                        path = TemplatePath(modulePath, row[0])
                        implicitMeme = SourceMeme(path, metaMeme, row[0])
                        memesToBeCreated.append(implicitMeme) 
                except Exception as e:
                    errorMsg = "SQL Error while building implicit meme %s.  Failed SQL Select statement: %s" %(strName, selectStatement)
                    logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                    raise Exceptions.PersistenceQueryError(errorMsg)
            else:
                explicitMeme = SourceMeme(path, metaMeme)
                memesToBeCreated.append(explicitMeme)
            
            #Now that we have our list of memes to be created, lets actually fill them in    
            for meme in memesToBeCreated:
                propNameOccurances = {}
                for propertyElement in memeElement.getElementsByTagName("MemeProperty"):
                    propName = propertyElement.getAttribute("name")
                    propValueStr= propertyElement.getAttribute("value")
                    
                    #Try to make sure that any given MemeProperty only occurs once
                    try:
                        assert propName not in propNameOccurances
                        #all clear.  This was just to ensure that there is NOT already an entry.
                        propNameOccurances[propName] = 'X'
                        meme.setProperty(propName, propValueStr)
                    except:
                        propError = "Meme %s has property %s that occurs multiple times in definition" % (path.fullTemplatePath, propName)
                        logQ.put( [logType , logLevel.WARNING , method , propError])
                    
                    
                for memberElement in memeElement.getElementsByTagName("MemberMeme"):
                    memberID = memberElement.getAttribute("memberID")
                    occurrence= memberElement.getAttribute("occurrence")
                    lt = 0  #linkType = ATOMIC
                    try:
                        xmlLT = memberElement.getAttribute("linktype")
                        if xmlLT == "subatomic":
                            lt = 1 #linkType = SUBATOMIC
                    except: pass
                    meme.addMemberMeme(memberID, occurrence, lt)
                    
                for modifiesElement in memeElement.getElementsByTagName("MemeEnhancements"):
                    for idElement in modifiesElement.getElementsByTagName("MemeID"):
                        enhancementID = idElement.firstChild.data
                        meme.addEnhancement(enhancementID)
                    
                try:
                    isSingletonStr = memeElement.getAttribute("singleton")
                    if isSingletonStr == "true":
                        meme.setSingleton(True)
                except:
                    pass
                    
                #ListOfTags
                for tagElement in memeElement.getElementsByTagName("Tag"):
                    tagRaw = tagElement.firstChild.data
                    tag = str(tagRaw)
                    meme.addTag(tag)
                    
                    
                #clones
                for clonedMemberElement in memeElement.getElementsByTagName("ClonedMember"):
                    metamemeToBeCloned = clonedMemberElement.getAttribute("memberMetaMeme")
                    meme.clones.append(metamemeToBeCloned)
                
                #We need to make sure that we have a valid Design Time DB connection
                dbDesignTimeCon = None
                if (persistenceType == ":memory:") or (persistenceType == "none"):
                    global createTestData
                    if createTestData is True:
                        #Dynamicall create astandard regression test data in-memory.  This is only used or testing
                        #In the Git repository, containing the Graphyne package, there are sibling modules that collectively make up
                        #  the Graphyne test harness.  Additionally, there is a sibling package, called TestUtils.  TestUtils contains
                        #  utilitied for generating design time data in regression testing.
                        try:
                            import TestUtils   
                            import sqlite3 as dtDBDriverSQLiteDT
                            dbDesignTimeCon = dtDBDriverSQLiteDT.connect(':memory:')
                            TestUtils.CreateDesignTimeData.createDB(dbDesignTimeCon)
                        except Exception as e:
                            errorMsg = "Failed to create design time test data.  The likely error is as follows:"
                            errorMsg = "%s  Graph.startDB was apparently started with a persistence type of ':memory:' or 'none' and the createTestDatabase option set to True." %errorMsg
                            errorMsg = "%s  This paremeter combintaion is only intended for regression testing of Graphyne and is invoked by the regression test modules in the" %errorMsg
                            errorMsg = "%s Github repository for Graphyne, at https://github.com/davidhstocker/Graphyne.  In any case, a traceback of the underlying exception is provided." %errorMsg
                            errorMsg = "%s  \n\nIt whould be noted that in this case, the environment (PYTHONPATH) should include the parent directory of TestUtils.  Env= %s" %(errorMsg, os.environ)
                            errorMsg = "%s  \n\nTraceback = %s" %(errorMsg, e)
                            raise Exceptions.InconsistentPersistenceArchitecture(persistenceDB, persistenceDB, errorMsg)
                else:
                    #designTimeConnection is passed as an arg at startup.  it might be a string representing a file location of an sqlite file, or a pyodbc connection string.
                    #We don't yet know which it is
                    try:
                        #first try to see if designTimeConnection is a reference to a sqlite ile
                        import sqlite3 as dtDBDriverSQLite2
                        dbDesignTimeCon = dtDBDriverSQLite2.connect(dbConnection)
                    except Exception as e:
                        dbDesignTimeCon = dbConnection
                        if dbDesignTimeCon is None:
                            errorMessage = "persistence type is not none or sqlite :memory: and required database connection for implicit memes is missing"
                            raise Exceptions.MissingImlpicitMemeDatabase(errorMessage)
    
    
                #Todo
                #fill in the properties from the table
                if isImplicitMeme is True:
                    for implicitPropertyID in metaMeme.implicitMemeMasterData.properties.keys():
                        implicitPropertyColumn = metaMeme.implicitMemeMasterData.properties[implicitPropertyID]
                        #SELECT * FROM Customers WHERE Country='Mexico';
                        #Should return exactly one row
                        try:
                            #Set the SQL Syntax
                            try:
                                #selectStatement = sqlSyntax.selectImplicitMemesFromMetamemeTable
                                selectStatement = "SELECT %s FROM %s WHERE %s='%s'" %(implicitPropertyColumn, metaMeme.implicitMemeMasterData.table, metaMeme.implicitMemeMasterData.primaryKeyColumn, meme.path.templateName)
                            except:
                                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectImplicitMemesFromMetamemeTable, as sqlSyntax has not been defined")
    
                            cursor = dbDesignTimeCon.cursor()
                            cursor.execute(selectStatement)
                            #cursor.execute(selectStatement, (implicitPropertyColumn, metaMeme.implicitMemeMasterData.table, metaMeme.implicitMemeMasterData.primaryKeyColumn, meme.path.templateName, ))
                            for row in cursor:
                                meme.setProperty(implicitPropertyID, row[0])
                        except Exception as e:
                            errorMsg = "SQL Error while retreiving properties in implicit meme %s.  Failed SQL Select statement: %s" %(strName, selectStatement)
                            logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                            raise Exceptions.PersistenceQueryError(errorMsg)
                
                
                if isImplicitMeme is True:
                    try:
                        pass
                    except:
                        pass
                    
                    
                    try:
                        #Build the forward references
                        logQ.put( [logType , logLevel.INFO , method , "Implict Meme %s has %s forward references" %(metaMeme.implicitMemeMasterData.table, len(metaMeme.implicitMemeMasterData.forwardReferences))])
                        for fr in metaMeme.implicitMemeMasterData.forwardReferences:
                            #first, determine the foreign key value to be used in the forward reference
                            
                            foreignKeyValue = None
                            
                            try:
                                #Set the SQL Syntax
                                try:
                                    #selectStatement = sqlSyntax.selectImplicitMemesForwardReferences
                                    selectStatement = "SELECT %s FROM %s WHERE %s='%s'" %(fr.parentColumn, metaMeme.implicitMemeMasterData.table, metaMeme.implicitMemeMasterData.primaryKeyColumn, meme.path.templateName)
                                except:
                                    raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectImplicitMemesForwardReferences, as sqlSyntax has not been defined")
    
                                cursor = dbDesignTimeCon.cursor()
                                cursor.execute(selectStatement)
                                #cursor.execute(selectStatement, (fr.parentColumn, metaMeme.implicitMemeMasterData.table, metaMeme.implicitMemeMasterData.primaryKeyColumn, meme.path.templateName, ))
                                for row in cursor:
                                    foreignKeyValue = row[0]
                            except Exception as e:
                                errorMsg = "SQL Error while retreiving forward references in implicit meme %s.  Failed SQL Select statement: %s" %(metaMeme.implicitMemeMasterData.table, selectStatement)
                                logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                                raise Exceptions.PersistenceQueryError(errorMsg)
                        
                            if foreignKeyValue is not None:
                                try:
                                    if hasattr(fr, 'path'):
                                        frPath = fr.path
                                        meme.implicitReferences[foreignKeyValue] = frPath
                                except Exception as e:
                                    errorMsg = "Error assigning forward implicit reference %s to implicit meme %s.  Traceback: %s" %(foreignKeyValue, metaMeme.implicitMemeMasterData.table, e)
                                    logQ.put( [logType , logLevel.WARNING , method , errorMsg])
           
                        #Build the forward references
                        logQ.put( [logType , logLevel.INFO , method , "Implict Meme %s has %s backward references" %(metaMeme.implicitMemeMasterData.table, len(metaMeme.implicitMemeMasterData.backReferences))])
                        for br in metaMeme.implicitMemeMasterData.backReferences:
                            if br.backReferenceColumn is not None:
                                #first, go to the child table and get all of the primary keys, where the parentColumn (containing the back referene) points to the ID of the current meme (meme.path.templateName)
                                foreignKeyValues = []
                                try:
                                    #Set the SQL Syntax
                                    try:
                                        selectStatement = "SELECT %s FROM %s WHERE %s='%s'" %(br.childColumn, br.table, br.backReferenceColumn, meme.path.templateName)
                                    except Exception as e:
                                        raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectImplicitMemesBackwardReferences, as sqlSyntax has not been defined")
    
                                    cursor = dbDesignTimeCon.cursor()
                                    cursor.execute(selectStatement)
                                    #cursor.execute(selectStatement, (br.childColumn, br.table, br.backReferenceColumn, meme.path.templateName, ))
                                    for row in cursor:
                                        foreignKeyValue = row[0]
                                        if foreignKeyValue is not None:
                                            foreignKeyValues.append(foreignKeyValue)
                                except Exception as e:
                                    errorMsg = "SQL Error while retreiving back references in implicit meme %s.  Failed SQL Select statement: %s" %(metaMeme.implicitMemeMasterData.table, selectStatement)
                                    logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                                    raise Exceptions.PersistenceQueryError(errorMsg)
                                
                               
                                #create an implicitReferences entry for every entry in foreignKeyValues
                                for unusedChildTpParentReference in foreignKeyValues:
                                    try:
                                        brPath = br.path
                                        meme.implicitReferences[unusedChildTpParentReference] = brPath
                                    except Exception as e:
                                        errorMsg = "Error assigning backward implicit reference %s to implicit meme %s.  Traceback: %s" %(unusedChildTpParentReference, metaMeme.implicitMemeMasterData.table, e)
                                        logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                    except Exceptions.MissingImlpicitMemeDatabase as e:
                        logQ.put( [logType , logLevel.ERROR , method , errorMsg])
                    except Exception as e:
                        errorMsg = "Error assigning implicit references implicit meme %s.  Traceback: %s" %(meme.path.templateName, e)
                        logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                 
                memes.append(meme)
                debugMemes[meme.localPath] = meme.implicitReferences
                logQ.put( [logType , logLevel.DEBUG , method , "Read %s from %s" %(meme.path.templateName, modulePath)])
    except Exceptions.InconsistentPersistenceArchitecture as e:
        raise e
    except Exception as e:
        errorMsg =  "Fatal error while loading module %s.  Module not completely loaded.  Traceback = %s" %(modulePath, e)
        logQ.put( [logType , logLevel.ERROR , method , errorMsg])
    
    #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
    return memes



def getSourceMemesExtension(iterationsList, sourceMemeList):
    """
        Determine which source memes need to be cloned.  And return the list
    """
    method = moduleName + '.getSourceMemesExtension'
    returnList = []
    updatesSourceMemeList = []
    for sourceMeme in iterationsList:
        for cloneMe in sourceMeme.clones:
            '''    find the relevant member source meme and clone it.  Replace the path with the relevant values
            '''
            for possibleSMToBeCloned in sourceMemeList:
                if possibleSMToBeCloned.metaMeme.path.fullTemplatePath == cloneMe:
                    #clone the sourcememe and add it to returnList
                    try:
                        #irst, we create a new, blank, SourceMeme
                        oldMemberPath = possibleSMToBeCloned.path.fullTemplatePath
                        newMemberName = "%s_%s" %(possibleSMToBeCloned.path.templateName, sourceMeme.path.templateName)
                        path = TemplatePath(possibleSMToBeCloned.path.modulePath, newMemberName)
                        clonedSourceMeme = SourceMeme(path, possibleSMToBeCloned.metaMeme)
                        
                        #Next, we deepcopy the contents over from possibleSMToBeCloned
                        # Note - we do a stepwise copy, because deepcopy is not threadsafe and the reentrant lock on SourceMeme causes an exception to be thrown if we try to copy it in one shot  
                        clonedSourceMeme.memberMemes = copy.deepcopy(possibleSMToBeCloned.memberMemes)
                        clonedSourceMeme.properties = copy.deepcopy(possibleSMToBeCloned.properties)
                        clonedSourceMeme.implicitReferences = copy.deepcopy(possibleSMToBeCloned.implicitReferences)
                        clonedSourceMeme.clones = copy.deepcopy(possibleSMToBeCloned.clones)
                        clonedSourceMeme.enhances = copy.deepcopy(possibleSMToBeCloned.enhances)
                        clonedSourceMeme.tags = copy.deepcopy(possibleSMToBeCloned.tags)
                        clonedSourceMeme.isSingleton = copy.deepcopy(possibleSMToBeCloned.isSingleton)
                        clonedSourceMeme.invalidProps = copy.deepcopy(possibleSMToBeCloned.invalidProps)
                        clonedSourceMeme.entityUUID = copy.deepcopy(possibleSMToBeCloned.entityUUID)
                        clonedSourceMeme.inactive = copy.deepcopy(possibleSMToBeCloned.inactive)
                        clonedSourceMeme.localPath = newMemberName
                        if possibleSMToBeCloned.metaMeme.isCloneable == False:
                            errorMessage = "%s is not cloneable" % (possibleSMToBeCloned.path.fullTemplatePath)
                            loggedError = Exceptions.DisallowedCloneError(errorMessage)
                            clonedSourceMeme.validationErrors.append(loggedError)
                            logQ.put( [logType , logLevel.WARNING , method , errorMessage ])
                        try:
                            sourceMeme.swapImplicitReference(clonedSourceMeme.path.templateName, possibleSMToBeCloned.path.templateName)
                            returnList.append(clonedSourceMeme) #We'll be adding this to the  returnList
                        except Exception as e:
                            pass
                            #debug
                            #sourceMeme.swapImplicitReference(clonedSourceMeme.path.templateName, possibleSMToBeCloned.path.templateName)
                        
                        #Let's do a recursive call to ensure that we get ALL requires extensions
                        if len(clonedSourceMeme.clones) > 0:
                            returnListExtension = getSourceMemesExtension([clonedSourceMeme], sourceMemeList)
                            returnList.extend(returnListExtension)
                            
                        toBeTransformedList = list(sourceMeme.implicitReferences.keys())
                        for toBeTransformed in toBeTransformedList:
                            if oldMemberPath in toBeTransformed:
                                implicitReferenceValue = sourceMeme.implicitReferences[toBeTransformed]
                                del sourceMeme.implicitReferences[toBeTransformed]
                                newlyTransformed = toBeTransformed.replace(oldMemberPath, path.fullTemplatePath)
                                sourceMeme.implicitReferences[newlyTransformed] = implicitReferenceValue
                                

                    except Exception as e:
                        errorMsg = "Error while cloning %s's member %s.  Traceback = %s" %(sourceMeme.fullTemplatePath, possibleSMToBeCloned.metaMeme.path.fullTemplatePath, e)
                        logQ.put( [logType , logLevel.WARNING , method , errorMsg ])
        updatesSourceMemeList.append(sourceMeme)
    updatesSourceMemeList.extend(returnList)
    return updatesSourceMemeList 
        

 


def filterListDuplicates(listToFilter):
    # Not order preserving
    keys = {}
    for e in listToFilter:
        keys[e] = 1
    return list(keys.keys())


#A helper method for finding the location of an entity State Event Script, when something went wrong.
def getScriptLocation(entityID, eventType, propID = None):
    """
        This method is called whenever a State Event Script throws an exception.  It's purpose is to find the filesystem location of the script that thre the exception.
        This is useful for tracking down bugs in SES scripts.  When entities are intiialized, the SES script classes are initialized and added directly to the Entities as
        callable objects.  This gives a performance boost, as we can skip the graph traverses; tracking down the child SES entity and then the script entity.  SES scripts
        are defined at design time and remain static for the lifetime of an entity.  As the entity is 'compiled', when there is an exception taised by an SES script, we 
        have to make graph traverses to assemble the information that the graph designer will need to licate the offending script and troubleshoot what happened.
        
        entityID = The UUID of the entity whose SES script raised the exception.
        eventType = Which of that entity's registered SES events raised the exception.
        propID = If the event is the property changed event, then this should be filled with a string value, the entity property associated with the SES event.  If this is
        any other kind of event, then this property will be None.
        
        
    """                   
    scriptLoc = None
    try:
        #find the location of the script
        theEntity = entityRepository.getEntity(entityID)
        sesEntities = theEntity.getLinkedEntitiesByMetaMemeType('Graphyne.DNA.StateEventScript', linkTypes.SUBATOMIC)
        for sesEntityUUID in sesEntities:
            sesEntity = entityRepository.getEntity(sesEntityUUID)
            state = sesEntity.getPropertyValue('State')
            if state == eventType:
                scriptEntities = sesEntity.getLinkedEntitiesByMetaMemeType('Graphyne.DNA.Script', linkTypes.SUBATOMIC)
                for scriptEntityUUID in scriptEntities:
                    scriptEntity = entityRepository.getEntity(scriptEntityUUID)
                    scriptLoc = scriptEntity.getPropertyValue('Script')
        return scriptLoc
    except Exception:
        fullerror = sys.exc_info()
        errorID = str(fullerror[0])
        errorMsg = str(fullerror[1])
        tb = sys.exc_info()[2]
        raise Exceptions.EventScriptFailure("%s event can't be associated with event script.  Nested Traceback %s: %s" %(eventType, errorID, errorMsg)).with_traceback(tb)

        

#def runscript(script):
#    pass
    
    
    
#/Engine
#API
class API(object):
    scriptDict = {}
 
    def __init__(self):
        self.scriptDict["createEntityFromMeme"] = createEntityFromMeme()
        self.scriptDict["addEntityDecimalProperty"] = addEntityDecimalProperty()
        self.scriptDict["addEntityIntegerProperty"] = addEntityIntegerProperty()
        self.scriptDict["addEntityListProperty"] = addEntityListProperty()
        self.scriptDict["addEntityStringProperty"] = addEntityStringProperty()
        self.scriptDict["addEntityBooleanProperty"] = addEntityBooleanProperty()
        self.scriptDict["addEntityTaxonomy"] = addEntityTaxonomy()
        self.scriptDict["destroyEntity"] = destroyEntity()
        self.scriptDict["getAllEntitiesByTag"] = getAllEntitiesByTag()
        self.scriptDict["getAllEntitiesByTaxonomy"] = getAllEntitiesByTaxonomy()
        self.scriptDict["getEntitiesByMemeType"] = getEntitiesByMemeType()
        self.scriptDict["getEntitiesByMetaMemeType"] = getEntitiesByMetaMemeType()
        self.scriptDict["getEntity"] = getEntity()
        self.scriptDict["getAllEntities"] = getAllEntities()
        self.scriptDict["getEntityMemeType"] = getEntityMemeType()
        self.scriptDict["getEntityMetaMemeType"] = getEntityMetaMemeType()
        self.scriptDict["getEntityHasProperty"] = getEntityHasProperty()
        self.scriptDict["getEntityPropertyType"] = getEntityPropertyType()
        self.scriptDict["getEntityPropertyValue"] = getEntityPropertyValue()
        self.scriptDict["addEntityLink"] = addEntityLink()
        self.scriptDict["getLinkCounterpartsByType"] = getLinkCounterpartsByType()
        self.scriptDict["getLinkCounterpartsByMetaMemeType"] = getLinkCounterpartsByMetaMemeType()
        self.scriptDict["getHasCounterpartsByType"] = getHasCounterpartsByType()
        self.scriptDict["getHasCounterpartsByMetaMemeType"] = getHasCounterpartsByMetaMemeType()
        self.scriptDict["getHasCounterpartsByTag"] = getHasCounterpartsByTag()
        self.scriptDict["getLinkCounterpartsByTag"] = getLinkCounterpartsByTag()
        self.scriptDict["getTraverseReport"] = getTraverseReport()
        self.scriptDict["getAreEntitiesLinked"] = getAreEntitiesLinked()
        self.scriptDict["getIsEntitySingleton"] = getIsEntitySingleton()
        self.scriptDict["getIsEntityTaxonomyExact"] = getIsEntityTaxonomyExact()
        self.scriptDict["getIsEntityTaxonomyGeneralization"] = getIsEntityTaxonomyGeneralization()
        self.scriptDict["getIsEntityTaxonomySpecialization"] = getIsEntityTaxonomySpecialization()
        self.scriptDict["getLinkCounterpartsByType"] = getLinkCounterpartsByType()
        self.scriptDict["instantiateEntity"] = instantiateEntity()
        self.scriptDict["removeEntityLink"] = removeEntityLink()
        self.scriptDict["removeAllCounterpartsOfType"] = removeAllCounterpartsOfType()
        self.scriptDict["removeAllCounterpartsOfTag"] = removeAllCounterpartsOfTag()
        self.scriptDict["removeEntityProperty"] = removeEntityProperty()
        self.scriptDict["removeEntityTaxonomy"] = removeEntityTaxonomy()
        self.scriptDict["removeAllCustomPropertiesFromEntity"] = removeAllCustomPropertiesFromEntity()
        self.scriptDict["revertEntityPropertyValues"] = revertEntityPropertyValues()
        self.scriptDict["revertEntity"] = revertEntity()
        self.scriptDict["setEntityPropertyValue"] = setEntityPropertyValue()
        self.scriptDict["getIsMemeSingleton"] = getIsMemeSingleton()
        self.scriptDict["setStateEventScript"] = setStateEventScript()
        self.scriptDict["installPythonExecutor"] = installPythonExecutor()
        self.scriptDict["getMemeExists"] = getMemeExists()
        self.scriptDict["evaluateEntity"] = evaluateEntity()
        self.scriptDict["getCluster"] = getCluster()
        self.scriptDict["getClusterJSON"] = getClusterJSON()
        self.scriptDict["getClusterMembers"] = getClusterMembers()
        self.scriptDict["getChildMemes"] = getChildMemes()
        self.scriptDict["getParentMemes"] = getParentMemes()
        self.scriptDict["getChildMetaMemes"] = getChildMetaMemes()
        self.scriptDict["getParentMetaMemes"] = getParentMetaMemes()
        self.scriptDict["getExtendingMetamemes"] = getExtendingMetamemes()
        self.scriptDict["getEnhancingMetamemes"] = getEnhancingMetamemes()
        self.scriptDict["getEnhancedMetamemes"] = getEnhancedMetamemes()
        self.scriptDict["getEnhanceableMemes"] = getEnhanceableMemes()
        self.scriptDict["getEnhancedMemes"] = getEnhancedMemes()
        self.scriptDict["getEnhancingMemes"] = getEnhancingMemes()
        self.scriptDict["hotLoadTemplate"] = hotLoadTemplate()
        self.scriptDict["sourceMemeCreate"] = sourceMemeCreate()
        self.scriptDict["sourceMemePropertySet"] = sourceMemePropertySet()
        self.scriptDict["sourceMemePropertyRemove"] = sourceMemePropertyRemove()
        self.scriptDict["sourceMemeMemberAdd"] = sourceMemeMemberAdd()
        self.scriptDict["sourceMemeMemberRemove"] = sourceMemeMemberRemove()
        self.scriptDict["sourceMemeEnhancementAdd"] = sourceMemeEnhancementAdd()
        self.scriptDict["sourceMemeEnhancementRemove"] = sourceMemeEnhancementRemove()
        self.scriptDict["sourceMemeTagAdd"] = sourceMemeTagAdd()
        self.scriptDict["sourceMemeTagRemove"] = sourceMemeTagRemove()
        self.scriptDict["sourceMemeSetSingleton"] = sourceMemeSetSingleton()
        self.scriptDict["sourceMemeCompile"] = sourceMemeCompile()
        self.scriptDict["sourceMemeValidate"] = sourceMemeValidate()
        self.scriptDict["mapBroker"] = MapBroker()
        self.scriptDict["reduceBroker"] = ReduceBroker()
        self.scriptDict["getHasTaxonomy"] = getHasTaxonomy()
        self.scriptDict["getTaxonomy"] = getTaxonomy()
    
    def getAPI(self):
        returnCopy = copy.deepcopy(self)
        return returnCopy
    
    
    def initialize(self):
        try:
            self._addEntityDecimalProperty = self.scriptDict["addEntityDecimalProperty"]
            self._addEntityIntegerProperty = self.scriptDict["addEntityIntegerProperty"]
            self._addEntityListProperty = self.scriptDict["addEntityListProperty"]
            self._addEntityStringProperty = self.scriptDict["addEntityStringProperty"]
            self._addEntityBooleanProperty = self.scriptDict["addEntityBooleanProperty"]
            self._addEntityTaxonomy = self.scriptDict["addEntityTaxonomy"]
            self._addEntityLink = self.scriptDict["addEntityLink"]
            self._createEntityFromMeme = self.scriptDict["createEntityFromMeme"]
            self._destroyEntity = self.scriptDict["destroyEntity"]
            self._getAllEntitiesByTag = self.scriptDict["getAllEntitiesByTag"]
            self._getAllEntitiesByTaxonomy = self.scriptDict["getAllEntitiesByTaxonomy"]
            self._getEntitiesByMemeType = self.scriptDict["getEntitiesByMemeType"]
            self._getEntitiesByMetaMemeType = self.scriptDict["getEntitiesByMetaMemeType"]
            self._getEntity = self.scriptDict["getEntity"]
            self._getAllEntities = self.scriptDict["getAllEntities"]
            self._getEntityMemeType = self.scriptDict["getEntityMemeType"]
            self._getEntityMetaMemeType = self.scriptDict["getEntityMetaMemeType"]
            self._getEntityHasProperty = self.scriptDict["getEntityHasProperty"]
            self._getEntityPropertyType = self.scriptDict["getEntityPropertyType"]
            self._getEntityPropertyValue = self.scriptDict["getEntityPropertyValue"]
            self._getLinkCounterpartsByType = self.scriptDict["getLinkCounterpartsByType"]
            self._getLinkCounterpartsByMetaMemeType = self.scriptDict["getLinkCounterpartsByMetaMemeType"]
            self._getHasCounterpartsByType = self.scriptDict["getHasCounterpartsByType"]
            self._getHasCounterpartsByMetaMemeType = self.scriptDict["getHasCounterpartsByMetaMemeType"]
            #self._getLinkCounterparts = self.scriptDict["getLinkCounterparts"]
            self._getLinkCounterpartsByType = self.scriptDict["getLinkCounterpartsByType"]
            self._getLinkCounterpartsByTag = self.scriptDict["getLinkCounterpartsByTag"]
            self._getHasCounterpartsByTag = self.scriptDict["getHasCounterpartsByTag"]
            self._getAreEntitiesLinked = self.scriptDict["getAreEntitiesLinked"]
            self._getIsEntitySingleton = self.scriptDict["getIsEntitySingleton"]
            self._getTraverseReport = self.scriptDict["getTraverseReport"]
            self._getIsEntityTaxonomyExact = self.scriptDict["getIsEntityTaxonomyExact"]
            self._getIsEntityTaxonomyGeneralization = self.scriptDict["getIsEntityTaxonomyGeneralization"]
            self._getIsEntityTaxonomySpecialization = self.scriptDict["getIsEntityTaxonomySpecialization"]
            self._getIsMemeSingleton = self.scriptDict["getIsMemeSingleton"]
            self._getMemeExists = self.scriptDict["getMemeExists"]
            self._instantiateEntity = self.scriptDict["instantiateEntity"]
            self._removeEntityLink = self.scriptDict["removeEntityLink"]
            self._removeAllCounterpartsOfType = self.scriptDict["removeAllCounterpartsOfType"]
            self._removeAllCounterpartsOfTag = self.scriptDict["removeAllCounterpartsOfTag"]
            self._removeAllCustomPropertiesFromEntity = self.scriptDict["removeAllCustomPropertiesFromEntity"]
            self._removeEntityProperty = self.scriptDict["removeEntityProperty"]
            self._removeEntityTaxonomy = self.scriptDict["removeEntityTaxonomy"]
            self._revertEntityPropertyValues = self.scriptDict["revertEntityPropertyValues"]
            self._revertEntity = self.scriptDict["revertEntity"]
            self._setEntityPropertyValue = self.scriptDict["setEntityPropertyValue"]
            self._setStateEventScript = self.scriptDict["setStateEventScript"]
            self._installPythonExecutor = self.scriptDict["installPythonExecutor"]
            self._evaluateEntity = self.scriptDict["evaluateEntity"]
            self._getCluster = self.scriptDict["getCluster"]
            self._getClusterJSON = self.scriptDict["getClusterJSON"]
            self._getClusterMembers = self.scriptDict["getClusterMembers"]
            self._getChildMemes = self.scriptDict["getChildMemes"]
            self._getParentMemes = self.scriptDict["getParentMemes"]
            self._getChildMetaMemes = self.scriptDict["getChildMetaMemes"]
            self._getParentMetaMemes = self.scriptDict["getParentMetaMemes"]
            self._getExtendingMetamemes = self.scriptDict["getExtendingMetamemes"]
            self._getEnhancingMetamemes = self.scriptDict["getEnhancingMetamemes"]        
            self._getEnhancedMetamemes = self.scriptDict["getEnhancedMetamemes"]
            self._getEnhanceableMemes = self.scriptDict["getEnhanceableMemes"]          
            self._getEnhancedMemes = self.scriptDict["getEnhancedMemes"]
            self._getEnhancingMemes = self.scriptDict["getEnhancingMemes"]         
            self._hotLoadTemplate = self.scriptDict["hotLoadTemplate"] 
            self._sourceMemeCreate = self.scriptDict["sourceMemeCreate"]
            self._sourceMemePropertySet = self.scriptDict["sourceMemePropertySet"]
            self._sourceMemePropertyRemove = self.scriptDict["sourceMemePropertyRemove"]
            self._sourceMemeMemberAdd = self.scriptDict["sourceMemeMemberAdd"]
            self._sourceMemeMemberRemove = self.scriptDict["sourceMemeMemberRemove"]
            self._sourceMemeEnhancementAdd = self.scriptDict["sourceMemeEnhancementAdd"]
            self._sourceMemeEnhancementRemove = self.scriptDict["sourceMemeEnhancementRemove"]
            self._sourceMemeTagAdd = self.scriptDict["sourceMemeTagAdd"]
            self._sourceMemeTagRemove = self.scriptDict["sourceMemeTagRemove"]
            self._sourceMemeSetSingleton = self.scriptDict["sourceMemeSetSingleton"]
            self._sourceMemeCompile = self.scriptDict["sourceMemeCompile"]
            self._sourceMemeValidate = self.scriptDict["sourceMemeValidate"]
            self._getTaxonomy = self.scriptDict["getTaxonomy"]
            self._getHasTaxonomy = self.scriptDict["getHasTaxonomy"]
                    
            self._map = self.scriptDict["mapBroker"]
            self._reduce =self.scriptDict["reduceBroker"]
        except Exception as e:
            errorMsg = "Failed to initialize script API.  Traceback = %s" %e
            logQ.put( [logType , logLevel.ERROR , "API.initialize", errorMsg])
            
            
    
    def addEntityDecimalProperty(self, entityUUID, name, value):
        try:
            dValue = decimal.Decimal(value)
            params = [entityUUID, name, dValue]
            entity = self._addEntityDecimalProperty.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: addEntityDecimalProperty(%s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, name, value, e)
            except:
                exception = "Action on entity of unknown type: addEntityDecimalProperty(%s, %s, %s).  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, name, value, e)
            raise Exceptions.ScriptError(exception)
        
        
    def addEntityIntegerProperty(self, entityUUID, name, value):
        try:
            iValue = int(value)
            params = [entityUUID, name, iValue]
            entity = self._addEntityIntegerProperty.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: addEntityIntegerProperty(%s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, name, value, e)
            except:
                exception = "Action on entity of unknown type: addEntityIntegerProperty(%s, %s, %s).  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, name, value, e)
            raise Exceptions.ScriptError(exception)
        
        
    def addEntityListProperty(self, entityUUID, name, value):
        try:
            params = [entityUUID, name, value]
            entity = self._addEntityListProperty.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: addEntityListProperty(%s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, name, value, e)
            except:
                exception = "Action on entity of unknown type: addEntityListProperty(%s, %s, %s).  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, name, value, e)
            raise Exceptions.ScriptError(exception)
        
        
    def addEntityStringProperty(self, entityUUID, name, value):
        try: 
            sValue = str(value)
            params = [entityUUID, name, sValue]
            entity = self._addEntityStringProperty.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: addEntityStringProperty(%s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, name, value, e)
            except:
                exception = "Action on entity of unknown type: addEntityStringProperty(%s, %s, %s).  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, name, value, e)
            raise Exceptions.ScriptError(exception) 
        
        
    def addEntityBooleanProperty(self, entityUUID, name, value):
        try: 
            sValue = str(value)
            params = [entityUUID, name, sValue]
            entity = self._addEntityBooleanProperty.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: addEntityBooleanProperty(%s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, name, value, e)
            except:
                exception = "Action on entity of unknown type: addEntityBooleanProperty(%s, %s, %s).  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, name, value, e)
            raise Exceptions.ScriptError(exception)         
 
        
        
    def addEntityTaxonomy(self, entityUUID, taxonomy):
        try: 
            params = [entityUUID, taxonomy]
            entity = self._addEntityTaxonomy.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: addEntityTaxonomy(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, taxonomy, e)
            except:
                exception = "Action on entity of unknown type: addEntityTaxonomy(%s, %s).  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, taxonomy, e)
            raise Exceptions.ScriptError(exception)   
        
        
    def addEntityLink(self, entityUUID1, entityUUID2, linkAttributes = {}, linkType = 0):
        try: 
            params = [entityUUID1, entityUUID2, linkAttributes, linkType]
            returnArray = self._addEntityLink.execute(params)
            return returnArray
        except Exceptions.EventScriptFailure as e:
            raise e
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID1)
                exception = "Action on %s entity: addEntityLink(%s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID1, entityUUID2, linkType, e)
            except Exceptions.EntityLinkFailureError as e:
                raise Exceptions.ScriptError(e)
            except Exception as e:
                exception = "Error while trying to link entitiese: addEntityLink(%s, %s, %s).  traceback = %s" %(entityUUID1, entityUUID2, linkType, e)
                raise Exceptions.ScriptError(exception)       
        
        
    def createEntityFromMeme(self, memePath, ActionID = None, Subject = None, Controller = None, supressInit = False):
        try: 
            params = [memePath, ActionID, Subject, Controller, supressInit]
            entity = self._createEntityFromMeme.execute(params)
            return entity
        except Exceptions.StateEventScriptInitError as e:
            #Build up a full java or C# style stacktrace, so that devs can track down errors in script modules within repositories
            tb = sys.exc_info()[2]
            exception = "createEntityFromMeme(%s, %s, %s, %s) traceback = %s" %(memePath, ActionID, Subject, Controller, e)
            logQ.put( [logType , logLevel.WARNING , "createEntityFromMeme" , exception])
            raise Exceptions.ScriptError(exception).with_traceback(tb)
        except Exception as e:
            exception = "createEntityFromMeme(%s, %s, %s, %s) traceback = %s" %(memePath, ActionID, Subject, Controller, e)
            raise Exceptions.ScriptError(exception)  
        
    def createEntity(self):
        try: 
            params = ["Graphyne.Generic", None, None, None, False]
            entity = self._createEntityFromMeme.execute(params)
            return entity
        except Exception as e:
            exception = "createEntity(%s) traceback = %s" %("Graphyne.Generic", e)
            raise Exceptions.ScriptError(exception)
                  
        
        
    def destroyEntity(self, entityUUID):
        try: 
            params = [entityUUID]
            returnvalue = self._destroyEntity.execute(params)
            return returnvalue
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: destroyEntity(%s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, e)
            except:
                exception = "Action on entity of unknown type: destroyEntity(%s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)          
        
        
    def getAllEntitiesByTag(self, tag):
        try: 
            params = [tag]
            entities = self._getAllEntitiesByTag.execute(params)
            return entities
        except Exception as e:
            exception = "getAllEntitiesByTag(%s) error %s" %(tag, e)
            raise Exceptions.ScriptError(exception)  
        
        
    def getAllEntitiesByTaxonomy(self, taxonomy):
        try: 
            params = [taxonomy]
            entities = self._getAllEntitiesByTaxonomy.execute(params)
            return entities
        except Exception as e:
            exception = "getAllEntitiesByTaxonomy(%s) error %s" %(taxonomy, e)
            raise Exceptions.ScriptError(exception)   


    def getEntitiesByMemeType(self, meme):
        try: 
            params = [meme]
            entities = self._getEntitiesByMemeType.execute(params)
            return entities
        except Exception as e:
            exception = "getEntitiesByMemeType(%s) error %s" %(meme, e)
            raise Exceptions.ScriptError(exception)  
        
        
    def getEntitiesByMetaMemeType(self, metaMeme):
        try: 
            params = [metaMeme]
            entities = self._getEntitiesByMetaMemeType.execute(params)
            return entities
        except Exception as e:
            #debug
            entities = self._getEntitiesByMetaMemeType.execute(params)
            #/debug
            exception = "getEntitiesByMetaMemeType(%s) error %s" %(metaMeme, e)
            raise Exceptions.ScriptError(exception)  
        

    """
    def getAllAgentsInAgentScope(self, agentUUID):
        try: 
            params = [agentUUID]
            entities = self._getAllAgentsInAgentScope.execute(params)
            return entities
        except Exception as e:
            exception = "getAllAgentsInAgentScope(%s) error %s" %(agentUUID, e)
            raise Exceptions.ScriptError(exception)
    """ 
       

    def getEntity(self, entityUUID):
        try: 
            params = [entityUUID]
            ent = self._getEntity.execute(params)
            return ent
        except Exceptions.NoSuchEntityError as e:
            exception = "getEntity(%s) error %s" %(entityUUID, e)
            raise Exceptions.NoSuchEntityError(exception)
        except Exception as e:
            exception = "getEntity(%s) error %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)      
        
        
    def getAllEntities(self):
        try: 
            ent = self._getAllEntities.execute()
            return ent
        except Exception as e:
            exception = "getAllEntities() error %s" %(e)
            raise Exceptions.ScriptError(exception)  
        
        
        
    def getEntityMemeType(self, entityUUID):
        try: 
            params = [entityUUID]
            ent = self._getEntityMemeType.execute(params)
            return ent
        except Exception as e:
            exception = "getEntityMemeType(%s) error %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)  
        
        
    def getEntityMetaMemeType(self, entityUUID):
        try: 
            params = [entityUUID]
            ent = self._getEntityMetaMemeType.execute(params)
            return ent
        except Exception as e:
            exception = "getEntityMemeType(%s) error %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)  

        
    def getEntityHasProperty(self, entityUUID, propertyName, ActionID = None, Subject = None, Controller = None):
        try: 
            params = [entityUUID, propertyName, ActionID, Subject, Controller]
            hasProperty = self._getEntityHasProperty.execute(params)
            return hasProperty
        except Exception:
            errorMessage = ""
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            tb = sys.exc_info()[2]
            try:
                entity = self.getEntity(entityUUID)
                errorMessage = "Action on %s entity: getEntityHasProperty(%s, %s, %s, %s, %s) traceback = %s : %s" %(entity.memePath.fullTemplatePath, entityUUID, propertyName, ActionID, Subject, Controller, errorID, tb)
            except:
                errorMessage = "Action on entity of unknown type: getEntityHasProperty(%s, %s, %s, %s, %s) .  Possible reason is that entity is not in repository.  traceback = %s : %s" %(entityUUID, propertyName, ActionID, Subject, Controller, errorID, tb)
            raise Exceptions.ScriptError(errorMessage)          
        
        
    def getEntityPropertyType(self, entityUUID, propertyName, ActionID = None, Subject = None, Controller = None):
        try: 
            params = [entityUUID, propertyName, ActionID, Subject, Controller]
            propType = self._getEntityPropertyType.execute(params)
            return propType
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getEntityPropertyType(%s, %s, %s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, propertyName, ActionID, Subject, Controller, e)
            except:
                exception = "Action on entity of unknown type: getEntityPropertyType(%s, %s, %s, %s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, propertyName, ActionID, Subject, Controller, e)
            raise Exceptions.ScriptError(exception)             
        
        
        
    def getEntityPropertyValue(self, entityUUID, propertyName, ActionID = None, Subject = None, Controller = None):
        try: 
            params = [entityUUID, propertyName, ActionID, Subject, Controller]
            value = self._getEntityPropertyValue.execute(params)
            return value
        except Exceptions.EntityPropertyMissingValueError:
            fullerror = sys.exc_info()
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            raise Exceptions.ScriptError(errorMsg).with_traceback(tb)
        except Exception:
            errorMessage = ""
            fullerror = sys.exc_info()
            errorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            try:
                entity = self.getEntity(entityUUID)
                errorMessage = "Action on %s entity: getEntityPropertyValue(%s, %s, %s, %s, %s)" %(entity.memePath.fullTemplatePath, entityUUID, propertyName, ActionID, Subject, Controller)
            except Exception:
                errorMessage = "Action on entity of unknown type: getEntityPropertyValue(%s, %s, %s, %s, %s) .  Possible reason is that entity is not in repository." %(entityUUID, propertyName, ActionID, Subject, Controller)
            raise Exceptions.ScriptError(errorMessage).with_traceback(tb)          



    def getHasCounterpartsByType(self, entityUUID, memePath, linkType = None, isMeme = True, fastSearch = False):
        try: 
            if fastSearch == True:
                excludeClusterList = []
            else:
                excludeClusterList = None
            params = [entityUUID, memePath, linkType, excludeClusterList, isMeme]
            hasCounterparts = self._getHasCounterpartsByType.execute(params)
            return hasCounterparts
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getHasCounterpartsByType(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, memePath, e)
            except:
                exception = "Action on entity of unknown type: getHasCounterpartsByType(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, memePath, e)
            raise Exceptions.ScriptError(exception)
        
    
    #Todo - this needs to have its params tweaked: linkDirectionTypes.BIDIRECTIONAL, '', None, linkAttributeOperatorTypes.EQUAL    
    def getCounterpartsByType(self, entityUUID, memePath, linkType = None, isMeme = True, fastSearch = False):
        try: 
            if fastSearch == True:
                excludeClusterList = []
            else:
                excludeClusterList = None
            params = [entityUUID, memePath, linkType, excludeClusterList, isMeme]
            counterparts = self._getLinkCounterpartsByType.execute(params)
            return counterparts
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getLinkCounterpartsByType(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, memePath, e)
            except:
                exception = "Action on entity of unknown type: getLinkCounterpartsByType(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, memePath, e)
            raise Exceptions.ScriptError(exception)        
        
        
    def getAreEntitiesLinked(self, entityUUID, memberUUID):
        try: 
            params = [entityUUID, memberUUID]
            hasMember = self._getAreEntitiesLinked.execute(params)
            return hasMember
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getAreEntitiesLinked(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, memberUUID, e)
            except:
                exception = "Action on entity of unknown type: getAreEntitiesLinked(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, memberUUID, e)
            raise Exceptions.ScriptError(exception)            
        
        
    def getIsEntitySingleton(self, entityUUID):
        try: 
            params = [entityUUID]
            isSingleton = self._getIsEntitySingleton.execute(params)
            return isSingleton
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getIsEntitySingleton(%s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, e)
            except:
                exception = "Action on entity of unknown type: getIsEntitySingleton(%s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)          
             
        
        
    def getIsEntityTaxonomyExact(self, entityUUID, taxonomy):
        try: 
            params = [entityUUID, taxonomy]
            isSingleton = self._getIsEntityTaxonomyExact.execute(params)
            return isSingleton
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getIsEntityTaxonomyExact(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, taxonomy, e)
            except:
                exception = "Action on entity of unknown type: getIsEntityTaxonomyExact(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, taxonomy, e)
            raise Exceptions.ScriptError(exception)         
        
        
        
    def getIsEntityTaxonomyGeneralization(self, entityUUID, taxonomy):
        try: 
            params = [entityUUID, taxonomy]
            isGeneralization = self._getIsEntityTaxonomyGeneralization.execute(params)
            return isGeneralization
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getIsEntityTaxonomyGeneralization(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, taxonomy, e)
            except:
                exception = "Action on entity of unknown type: getIsEntityTaxonomyGeneralization(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, taxonomy, e)
            raise Exceptions.ScriptError(exception)         
        
        
        
    def getIsEntityTaxonomySpecialization(self, entityUUID, taxonomy):
        try: 
            params = [entityUUID, taxonomy]
            isSpecialization = self._getIsEntityTaxonomySpecialization.execute(params)
            return isSpecialization
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getIsEntityTaxonomySpecialization(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, taxonomy, e)
            except:
                exception = "Action on entity of unknown type: getIsEntityTaxonomySpecialization(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, taxonomy, e)
            raise Exceptions.ScriptError(exception)
                

    def getIsMemeSingleton(self, memePath):
        try: 
            params = [memePath]
            isSingleton = self._getIsMemeSingleton.execute(params)
            return isSingleton
        except Exception as e:
            exception = "getIsMemeSingleton(%s) error %s" %(memePath, e)
            raise Exceptions.ScriptError(exception)         
        
        
    def getLinkCounterpartsByType(self, entityUUID, memePath, linkType = None, fastSearch = False):
        #try: 
        if fastSearch == True:
            excludeClusterList = []
        else:
            excludeClusterList = None
        params = [entityUUID, memePath, linkType, excludeClusterList]
        entities = self._getLinkCounterpartsByType.execute(params)
        filteredEntities = filterListDuplicates(entities)
        return filteredEntities
        #except Exception as e:
            #entityID = entityUUID
            #exception = None
            #try:
                #entity = self.getEntity(entityUUID)
                #exception = "Action on %s entity: getLinkCounterpartsByType(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, memePath, e)
            #except:
                #exception = "Action on entity of unknown type: getLinkCounterpartsByType(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, memePath, e)
            #raise Exceptions.ScriptError(exception)    
            
            
    def getLinkCounterpartsByMetaMemeType(self, entityUUID, metaMemePath, linkType = None, returnUniqueValuesOnly = True):
        #try: 
        params = [entityUUID, metaMemePath, linkType, returnUniqueValuesOnly]
        entities = self._getLinkCounterpartsByMetaMemeType.execute(params)
        return entities
        #except Exception as e:
            #entityID = entityUUID
            #exception = None
            #try:
                #entity = self.getEntity(entityUUID)
                #exception = "Action on %s entity: getLinkCounterpartsByType(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, memePath, e)
            #except:
                #exception = "Action on entity of unknown type: getLinkCounterpartsByType(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, memePath, e)
            #raise Exceptions.ScriptError(exception)   
            
            
    def getHasCounterpartsByMetaMemeType(self, entityUUID, metaMemePath, linkType = None):
        try: 
            params = [entityUUID, metaMemePath, linkType]
            hasCounterparts = self._getHasCounterpartsByMetaMemeType.execute(params)
            return hasCounterparts
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: _getHasCounterpartsMetaMemeByType(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, metaMemePath, e)
            except:
                exception = "Action on entity of unknown type: _getHasCounterpartsMetaMemeByType(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, metaMemePath, e)
            raise Exceptions.ScriptError(exception)
        
            
            
    def getLinkCounterparts(self, entityUUID, linkType = None):
        try: 
            params = [entityUUID, "*", linkType, []]
            entities = self._getLinkCounterpartsByType.execute(params)
            filteredEntities = filterListDuplicates(entities)
            return filteredEntities
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: getLinkCounterparts(%s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, e)
            except:
                exception = "Action on entity of unknown type: getLinkCounterparts(%s) .  Possible reason is that entity is not in database.  traceback = %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)  
        
        
    def getTraverseReport(self, entityUUID, traversePath, isMeme = True, linkType = 0):
        #getTraverseReport(self, splitPath, isMeme, lthLevel = 0, linkType = 0, excludeLinks = [], returnUniqueValuesOnly = True, excludeCluster = []):
        returnUniqueValuesOnly = True
        params = [entityUUID, traversePath, isMeme, linkType, returnUniqueValuesOnly]
        traverseLinks, traverseNeighbors, traverseOrder = self._getTraverseReport.execute(params)
        traverseNodes = []
        
        #TraverseOder is a dict containing the members along the traverse path, including their linear pisition in the "position" attribute.
        #traverseNeighbors contains everything that was noted as a neighbor of any node while traversing.  Their linear position is "-1"
        #In principle, the traverse order members should also exist in that dict as members as well
        #We Want to merge traverseOrder into traverseNeighbors, without revertying any existing traverseOrder member positions to -1
        for neighborKey in traverseNeighbors:
            if neighborKey not in traverseOrder:
                traverseOrder[neighborKey] = traverseNeighbors[neighborKey]
        for nodeKey in traverseOrder.keys():
            traverseNodes.append(traverseOrder[nodeKey])
        fullReport = {"nodes" : traverseNodes, "links" : traverseLinks }
        return fullReport
    
    
    
    def getTraverseReportJSON(self, entityUUID, traversePath, isMeme = True, linkType = 0):
        #getTraverseReport(self, splitPath, isMeme, lthLevel = 0, linkType = 0, excludeLinks = [], returnUniqueValuesOnly = True, excludeCluster = []):
        returnUniqueValuesOnly = True
        params = [entityUUID, traversePath, isMeme, linkType, returnUniqueValuesOnly]
        traverseLinks, traverseNeighbors, traverseOrder = self._getTraverseReport.execute(params)
        traverseNodes = []
        
        #TraverseOder is a dict containing the members along the traverse path, including their linear pisition in the "position" attribute.
        #traverseNeighbors contains everything that was noted as a neighbor of any node while traversing.  Their linear position is "-1"
        #In principle, the traverse order members should also exist in that dict as members as well
        #We Want to merge traverseOrder into traverseNeighbors, without revertying any existing traverseOrder member positions to -1
        for neighborKey in traverseNeighbors:
            if neighborKey not in traverseOrder:
                traverseOrder[neighborKey] = traverseNeighbors[neighborKey]
        for nodeKey in traverseOrder.keys():
            traverseNodes.append(traverseOrder[nodeKey])
        fullReport = {"nodes" : traverseNodes, "links" : traverseLinks }
        fullReportJSON = json.dumps(fullReport)
        return fullReportJSON
    
        
                
        
    def getMemeExists(self, memePath):
        try: 
            params = [memePath]
            memeExists = self._getMemeExists.execute(params)
            return memeExists
        except Exception as e:
            exception = "getMemeExists(%s) error %s" %(memePath, e)
            raise Exceptions.ScriptError(exception)     
        
        
    def instantiateEntity(self, entityUUID):
        try: 
            params = [entityUUID]
            unusedMemeExists = self._instantiateEntity.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: instantiateEntity(%s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, e)
            except:
                exception = "Action on entity of unknown type: instantiateEntity(%s) .  Possible reason is that entity is not in database.  traceback = %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)     
                
        
    def removeEntityLink(self, entityUUID, memberUUID):
        try: 
            params = [entityUUID, memberUUID]
            returnArray = self._removeEntityLink.execute(params)
            return returnArray
        except Exceptions.EventScriptFailure as e:
            raise e 
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: removeEntityLink(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, memberUUID, e)
            except:
                exception = "Action on entity of unknown type: removeEntityLink(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, memberUUID, e)
                raise Exceptions.ScriptError(exception)          
        
        
        
    def removeAllCounterpartsOfType(self, entityUUID, memePath):
        try: 
            params = [entityUUID, memePath]
            unusedMemeExists = self._removeAllCounterpartsOfType.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: removeAllCounterpartsOfType(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, memePath, e)
            except:
                exception = "Action on entity of unknown type: removeAllCounterpartsOfType(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, memePath, e)
            raise Exceptions.ScriptError(exception)          
        

    def removeAllCounterpartsOfTag(self, entityUUID, tag):
        try: 
            params = [entityUUID, tag]
            unusedMemeExists = self._removeAllCounterpartsOfTag.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: removeAllCounterpartsOfTag(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, tag, e)
            except:
                exception = "Action on entity of unknown type: removeAllCounterpartsOfTag(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, tag, e)
            raise Exceptions.ScriptError(exception)  
        
        
    def removeAllCustomPropertiesFromEntity(self, entityUUID):
        try: 
            params = [entityUUID]
            unusedMemeExists = self._removeAllCustomPropertiesFromEntity.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: removeAllCustomPropertiesFromEntity(%s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, e)
            except:
                exception = "Action on entity of unknown type: removeAllCustomPropertiesFromEntity(%s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception) 

        
    def removeEntityProperty(self, entityUUID, propertyName, drilldown = False):
        try: 
            params = [entityUUID, propertyName, drilldown]
            unusedMemeExists = self._removeEntityProperty.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: removeEntityProperty(%s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, propertyName, drilldown, e)
            except:
                exception = "Action on entity of unknown type: removeEntityProperty(%s, %s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, propertyName, drilldown, e)
            raise Exceptions.ScriptError(exception)       
        
        
    def removeEntityTaxonomy(self, entityUUID, taxonomy):
        try: 
            params = [entityUUID, taxonomy]
            unusedMemeExists = self._removeEntityTaxonomy.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: removeEntityTaxonomy(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, taxonomy, e)
            except:
                exception = "Action on entity of unknown type: removeEntityTaxonomy(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, taxonomy, e)
            raise Exceptions.ScriptError(exception)
        
        

    def revertEntity(self, entityUUID, drilldown = False):
        try: 
            params = [entityUUID, drilldown]
            unusedMemeExists = self._revertEntity.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: revertEntity(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, drilldown, e)
            except:
                exception = "Action on entity of unknown type: revertEntity(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, drilldown, e)
            raise Exceptions.ScriptError(exception)



            
    def revertEntityPropertyValues(self, entityUUID, drilldown = False):
        try: 
            params = [entityUUID, drilldown]
            unusedMemeExists = self._revertEntityPropertyValues.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: revertEntityPropertyValues(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, drilldown, e)
            except:
                exception = "Action on entity of unknown type: revertEntityPropertyValues(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, drilldown, e)
            raise Exceptions.ScriptError(exception)
             
        
        
    def setEntityPropertyValue(self, entityUUID, propertyName, propertyValue):
        try: 
            params = [entityUUID, propertyName, propertyValue]
            returnValue = self._setEntityPropertyValue.execute(params)
            return returnValue
        except Exceptions.EventScriptFailure as e:
            raise e
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: setEntityPropertyValue(%s, %s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, propertyName, propertyValue, e)
            except:
                exception = "Action on entity of unknown type: setEntityPropertyValue(%s, %s, %s).  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, propertyName, propertyValue, e)
            raise Exceptions.ScriptError(exception)  
        
        
    def setStateEventScript(self, entityUUID, scriptLocation):
        try: 
            params = [entityUUID, scriptLocation]
            unusedMemeExists = self._setStateEventScript.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: setStateEventScript(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, scriptLocation, e)
            except:
                exception = "Action on entity of unknown type: setStateEventScript(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, scriptLocation, e)
            raise Exceptions.ScriptError(exception) 
        
    def installPythonExecutor(self, entityUUID, callableObject):
        try: 
            params = [entityUUID, callableObject]
            #assert callable(callableObject)
            unusedMemeExists = self._installPythonExecutor.execute(params)
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity %s: installPythonExecutor.  Traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, e)
            except:
                exception = "Action on entity of unknown type %s: installPythonExecutor.  Possible reason is that entity is not in repository.  Traceback = %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception) 
 
    """ Passing either a UUID of a specific entity, or the fully resolved path of a singleton in entityUUID
        If it is a fully resolved path that is passed and the entity does not exist yet (i.e. the meme is not a singleton),
            then this method will also force its creation.   
        supressInit determines whether or not to initialize entities that are created for evaluation """    
    def evaluateEntity(self, entityUUID, runtimeVariables = {}, actionID = None, subjectID = None, objectID = (), supressInit = False):
        try:
            #ToDo - fully resolved path of singleton still broken here
            params = {"entityID" : entityUUID, "runtimeVariables" : runtimeVariables, "actionID":actionID, "subjectID":subjectID, "objectID":objectID, "supressInit":supressInit}
            evalResult = self._evaluateEntity.execute(entityUUID, params)
            return evalResult
        except Exceptions.EventScriptFailure as e:
            raise e
        except Exceptions.ScriptError as e:
            raise e
        except Exceptions.NoSuchEntityError as e:
            exception = "Action on entity of unknown type: evaluateEntity(%s, %s) fails because that entity is not in repository.  traceback = %s" %(entityUUID, runtimeVariables, e)
            raise Exceptions.ScriptError(exception) 
        except Exception as e:
            exception = None
            try:
                entity = self.getEntity(entityUUID)
                exception = "Action on %s entity: evaluateEntity(%s, %s) traceback = %s" %(entity.memePath.fullTemplatePath, entityUUID, runtimeVariables, e)
            except:
                exception = "Action on entity of unknown type: evaluateEntity(%s, %s) .  Possible reason is that entity is not in repository.  traceback = %s" %(entityUUID, runtimeVariables, e)
            raise Exceptions.ScriptError(exception) 


    """
    # Deprecated - todo, remove
    def getTemplateCatalog(self):
        try: 
            params = []
            evalResult = self._getTemplateCatalog.execute(params)
            return evalResult
        except Exception as e:
            exception = "Template Catalog Read Failed. traceback = %s" %(e)
            raise Exceptions.ScriptError(exception)       
        


    def getTemplateHeadRevisionUUID(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getTemplateHeadRevisionUUID.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get Template %s head revision Failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)   
    """
        

    def getEntityCounterparts(self, entityUUID):
        global linkRepository
        try: 
            #params = [entityUUID]
            evalResult = linkRepository.getCounterpartIndices(entityUUID)
            return evalResult
        except KeyError:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            nestEerrorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            errorMsg = "Get counterparts of entity %s failed. Nested Traceback = %s: %s" %(entityUUID, errorID, nestEerrorMsg)
            logQ.put( [logType , logLevel.WARNING , "Graph.api.getEntityCounterparts" , errorMsg])
            raise Exceptions.ScriptError(errorMsg).with_traceback(tb)
        except Exception:
            try:
                meme = self.getEntityMemeType(entityUUID)
                fullerror = sys.exc_info()
                errorID = str(fullerror[0])
                nestEerrorMsg = str(fullerror[1])
                tb = sys.exc_info()[2]
                errorMsg = "Get counterparts of %s entity %s failed. Nested Traceback = %s: %s" %(meme, entityUUID, errorID, nestEerrorMsg)
                logQ.put( [logType , logLevel.WARNING , "Graph.api.getEntityCounterparts" , errorMsg])
                raise Exceptions.ScriptError(errorMsg).with_traceback(tb)
            except:
                fullerror = sys.exc_info()
                errorID = str(fullerror[0])
                nestEerrorMsg = str(fullerror[1])
                tb = sys.exc_info()[2]
                errorMsg = "Get counterparts of entity %s failed. Nested Traceback = %s: %s" %(entityUUID, errorID, nestEerrorMsg)
                logQ.put( [logType , logLevel.WARNING , "Graph.api.getEntityCounterparts" , errorMsg])
                raise Exceptions.ScriptError(errorMsg).with_traceback(tb)


    def getCluster(self, entityUUID, linkType = 0, crossSingletons = False):
        try: 
            params = [entityUUID, linkType, crossSingletons]
            evalResult = self._getCluster.execute(params)
            return evalResult
        except Exception:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            nestEerrorMsg = str(fullerror[1])
            tb = sys.exc_info()[2]
            errorMsg = "Get Cluster of entity %s failed. Nested Traceback = %s: %s" %(entityUUID, errorID, nestEerrorMsg)
            logQ.put( [logType , logLevel.WARNING , "Graph.api.getEntityCounterparts" , errorMsg])
            raise Exceptions.ScriptError(errorMsg).with_traceback(tb)

        
        
    def getClusterJSON(self, entityUUID, linkType = 0, crossSingletons = False):
        """
            Acts as a wrapper for getCluster() and returns the result as a JSON, instead of as a native Python dict
        """
        try: 
            params = [entityUUID, linkType, crossSingletons]
            evalResult = self._getClusterJSON.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get Cluster JSON of entity %s failed. traceback = %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)

        
    def getClusterMembers(self, entityUUID, linkType = 0, crossSingletons = False):
        try: 
            params = [entityUUID, linkType, crossSingletons]
            evalResult = self._getClusterMembers.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get Cluster Members of entity %s failed. traceback = %s" %(entityUUID, e)
            raise Exceptions.ScriptError(exception)
    
        
    def getChildMemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getChildMemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get child memes of meme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)
        

    def getParentMemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getParentMemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get parent memes of meme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)  
        
    def getChildMetaMemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getChildMetaMemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get child metamemes of metameme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)
        

    def getParentMetaMemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getParentMetaMemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get parent metamemes of metameme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)     
                     
        
    def getExtendingMetamemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getExtendingMetamemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get extending metamemes of metameme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)
        

    def getEnhancingMetamemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getEnhancingMetamemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get enhancing metamemes of metameme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception) 
        
    def getEnhancedMetamemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getEnhancedMetamemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get enhanced metamemes of metameme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)
        

    def getEnhanceableMemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getEnhanceableMemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get enhancable memes of meme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)


    def getEnhancedMemes(self, tempLateFullPath):
        try: 
            params = [tempLateFullPath]
            evalResult = self._getEnhancedMemes.execute(params)
            return evalResult
        except Exception as e:
            exception = "Get enhanced memes of meme %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)        

    def hotLoadTemplate(self, tempLateFullPath, templateAsString):
        try: 
            params = [tempLateFullPath, templateAsString]
            evalResult = self._hotLoadTemplate.execute(params)
            return evalResult
        except Exception as e:
            exception = "Hot loading new version of %s failed. traceback = %s" %(tempLateFullPath, e)
            raise Exceptions.ScriptError(exception)
        
        
    def sourceMemeCreate(self, memeName, modulePath = "Graphyne", metamemePath = "Graphyne.GenericMetaMeme"):
        try: 
            params = [modulePath, memeName, metamemePath]
            evalResult = self._sourceMemeCreate.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e  
        
        
    def sourceMemePropertySet(self, fullTemplatePath, propName, propValueStr, propType = "string"):
        try: 
            params = [fullTemplatePath, propName, propValueStr, propType]
            evalResult = self._sourceMemePropertySet.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e 
        
        
    def sourceMemePropertyRemove(self, fullTemplatePath, propName):
        try: 
            params = [fullTemplatePath, propName]
            evalResult = self._sourceMemePropertyRemove.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e 
        
        
    def sourceMemeMemberAdd(self, fullTemplatePath, memberID, occurrence, lt = linkTypes.ATOMIC):
        try:
            occurrence = str(occurrence) #Make sure to cast it to string, so that we can handle it as int or string.
            params = [fullTemplatePath, memberID, occurrence, lt]
            evalResult = self._sourceMemeMemberAdd.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e 
        
              
    def sourceMemeMemberRemove(self, fullTemplatePath, memberID):
        try: 
            params = [fullTemplatePath, memberID]
            evalResult = self._sourceMemeMemberRemove.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e 
        
        
    def sourceMemeEnhancementAdd(self, sourceMemeID, targetMemeID):
        try: 
            params = [sourceMemeID, targetMemeID]
            evalResult = self._sourceMemeEnhancementAdd.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e
        
        
    def sourceMemeEnhancementRemove(self, sourceMemeID, targetMemeID):
        try: 
            params = [sourceMemeID, targetMemeID]
            evalResult = self._sourceMemeEnhancementRemove.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e
        
        
    def sourceMemeTagAdd(self, fullTemplatePath, tag):
        try: 
            params = [fullTemplatePath, tag]
            evalResult = self._sourceMemeTagAdd.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e
        
        
    def sourceMemeTagRemove(self, fullTemplatePath, tag):
        try: 
            params = [fullTemplatePath, tag]
            evalResult = self._sourceMemeTagRemove.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e
        
        
    def sourceMemeSetSingleton(self, fullTemplatePath, isSingleton):
        try: 
            params = [fullTemplatePath, isSingleton]
            evalResult = self._sourceMemeSetSingleton.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e


    def sourceMemeCompile(self, fullTemplatePath, validate = True):
        try: 
            params = [fullTemplatePath, validate]
            evalResult = self._sourceMemeCompile.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e
        
        
    def sourceMemeValidate(self, fullTemplatePath):
        try: 
            params = [fullTemplatePath]
            evalResult = self._sourceMemeValidate.execute(params)
            return evalResult
        except Exceptions.ScriptError as e:
            raise e
                
        
    def getScriptFromPath(self, scriptLocation):
        try:
            splitName = scriptLocation.rpartition('.')
            className = None
            modName = None
            
            #moduleName = "RMLRepository." + splitName[0]
            modName = splitName[0]
            className = str(splitName[2])
                 
            mod = Fileutils.getModuleFromResolvedPath(modName)
            tmpClass = getattr(mod, className)

            return tmpClass
        except Exception as e:
            exception = "Unable to retreive script handler from location %s.  Traceback = %s" %(scriptLocation, e)
            raise Exceptions.ScriptError(exception) 


    def writeDebug(self, statement):
        method = moduleName + '.writeLog'
        try:
            logQ.put( [logType , logLevel.DEBUG , method , statement])
        except Exception as e:
            exception = "Unable to log statement %s.  Traceback = %s" %(statement, e)
            raise Exceptions.ScriptError(exception) 
        
        
    def writeLog(self, statement):
        method = moduleName + '.writeLog'
        try:
            logQ.put( [logType , logLevel.INFO , method , statement])
        except Exception as e:
            exception = "Unable to log statement %s.  Traceback = %s" %(statement, e)
            raise Exceptions.ScriptError(exception) 
        
    def writeError(self, statement):
        method = moduleName + '.writeWarning'
        try:
            logQ.put( [logType , logLevel.WARNING, method , statement])
        except Exception as e:
            exception = "Unable to log statement %s.  Traceback = %s" %(statement, e)
            raise Exceptions.ScriptError(exception) 
        
        
    def map(self, mapFunction, mapParams, argumentMap):
        try:
            evalResult = self._map.execute(mapFunction, mapParams, argumentMap)
            return evalResult
        except Exception as e:
            exception = "Unable to map %s [%s].  Traceback = %s" %(mapFunction, mapParams, e)
            raise Exceptions.ScriptError(exception) 
        
    def reduce(self, reduceFunction, reduceParams):
        try:
            evalResult = self._map.execute(reduceFunction, reduceParams)
            return evalResult
        except Exception as e:
            exception = "Unable to reduce %s [%s].  Traceback = %s" %(reduceFunction, reduceParams, e)
            raise Exceptions.ScriptError(exception) 
        
    def getTaxonomy(self, memeFullTemplatePath):
        try:
            params = [memeFullTemplatePath]
            evalResult = self._getTaxonomy.execute(params)
            return evalResult
        except Exception as e:
            exception = "Unable to get the metamemes of %s.  Traceback = %s" %(memeFullTemplatePath, e)
            raise Exceptions.ScriptError(exception)     
        
    def getHasTaxonomy(self, memeFullTemplatePath, taxonomyFullTemplatePath):
        try:
            params = [memeFullTemplatePath, taxonomyFullTemplatePath]
            evalResult = self._getHasTaxonomy.execute(params)
            return evalResult
        except Exception as e:
            exception = "Unable to determine if %s has %s as a taxonomy.  Traceback = %s" %(memeFullTemplatePath, taxonomyFullTemplatePath, e)
            raise Exceptions.ScriptError(exception) 
        
#/api
api = API()
api.initialize()          
