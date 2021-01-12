"""
   Scripting.py: Script API interface module
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'


from Graphyne import Graph as Graph
import threading


moduleName = 'Scripting'


class StateEventScript(threading.Thread):
    """
        The base class for property change state event scripts.
    """
    
    className = "Echo"
    
    def __init__(self):
        self.entityLock = threading.RLock()
        
    def setState(self, propertyID):
        self.propertyID = propertyID
        
    def execute(self, entityID, params):
        """
            Override this method to implement the execute
        """
        return None
    
    


class API(threading.Thread):

    def __init__(self):
        self.localFacade = Graph.api.getAPI()



    def addEntityDecimalProperty(self, entityUUID, name, value):
        self.localFacade.addEntityDecimalProperty(entityUUID, name, value)
        
        
    def addEntityIntegerProperty(self, entityUUID, name, value):
        self.localFacade.addEntityIntegerProperty(entityUUID, name, value)
        
        
    def addEntityListProperty(self, entityUUID, name, value):
        self.localFacade.addEntityListProperty(entityUUID, name, value)
        
        
    def addEntityStringProperty(self, entityUUID, name, value):
        self.localFacade.addEntityStringProperty(entityUUID, name, value)
        
    
    def addEntityBooleanProperty(self, entityUUID, name, value):
        self.localFacade.addEntityBooleanProperty(entityUUID, name, value)
        
        
    def addEntityTaxonomy(self, entityUUID, taxonomy):
        self.localFacade.addEntityTaxonomy(entityUUID, taxonomy)
        
    def addEntityLink(self, entityUUID1, entityUUID2, linkAttributes = {}, linkType = Graph.linkTypes.ATOMIC):
        self.localFacade.addEntityLink(entityUUID1, entityUUID2, linkAttributes, linkType)        
        
        
    def createEntityFromMeme(self, memePath, ActionID = None, Subject = None, Controller = None, supressInit = False):
        try:
            returnMe = self.localFacade.createEntityFromMeme(memePath, ActionID, Subject, Controller, supressInit)
            return returnMe 
        except:
            return None   
              
        
        
    def destroyEntity(self, entityUUID):
        self.localFacade.destroyEntity(entityUUID)         
        
        
    def getAllEntitiesByTag(self, tag):
        returnMe = self.localFacade.getAllEntitiesByTag(tag)
        return returnMe  
        
        
    def getAllEntitiesByTaxonomy(self, taxonomy):
        returnMe = self.localFacade.getAllEntitiesByTaxonomy(taxonomy)
        return returnMe        
    
    '''
    def getAllAgentsInAgentScope(self, subjectAgentID):
        """ Returns a list of object agents that share a common scope with the subject agent """
        returnMe = self.localFacade.getAllAgentsInAgentScope(subjectAgentID)
        return returnMe 
    
    
    def getAllLandmarksInAgentScope(self, subjectAgentID):
        """ 
        Returns all landmarks (whether or not they are associated with any agent) that share a common scope with the subject agent
        """
        returnMe = self.localFacade.getAllLandmarksInAgentScope(subjectAgentID)
        return returnMe 
    
    
    def getAllAgentsInAgentView(self, subjectAgentID):
        """ 
        Returns all object agents that the subject agent can 'see'; meaning that their scope intersects the subject agent's view
        """
        returnMe = self.localFacade.getAllAgentsInAgentView(subjectAgentID)
        return returnMe 
    
    
    def getAllLandmarksInAgentView(self, subjectAgentID):
        """ 
        Returns all landmarks (whether or not they are associated with any agent) that the subject agent can 'see'; 
            meaning that their scope intersects the subject agent's view
        """
        returnMe = self.localFacade.getAllLandmarksInAgentView(subjectAgentID)
        return returnMe 
    
    
    def getAllAgentsWithAgentView(self, subjectAgentID):
        """ 
        Returns all object agents that can 'see' the subject agent; meaning that their view intersects the subject agent's scope
        """
        returnMe = self.localFacade.getAllAgentsWithAgentView(subjectAgentID)
        return returnMe 
    
    
    def getAllLandmarksWithAgentView(self, subjectAgentID):
        """ 
        Returns all landmarks (whether or not they are associated with any agent) that can 'see' the subject agent; 
            meaning that their view intersects the subject agent's scope
        """
        returnMe = self.localFacade.getAllLandmarksWithAgentView(subjectAgentID)
        return returnMe 
    
    
    def getAllAgentsInSpecifiedPage(self, pageID):
        """ 
        Returns all object agents in scope of the specified page.  
        """
        returnMe = self.localFacade.getAllAgentsInSpecifiedPage(pageID)
        return returnMe 
    
    def getAllAgentsWithViewOfSpecifiedPage(self, pageID):
        """ 
        Returns all object agents in scope of the specified page.  
        """
        returnMe = self.localFacade.getAllAgentsWithViewOfSpecifiedPage(pageID)
        return returnMe 
    '''
    
    def getEntity(self, entityUUID):
        returnMe = self.localFacade.getEntity(entityUUID)
        return returnMe     
    
    def getEntityMemeType(self, entityUUID):
        returnMe = self.localFacade.getEntityMemeType(entityUUID)
        return returnMe     
    
    def getEntityMetaMemeType(self, entityUUID):
        returnMe = self.localFacade.getEntityMetaMemeType(entityUUID)
        return returnMe     
        
        
    def getEntityHasProperty(self, entityUUID, propertyName):
        returnMe = self.localFacade.getEntityHasProperty(entityUUID, propertyName)
        return returnMe         
        
        
    def getEntityPropertyType(self, entityUUID, propertyName):
        returnMe = self.localFacade.getEntityPropertyType(entityUUID, propertyName)
        return returnMe           
        
        
    def getEntityPropertyValue(self, entityUUID, propertyName):
        returnMe = self.localFacade.getEntityPropertyValue(entityUUID, propertyName)
        return returnMe          
        
        
    def getHasCounterpartsByType(self, entityUUID, memePath, linkType = None, isMeme = True):
        returnMe = self.localFacade.getHasCounterpartsByType(entityUUID, memePath, linkType, isMeme)
        return returnMe     
    
    
    #Todo - needs to have params tweaked: linkDirectionTypes.BIDIRECTIONAL, '', None, linkAttributeOperatorTypes.EQUAL
    def getLinkCounterpartsByType(self, entityUUID, memePath, linkType = None):
        returnMe = self.localFacade.getCounterpartsByType(entityUUID, memePath, linkType)
        return returnMe
    
    #Todo - needs to have params tweaked: linkDirectionTypes.BIDIRECTIONAL, '', None, linkAttributeOperatorTypes.EQUAL
    def getLinkCounterpartsByMetaMemeType(self, entityUUID, metamemePath, linkType = None):
        returnMe = self.localFacade.getCounterpartsByType(entityUUID, metamemePath, linkType, False)
        return returnMe
       
        
    def getLinkCounterparts(self, entityUUID):
        returnMe = self.localFacade.getLinkCounterparts(entityUUID)
        return returnMe            
        
        
    def getIsEntitySingleton(self, entityUUID):
        returnMe = self.localFacade.getIsEntitySingleton(entityUUID)
        return returnMe              
        
        
    def getIsEntityTaxonomyExact(self, entityUUID, taxonomy):
        returnMe = self.localFacade.getIsEntityTaxonomyExact(entityUUID, taxonomy)
        return returnMe         
        
        
    def getIsEntityTaxonomyGeneralization(self, entityUUID, taxonomy):
        returnMe = self.localFacade.getIsEntityTaxonomyGeneralization(entityUUID, taxonomy)
        return returnMe        
        
        
    def getIsEntityTaxonomySpecialization(self, entityUUID, taxonomy):
        returnMe = self.localFacade.getIsEntityTaxonomySpecialization(entityUUID, taxonomy)
        return returnMe
                
    
    def getIsMemeSingleton(self, memePath):
        returnMe = self.localFacade.getIsMemeSingleton(memePath)
        return returnMe         
        
        
    def getMemeExists(self, memePath):
        returnMe = self.localFacade.getMemeExists(memePath)
        return returnMe    
    
    
    def getMemeMetaMeme(self, memePath): 
        returnMe = self.localFacade.getParentMetaMemes(memePath)
        return returnMe 
        
        
    def instantiateEntity(self, entityUUID):
        self.localFacade.instantiateEntity(entityUUID) 
                
        
    def removeEntityLink(self, entityUUID, memberUUID):
        self.localFacade.removeEntityLink(entityUUID, memberUUID)         
        
        
    def removeAllCustomPropertiesFromEntity(self, entityUUID):
        self.localFacade.removeAllCustomPropertiesFromEntity(entityUUID)
    
        
    def removeEntityProperty(self, entityUUID, propertyName):
        self.localFacade.removeEntityProperty(entityUUID, propertyName)        
        
        
    def removeEntityTaxonomy(self, entityUUID, taxonomy):
        self.localFacade.removeEntityTaxonomy(entityUUID, taxonomy)   
        
    
        
    def revertEntityPropertyValues(self, entityUUID, drilldown = False):
        self.localFacade.revertEntityPropertyValues(entityUUID, drilldown)       
        
        
    def setEntityPropertyValue(self, entityUUID, propertyName, propertyValue):
        self.localFacade.setEntityPropertyValue(entityUUID, propertyName, propertyValue)  
        
        
    def setStateEventScript(self, entityUUID, setStateEventScript):
        self.localFacade.setStateEventScript(entityUUID, setStateEventScript)  
        
        
    def evaluateEntity(self, entityUUID, runtimeVariables, ActionID = None, Subject = None, Controller = None, supressInit = False):
        #memePath, ActionID = None, Subject = None, Controller = None, supressInit = False
        result = self.localFacade.evaluateEntity(entityUUID, runtimeVariables, ActionID, Subject, Controller, supressInit)  
        return result
        
    def getScriptFromPath(self, scriptLocation):
        scriptObject = self.localFacade.getScriptFromPath(scriptLocation)  
        return scriptObject   
    
    def installPythonExecutor(self, entityUUID, callableObject):
        try:
            #assert callable(callableObject)
            unusedScriptObject = self.localFacade.installPythonExecutor(entityUUID, callableObject)
        except Exception as e:
            unusedCatch = e  

    def writeDebug(self, statement):
        uStatement = str(statement)
        self.localFacade.writeDebug(uStatement)  
    
    def writeLog(self, statement):
        uStatement = str(statement)
        self.localFacade.writeLog(uStatement)  
        
    def writeError(self, statement):
        uStatement = str(statement)
        self.localFacade.writeError(uStatement) 
        
    def getEntityCounterparts(self, entityUUID):
        overview = self.localFacade.getEntityCounterparts(entityUUID) 
        return overview 
        
    def getClusterMembers(self, entityUUID, linkTypes = 0, crossSingletons = False):
        overview = self.localFacade.getClusterMembers(entityUUID, linkTypes, crossSingletons) 
        return overview 
    
    def sourceMemeCreate(self, modulePath, memeName, metamemePath):
        valReport = self.localFacade.sourceMemeCreate(modulePath, memeName, metamemePath) 
        return valReport 
    
    def sourceMemePropertySet(self, fullTemplatePath, propName, propValueStr):
        valReport = self.localFacade.sourceMemePropertySet(fullTemplatePath, propName, propValueStr) 
        return valReport 
    
    def sourceMemePropertyRemove(self, fullTemplatePath, propName):
        valReport = self.localFacade.sourceMemePropertyRemove(fullTemplatePath, propName) 
        return valReport 
    
    def sourceMemeMemberAdd(self, fullTemplatePath, memberID, occurrence):
        valReport = self.localFacade.sourceMemeMemberAdd(fullTemplatePath, memberID, occurrence) 
        return valReport 
    
    def sourceMemeMemberRemove(self, fullTemplatePath, memberID):
        valReport = self.localFacade.sourceMemeMemberRemove(fullTemplatePath, memberID)
        return valReport 
    
    def sourceMemeEnhancementAdd(self, fullTemplatePath, memeID):
        valReport = self.localFacade.sourceMemeEnhancementAdd(fullTemplatePath, memeID)
        return valReport 
    
    def sourceMemeEnhancementRemove(self, fullTemplatePath, memeID):
        valReport = self.localFacade.sourceMemeEnhancementRemove(fullTemplatePath, memeID)
        return valReport 
    
    def sourceMemeTagAdd(self, fullTemplatePath, tag):
        valReport = self.localFacade.sourceMemeTagAdd(fullTemplatePath, tag)
        return valReport 
    
    def sourceMemeTagRemove(self, fullTemplatePath, tag):
        valReport = self.localFacade.sourceMemeTagRemove(fullTemplatePath, tag)
        return valReport 
    
    def sourceMemeSetSingleton(self, fullTemplatePath, isSingleton):
        valReport = self.localFacade.sourceMemeSetSingleton(fullTemplatePath, isSingleton)
        return valReport 
    
    def sourceMemeCompile(self, fullTemplatePath, validate = True):
        valReport = self.localFacade.sourceMemeCompile(fullTemplatePath, validate)
        return valReport 
    
    def sourceMemeValidate(self, fullTemplatePath):
        valReport = self.localFacade.sourceMemeValidate(fullTemplatePath)
        return valReport 
    
    def map(self, mapFunction, paramSet, argumentMap):
        mapResult = self.localFacade.map(mapFunction, paramSet, argumentMap)
        return mapResult 
    
    def reduce(self, reduceFunction, paramSet):
        results = self.localFacade.reduce(reduceFunction, paramSet)
        return results 
    
    def getHasTaxonomy(self, memeFullTemplatePath, taxonomyFullTemplatePath):
        overview = self.localFacade.getHasTaxonomy(memeFullTemplatePath, taxonomyFullTemplatePath) 
        return overview
    
    def getTaxonomy(self, memeFullTemplatePath):
        overview = self.localFacade.getTaxonomy(memeFullTemplatePath) 
        return overview   

