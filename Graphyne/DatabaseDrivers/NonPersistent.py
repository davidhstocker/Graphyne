"""
   NonPersistent.py: (Non)Persistence Module, using native Python dictionaries for holding the Entity Repository.
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'


from .. import Exceptions
import uuid
from decimal import Decimal


moduleName = 'DatabaseDrivers.NonPersistent'



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
        
        
class LinkType(object):
    ATOMIC = 0
    SUBATOMIC = 1
    ALIAS = 2 
    
    
    
class LinkDirectionType(object):
    BIDIRECTIONAL = 0
    OUTBOUND = 1
    INBOUND = 2
    
    
    
class linkAttributeOperatorType(object):
    EQUAL = 0
    EQUALORGREATER = 1
    EQUALORLESS = 2
    GREATER = 3
    LESS = 4
    NOTEQUAL = 5
    IN = 6
    NOTIN = 7


#To be 'circularly' imported, via the initialize function.  
global logQ
#global templateRepository
global api

def initialize(iapi, itemplateRepository, ilogQ, iConnection = None, passedPersistence = None, reInitialize = False):
    """
        iConnection, passedPersistence and reInitialize are simply ignored, but included in the constructor to maintain interface compatability with RelationalDatabase.py
    """
    global logQ
    global templateRepository
    global api
    logQ = ilogQ
    templateRepository = itemplateRepository
    api = iapi


def setPersistence(unusedDB):
    ''' Method only used to maintain compatibility with the persistence modules, such as RelationalDatabase.py'''
    pass    
    

global logType 
global linkTypes
global linkAttributeOperator
global linkDirectionType
logTypes =  LogType()
logType = logTypes.ENGINE
logLevel = LogLevel()
linkTypes = LinkType()  
linkAttributeOperator = linkAttributeOperatorType()
linkDirectionType = LinkDirectionType()



class EntityRepository(object):
    ''' The default (no persistence) entity instance catalog'''
    className = "EntityRepository" 
    
    def __init__(self):
        #self.indexByAssociation= {}
        #self.indexByClass = {}
        self.indexByType = {}
        self.indexByID = {} 
        self.indexByTag = {}
        #self.indexByTaxonomy = {}
        self.indexByPage = {}
        

    def getEntitiesByTag(self, tag, zone = None):
        ''' return all entities (possibly restricted by zone) with tag 
            returns empty list when no instance of tag in repo'''
        #method = moduleName + '.' +  self.className + '.getEntitiesByTag'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        returnEntities = []
        validEntities = {}
        
        entities = self.indexByTag(tag)
        for entityID in entities:
            try:
                entity = self.indexByID[entityID]
                if entity.depricated != True:
                    entity.entityLock.acquire()
                    validEntities[entityID] = False
                    try:
                        if zone is None:
                            validEntities[entityID] = True
                        else:
                            try:
                                zoneEntities = self.indexByPage[zone]
                                for zoneEntityID in zoneEntities:
                                    try:
                                        if zoneEntityID not in validEntities:
                                            validEntities[zoneEntityID] = True
                                    except: pass
                            except:
                                e = "zone %s does not exist" %(zone)
                                raise Exceptions.NoSuchZoneError(e)
                    except Exceptions.NoSuchZoneError as e:
                        raise Exceptions.NoSuchZoneError(e)
                    except Exception as e:
                        raise e                
                    finally:
                        entity.entityLock.release()
                
                for validEntityID in validEntities.keys():
                    if validEntities[validEntityID] == True:
                        returnEntities.append(validEntityID)
            except:
                pass
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnEntities
    
    

    def getEntitiesByType(self, memePath, zone = None):
        ''' return all entities (possibly restricted by zone) with parent meme type 
            returns empty list when no instance of tag in repo'''
        
        '''
            This method currently has a workaround implementation. EntityRepository.indexByType is currently not maintained by the Entity methods and is left empty.
            I it were in use, it would greatly speed up our access.  Otherwise, we have to (expensively) iterate over the entire repo; which is the current workaround
        '''
        method = moduleName + '.' +  self.className + '.getEntitiesByType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        returnEntities = []
        validEntities = {}
        
        try:
            '''
            #Workaround
            for entity in self.indexByID.itervalues():
                if entity.memePath.fullTemplatePath == memePath:
                    if entity.depricated != True:
                        entity.entityLock.acquire(True)
                        validEntities[entity.uuid] = False
                        try:
                            if zone is None:
                                validEntities[entity.uuid] = True
                            else:
                                try:
                                    zoneEntities = self.indexByPage[zone]
                                    for zoneEntityID in zoneEntities:
                                        try:
                                            assert zoneEntityID in validEntities
                                            validEntities[zoneEntityID] = True
                                        except AssertionError: pass
                                except:
                                    e = "zone %s does not exist" %(zone)
                                    raise Exceptions.NoSuchZoneError(e)
                        except Exceptions.NoSuchZoneError as e:
                            raise Exceptions.NoSuchZoneError(e)
                        except Exception as e:
                            raise e                
                        finally:
                            entity.entityLock.release()
            for validEntityID in validEntities.iterkeys():
                if validEntities[validEntityID] == True:
                    returnEntities.append(validEntityID)
            #/Workaround
            '''
            #The following code requires the EntityRepository.indexByType to be implemented
            entities = self.indexByType[memePath]
            for entityID in entities:
                try:
                    entity = self.indexByID[entityID]
                    if entity.depricated != True:
                        entity.entityLock.acquire(True)
                        validEntities[entityID] = False
                        try:
                            if zone is None:
                                validEntities[entityID] = True
                            else:
                                try:
                                    zoneEntities = self.indexByPage[zone]
                                    for zoneEntityID in zoneEntities:
                                        try:
                                            assert zoneEntityID in validEntities
                                            validEntities[zoneEntityID] = True
                                        except AssertionError: pass
                                except:
                                    e = "zone %s does not exist" %(zone)
                                    raise Exceptions.NoSuchZoneError(e)
                        except Exceptions.NoSuchZoneError as e:
                            raise Exceptions.NoSuchZoneError(e)
                        except Exception as e:
                            raise e                
                        finally:
                            entity.entityLock.release()
                    
                    for validEntityID in validEntities.keys():
                        if validEntities[validEntityID] == True:
                            returnEntities.append(validEntityID)
                except:
                    pass
                
        except Exceptions.NoSuchEntityError as e:
            raise e
        except Exception as e:
            errorMessage = "Error while collecting entities of meme type %s.  Traceback = %s" %(memePath, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMessage])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnEntities



    def getEntitiesByMetaMemeType(self, metaMemePath):
        ''' return all entities (possibly restricted by zone) with parent metameme type 
            returns empty list when no instance of tag in repo'''
        method = moduleName + '.' +  self.className + '.getEntitiesByMetaMemeType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        returnEntities = []
        try:
            metaMeme = templateRepository.resolveTemplateAbsolutely(metaMemePath)
            if metaMeme is None:
                errorMsg = "No such metameme %s in the schema repository" %metaMemePath
                raise Exceptions.TemplatePathError(errorMsg)
            else:
                memes = metaMeme.collectMemes()    
                for memePath in memes:
                    try:
                        entityIDs = self.getEntitiesByType(memePath)
                        returnEntities.extend(entityIDs)
                    except Exceptions.NoSuchEntityError:
                        #so we don't actually have any entities deployed from this meme?  No problem
                        pass
                    except Exception as e:
                        #so we don't actually have any entities deployed from this meme?  No problem
                        errorMsg = "Error while trying to retrieve entities of metameme type %s.  Traceback = %s" %(metaMemePath, e)
                        logQ.put( [logType , logLevel.WARNING , method , errorMsg])
                return returnEntities
        except Exceptions.TemplatePathError as e:
            raise e
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    
    
    def getEntitiesByPage(self, zone):
        ''' return all entities in zone'''
        #method = moduleName + '.' +  self.className + '.getEntitiesByPage'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        returnEntities = []
        
        try:
            zoneEntities = self.indexByPage[zone]
            for entityID in zoneEntities:
                try:
                    entity = self.indexByID[entityID]
                    if entity.depricated != True:
                        returnEntities.append(entityID)
                except:
                    pass
        except:
            e = "page %s does not exist" %(zone)
            raise Exceptions.NoSuchZoneError(e)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnEntities
    
    
    
    def getEntity(self, uuid):
        ''' return entity with specified uuid'''
        #method = moduleName + '.' +  self.className + '.getEntity'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        returnEntity = None
        
        try:
            returnEntity = self.indexByID[uuid]
        except:
            try:
                #let's see if it is because of the type of variable by casting it to a string
                stringifiedUUID = getUUIDAsString(uuid)
                returnEntity = self.indexByID[stringifiedUUID]
            except KeyError as e:
                raise e
            except Exception as e:
                raise e
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnEntity
    
    
    
    
    def getAllEntities(self):
        ''' returns a list with the uuid of every entity currently in the repo'''
        #method = moduleName + '.' +  self.className + '.getEntity'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        returnEntities = []
        
        try:
            for returnEntityID in list(self.indexByID.keys()):
                returnEntities.append(returnEntityID)
        except Exception as e:
            raise e
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return returnEntities
 
 
    def getAllArchivedEntities(self, activeState = None):
        """ 
            In the relational module, this method returns a list of tuples for all archived entities, with the appropriate 'depricated' flag.
            Since there is no persistence when using this module as 'persistence', simpe return an empty list 
        """
        return []
    
    
    
    def getEntitiesByTaxonomy(self, taxonomy, onlyFullTax = False, zone = None):
        """ fetch Entities using a templatePath object """
        #method = moduleName + '.' +  self.className + '.getEntitiesByTaxonomy'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        instances = []
        fullTaxInstances = []
        
        if zone is None:
            instances = self.indexByTaxonomy[taxonomy]
        else:
            instancesSuperset = self.indexByTaxonomy[taxonomy]
            for instance in instancesSuperset:
                # Only agents have a location.  Materials and Controllers will be filtered out
                if type(instance) == 'Agent':
                    try:
                        if instance.location.zone == zone:
                            instances.append[instance]
                    except:
                        pass
        
        # if onlyFullTax == True, then restrict it to those instances            
        if onlyFullTax == False:
            fullTaxInstances = instances  
        else:
            for instance in instances:
                try:
                    if taxonomy == instance.taxonomy.fullPath:
                        fullTaxInstances.append(instance)
                except:
                    pass          
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return fullTaxInstances



    def addEntityProvisional(self, entitityUUID, masterEntityID, isDepricated, memePath, metaMeme):
        """
            This method is not needed in the non-persistent scenario.  It is used in the relational database persistence case, so that the entity UUID can be used as a 
            foreign key before the entity if fully bootstrapped.
        """
        pass 
    
    

    def addEntity(self, entity):
        """         self.indexByAssociation= {}
        self.indexByClass = {}
        self.indexByID = {} 
        self.indexByTag = {}
        self.indexByTaxonomy = {}
        self.indexByPage = {} """
        #method = moduleName + '.' +  self.className + '.addEntity'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        entityID = entity.uuid
        entity.setThreadable()
        self.indexByID[entityID] = entity
        
        #index by tag 
        #It is important to note that unlike indexByID, indexByTag does not contain the actual entities.  It acts as a lookup table, referencing IDs
        for tag in entity.tags:
            taggedEntities = []
            try:
                taggedEntities = self.indexByTag[tag]
            except: pass #not a problem.  This might be the first time we are indexing an entity with this tag
            taggedEntities.append(entityID)
            filterListDuplicates(taggedEntities)
            self.indexByTag[tag] = taggedEntities   
        
        #index by type
        #Functions similar to indexByTag, above
        entitiesOfMeme = []
        try:
            entitiesOfMeme = self.indexByType[entity.memePath.fullTemplatePath]
        except: pass #not a problem.  This might be the first time we are indexing an entity from this meme
        entitiesOfMeme.append(entityID)
        filterListDuplicates(entitiesOfMeme)
        self.indexByType[entity.memePath.fullTemplatePath] = entitiesOfMeme
        
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])

    def addEntityToIndex(self, entity):
        """
            An abbreviated addEntity method that only adds it to self.indexById.  This method is needed with database persistence, 
                but should not be called in the no-persistence scenario 
        """
        raise Exceptions.InconsistentPersistenceArchitecture("EntityRepository.addEntityToIndex() should not be called in the non-persistent scenario!")
    

    def addEntityListProperty(self, entityID, propName, propValues, memePath = None):
        """stub method for maintaining API interface compatibility with the RelationalDatabase"""
        pass        
        
    def addEntityStringProperty(self, entityID, propName, propValue, memePath = None, restList = None):
        """stub method for maintaining API interface compatibility with the RelationalDatabase"""
        pass
        
    def addEntityDecimalProperty(self, entityID, propName, propValue, memePath = None, restMin= None, restMax = None, restList = None):
        """stub method for maintaining API interface compatibility with the RelationalDatabase"""
        pass
        
    def addEntityIntegerProperty(self, entityID, propName, propValue, memePath = None, restMin= None, restMax = None, restList = None):
        """stub method for maintaining API interface compatibility with the RelationalDatabase"""
        pass
        
    def addEntityBooleanProperty(self, entityID, propName, propValue, memePath = None):
        """stub method for maintaining API interface compatibility with the RelationalDatabase"""
        pass
    
    def getAgent(self):
        return None
    
    def getAllAgents(self):
        return list(self.indexByID.keys())
    
    def getAgentsByType(self, agentType):
        agents = []
        return agents
    
    def getAgentsByPage(self, zoneID, agentType = None):
        agents = []
        return agents
    
    def getAllControllers(self):
        controllers = []
        return controllers



class EntityLink(object):
    className = "EntityLink"
    
    def __init__(self, memberID1, memberID2, membershipType, linkAttributes = {}, keyLink = None, masterEntity = None):
        #method = moduleName + '.' +  self.className + '.__init__'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.memberID1 = memberID1
        self.memberID2 = memberID2
        self.attributes = linkAttributes
        self.membershipType = membershipType
        self.keyLink = keyLink
        self.masterEntity = masterEntity
        self.uuid = uuid.uuid1()
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
        
    def getMembershipType(self):
        #method = moduleName + '.' +  self.className + '.getMembershipType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return self.membershipType
    
    def makeAtomic(self):
        #method = moduleName + '.' +  self.className + '.makeAtomic'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.membershipType = linkTypes.ATOMIC
        self.keyLink = None
        self.masterEntity = None
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        

    def makeSubAtomic(self, masterEntity):
        #method = moduleName + '.' +  self.className + '.makeSubAtomic'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.membershipType = linkTypes.SUBATOMIC
        self.masterEntity = masterEntity
        self.keyLink = None
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
    def makeAlias(self, keyLink):
        #method = moduleName + '.' +  self.className + '.makeAlias'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        self.membershipType = linkTypes.ALIAS
        self.keyLink = keyLink
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
    def getCounterpartUUID(self, uuid):
        #method = moduleName + '.' +  self.className + '.getCounterpartUUID'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        returnID = None
        if self.memberID1 == uuid:
            returnID = self.memberID1
        elif self.memberID2 == uuid:
            returnID = self.memberID2
        else:
            #todo need exception
            member1Meme = ""
            member2Meme = ""
            try:
                member1Meme = api.getEntityMemeType(self.memberID1)
                member2Meme = api.getEntityMemeType(self.memberID2)
                testEntityMeme = api.getEntityMemeType(uuid)
            except Exception as e:
                raise e
            errorMsg = "%s entity %s not a member of link %s.  It has members %s %s and %s %s" %(testEntityMeme, uuid, self.uuid, member1Meme, self.memberID1, member2Meme, self.memberID2)
            raise Exceptions.EntityNotInLinkError(errorMsg)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"]) 
        return returnID       
        
        
    def getCounterpartEntity(self, uuid):
        #method = moduleName + '.' +  self.className + '.getCounterpartEntity'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        counterpartUUID = self.getCounterpartUUID(uuid)
        counterpartEntity = entityRepository.getEntity(counterpartUUID)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return counterpartEntity
    
    
    def getKeyLink(self):
        #method = moduleName + '.' +  self.className + '.getKeyLink'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return self.keyLink
    
    
    def getMasterEntityUUID(self):
        #method = moduleName + '.' +  self.className + '.getKeyLink'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return self.masterEntity
    
    
    def getMasterEntity(self):
        #method = moduleName + '.' +  self.className + '.getKeyLink'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        entity = entityRepository.getEntity(self.masterEntity)
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        return entity
    


class LinkRepository(object):
    """ A catalog of Entity links 
        
    indexByID - A listing of entity links, by link UUID 
         
    """ 
        
    className = "LinkRepository"    
    
    def __init__(self):
        self.indexByID = {}
        self.indexByAssociation = {}
        
        
    def getAllLinks(self, entityUUID):
        linkList = []
        filteredLinkList = []
        try:
            linkDictInbound = self.getAllInboundLinks(entityUUID)
            linkDictOutbound = self.getAllOutboundLinks(entityUUID)
            linkList.extend(linkDictInbound)
            linkList.extend(linkDictOutbound)
            linkList.append(entityUUID)
            filteredLinkList = filterListDuplicates(linkList)
            return filteredLinkList
        except KeyError as e:
            raise e
        except Exception as e:
            raise e        
            
            
    def getAllInboundLinks(self, entityUUID):
        try:
            linkDict = self.indexByAssociation[entityUUID]
            return linkDict["inbound"]
        except KeyError as e:
            raise e
        except Exception as e:
            raise e
    
    def getAllOutboundLinks(self, entityUUID):
        try:
            linkDict = self.indexByAssociation[entityUUID]
            return linkDict["outbound"]
        except KeyError as e:
            raise e
        except Exception as e:
            raise e
        
    
    def getCounterpartTypeList(self, entityUUID):
        """ A little debugging method for determining the types of counterparts an entity has """
        
        counterparts = []
        assocList = []
        try:
            #assocList = self.indexByAssociation[getUUIDAsString(EntityUUID)]
            assocList = self.indexByAssociation[entityUUID]
        except:
            #no associations
            pass  
         
        for assocKey in assocList:
            memberType = api.getEntityMemeType(assocKey)
            counterparts.append(memberType)    
            
        return counterparts
 
    
    
    def getCounterpartIndices(self, entityUUID):
        """A debugging method for listing the uuid:meme-type pair listing for an entity's counterparts  """
        
        counterparts = []
        assocList = []
        try:
            #assocList = self.indexByAssociation[getUUIDAsString(EntityUUID)]
            assocList = self.indexByAssociation[entityUUID]
        except:
            #no associations
            pass  
         
        for assocKey in assocList:
            memberType = api.getEntityMemeType(assocKey)
            counterparts.append([assocKey, memberType])    
            
        return counterparts
        
    
    #Todo 
    def getCounterparts(self, entityUUID, linkDirection = linkDirectionType.BIDIRECTIONAL, traverseParameters = [], nodeParameters = [], memType = None, excludeLinks = []):
        ''' return a list of members with the specified link Type
        EntityUUID - the uuid of the entity for which we are finging counterparts
        traverseParameters - a list of Graph.TraverseParameter objects.  Each one supplied acts to filter the list of links to be removed.
            -if traverseParameters is empty, then all of the the links from memberID1 to memberID2 are removed
            Graph.TraverseParameter has three attributes: operator, parameter and value
                -if parameter, but value is null, then then all of the the links from memberID1 to memberID2, containing that parameter, are removed
        nodeParameters - the same as traverseParameters, but for the entity counterparts
        memType - The type of link sought.  None means all link types are valid
        excludeLinks - an explicit list of entity link uuids to be excluded from the search
        '''
        #method = moduleName + '.' +  self.className + '.getCounterparts'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        try:
            if (memType != linkTypes.ALIAS) and (memType != linkTypes.ATOMIC) and (memType != linkTypes.SUBATOMIC):
                memType = None
            counterparts = []
            assocList = []
            
            inboundList = []
            outboundList = []
            try:
                #assocList = self.indexByAssociation[getUUIDAsString(EntityUUID)]
                inboundOutbound = self.indexByAssociation[entityUUID]
                inboundList = inboundOutbound["inbound"]
                outboundList = inboundOutbound["outbound"]
                if linkDirection == linkDirectionType.BIDIRECTIONAL:
                    assocList.extend(inboundList)
                    assocList.extend(outboundList)
                elif linkDirection == linkDirectionType.INBOUND:
                    assocList.extend(inboundList)
                elif linkDirection == linkDirectionType.OUTBOUND:
                    assocList.extend(outboundList)
                else:
                    #if we land here, then linkDirectionType is not one of the allowed values
                    errorMsg = "%s.getCounterparts called with invalid linkDirection parameter %s.  " %(self.__class__, linkDirection)
                    errorMsg = "Valid values are linkDirectionType.BIDIRECTIONAL (%s), " %(errorMsg, linkDirectionType.BIDIRECTIONAL)
                    errorMsg = "linkDirectionType.INBOUND (%s), " %(errorMsg, linkDirectionType.INBOUND)
                    errorMsg = "and linkDirectionType.OUTBOUND (%s)" %(errorMsg, linkDirectionType.OUTBOUND)
                    raise Exceptions.UndefinedReferenceDirectionalityError(errorMsg)
            except Exceptions.UndefinedReferenceDirectionalityError as e:
                raise e
            except KeyError:
                #no associations, no problem
                pass
            
            #now we need to filter assocList down to only the values that match the attribute test
            filterUsOut = []
            for assocKey in assocList:
                attribTest = True
                for traverseParameter in traverseParameters:
                    try:
                        localattribTest = self.testLinkForAttribute(assocKey, traverseParameter.parameter, traverseParameter.value, traverseParameter.operator)
                        if localattribTest == False:
                            attribTest = False
                    except AttributeError:
                        errorMessage = "NonPersistent.LinkRepository.getCounterparts called without valid list of Graph.TraverseParameter objects.  Traceback = %s" %e
                        raise AttributeError(errorMessage)
                if attribTest is False:
                    filterUsOut.append(assocKey)
                
            if memType is not None:
                if (linkDirection == linkDirectionType.BIDIRECTIONAL) or (linkDirection == linkDirectionType.INBOUND):
                    for linkUUID in inboundList:
                        if (linkUUID not in excludeLinks) and (linkUUID not in filterUsOut):
                            stringifiedLinkUUID = getUUIDAsString(linkUUID)
                            linkObject = self.indexByID[stringifiedLinkUUID]
                            linkType = linkObject.membershipType
                            if (linkType is not None) and (memType == linkType):
                                attributesValid = self.testLinkedEntityForAttributes(linkObject.memberID1, nodeParameters)
                                if attributesValid == True:
                                    counterparts.append(linkObject.memberID1) #The entity where the reference originates
                if (linkDirection == linkDirectionType.BIDIRECTIONAL) or (linkDirection == linkDirectionType.OUTBOUND):
                    for linkUUID in outboundList:
                        if (linkUUID not in excludeLinks) and (linkUUID not in filterUsOut):
                            stringifiedLinkUUID = getUUIDAsString(linkUUID)
                            linkObject = self.indexByID[stringifiedLinkUUID]
                            linkType = linkObject.membershipType
                            if (linkType is not None) and (memType == linkType):
                                attributesValid = self.testLinkedEntityForAttributes(linkObject.memberID2, nodeParameters)
                                if attributesValid == True:
                                    counterparts.append(linkObject.memberID2) #The entity where the reference ends
            else:
                if (linkDirection == linkDirectionType.BIDIRECTIONAL) or (linkDirection == linkDirectionType.INBOUND):
                    for linkUUID in inboundList:
                        if (linkUUID not in excludeLinks) and (linkUUID not in filterUsOut):
                            linkUUIDAsString = getUUIDAsString(linkUUID)
                            linkObject = self.indexByID[linkUUIDAsString]
                            attributesValid = self.testLinkedEntityForAttributes(linkObject.memberID1, nodeParameters)
                            if attributesValid == True:
                                counterparts.append(linkObject.memberID1) #The entity where the reference originates
                if (linkDirection == linkDirectionType.BIDIRECTIONAL) or (linkDirection == linkDirectionType.OUTBOUND):
                    for linkUUID in outboundList:
                        if (linkUUID not in excludeLinks) and (linkUUID not in filterUsOut):
                            linkUUIDAsString = getUUIDAsString(linkUUID)
                            linkObject = self.indexByID[linkUUIDAsString]
                            attributesValid = self.testLinkedEntityForAttributes(linkObject.memberID2, nodeParameters)
                            if attributesValid == True:
                                counterparts.append(linkObject.memberID2) #The entity where the reference ends
    
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
            return counterparts  
        except AttributeError as e:
            raise e
        except Exception as e:
            raise e
 
 

    def testLinkedEntityForAttributes(self, entityID, nodeParameters = []): 
        """
        nodeParameters - a list of Graph.TraverseParameter objects.  Each one supplied acts to filter the list of links to be removed.
            -if traverseParameters is empty, then all of the the links from memberID1 to memberID2 are removed
            Graph.TraverseParameter has three attributes: operator, parameter and value
                -if parameter, but value is null, then then all of the the links from memberID1 to memberID2, containing that parameter, are removed
        """
        try:
            attribTest = True
            for nodeParameter in nodeParameters:
                localattribTest = testEntityForAttribute(entityID, nodeParameter.parameter, nodeParameter.value, nodeParameter.operator)
                if localattribTest == False:
                    attribTest = False 
            return attribTest  
        except AttributeError as e:
            errorMessage = "testLinkedEntityForAttributes called without valid list of Graph.TraverseParameter objects.  Traceback = %s" %e
            raise AttributeError(errorMessage)


    def testLinkForAttribute(self, linkID, attributeName = '', value = None, operator = linkAttributeOperator.EQUAL):
        '''
            tests the link for the given attribute/value/operator combination and returns True or False
             -if value is None, then the method simply tests for the presence of attributeName among the link's attributes
             -otherwise, it tests the value of the attribute against the supplied value/operator rules
             -if attributeName is empty, then return True
        '''
        if len(attributeName) < 1:
            #if attributeName is empty, always return true
            return True
        else:
            returnVal = False
            try:
                linkUUIDAsString = getUUIDAsString(linkID)
                entityLink = self.indexByID[linkUUIDAsString]
                try:
                    #if the next line does not raise an exception, then we have the attribute in this link
                    testForAttribute = entityLink.attributes[attributeName]
                    if value is None:
                        #if value is none, then we don't bother testing the actual value of the attribute.  It's presence is enough
                        returnVal = True
                    else:
                        #simple tests for presence
                        #if the attribute is not in the link, we should never reach this block of code.  A KeyError exception would have been raised on attribute retrieval.
                        #  In the catch block, we double check to see if the operator is linkAttributeOperator.NOTIN, but here the only valid IN operator is linkAttributeOperator.IN
                        if operator == linkAttributeOperator.NOTIN: 
                            returnVal = False
                        elif operator == linkAttributeOperator.IN:
                            returnVal = True
                        
                        #make sure that we try to normalize the types of value and testForAttribute
                        try:
                            if type(testForAttribute) == type(1.0):
                                value = float(value)
                            elif type(testForAttribute) == type(1):
                                value = int(value)
                            elif type(testForAttribute) == type('1'):
                                value = str(value)
                            else:
                                errorMsg = "Can't compare filter value %s of type %s to link attribute %s of type %s."  %(attributeName, type(value), attributeName, type(testForAttribute))
                                raise TypeError(errorMsg)
                        except TypeError as e:
                            raise e
                        except Exception as e:
                            raise e
                        
                        if (operator == linkAttributeOperator.EQUAL) and (value == testForAttribute): returnVal = True
                        elif (operator == linkAttributeOperator.EQUALORGREATER) and (value >= testForAttribute): returnVal = True  
                        elif (operator == linkAttributeOperator.EQUALORLESS) and (value <= testForAttribute): returnVal = True 
                        elif (operator == linkAttributeOperator.GREATER) and (value > testForAttribute): returnVal = True 
                        elif (operator == linkAttributeOperator.LESS) and (value < testForAttribute): returnVal = True
                        elif (operator == linkAttributeOperator.NOTEQUAL) and (value != testForAttribute): returnVal = True
                        elif operator == linkAttributeOperator.IN: pass #already checked above.  The check is here (despite possible performance penalty) to make the code block more readable
                        elif operator == linkAttributeOperator.NOTIN: pass #already checked above.  The check is here (despite possible performance penalty) to make the code block more readable
                        elif (operator < 8) and (operator > -1):
                            #operator is a valid value, but the test did not match
                            pass #returnVal = False.   
                        else:
                            badOperatorMsg = "%s.testLinkForAttribute called with invalid attribute comparison operator parameter %s.  " %(self.__class__, operator)
                            badOperatorMsg = "Valid values are linkAttributeOperator.EQUAL (%s), " %(badOperatorMsg, linkAttributeOperator.EQUAL)
                            badOperatorMsg = "linkAttributeOperator.EQUALORGREATER (%s), " %(badOperatorMsg, linkAttributeOperator.EQUALORGREATER)
                            badOperatorMsg = "linkAttributeOperator.EQUALORLESS (%s), " %(badOperatorMsg, linkAttributeOperator.EQUALORLESS)
                            badOperatorMsg = "linkAttributeOperator.GREATER (%s), " %(badOperatorMsg, linkAttributeOperator.GREATER)
                            badOperatorMsg = "linkAttributeOperator.LESS (%s), " %(badOperatorMsg, linkAttributeOperator.LESS)
                            badOperatorMsg = "linkAttributeOperator.NOTEQUAL (%s), " %(badOperatorMsg, linkAttributeOperator.NOTEQUAL)
                            badOperatorMsg = "linkAttributeOperator.IN (%s), " %(badOperatorMsg, linkAttributeOperator.IN)
                            badOperatorMsg = "and linkAttributeOperator.NOTIN (%s)" %(badOperatorMsg, linkAttributeOperator.NOTIN)
                            raise Exceptions.UndefinedReferenceValueComparisonOperator(badOperatorMsg)
                except KeyError:
                    #The attribute is not in entityLink.attributes{}.  If operator == linkAttributeOperator.NOTIN, then this is valid  
                    if operator == linkAttributeOperator.NOTIN: 
                        returnVal = True
                except TypeError as e:
                    raise e
                except Exceptions.UndefinedReferenceValueComparisonOperator as e:
                    raise e
                except Exception as e:
                    raise e
            except KeyError:
                operatorAsString = '=='
                if operator == linkAttributeOperator.EQUALORGREATER: operatorAsString = '>='
                elif operator == linkAttributeOperator.EQUALORLESS: operatorAsString = '<='
                elif operator == linkAttributeOperator.GREATER: operatorAsString = '>'
                elif operator == linkAttributeOperator.LESS: operatorAsString = '<'
                elif operator == linkAttributeOperator.NOTEQUAL: operatorAsString = '!='
                errorMessage = "attributeName %s, value %s, operator %s" %(attributeName, value, operatorAsString)
                raise Exceptions.UnknownLinkError(errorMessage)
            except Exceptions.UndefinedReferenceValueComparisonOperator as e:
                raise e
            except Exception as e:
                raise e
            finally:
                return returnVal
 
 

    
    def removeLink(self, memberID1, memberID2, traverseParameters = []):
        ''' remove references from memberID1 to memberID2, where the conditions of the parameterization are met.
            traverseParameters - a list of Graph.TraverseParameter objects.  Each one supplied acts to filter the list of links to be removed.
                -if traverseParameters is empty, then all of the the links from memberID1 to memberID2 are removed
                Graph.TraverseParameter has three attributes: operator, parameter and value
                    -if parameter, but value is null, then then all of the the links from memberID1 to memberID2, containing that parameter, are removed
        '''
        #method = moduleName + '.' +  self.className + '.catalogLink'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        try:
            try:
                assocList1 = self.indexByAssociation[memberID1]
            except KeyError as e:
                errorMsg = "There are no links originating from %s" %e
                raise Exceptions.EntityNotInLinkError(errorMsg)
            try:
                assocList2 = self.indexByAssociation[memberID2]
            except KeyError as e:
                errorMsg = "There are no links originating from %s" %e
                raise Exceptions.EntityNotInLinkError(errorMsg)
                            
            #since the link goes from 1 to 2, we can find it in memberID1's outbound list
            outboundLinks = {}
            inboundLinks = {}
            outboundLinkIDs = assocList1["outbound"]
            outboundLinkIDstrings = []
            inboundLinkIDs = assocList2["inbound"]
            inboundLinkIDstrings = []
            for outboundLinkID in outboundLinkIDs:
                olAsString = getUUIDAsString(outboundLinkID)
                entityLink = self.indexByID[olAsString]
                outboundLinks[olAsString] = entityLink
                outboundLinkIDstrings.append(olAsString)
            for inboundLinkID in inboundLinkIDs:
                ilAsString = getUUIDAsString(inboundLinkID)
                entityLink = self.indexByID[ilAsString]
                inboundLinks[ilAsString] = entityLink
                inboundLinkIDstrings.append(ilAsString)
            outboundLinksSet = set(outboundLinkIDstrings)
            inboundLinksSet = set(inboundLinkIDstrings)
            
            #Let's first filter to all links from 1 to 2
            allLinksFrom1To2 = []
            for outboundLinkKey in outboundLinks.keys():
                outboundLink = outboundLinks[outboundLinkKey]
                if outboundLink.memberID2 == memberID2:
                    allLinksFrom1To2.append(olAsString)
                    
            #Now the safety check, so that we don't get a corrupt link repository            
            #Let's first filter to all links from 1 to 2
            allLinksFrom2To1 = []
            for inboundLinkKey in inboundLinks.keys():
                inboundLink = inboundLinks[inboundLinkKey]
                if inboundLink.memberID1 == memberID1:
                    allLinksFrom2To1.append(ilAsString)

            #Now filter the removal list by traverseParameters
            #if traverseParameters is not empty, then filter it according to the rules in the traverseParameters 
            linksToBeRemoved = []
            linksToBeRemovedCheckSum = []
            if (len(traverseParameters) < 1):
                linksToBeRemoved = allLinksFrom1To2
                linksToBeRemovedCheckSum = allLinksFrom2To1
            else:
                for linkFrom1To2 in allLinksFrom1To2:
                    for traverseParameter in traverseParameters:
                        #Graph.TraverseParameter has three attributes: operator, parameter and value
                        attributeTest = self.testLinkForAttribute(linkFrom1To2, traverseParameter.parameter, traverseParameter.value, traverseParameter.operator)
                        if attributeTest is True:
                            linksToBeRemoved.append(linkFrom1To2)
                for linkFrom2To1 in allLinksFrom2To1:
                    for traverseParameter in traverseParameters:
                        #Graph.TraverseParameter has three attributes: operator, parameter and value
                        attributeTest = self.testLinkForAttribute(linkFrom2To1, traverseParameter.parameter, traverseParameter.value, traverseParameter.operator)
                        if attributeTest is True:
                            linksToBeRemovedCheckSum.append(linkFrom2To1)
                        
            #linksToBeRemoved and linksToBeRemovedCheckSum should be the same.
            linksToBeRemovedCSSet = set(linksToBeRemoved)
            linksToBeRemovedCheckSumCSSet = set(linksToBeRemovedCheckSum)
            checkSumSet = linksToBeRemovedCSSet.symmetric_difference(linksToBeRemovedCheckSumCSSet)
            if len(checkSumSet) > 0:
                #Houston, we have a problem
                problemForwardReferences = linksToBeRemovedCSSet.difference(linksToBeRemovedCheckSumCSSet)
                problemBackwardReferences = linksToBeRemovedCheckSumCSSet.difference(linksToBeRemovedCSSet)
                errorMessage = "Corrupt reference pairing between entity %s and %s.  The following references originate with %s and should end  at %s, but don't: %s.  The following references ens at %s and should originate from %s, but don't: %s." %(memberID1, memberID2, memberID1, memberID2, problemForwardReferences, memberID2, memberID1, problemBackwardReferences)
                raise Exceptions.UnanchoredReferenceError(errorMessage)
            
            #I we get to here, linksToBeRemovedCSSet and linksToBeRemovedCheckSumCSSet are the same.  Use either for removal
            outboundLinksSet.difference_update(linksToBeRemovedCSSet)
            inboundLinksSet.difference_update(linksToBeRemovedCSSet)
            assocList1["outbound"] = list(outboundLinksSet)
            assocList2["inbound"] = list(inboundLinksSet)
            self.indexByAssociation[memberID1] = assocList1
            self.indexByAssociation[memberID2] = assocList2
            
            #Don't forget to remove the links from the main index
            for linkToBeRemoved in linksToBeRemoved:
                self.indexByID.pop(linkToBeRemoved, None)
                    
        except Exceptions.EntityNotInLinkError as e:
            raise e     
        except Exception as e:
            #no associations for stringID1
            raise e
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])




    def catalogLink(self, memberID1, memberID2, membershipType = 0, linkAttributes = {}, keyLink = None, masterEntity = None):  
        ''' add the link to the listing.
            indexByAssociation is a dict, where each memberID is a key
            each item in indexByAssociation contains a second dict (called inboundOutbound in the code, below), with the keys "inbound" and "outbound"
            
            indexByAssociation
                |
                inboundOutbound ({"inbound":[],"outbound":[]})
        '''
        #method = moduleName + '.' +  self.className + '.catalogLink'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        link = EntityLink(memberID1, memberID2, membershipType, linkAttributes, keyLink, masterEntity)
        
        try:
            uuidAsString = getUUIDAsString(link.uuid)
            try:
                assoc1 = self.indexByAssociation[memberID1]
                try:
                    assoc1Outbound = assoc1["outbound"]
                    assoc1Outbound.append(link.uuid)
                    assoc1["outbound"] = assoc1Outbound
                    self.indexByAssociation[memberID1] = assoc1
                except Exception as e:
                    raise e
            except KeyError:
                #assoc1 entity has no links.  this is fine.  We can comfortably blindly index the link
                assoc1 = {"outbound" : [link.uuid], "inbound" : []}
                self.indexByAssociation[memberID1] = assoc1 
            except Exception as e:
                raise e
                
            try:
                assoc2 = self.indexByAssociation[memberID2]
                try:
                    assoc2Inbound = assoc2["inbound"]
                    assoc2Inbound.append(link.uuid)
                    assoc2["inbound"] = assoc2Inbound
                    self.indexByAssociation[memberID2] = assoc2
                except Exception as e:
                    raise e
            except KeyError:
                #assoc1 entity has no links.  this is fine.  We can comfortably blindly index the link
                assoc2 = {"outbound" : [], "inbound" : [link.uuid]}
                self.indexByAssociation[memberID2] = assoc2 
            except Exception as e:
                raise e
            self.indexByID[uuidAsString] = link
                           
        except Exception as e:
            raise e

        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
  
  
  
        
