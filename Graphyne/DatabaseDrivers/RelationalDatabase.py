"""
   RelationalDatabase.py: Persistence Module, using ODBC connections to SQL databases for holding the Entity Repository.
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'

# Start Boilerplate

from .. import Exceptions
import uuid
from decimal import Decimal

#To be 'circularly' imported, via the initialize function.  
global logQ
global templateRepository
global api
global dbDriverModule 
global connectionString
global persistence
global sqlSyntax
moduleName = 'DatabaseDrivers.RelationalDatabase'
dbDriverModule = None  #set with setPersistence()
persistence = None
sqlSyntax = None


class EntityPropertyType(object):
    String = 0
    Integer = 1
    Decimal = 2
    Boolean = 3
    List = 4
    

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


class EntityActiveState(object):
    ACTIVE = 0
    DEPRICATED = 1
    ALL = 2 
            
        
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



def initialize(iapi, itemplateRepository, ilogQ, iConnectionString, passedPersistence, reInitialize = False, canCommit = True):
    global logQ
    global templateRepository
    global api
    global entityRepository
    global connectionString
    global persistence
    connectionString = iConnectionString
    logQ = ilogQ
    templateRepository = itemplateRepository
    api = iapi
    persistence = passedPersistence
    ensureDatabase()
    if reInitialize == True:
        emptyDatabase(canCommit)
    entityRepository = EntityRepository()
  

    

global logType 
global linkTypes
global linkAttributeOperator
global linkDirectionType
global entityPropTypes
global entityActiveStates
entityActiveStates = EntityActiveState()  
entityPropTypes = EntityPropertyType()
logTypes =  LogType()
logType = logTypes.ENGINE
logLevel = LogLevel()
linkTypes = LinkType()  
linkAttributeOperator = linkAttributeOperatorType()
linkDirectionType = LinkDirectionType()

#################
# End Boilerplate
#################


def applySchema():
    global persistence
    global sqlSyntax
    sqlSyntax.createRuntimeDB(persistence)
    
    
def dropDatabase(canCommit = True):
    global persistence
    global sqlSyntax
    cursor = persistence.cursor()
    tables = ["EntityLinkPropertyBooleans",
              "EntityLinkPropertyStrings",
              "EntityLinkPropertyDecimals",
              "EntityLinkPropertyIntegers",
              "EntityLink",
              "EntityTags",
              "EntityPropertyLists",
              "EntityPropertyBooleans",
              "EntityPropertyStrings",
              "EntityPropertyTexts",
              "EntityPropertyDecimals",
              "EntityPropertyIntegers",
              "Entity"]
    for tableToBeDropped in tables:
        cursor.execute("DROP TABLE %s" %tableToBeDropped)
    persistence.commit()
    
    
def emptyDatabase(canCommit = True):
    global persistence
    global sqlSyntax
    tables = ["EntityLinkPropertyBooleans",
              "EntityLinkPropertyStrings",
              "EntityLinkPropertyDecimals",
              "EntityLinkPropertyIntegers",
              "EntityLink",
              "EntityTags",
              "EntityPropertyLists",
              "EntityPropertyBooleans",
              "EntityPropertyStrings",
              "EntityPropertyTexts",
              "EntityPropertyDecimals",
              "EntityPropertyIntegers",
              "Entity"]
    if canCommit == True:
        cursor = persistence.cursor()
        try:
            for tableToBeDropped in tables:
                #Unusually, we don't use SQL parameterization here.  This is because MS SQL Server dot not respond to the DELETE FROM command and rather uses TRUNCATE TABLE
                #TRUNCATE TABLE does not work with parameterization , but since no external input is involved here, we don't incur any SQL injection risks in this case
                toBeDropped = "%s %s" %(sqlSyntax.clearTable, tableToBeDropped)
                cursor.execute(toBeDropped)
            persistence.commit()
        except Exception as e:
            cursor.rollback()
    else:
        #sqlite has no support for commit andf rollback
        try:
            for tableToBeDropped in tables:
                toBeDropped = "%s %s" %(sqlSyntax.clearTable, tableToBeDropped)
        except Exception as e:
            print(e)
    ensureDatabase()
    
    
def resetDatabase(canCommit = True):
    try:
        emptyDatabase(canCommit)
    except: 
        #db already exists
        applySchema()
        

def ensureDatabase():
    try:
        applySchema()
    except:
        pass
    



class EntityRepository(object):
    ''' The default (no persistence) entity instance catalog'''
    className = "EntityRepository" 
    
    def __init__(self):
        self.indexByID = {} 
 
 
    def genericEntitySelect(self, sqlSelectStatement):
        '''
            A generic method for executing select statements and returning a result.
            #I this were java or c#, it would be a private method
        '''
        global persistence
        
        entityList = []
        cursor = persistence.cursor()
        cursor.execute(sqlSelectStatement)
        rawCursorResult = cursor.fetchall() 
        for cursorResRow in rawCursorResult:
            #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
            entityList.append(cursorResRow[0])
        entitySet = set(entityList)
        if len(entitySet) < 1:
            raise Exceptions.NoSuchEntityError() 
        returnEntities =  list(entitySet)
        return returnEntities
    
        

    def getEntitiesByTag(self, tag, zone = None):
        ''' return all entities (possibly restricted by zone) with tag 
            returns empty list when no instance of tag in repo'''
        method = moduleName + '.' +  self.className + '.getEntitiesByTag'
        global persistence
        
        #Set the SQL Syntax
        global sqlSyntax
        try:
            entitySelectStatement = sqlSyntax.selectGetEntitiesByTag
        except:
            raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectGetEntitiesByTag, as sqlSyntax has not been defined")

        try:
            entityList = []
            cursor = persistence.cursor()
            cursor.execute(entitySelectStatement, (tag, ))
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                entityList.append(cursorResRow[0])
            return entityList
        except Exceptions.NoSuchEntityError as e:
            return []
        except Exception as e:
            errorMessage = "Error while collecting entities of tag %s.  Traceback = %s" %(tag, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMessage])
            raise e
    

    def getEntitiesByType(self, memePath, zone = None):
        ''' return all entities (possibly restricted by zone) with parent meme type 
            returns empty list when no instance of tag in repo'''
        method = moduleName + '.' +  self.className + '.getEntitiesByType'
        global persistence
        
        #Set the SQL Syntax
        global sqlSyntax
        try:
            entitySelectStatement = sqlSyntax.selectGetEntitiesByType
        except:
            raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectGetEntitiesByType, as sqlSyntax has not been defined")

        try:
            entityList = []
            cursor = persistence.cursor()
            cursor.execute(entitySelectStatement, (memePath, ))
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                entityList.append(cursorResRow[0])
            return entityList
        except Exception as e:
            errorMessage = "Error while collecting entities of meme type %s.  Traceback = %s" %(memePath, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMessage])
            raise e



    def getEntitiesByMetaMemeType(self, metaMemePath, zone = None):
        ''' return all entities (possibly restricted by zone) with parent metameme type 
            returns empty list when no instance of tag in repo'''
        method = moduleName + '.' +  self.className + '.getEntitiesByMetaMemeType'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        global persistence
        
        #Set the SQL Syntax
        global sqlSyntax
        try:
            entitySelectStatement = sqlSyntax.selectGetEntitiesByMetamemeType
        except:
            raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectGetEntitiesByMetamemeType, as sqlSyntax has not been defined")

        try:
            entityList = []
            cursor = persistence.cursor()
            cursor.execute(entitySelectStatement, (metaMemePath, ))
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                entityList.append(cursorResRow[0])
            return entityList
        except Exception as e:
            errorMessage = "Error while collecting entities of metaMeme type %s.  Traceback = %s" %(metaMemePath, e)
            logQ.put( [logType , logLevel.WARNING , method , errorMessage])
            raise e
        
        
    
    
    def getEntitiesByPage(self, zone):
        ''' This method is depricated'''
        return []
    
 
 
 
    def getEntity(self, uuid):
        ''' Returns the entity with specified uuid, from the indexByID dictionary.  '''
        #method = moduleName + '.' +  self.className + '.getEntity'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        returnEntity = None
        
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
 
    
    
   
    def getAllEntities(self, activeState = entityActiveStates.ACTIVE):
        ''' returns a list with the uuid of every entity currently in the repo, possibly filtered by the depricated flag'''
        global persistence
        returnEntities = []
        try:
            #Set the SQL Syntax
            global sqlSyntax
            try:
                entitySelectStatement = sqlSyntax.selectGetAllEntities
                if activeState == 0:
                    entitySelectStatement = sqlSyntax.selectGetAllEntitiesActive0
                if activeState == 1:
                    entitySelectStatement = sqlSyntax.selectGetAllEntitiesActive1
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectGetAllEntities, as sqlSyntax has not been defined")

            cursor = persistence.cursor()
            cursor.execute(entitySelectStatement)
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                returnEntities.append(cursorResRow[0])
            return returnEntities    
        except Exception as e:
            unused = e
            
            
    def getAllArchivedEntities(self, activeState = entityActiveStates.ACTIVE):
        """ return a list of tuples for all archived entities, with the appropriate 'depricated' flag """
        global sqlSyntax
        entitySelectStatement = sqlSyntax.selectGetAllEntitiesActive0
        global persistence
        returnEntities = []
        try:
            #Set the SQL Syntax
            try:
                if activeState == 0:
                    entitySelectStatement = sqlSyntax.selectGetRessurectedEntities0
                if activeState == 1:
                    entitySelectStatement = sqlSyntax.selectGetRessurectedEntities1
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectGetAllEntities, as sqlSyntax has not been defined")

            cursor = persistence.cursor()
            cursor.execute(entitySelectStatement)
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                returnTuple = [cursorResRow[0], cursorResRow[1], cursorResRow[2], cursorResRow[3]]
                returnEntities.append(returnTuple)
            return returnEntities    
        except Exception as e:
            unused = e
    


    def addEntityProvisional(self, entitityUUID, masterEntityID, isDepricated, memePath, metaMeme):
        """
            This is a placeholder method to get the entity into the database, so that primary key constraints are not violated when running mergeEnhancements().
            When we create entities, we need to build up the "child" network of entities - if any - and link them to the entity being created.  (it is a recursive operation)
            Since we need to build up this network before the entity if fully bootstraped, we need to add a record to the entity table, so that these links can be created.
            This is only a partial registration.  addEntity() finishes the operation.
            
            isDepricated = True/False
            memePath = entity.memePath.fullTemplatePath
            metaMeme = entity.metaMeme
        """
        global persistence
        global sqlSyntax

        #real insertion   
        cursor = persistence.cursor()
        try:
            #Set the SQL Syntax
            try:
                sqlInsertStatement = sqlSyntax.insertEntity
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.insertEntity, as sqlSyntax has not been defined")
            stringifiedUUID = getUUIDAsString(entitityUUID)
            stringifiedMasterEntityUUID = getUUIDAsString(entitityUUID)
            cursor.execute(sqlInsertStatement, (stringifiedUUID, int(isDepricated), memePath, metaMeme, stringifiedMasterEntityUUID))
        except Exception as e:
            #We should never see this and we have a problem if we do
            persistence.rollback()
            errorMsg = "Database rollback on provisional insert of entity of meme type %s of metameme type %s.  Traceback = %s" %(memePath, metaMeme, e)
            logQ.put( [logType , logLevel.ERROR , "RelationalDatabase.EntityRepository.addEntityProvisional" , errorMsg])
            raise e        
        
    
    def addEntity(self, entity):
        """
            The general strategy is to build up a list of insert, update and delete statements; essentially a dynamic SQL script.
            
            If the entity is not already in the DB:
                Build an insert statement for the entity
                Build an insert statement for every property
                Build an insert statement for every tag
        """
        global persistence
        global sqlSyntax

        #First, collect all of the properties that need to go into satellite tables
        propsList = []
        propsString = []
        propsBoolean = []
        propsDecimal = []
        propsInteger = []
        
        for propKey in entity.properties:
            prop = entity.properties[propKey]
            if prop.propertyType == entityPropTypes.String:
                propsString.append(prop)
            elif prop.propertyType == entityPropTypes.Integer:
                propsInteger.append(prop)
            elif prop.propertyType == entityPropTypes.Decimal:
                propsDecimal.append(prop)
            elif prop.propertyType == entityPropTypes.Boolean:
                propsBoolean.append(prop)
            else:
                propsList.append(prop)

        uuidAsString = getUUIDAsString(entity.uuid)
                
        #Update Actually We initially inserted with the addEntityProvisional() method
        #entity now goes into the indexByID dictionary
        #entity.setThreadable()
        entity.setThreadable()
        self.indexByID[uuidAsString] = entity    
        
        #(initScriptName, execScriptName, terminateScriptName, entity.uuid, depricatedInt, entity.memePath, entity.metaMeme, initScriptSQLVal, execScriptSQLVal, terminateScriptSQLVal)
        cursor = persistence.cursor()
        try:
            for tag in entity.tags:
                #Set the SQL Syntax
                try:
                    sqlInsertStatement = sqlSyntax.insertEntityTags
                except:
                    raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.insertEntityTags, as sqlSyntax has not been defined")

                try:
                    cursor.execute(sqlInsertStatement, (uuidAsString, tag, ))
                except Exception as e:
                    raise e
            
            isInitialLoad = True    
            for prop in propsList:
                self.addEntityListProperty(uuidAsString, prop.name, prop.value, prop.memePath.fullTemplatePath, isInitialLoad)
            for prop in propsString:
                self.addEntityStringProperty(uuidAsString, prop.name, prop.value, prop.memePath.fullTemplatePath, str(prop.restList), isInitialLoad)
            for prop in propsDecimal:
                self.addEntityDecimalProperty(uuidAsString, prop.name, prop.value, prop.memePath.fullTemplatePath, prop.restMin, prop.restMax, prop.restList, isInitialLoad)
            for prop in propsInteger:
                self.addEntityIntegerProperty(uuidAsString, prop.name, prop.value, prop.memePath.fullTemplatePath, prop.restMin, prop.restMax, prop.restList, isInitialLoad)
            for prop in propsBoolean:
                self.addEntityBooleanProperty(uuidAsString, prop.name, prop.value, prop.memePath.fullTemplatePath, isInitialLoad)
            try:
                persistence.commit()
            except Exception as e:
                raise e
                           
        except Exceptions.EntityLinkFailureError as e:
            persistence.rollback()
            raise e
        except Exceptions.EntityPropertyDuplicateError as e:
            persistence.rollback()
            raise e
        except Exception as e:
            persistence.rollback()
            #debug
            #try:
            #    entity.entityLock = None
            #    self.addEntity(entity)
            #except Exception as e:
            #    pass
            #/debug
            raise e



    def addEntityToIndex(self, entity):
        """
            An abbreviated addEntity method that only adds it to self.indexById.  Use this method for restoring entities from persistence.  
                Since they are already in the database, we only need to ass the entity to indexById
        """
        uuidAsString = getUUIDAsString(entity.uuid)
        entity.setThreadable()
        self.indexByID[uuidAsString] = entity 



    def removeProperty(self, entityID, propertyID):
       
        #Set the SQL Syntax
        global sqlSyntax
        try:
            sqlDelLst = sqlSyntax.deleteEntityList
            sqlDelStr= sqlSyntax.deleteEntityString
            sqlDelTxt = sqlSyntax.deleteEntityText
            sqlDelDec = sqlSyntax.deleteEntityDecimal
            sqlDelInt= sqlSyntax.deleteEntityInteger
            sqlDelBln = sqlSyntax.deleteEntityBoolean
        except AttributeError as e:
            raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.xxx, as sqlSyntax has not been defined.  %s" %e)


        
        cursor = persistence.cursor()
        try:
            cursor.execute(sqlDelLst, (entityID, propertyID, ))
        except: 
            pass
        try:
            cursor.execute(sqlDelStr, (entityID, propertyID, ))
        except: 
            pass
        try:
            cursor.execute(sqlDelTxt, (entityID, propertyID, ))
        except: 
            pass
        try:
            cursor.execute(sqlDelDec, (entityID, propertyID, ))
        except: 
            pass
        try:
            cursor.execute(sqlDelInt, (entityID, propertyID, ))
        except: 
            pass
        try:
            cursor.execute(sqlDelBln, (entityID, propertyID, ))
        except: 
            pass
        pass
        persistence.commit()
        
        

    def addEntityListProperty(self, entityID, propName, propValues, memePath = None, initialLoad = False):
        """ 
            A method for adding ad hoc properties after entity creation 
            The initialLoad flag is used when creating an entity.  The self.addEntity() method saves the pickled archive
            entity into the DB and then does the property updates.  In this case, the archive entity already has the 
            property, but it is not yet in the DB.  So we call this method with initialLoad == True as a signal not
            to try updating the archive entity.
        """
        global persistence
        global sqlSyntax
        try:
            uuidAsString = getUUIDAsString(entityID)
            cursor = persistence.cursor()
            
            #Set the SQL Syntax
            try:
                sqlDeleteStatement = sqlSyntax.deleteEntityList
                sqlInsertStatement = sqlSyntax.insertEntityList
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.insertEntityTags, as sqlSyntax has not been defined")

            #Set the SQL Syntax
            try:
                sqlInsertStatement = sqlSyntax.selectAddEntityTest
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectAddEntityTest, as sqlSyntax has not been defined")



            cursor.execute(sqlDeleteStatement, (propName, ))
            for propValue in propValues:
                cursor.execute(sqlInsertStatement, (uuidAsString, propName, str(propValue), memePath, ))
            persistence.commit()
        except Exception as e:
            raise e
        
        
    def addEntityStringProperty(self, entityID, propName, propValue, memePath = None, restList = None, initialLoad = False):
        """ A method for adding ad hoc properties after entity creation 
            The initialLoad flag is used when creating an entity.  The self.addEntity() method saves the pickled archive
            entity into the DB and then does the property updates.  In this case, the archive entity already has the 
            property, but it is not yet in the DB.  So we call this method with initialLoad == True as a signal not
            to try updating the archive entity.
        """
        #Set the SQL Syntax
        global persistence
        global sqlSyntax
        uuidAsString = getUUIDAsString(entityID)
        cursor = persistence.cursor() 
        
        try:
            
            try:
                if (restList is not None) and (memePath is not None):      
                    if len(propValue) < 100:
                        sqlInsertStatement = sqlSyntax.insertEntityStringRestricted
                    else:
                        sqlInsertStatement = sqlSyntax.insertEntityTextRestricted
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, ))
                elif (restList is None) and (memePath is not None):      
                    if len(propValue) < 100:
                        sqlInsertStatement = sqlSyntax.insertEntityStringUnRestricted
                    else:
                        sqlInsertStatement = sqlSyntax.insertEntityTextUnRestricted
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, ))
                else:      
                    if len(propValue) < 100:
                        sqlInsertStatement = sqlSyntax.insertEntityString
                    else:
                        sqlInsertStatement = sqlSyntax.insertEntityText
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, ))
            except AttributeError as e:
                raise e
        except Exception as e:
            persistence.commit()
            raise e
        except Exception as e:
            raise e
        
        
    def addEntityDecimalProperty(self, entityID, propName, propValue, memePath = None, restMin= None, restMax = None, restList = None, initialLoad = False):
        """ A method for adding ad hoc properties after entity creation 
            The initialLoad flag is used when creating an entity.  The self.addEntity() method saves the pickled archive
            entity into the DB and then does the property updates.  In this case, the archive entity already has the 
            property, but it is not yet in the DB.  So we call this method with initialLoad == True as a signal not
            to try updating the archive entity.        
        """
        #addDecimalProperty(self, name, value, constrained = None, restMin = None, restMax = None, restList = None, memePath = None)
        global persistence
        uuidAsString = getUUIDAsString(entityID)
        cursor = persistence.cursor() 
        
        global sqlSyntax
        try:
            #Set the SQL Syntax
            try:
                if (restMin is not None) and (restMax is not None) and (restList is not None):
                    sqlInsertStatement = sqlSyntax.insertEntityDecimalRestrictionsAll
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, float(propValue), float(restMin), float(restMax), str(restList), memePath, ))
                elif (restMin is not None) and (restMax is not None) and (restList is None):
                    sqlInsertStatement = sqlSyntax.insertEntityDecimalRestrictionsMinMax
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, float(propValue), float(restMin), float(restMax), memePath, ))
                elif (restMin is not None) and (restMax is None) and (restList is not None):
                    sqlInsertStatement = sqlSyntax.insertEntityDecimalRestrictionsMinList
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, float(propValue), float(restMin), str(restList), memePath, ))
                elif (restMin is None) and (restMax is not None) and (restList is not None):
                    sqlInsertStatement = sqlSyntax.insertEntityDecimalRestrictionsMaxList
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, float(propValue), float(restMax), str(restList), memePath, ))
                elif (restMin is None) and (restMax is None) and (restList is not None):
                    sqlInsertStatement = sqlSyntax.insertEntityDecimalRestrictionsList
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, float(propValue), str(restList), memePath, ))
                elif (restMin is None) and (restMax is not None) and (restList is None):
                    sqlInsertStatement = sqlSyntax.insertEntityDecimalRestrictionsMax
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, float(propValue), float(restMax), memePath, ))
                elif (restMin is not None) and (restMax is None) and (restList is None):
                    sqlInsertStatement = sqlSyntax.insertEntityDecimalRestrictionsMin
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, float(propValue), float(restMin), memePath, ))
                elif (restMin is None) and (restMax is None) and (restList is None):
                    sqlInsertStatement = sqlSyntax.insertEntityDecimalRestrictions
                    cursor.execute(sqlInsertStatement, (uuidAsString, propName, float(propValue), memePath, ))
            except AttributeError as e:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.xxx, as sqlSyntax has not been defined.  %s" %e)
            finally:
                persistence.commit()
        except Exceptions.UndefinedSQLSyntax as e:
            raise e
        except Exception as e:
            raise e
        
        
        
    def addEntityIntegerProperty(self, entityID, propName, propValue, memePath = None, restMin= None, restMax = None, restList = None, initialLoad = False):
        """ A method for adding ad hoc properties after entity creation 
            The initialLoad flag is used when creating an entity.  The self.addEntity() method saves the pickled archive
            entity into the DB and then does the property updates.  In this case, the archive entity already has the 
            property, but it is not yet in the DB.  So we call this method with initialLoad == True as a signal not
            to try updating the archive entity.
        """
        #addDecimalProperty(self, name, value, constrained = None, restMin = None, restMax = None, restList = None, memePath = None)
        global persistence
        uuidAsString = getUUIDAsString(entityID)
        cursor = persistence.cursor() 
        
        try:
            #Set the SQL Syntax
            global sqlSyntax
            try:
                #Set the SQL Syntax
                try:
                    if (restMin is not None) and (restMax is not None) and (restList is not None):
                        sqlInsertStatement = sqlSyntax.insertEntityIntegerRestrictionsAll
                        cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, restMin, restMax, str(restList), memePath, ))
                    elif (restMin is not None) and (restMax is not None) and (restList is None):
                        sqlInsertStatement = sqlSyntax.insertEntityIntegerRestrictionsMinMax
                        cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, restMin, restMax, memePath, ))
                    elif (restMin is not None) and (restMax is None) and (restList is not None):
                        sqlInsertStatement = sqlSyntax.insertEntityIntegerRestrictionsMinList
                        cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, restMin, str(restList), memePath, ))
                    elif (restMin is None) and (restMax is not None) and (restList is not None):
                        sqlInsertStatement = sqlSyntax.insertEntityIntegerRestrictionsMaxList
                        cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, restMax, str(restList), memePath, ))
                    elif (restMin is None) and (restMax is None) and (restList is not None):
                        sqlInsertStatement = sqlSyntax.insertEntityIntegerRestrictionsList
                        cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, str(restList), memePath, ))
                    elif (restMin is None) and (restMax is not None) and (restList is None):
                        sqlInsertStatement = sqlSyntax.insertEntityIntegerRestrictionsMax
                        cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, restMax, memePath, ))
                    elif (restMin is not None) and (restMax is None) and (restList is None):
                        sqlInsertStatement = sqlSyntax.insertEntityIntegerRestrictionsMin
                        cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, restMin, memePath, ))
                    elif (restMin is None) and (restMax is None) and (restList is None):
                        sqlInsertStatement = sqlSyntax.insertEntityIntegerRestrictions
                        cursor.execute(sqlInsertStatement, (uuidAsString, propName, propValue, memePath, ))
                except AttributeError as e:
                    raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.xxx, as sqlSyntax has not been defined.  %s" %e)
                except Exception as e:
                    raise e
            except Exception as e:
                raise e
            finally:
                persistence.commit()
        except Exceptions.UndefinedSQLSyntax as e:
            raise e
        except Exception as e:
            raise e
        
        
    def addEntityBooleanProperty(self, entityID, propName, propValue, memePath = None, initialLoad = False):
        """ A method for adding ad hoc properties after entity creation 
            The initialLoad flag is used when creating an entity.  The self.addEntity() method saves the pickled archive
            entity into the DB and then does the property updates.  In this case, the archive entity already has the 
            property, but it is not yet in the DB.  So we call this method with initialLoad == True as a signal not
            to try updating the archive entity.
        """
        #addDecimalProperty(self, name, value, constrained = None, restMin = None, restMax = None, restList = None, memePath = None)
        global persistence
        uuidAsString = getUUIDAsString(entityID)
        cursor = persistence.cursor() 
        
        try:
            #Set the SQL Syntax
            global sqlSyntax
            try:
                sqlInsertStatement = sqlSyntax.insertEntityBoolean
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.insertEntityBoolean, as sqlSyntax has not been defined")
            try:
                if propValue.upper() == "TRUE": 
                    propValue = True
            except:
                pass 
            cursor.execute(sqlInsertStatement, (uuidAsString, propName, int(propValue), memePath, )) 
            
            persistence.commit()
        except Exception as e:
            raise e
        

    def getAllEntityProperties(self, entityID):
        """
            Returns a list of tuples, contain the entity's properties
            
            Each tuple is in the constructor format of the Graph.EntityProperty.__init__() ,method
            [name, value, propertyType, constrained = False, restMin = None, restMax = None, restList = None, memePath = None]
        """
        entityProperties = []
        
        try:
            uuidAsString = getUUIDAsString(entityID)
            cursor = persistence.cursor() 
            global sqlSyntax
            
            try:
                sqlSelectGetEntityPropertyLists = sqlSyntax.selectGetEntityPropertyLists        #Returns: [entityID, propName, propVal, memePath]
                sqlSelectGetEntityPropertyBooleans = sqlSyntax.selectGetEntityPropertyBooleans  #Returns: [entityID, propName, propVal, memePath]
                sqlSelectGetEntityPropertyStrings = sqlSyntax.selectGetEntityPropertyStrings    #Returns: [entityID, propName, propVal, restList, memePath]
                sqlSelectGetEntityPropertyTexts = sqlSyntax.selectGetEntityPropertyTexts        #Returns: [entityID, propName, propVal, restList, memePath]
                sqlSelectGetEntityPropertyDecimals = sqlSyntax.selectGetEntityPropertyDecimals  #Returns: [entityID, propName, propVal, restMin, restMax, restList, memePath]
                sqlSelectGetEntityPropertyIntegers= sqlSyntax.selectGetEntityPropertyIntegers   #Returns: [entityID, propName, propVal, restMin, restMax, restList, memePath]
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectGetEntityPropertyXXX, as sqlSyntax has not been defined")
            
            #Lists
            cursor.execute(sqlSelectGetEntityPropertyLists, (uuidAsString, )) 
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #EntityProperty.propertyType = 4
                #[name, value, propertyType, constrained = False, restMin = None, restMax = None, restList = None, memePath = None]
                propertyTuple = [cursorResRow[1], cursorResRow[2], 4, False, None, None, None, cursorResRow[3]]
                entityProperties.append(propertyTuple)
                
            #Booleans
            cursor.execute(sqlSelectGetEntityPropertyBooleans, (uuidAsString, )) 
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #EntityProperty.propertyType = 3
                #[name, value, propertyType, constrained = False, restMin = None, restMax = None, restList = None, memePath = None]
                propertyTuple = [cursorResRow[1], cursorResRow[2], 3, False, None, None, None, cursorResRow[3]]
                entityProperties.append(propertyTuple)
                
            #Strings
            cursor.execute(sqlSelectGetEntityPropertyStrings, (uuidAsString, )) 
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #EntityProperty.propertyType = 0
                #[name, value, propertyType, constrained = False, restMin = None, restMax = None, restList = None, memePath = None]
                if cursorResRow[3] is not None:
                    propertyTuple = [cursorResRow[1], cursorResRow[2], 0, True, None, None, cursorResRow[3], cursorResRow[4]]
                else:
                    propertyTuple = [cursorResRow[1], cursorResRow[2], 0, False, None, None, cursorResRow[3], cursorResRow[4]]
                entityProperties.append(propertyTuple)
                
            #Texts
            cursor.execute(sqlSelectGetEntityPropertyTexts, (uuidAsString, )) 
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #EntityProperty.propertyType = 0
                #[name, value, propertyType, constrained = False, restMin = None, restMax = None, restList = None, memePath = None]
                if cursorResRow[3] is not None:
                    propertyTuple = [cursorResRow[1], cursorResRow[2], 0, True, None, None, cursorResRow[3], cursorResRow[4]]
                else:
                    propertyTuple = [cursorResRow[1], cursorResRow[2], 0, False, None, None, cursorResRow[3], cursorResRow[4]]
                entityProperties.append(propertyTuple)
                
            #Decimals
            cursor.execute(sqlSelectGetEntityPropertyDecimals, (uuidAsString, )) 
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #EntityProperty.propertyType = 2
                #[name, value, propertyType, constrained = False, restMin = None, restMax = None, restList = None, memePath = None]
                if (cursorResRow[3] is not None) or (cursorResRow[4] is not None) or (cursorResRow[5] != '[]'):
                    propertyTuple = [cursorResRow[1], cursorResRow[2], 2, True, cursorResRow[3], cursorResRow[4], cursorResRow[5], cursorResRow[6]]
                else:
                    propertyTuple = [cursorResRow[1], cursorResRow[2], 2, False, cursorResRow[3], cursorResRow[4], cursorResRow[5], cursorResRow[6]]
                entityProperties.append(propertyTuple)
                
            #integers
            cursor.execute(sqlSelectGetEntityPropertyIntegers, (uuidAsString, )) 
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #EntityProperty.propertyType = 1
                #[name, value, propertyType, constrained = False, restMin = None, restMax = None, restList = None, memePath = None]
                if (cursorResRow[3] is not None) or (cursorResRow[4] is not None) or (cursorResRow[5] is not None):
                    propertyTuple = [cursorResRow[1], cursorResRow[2], 1, True, cursorResRow[3], cursorResRow[4], cursorResRow[5], cursorResRow[6]]
                else:
                    propertyTuple = [cursorResRow[1], cursorResRow[2], 1, False, cursorResRow[3], cursorResRow[4], cursorResRow[5], cursorResRow[6]]
                entityProperties.append(propertyTuple)
            
            return entityProperties
        except Exception as e:
            raise e
 
        

    def removeEntity(self, uuid):
        ''' remove entity with specified uuid.  The graph API is responsible for making sure that all links are already removed'''
        #method = moduleName + '.' +  self.className + '.removeEntity'
        #logQ.put( [logType , logLevel.DEBUG , method , "entering"])
        
        try:
            #A single entity makes its presence known in many, many tables
            sqlDelLink = sqlSyntax.removeLinks
            sqlDelEntity = sqlSyntax.removeEntity
            sqlDelLinkBool = sqlSyntax.removeLinkAttributeBool
            sqlDelLinkInt = sqlSyntax.removeLinkAttributeInt
            sqlDelLinkDec = sqlSyntax.removeLinkAttributeDec
            sqlDelLinkString = sqlSyntax.removeLinkAttributeStr
            sqlDelLst = sqlSyntax.removeEntityPropertyLists
            sqlDelStr= sqlSyntax.removeEntityPropertyStrings
            sqlDelTxt = sqlSyntax.removeEntityPropertyTexts
            sqlDelDec = sqlSyntax.removeEntityPropertyDecimals
            sqlDelInt= sqlSyntax.removeEntityPropertyIntegers
            sqlDelBln = sqlSyntax.removeEntityPropertyBooleans
        except AttributeError as e:
            raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.xxx, as sqlSyntax has not been defined.  %s" %e)
        
        try:
            uuidAsString = getUUIDAsString(uuid)
            
            try:
                #First, remove it from the index
                del self.indexByID[uuid]
            except KeyError:
                #KeyError exceptions get thrown when the uuid is not present in indexByID
                try:
                    #let's see if it is because of the type of variable by casting it to a string
                    stringifiedUUID = getUUIDAsString(uuid)
                    del self.indexByID[stringifiedUUID]
                except KeyError as e:
                    raise e
                except Exception as e:
                    raise e
            
            #Remove entity references from the database
            with persistence:
                cursor = persistence.cursor() 
                cursor.execute(sqlDelLinkBool, (uuidAsString, )) 
                cursor.execute(sqlDelLinkInt, (uuidAsString, )) 
                cursor.execute(sqlDelLinkDec, (uuidAsString, )) 
                cursor.execute(sqlDelLinkString, (uuidAsString, )) 
                cursor.execute(sqlDelLst, (uuidAsString, )) 
                cursor.execute(sqlDelStr, (uuidAsString, )) 
                cursor.execute(sqlDelTxt, (uuidAsString, )) 
                cursor.execute(sqlDelDec, (uuidAsString, )) 
                cursor.execute(sqlDelInt, (uuidAsString, )) 
                cursor.execute(sqlDelBln, (uuidAsString, )) 
                cursor.execute(sqlDelLink, (uuidAsString, uuidAsString)) 
                cursor.execute(sqlDelEntity, (uuidAsString, )) 

            
        except KeyError:
            raise Exceptions.NoSuchEntityError("Can't delete entity %s.  Key Error in Entity repository cache.  Traceback =  %s" %(uuid, e))
        except AttributeError as e:
            raise Exceptions.NoSuchEntityError("Can't delete entity %s.  Problem executing SQL DELETE FROM.  Traceback =  %s" %(uuid, e))
        except Exception as e:
            raise e
            
            
    
    #Remove Depricated Methods
    #Depricated
    def getAgent(self):
        return None
    
    def getAllAgents(self):
        return self.getAllEntities()
    
    def getAgentsByType(self, agentType):
        agents = []
        return agents
    
    def getAgentsByPage(self, zoneID, agentType = None):
        agents = []
        return agents
    
    def getAllControllers(self):
        controllers = []
        return controllers
    #Depricated





class LinkRepository(object):
    """ A catalog of Entity links 
        
    indexByID - A listing of entity links, by link UUID 
         
    """ 
    global persistence
    def getAllLinks(self, entityUUID):
        try:
            linkList = self.getAllInboundLinks(entityUUID, True)
            outboundList = self.getAllOutboundLinks(entityUUID, True)
            linkList.extend(outboundList)
            return linkList 
        except Exception as e:
            raise e        
            
         
    def getAllInboundLinks(self, entityUUID, wholeTuples = False): 
        """
            Get all of the links pointing to the given entity.  If wholeTuples is true, then return the list of 
            tuples from the SQL select statement on the EntityLinks table.  Otherwise, only the entity UUID 
            (the first item in the tuple) is returned.
        """
        try:
            global persistence
            uuisAsString = getUUIDAsString(entityUUID)
            linkList = []

            #Set the SQL Syntax
            global sqlSyntax
            try:
                linkSelectStatement = sqlSyntax.selectAllInboundLinks
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectAllInboundLinks, as sqlSyntax has not been defined")

            cursor = persistence.cursor()
            cursor.execute(linkSelectStatement, (uuisAsString, ))
            rawCursorResult = cursor.fetchall() 
            
            #Debug
            
            try:
                linkSelectStatementTest = "SELECT memberID2 FROM EntityLink"
                cursorTest = persistence.cursor()
                cursorTest.execute(linkSelectStatementTest, ())
                rawCursorResultTest = cursorTest.fetchall() 
                linkListTest = []
                for cursorResRowTest in rawCursorResultTest:
                    #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                    linkListTest.append(cursorResRowTest)
                """
                isIn = False
                if uuisAsString in linkListTest:
                    isIn = True
                """
            except Exception as e:
                pass
            
            #/Debug
            
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                if wholeTuples == True:
                    linkUUID = cursorResRow[0]
                    linkList.append(linkUUID)
                else:
                    linkList.append(cursorResRow)
            return linkList 
        except Exception as e:
            raise e
    
    def getAllOutboundLinks(self, entityUUID, wholeTuples = False):
        """
            Get all of the links pointing from the given entity.  If wholeTuples is true, then return the list of 
            tuples from the SQL select statement on the EntityLinks table.  Otherwise, only the entity UUID 
            (the first item in the tuple) is returned.
        """
        global persistence
        try:
            linkList = []
            
            #Set the SQL Syntax
            global sqlSyntax
            try:
                linkSelectStatement = sqlSyntax.selectAllOutboundLinks
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectAllOutboundLinks, as sqlSyntax has not been defined")

            cursor = persistence.cursor()
            uuisAsString = getUUIDAsString(entityUUID)
            cursor.execute(linkSelectStatement, (uuisAsString, ))
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                if wholeTuples == True:
                    linkUUID = cursorResRow[0]
                    linkList.append(linkUUID)
                else:
                    linkList.append(cursorResRow)
            return linkList 
        except KeyError as e:
            raise e
        except Exception as e:
            raise e
                
    
    def getCounterpartIndices(self, entityUUID):
        """A debugging method for listing the uuid:meme-type pair listing for an entity's counterparts  """
        global persistence
        counterparts = []
        try:
            linkList = []

            #Set the SQL Syntax
            global sqlSyntax
            try:
                linkSelectStatement = sqlSyntax.selectCounterpartIndices
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectCounterpartIndices, as sqlSyntax has not been defined")


            cursor = persistence.cursor()
            cursor.execute(linkSelectStatement, (entityUUID, ))
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                linkList.append(cursorResRow[0])

            #counterpartSelectStatement = 'SELECT memePath FROM Entity WHERE entityID IN (' + ','.join(map(str, linkList)) + ')'   
            for assocKey in linkList:
                counterpartSelectStatement = 'SELECT memePath FROM Entity WHERE entityID=?' 
                cursor.execute(counterpartSelectStatement, (assocKey, ))
                rawCursorResult = cursor.fetchall() 
                for cursorResRow in rawCursorResult:
                    #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                    counterparts.append([assocKey, cursorResRow[0]])                
        except Exception as e:
            #no associations.  debug aid only
            unusedCatchMe = e  
        return counterparts
        
    
    #Todo 
    def getCounterparts(self, entityUUID, linkDirection = linkDirectionType.BIDIRECTIONAL, traverseParameters = [], nodeParameters = [], memType = None, excludeLinks = []):
        ''' return a list of members with the specified link Type
        EntityUUID - the uuid of the entity for which we are finding counterparts
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
                if linkDirection == linkDirectionType.BIDIRECTIONAL:
                    inboundList = self.getAllInboundLinks(entityUUID)
                    outboundList = self.getAllOutboundLinks(entityUUID)
                    assocList.extend(inboundList)
                    assocList.extend(outboundList)
                elif linkDirection == linkDirectionType.INBOUND:
                    inboundList = self.getAllInboundLinks(entityUUID)
                    assocList.extend(inboundList)
                elif linkDirection == linkDirectionType.OUTBOUND:
                    outboundList = self.getAllOutboundLinks(entityUUID)
                    assocList.extend(outboundList)
                else:
                    #if we land here, then linkDirectionType is not one of the allowed values
                    errorMsg = "%s.getCounterparts called with invalid linkDirection parameter %s.  " %(self.__class__, linkDirection)
                    errorMsg = "%sValid values are linkDirectionType.BIDIRECTIONAL (%s), " %(errorMsg, linkDirectionType.BIDIRECTIONAL)
                    errorMsg = "%slinkDirectionType.INBOUND (%s), " %(errorMsg, linkDirectionType.INBOUND)
                    errorMsg = "%sand linkDirectionType.OUTBOUND (%s)" %(errorMsg, linkDirectionType.OUTBOUND)
                    raise Exceptions.UndefinedReferenceDirectionalityError(errorMsg)
            except Exceptions.UndefinedReferenceDirectionalityError as e:
                raise e
            except KeyError:
                #no associations, no problem
                pass
            
            #now we need to filter assocList down to only the values that match the attribute test
            filterUsOut = []
            for assoc in assocList:
                #entityID, memberID1 memberID2, membershipType, direction, masterEntity
                attribTest = True
                for traverseParameter in traverseParameters:
                    try:
                        localattribTest = self.testLinkForAttribute(assoc[0], traverseParameter.parameter, traverseParameter.value, traverseParameter.operator)
                        if localattribTest == False:
                            attribTest = False
                    except AttributeError:
                        errorMessage = "NonPersistent.LinkRepository.getCounterparts called without valid list of Graph.TraverseParameter objects.  Traceback = %s" %e
                        raise AttributeError(errorMessage)
                if attribTest is False:
                    filterUsOut.append(assoc[0])
                
            if memType is not None:
                if (linkDirection == linkDirectionType.BIDIRECTIONAL) or (linkDirection == linkDirectionType.INBOUND):
                    for link in inboundList:
                        #entityID, memberID1 memberID2, membershipType, direction, masterEntity
                        if (link[0] not in excludeLinks) and (link[0] not in filterUsOut):
                            if (link[3] is not None) and (memType == link[3]):
                                attributesValid = self.testLinkedEntityForAttributes(link[1], nodeParameters)
                                if attributesValid == True:
                                    counterparts.append(link[1]) #The entity where the reference originates
                if (linkDirection == linkDirectionType.BIDIRECTIONAL) or (linkDirection == linkDirectionType.OUTBOUND):
                    for link in outboundList:
                        #entityID, memberID1 memberID2, membershipType, direction, masterEntity
                        if (link[0] not in excludeLinks) and (link[0] not in filterUsOut):
                            if (link[3] is not None) and (memType == link[3]):
                                attributesValid = self.testLinkedEntityForAttributes(link[2], nodeParameters)
                                if attributesValid == True:
                                    counterparts.append(link[2]) #The entity where the reference ends
            else:
                if (linkDirection == linkDirectionType.BIDIRECTIONAL) or (linkDirection == linkDirectionType.INBOUND):
                    for link in inboundList:
                        #entityID, memberID1 memberID2, membershipType, direction, masterEntity
                        if (link[0] not in excludeLinks) and (link[0] not in filterUsOut):
                            attributesValid = self.testLinkedEntityForAttributes(link[1], nodeParameters)
                            if attributesValid == True:
                                counterparts.append(link[1]) #The entity where the reference originates
                if (linkDirection == linkDirectionType.BIDIRECTIONAL) or (linkDirection == linkDirectionType.OUTBOUND):
                    for link in outboundList:
                        #entityID, memberID1 memberID2, membershipType, direction, masterEntity
                        if (link[0] not in excludeLinks) and (link[0] not in filterUsOut):
                            attributesValid = self.testLinkedEntityForAttributes(link[2], nodeParameters)
                            if attributesValid == True:
                                counterparts.append(link[2]) #The entity where the reference ends
    
            #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
            #This method needs to return UUID objects
            counterpartUUIDs = []
            for counterpart in counterparts:
                counterpartUUID = uuid.UUID(counterpart)
                counterpartUUIDs.append(counterpartUUID)
            return counterpartUUIDs  
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
                global persistence
                linkUUIDAsString = getUUIDAsString(linkID)
                
                #Set the SQL Syntax
                global sqlSyntax
                try:
                    linkSelectStatementBool = sqlSyntax.selectLinkAttributeTestBool
                    linkSelectStatementInt = sqlSyntax.selectLinkAttributeTestInt
                    linkSelectStatementDec = sqlSyntax.selectLinkAttributeTestDec
                    linkSelectStatementStr = sqlSyntax.selectLinkAttributeTestStr
                except AttributeError as e:
                    raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.xxx, as sqlSyntax has not been defined.  %s" %e)

                
                try:
                    #if the next line does not raise an exception, then we have the attribute in this link
                    cursor = persistence.cursor()
                    testForAttribute = None
                    
                    #String
                    cursor.execute(linkSelectStatementStr, (linkUUIDAsString, attributeName, ))
                    rawCursorResult = cursor.fetchall() 
                    for cursorResRow in rawCursorResult:
                        if operator == linkAttributeOperator.NOTIN: returnVal = False
                        elif operator == linkAttributeOperator.IN: returnVal = True
                        testForAttribute = cursorResRow[0]
                        
                    #decimal
                    if testForAttribute is None:
                        cursor.execute(linkSelectStatementDec, (linkUUIDAsString, attributeName, ))
                        rawCursorResult = cursor.fetchall() 
                        for cursorResRow in rawCursorResult:
                            if operator == linkAttributeOperator.NOTIN: returnVal = False
                            elif operator == linkAttributeOperator.IN: returnVal = True
                            testForAttribute = cursorResRow[0]    
                            
                    #integer
                    if testForAttribute is None:
                        cursor.execute(linkSelectStatementInt, (linkUUIDAsString, attributeName, ))
                        rawCursorResult = cursor.fetchall() 
                        for cursorResRow in rawCursorResult:
                            if operator == linkAttributeOperator.NOTIN: returnVal = False
                            elif operator == linkAttributeOperator.IN: returnVal = True
                            testForAttribute = cursorResRow[0]     
                            
                    #boolean
                    if testForAttribute is None:
                        cursor.execute(linkSelectStatementBool, (linkUUIDAsString, attributeName, ))
                        rawCursorResult = cursor.fetchall() 
                        for cursorResRow in rawCursorResult:
                            if operator == linkAttributeOperator.NOTIN: returnVal = False
                            elif operator == linkAttributeOperator.IN: returnVal = True
                            testForAttribute = cursorResRow[0]                      
                            
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                    if ((testForAttribute is None) and (operator == linkAttributeOperator.NOTIN)):
                        #if value is none, then we don't bother testing the actual value of the attribute.  It's presence is enough
                        returnVal = True
                    else:
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
                            badOperatorMsg = "%sValid values are linkAttributeOperator.EQUAL (%s), " %(badOperatorMsg, linkAttributeOperator.EQUAL)
                            badOperatorMsg = "%slinkAttributeOperator.EQUALORGREATER (%s), " %(badOperatorMsg, linkAttributeOperator.EQUALORGREATER)
                            badOperatorMsg = "%slinkAttributeOperator.EQUALORLESS (%s), " %(badOperatorMsg, linkAttributeOperator.EQUALORLESS)
                            badOperatorMsg = "%slinkAttributeOperator.GREATER (%s), " %(badOperatorMsg, linkAttributeOperator.GREATER)
                            badOperatorMsg = "%slinkAttributeOperator.LESS (%s), " %(badOperatorMsg, linkAttributeOperator.LESS)
                            badOperatorMsg = "%slinkAttributeOperator.NOTEQUAL (%s), " %(badOperatorMsg, linkAttributeOperator.NOTEQUAL)
                            badOperatorMsg = "%slinkAttributeOperator.IN (%s), " %(badOperatorMsg, linkAttributeOperator.IN)
                            badOperatorMsg = "%sand linkAttributeOperator.NOTIN (%s)" %(badOperatorMsg, linkAttributeOperator.NOTIN)
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
        global persistence
        global sqlSyntax
        try:
            #start by selecting all links from member 1 to member 2
            linkList = []
            memberID1 = getUUIDAsString(memberID1)
            memberID2 = getUUIDAsString(memberID2)
            
            #Set the SQL Syntax
            try:
                linkSelectStatement = sqlSyntax.selectRemoveLinkTest
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectRemoveLinkTest, as sqlSyntax has not been defined")

            cursor = persistence.cursor()
            cursor.execute(linkSelectStatement, (memberID1, memberID2, ))
            rawCursorResult = cursor.fetchall() 
            for cursorResRow in rawCursorResult:
                #cursor.fetchall() returns a list of tuples, but in this case, we're only asking for a single value in the select statement
                linkList.append(cursorResRow)

            #Now filter the removal list by traverseParameters
            #if traverseParameters is not empty, then filter it according to the rules in the traverseParameters 
            linksToBeRemoved = []
            if len(linkList) > 0:
                if (len(traverseParameters) < 1):
                    linksToBeRemoved = linkList[0]
                else:
                    for link in linkList:
                        for traverseParameter in traverseParameters:
                            #Graph.TraverseParameter has three attributes: operator, parameter and value
                            attributeTest = self.testLinkForAttribute(link, traverseParameter.parameter, traverseParameter.value, traverseParameter.operator)
                            if attributeTest is True:
                                linksToBeRemoved.append(link)
                        
            #Don't forget to remove the links from the main index
            try:
                delBoolean = sqlSyntax.deleteLinkBoolean
                delString = sqlSyntax.deleteLinkString
                delDecimal = sqlSyntax.deleteLinkDecimal
                delIteger = sqlSyntax.deleteLinkInteger
                delLink = sqlSyntax.deleteLink
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectAddEntityTest, as sqlSyntax has not been defined")

            for linkToBeRemoved in linksToBeRemoved:
                cursor.execute(delBoolean, (linkToBeRemoved, ))
                cursor.execute(delString, (linkToBeRemoved, ))
                cursor.execute(delDecimal, (linkToBeRemoved, ))
                cursor.execute(delIteger, (linkToBeRemoved, ))
                cursor.execute(delLink, (linkToBeRemoved, ))
                    
        except Exceptions.EntityNotInLinkError as e:
            raise e     
        except Exception as e:
            #no associations for stringID1
            raise e
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])




    def catalogLink(self, memberID1, memberID2, membershipType = 0, linkAttributes = {}, masterEntity = None):  
        """
            Create an entity link and add it to the entity link repo.
            
            The general strategy is to build up a list of insert, update and delete statements; essentially a dynamic SQL script.
                This follows the same pattern as EntityRespoitory.addEntity(), which has a similar structure.
                It differs however, in that EntityRespoitory.addEntity() takes a Graph.Entity object as a parameter, while this method
                    is actually expected to create the object, add it to the repo and return the UUID.  In the no-persistence version
                    of this module, an actual EntityLink object is created and added to the repo.  here, we'll just write its properties 
                    directly to the DB. 
            
            If the entity is not already in the DB:
                Build an insert statement for the entity
                Build an insert statement for every property
                Build an insert statement for every tag
        """
        global persistence
        cursor = persistence.cursor()
        try:
            #First, collect all of the properties that need to go into satelite tables
            # This is a bit simpler than with entity properties; as we only have key and value and don't need a full Entity Property object
            propsString = []
            propsBoolean = []
            propsDecimal = []
            propsInteger = []
            entityLinkID = uuid.uuid1()
            entityLinkID = getUUIDAsString(entityLinkID)
            memberID1 = getUUIDAsString(memberID1)
            memberID2 = getUUIDAsString(memberID2)
            if masterEntity is not None:
                masterEntity = getUUIDAsString(masterEntity)
            
            for linkAttributeKey in list(linkAttributes.keys()):
                try:
                    if type(linkAttributes[linkAttributeKey]) == type(1.0):
                        propsDecimal.append(linkAttributeKey)
                    elif type(linkAttributes[linkAttributeKey]) == type(True):
                        propsBoolean.append(linkAttributeKey)
                    elif type(linkAttributes[linkAttributeKey]) == type(1):
                        propsInteger.append(linkAttributeKey)
                    elif type(linkAttributes[linkAttributeKey]) == type('1'):
                        propsString.append(linkAttributeKey)
                    else:
                        errorMessage = "Unable to create entity link with traverse parameter %s of type %s.  Entity link creation failed!" %(linkAttributeKey, type(linkAttributes[linkAttributeKey]))
                        raise Exceptions.EntityLinkFailureError(errorMessage)
                except Exceptions.EntityLinkFailureError as e:
                    raise e
                except Exception as e:
                    raise e
                                           
            #real insertion

            #Set the SQL Syntax
            global sqlSyntax
            try:
                if masterEntity is not None:
                    # (uuid.uuid1(), memberID1, memberID2, membershipType, masterEntity)
                    sqlInsertStatement = sqlSyntax.insertEntityCatalogLinkWithMaster
                    cursor.execute(sqlInsertStatement, (entityLinkID, memberID1, memberID2, membershipType, masterEntity, ))
                else:
                    # (uuid.uuid1(), memberID1, memberID2, membershipType)
                    sqlInsertStatement = sqlSyntax.insertEntityCatalogLinkNoMaster
                    cursor.execute(sqlInsertStatement, (entityLinkID, memberID1, memberID2, membershipType, ))      
            except AttributeError:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.insertEntityCatalogLinkNoMaster, as sqlSyntax has not been defined")
            except Exception as e:
                raise e

            try:
                for linkAttributeKey in propsString:
                    sqlInsertStatement = sqlSyntax.insertLinkAttributeString
                    cursor.execute(sqlInsertStatement, (entityLinkID, linkAttributeKey, str(linkAttributes[linkAttributeKey]), ))
                for linkAttributeKey in propsBoolean:
                    sqlInsertStatement = sqlSyntax.insertLinkAttributeBool
                    cursor.execute(sqlInsertStatement, (entityLinkID, linkAttributeKey, int(linkAttributes[linkAttributeKey]), ))
                for linkAttributeKey in propsDecimal:
                    sqlInsertStatement = sqlSyntax.insertLinkAttributeDec
                    cursor.execute(sqlInsertStatement, (entityLinkID, linkAttributeKey, float(linkAttributes[linkAttributeKey]), ))
                for linkAttributeKey in propsInteger:
                    sqlInsertStatement = sqlSyntax.insertLinkAttributeInt
                    cursor.execute(sqlInsertStatement, (entityLinkID, linkAttributeKey, int(linkAttributes[linkAttributeKey]), ))  
            except:
                raise Exceptions.UndefinedSQLSyntax("Can't execute sqlSqntax.selectAddEntityTest, as sqlSyntax has not been defined")
            
            persistence.commit()    
        except Exceptions.EntityLinkFailureError as e:
            raise e
        except Exception as e:
            cursor.rollback()
            raise e

        #Debug
        '''
        try:
            linkSelectStatementTest = sqlSyntax.selectAllLinks
            cursorTest = persistence.cursor()
            cursorTest.execute(linkSelectStatementTest, ())
            rawCursorResultTest = cursorTest.fetchall() 
            test = "me"
        except Exception as e:
            pass
        '''
        #persistence.commit()
        #/Debug
        #logQ.put( [logType , logLevel.DEBUG , method , "exiting"])
        
  
  
  
        
global entityRepository
global linkRepository
entityRepository = None
linkRepository = LinkRepository()


def setSyntax(syntaxChoice):
    global sqlSyntax
    if syntaxChoice is not None:
        sqlSyntax = syntaxChoice
    else:
        errorMsg = "SQL syntax must a non-none value"
        raise Exceptions.UndefinedSQLSyntax(errorMsg)


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
            return str(uuidAsString)
    except Exception as e:
        return "Traceback = %s" %e  
    
    
    
def filterListDuplicates(listToFilter):
    # Not order preserving
    keys = {}
    for e in listToFilter:
        keys[e] = 1
    return list(keys.keys())