global entityRepository
global linkRepository
entityRepository = EntityRepository()
linkRepository = LinkRepository()




def testEntityForAttribute(entityID, attributeName = '', value = None, operator = linkAttributeOperator.EQUAL):
    '''
        tests the link's counterpart entity for the given attribute/value/operator combination and returns True or False
         -if value is None, then the method simply tests for the presence of attributeName among the link's attributes
         -otherwise, it tests the value of the attribute against the supplied value/operator rules
         -if attributeName is empty, then return True
    '''
    if len(attributeName) < 1:
        #if attributeName is empty, always return true
        return True
    else:
        returnVal = False
        try:
            if value is None:
                #if value is none, then we don't bother testing the actual value of the attribute.  It's presence is enough
                returnVal = True
            else:
                #if the next line does not raise an exception, then we have the attribute in this link
                testForAttribute = api.getEntityHasProperty(entityID, attributeName)
                if operator == linkAttributeOperator.NOTIN: 
                    if testForAttribute == False:
                        returnVal = True
                elif operator == linkAttributeOperator.IN:
                    if testForAttribute == True:
                        returnVal = True
                elif testForAttribute == False:
                    #If we'll be for checking specific values and the attribute is not present, don't bother processing any further
                    returnVal = True
                else:
                    attributeValue = api.getEntityPropertyValue(entityID, attributeName)
                    
                    #Normalize attributeValue and value to ve the same type                   
                    proptype = api.getEntityPropertyType(entityID, attributeName)
                    proptype = proptype.lower()
                    if proptype == "integer":
                        value = int(value)
                    elif proptype == "boolean":
                        value = int(value)
                    elif proptype == "decimal":
                        value = Decimal(value)
                    elif proptype == "string":
                        pass
                    else:
                        errorMsg = "Properties of type %s can't be used for filtering in traverse queries"
                        raise Exceptions.TraverseFilterError(errorMsg)
                    
                    if (operator == linkAttributeOperator.EQUAL) and (value == attributeValue): returnVal = True
                    elif (operator == linkAttributeOperator.EQUALORGREATER) and (value >= attributeValue): returnVal = True  
                    elif (operator == linkAttributeOperator.EQUALORLESS) and (value <= attributeValue): returnVal = True 
                    elif (operator == linkAttributeOperator.GREATER) and (value > attributeValue): returnVal = True 
                    elif (operator == linkAttributeOperator.LESS) and (value < attributeValue): returnVal = True
                    elif (operator == linkAttributeOperator.NOTEQUAL) and (value != attributeValue): returnVal = True
                    elif (operator == linkAttributeOperator.NOTIN) and (value != attributeValue): returnVal = True
                    else:
                        entityType = api.getEntityMemeType(entityID)
                        badOperatorMsg = "testEntityForAttribute on entity %s called with invalid attribute comparison operator parameter %s.  " %(entityType, operator)
                        badOperatorMsg = "%s. Valid values are linkAttributeOperator.EQUAL (%s), " %(badOperatorMsg, linkAttributeOperator.EQUAL)
                        badOperatorMsg = "%s linkAttributeOperator.EQUALORGREATER (%s), " %(badOperatorMsg, linkAttributeOperator.EQUALORGREATER)
                        badOperatorMsg = "%s linkAttributeOperator.EQUALORLESS (%s), " %(badOperatorMsg, linkAttributeOperator.EQUALORLESS)
                        badOperatorMsg = "%s linkAttributeOperator.GREATER (%s), " %(badOperatorMsg, linkAttributeOperator.GREATER)
                        badOperatorMsg = "%s linkAttributeOperator.LESS (%s), " %(badOperatorMsg, linkAttributeOperator.LESS)
                        badOperatorMsg = "%s linkAttributeOperator.NOTEQUAL (%s), " %(badOperatorMsg, linkAttributeOperator.NOTEQUAL)
                        badOperatorMsg = "%s linkAttributeOperator.IN (%s), " %(badOperatorMsg, linkAttributeOperator.IN)
                        badOperatorMsg = "%s and linkAttributeOperator.NOTIN (%s)" %(badOperatorMsg, linkAttributeOperator.NOTIN)
                        raise Exceptions.UndefinedReferenceValueComparisonOperator(badOperatorMsg)
        except KeyError:
            operatorAsString = '=='
            if operator == linkAttributeOperator.EQUALORGREATER: operatorAsString = '>='
            elif operator == linkAttributeOperator.EQUALORLESS: operatorAsString = '<='
            elif operator == linkAttributeOperator.GREATER: operatorAsString = '>'
            elif operator == linkAttributeOperator.LESS: operatorAsString = '<'
            elif operator == linkAttributeOperator.NOTEQUAL: operatorAsString = '!='
            errorMessage = "attributeName %s, value %s, operator %s" %(attributeName, value, operatorAsString)
            raise Exceptions.UnknownLinkError(errorMessage)
        except Exceptions.UndefinedReferenceValueComparisonOperator as e:
            raise e
        except Exception as e:
            raise e
        finally:
            return returnVal
 
    
    
    
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
    
    
    
def filterListDuplicates(listToFilter):
    # Not order preserving
    keys = {}
    for e in listToFilter:
        keys[e] = 1
    return list(keys.keys())