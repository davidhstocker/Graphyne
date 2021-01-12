
import decimal
import threading
import sys
from . import Graph
from . import Scripting
from . import Exceptions


class ArgumentType(object):
    SIMPLE = 0
    ATTRIBUTE = 1
    MULTI_ATTRIBUTE = 2
    
argumentType = ArgumentType()




class OperatorString(object):
    EQUAL = 0
    NOTEQUAL = 1
    LONGER = 2
    SHORTER = 3
    SAMELENGTH = 4
    NOTSAMELENGTH = 5
    STARTSWITH = 6
    ENDSWITH = 7 
    
    
class OperatorNumeric(object):
    EQUAL = 0
    NOTEQUAL = 1
    GREATERTHAN = 2
    LESSTHAN = 3
    EQUALORGREATERTHAN = 4
    EQUALORLESSTHAN = 5
    
    
class OperatorSet(object):
    AND = 0
    OR = 1
    NOT = 2
    
    
class LinkType(object):
    ATOMIC = 0
    SUBATOMIC = 1
    ALIAS = 2 
    

operatorString = OperatorString()
operatorNumeric = OperatorNumeric()
operatorSet = OperatorSet()
linkTypes = LinkType()



#Argument Classes
class SimpleArgument(object):
    '''A very simple class for managing simple arguments of conditions.  Note that it is an abstract class and presumes that
    the implementing class has a uuid attribute '''
    className = "SimpleArgument"
    
    def initArgument(self, argumentPaths):
        self.argumentTag = None
        self.isSimple = True
        self.isAAA = False
        try:
            self.argumentTag = argumentPaths["ArgumentTag"]
        except Exception as e:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            errorMsg = str(fullerror[1])
            message = "WARNING - Unable to attach argument %s to condition %s.  Traceback = %s : %s" %(argumentPaths, argumentPaths["conditionMemeID"], errorID, errorMsg)
            Graph.api.writeError(message)
        
        
    def getArgumentValue(self, entityUUID = None):
        return self.argumentTag


    def getRequiredArgumentList(self):
        return []

    
    def getRequiredAgentPathList(self):
        return []
    
    
    




class AgentAttributeArgument(object):
    '''A simple class for managing agent arguments of conditions '''
    className = "AgentAttributeArgument"
    
    argumentPath = {}
    argumentTag = {}
    
    def initArgument(self, argumentPaths):
        self.isSimple = False
        self.isAAA = True
        self.subjectArgumentPath = argumentPaths["subjectArgumentPath"]
        #try:
            #test the argument path to ensure that it is valid
            #testValue = Graph.api.getEntityPropertyValue(conditionContainerUUID, self.subjectArgumentPath)
        #except Exception as e:
            # The method that tried to create the AAA must handle the exception, so rethrow it
            #errorMsg = "Agent Attribute Argument path %s is invalid.  Traceback = %s" %(self.subjectArgumentPath, e)
            #Graph.api.writeError(errorMsg)
            #raise Exceptions.MalformedArgumentPathError(errorMsg)

        
    def getArgumentValue(self, entityUUID):
        #    Walk through the agent to get the sought after value.
        returnValue = None
        
        try:
            returnValue = Graph.api.getEntityPropertyValue(entityUUID, self.subjectArgumentPath)
        except Exception as e:
            #The method that tried to create the AAA must handle the exception, so rethrow it
            errorMsg = "Can't get value from agent attribute argument %s for agent %s.  Traceback = %s" %(self.subjectArgumentPath, entityUUID, e)
            Graph.api.writeError(errorMsg)
            raise Exceptions.MismatchedArgumentPathError
        
        return returnValue
    
    
    
class MultiAgentAttributeArgument(object):
    '''A simple class for managing agent arguments of conditions '''
    className = "AgentAttributeArgument"
    
    subjectArgumentPath = {}
    
    def initArgument(self, argumentPaths):
        self.isSimple = False
        self.isAAA = True
        self.subjectArgumentPath = argumentPaths["subjectArgumentPath"]
        self.objectArgumentPath = argumentPaths["objectArgumentPath"]        


        
    def getArgumentValues(self, subjectUUID = None, objectUUID = None):
        #    Walk through the agent to get the sought after value.
        returnValue = []
        
        if (subjectUUID is None) or (objectUUID is None):
            errorMsg = "Can't evaluate multi agent condition.  Both subject and object are required"
            if subjectUUID is None:
                errorMsg = "%s.  Neither has been supplied" %(errorMsg)
            elif objectUUID is None:
                errorMsg = "%s.  Subject is %s, but no object has been supplied" %(errorMsg, subjectUUID)
            Graph.api.writeError(errorMsg)
            raise Exceptions.MismatchedArgumentPathError(errorMsg)            
        
        try:
            returnValue1 = Graph.api.getEntityPropertyValue(subjectUUID, self.subjectArgumentPath)
            returnValue.append(returnValue1)
            if returnValue1 is None:
                raise Exceptions.MismatchedArgumentPathError("Nothing at attribute path")
        except Exception as e:
            #The method that tried to create the AAA must handle the exception, so rethrow it
            errorMsg = "Can't get value from subject %s at attribute argument %s.  Traceback = %s" %(subjectUUID, self.subjectArgumentPath, e)
            Graph.api.writeError(errorMsg)
            raise Exceptions.MismatchedArgumentPathError(errorMsg)
        
        try:
            returnValue2 = Graph.api.getEntityPropertyValue(objectUUID, self.objectArgumentPath)
            returnValue.append(returnValue2)
            if returnValue2 is None:
                raise Exceptions.MismatchedArgumentPathError("Nothing at attribute path")
        except Exception as e:
            #The method that tried to create the AAA must handle the exception, so rethrow it
            errorMsg = "Can't get value from object %s at attribute argument %s.  Traceback = %s" %(objectUUID, self.objectArgumentPath, e)
            Graph.api.writeError(errorMsg)
            raise Exceptions.MismatchedArgumentPathError(errorMsg)
        
        return returnValue



    
    

class ConditionSet(threading.Thread):
    className = "ConditionSet"
    ''' A container object for referencing internationalzed descriptors from the catalog.'''
    
    def __init__(self, conditionContainerUUID, path, operator, childConditions):
        self.uuid = conditionContainerUUID
        self.meme = path
        self.operator = operator
        self.childConditions = childConditions
        self.entityLock = threading.RLock()
        
        
        
    def mapFunction(self, childCondition, argumentMap):
        localResult = Graph.api.evaluateEntity(childCondition, argumentMap)
        return localResult
        
       
    def execute(self, entityID, argumentMap):
        ''' 2 params: arg1, passedValue = None '''
        # This is a clumsy way of doing automatic datatype detection on the passed arguent arg1
        # All of the test methods use only two arguments, agent/argumentMap and passedValue
        # We need to be compatable with that as the calling method (which may be remote) does not 
        # strictly know the type of a child condition.
        # if arg1 is a dict, then we regard it as an argument map
        #    otherwise, we assume that it is an agent.
        try:
            resultSet = Graph.api.map(self.mapFunction, self.childConditions, argumentMap['runtimeVariables'])
            
            #Debug
            #childConditionMemeList = {}
            #for childCondition in self.childConditions:
            #    childConditionMeme = Graph.api.getEntityMemeType(childCondition)
            #    localResult = Graph.api.evaluateEntity(childCondition, argumentMap)
            #    childConditionMemeList[childConditionMeme] = localResult
            #Graph.api.writeDebug("argumentMap = %s" %argumentMap)
            #Graph.api.writeDebug("childConditionMemeList = %s" %childConditionMemeList)
            #/debug
            
            returnValue = False
            if self.operator == operatorSet.AND:
                # All must be true to return True
                if False in resultSet:
                    returnValue = False
                else:
                    returnValue = True
                    
            elif self.operator == operatorSet.OR:
                # Return True is any are True
                if True in resultSet:
                    returnValue = True
                    
            else:
                if True in resultSet:
                    returnValue = False
                else:
                    returnValue = True
                    
            return returnValue
        except Exceptions.ScriptError as e:
            errorMsg = "Condition set encountered problem while evaluating child condition %s.  Traceback = %s" %(self.meme, e)
            raise Exceptions.ScriptError(errorMsg)
        except Exceptions.MissingAgentError as agentPathList:
            errMsg = 'Condition set %s required agent attributes: %s' % (self.meme, agentPathList)
            raise Exceptions.MissingAgentError(errMsg)
        except Exceptions.MissingArgumentError as exception:
            errMsg = 'Test of condition set %s is missing required argument %s and can not be processed!' % (self.meme, exception)
            raise Exceptions.MissingArgumentError(errMsg)
        except Exceptions.MissingAgentPathError as exception:
            errMsg = 'test of condition set %s is missing required agent path %s and can not be processed!' % (self.meme, exception)
            raise Exceptions.MissingArgumentError(errMsg)
        #except Exception as e:
        return False




                    
class Condition(threading.Thread):
    ''' An abstract class for defining the three types of conditions, String, Int and Float '''
    className = "Condition"
    entityLock = threading.RLock()

    def initializeCondition(self, conditionContainerUUID, path, operator, valueList = None):
        self.uuid = conditionContainerUUID
        self.meme = path
        self.valueList = valueList
        self.operator = operator

        




class ConditionString(Condition):
    className = "ConditionString"

    def innerTest(self, valueList, passedValue = None):
        ''' return TRUE/FALSE based on the value of the condition  '''
        
        returnValue = False
        try:
            if passedValue is not None:
                # If there was a passed valuelist flagged for this condition, then us that
                try:
                    if ((self.operator == operatorString.EQUAL) and (valueList.__contains__(passedValue))): 
                        returnValue = True
                    elif ((self.operator == operatorString.NOTEQUAL) and not(valueList.__contains__(passedValue))): 
                        returnValue = True
                    else:
                        for valueEntry in valueList:  
                            if ((self.operator == operatorString.LONGER) and (len(valueEntry) < len(passedValue))) or\
                                ((self.operator == operatorString.SHORTER) and (len(valueEntry) > len(passedValue))) or\
                                ((self.operator == operatorString.SAMELENGTH) and ( len(valueEntry) == len(passedValue))) or\
                                ((self.operator == operatorString.NOTSAMELENGTH) and ( len(valueEntry) != len(passedValue))) or\
                                ((self.operator == operatorString.STARTSWITH) and ( passedValue.startswith(valueEntry) is True )) or\
                                ((self.operator == operatorString.ENDSWITH) and ( passedValue.endswith(valueEntry) is True )):
                                returnValue = True
                except Exception as e:
                    errorMsg = 'Call on condition %s has invalid variant and can not be processed for passed argument value %s!  Traceback = %s' % (self.meme, passedValue, e)
                    raise Exceptions.MalformedConditionalError(errorMsg)
            else:
                exception = 'Call on simple numer condition %s made without argument.  Simple conditions require arguments!' % (self.meme)
                raise Exceptions.MissingArgumentError(exception)

        except Exceptions.MalformedConditionalError(exception):
            errorMsg = 'Condition %s has error %s.  defaulting to False' % (exception, self.meme)
            Graph.api.writeError(errorMsg)
        except Exceptions.MissingArgumentError:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            errorMsg = str(fullerror[1])
            errorMsgPart1 = 'Missing argument on call to condition %s!  There needs to be either a stored comparison value set, or one passed from the calling constructor\n' %(self.meme)
            errorMsg = '%sCondition %s.  defaulting to False.  Traceback = %s : %s' % (self.meme, errorMsgPart1, errorID, errorMsg)
            Graph.api.writeError(errorMsg)     
        except Exception as e:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            errorMsg = str(fullerror[1])
            Graph.api.writeError('Condition %s.  defaulting to False %s : %s' % (self.meme, errorID, errorMsg))

        return returnValue



class ConditionStringSimple(ConditionString, SimpleArgument):
    className = "ConditionStringSimple"
    
    def __init__(self, conditionContainerUUID, path, operator, argument, valueList = None):
        self.initializeCondition(conditionContainerUUID, path, operator, valueList)
        self.initArgument(argument)
        
    def execute(self, entityID, argumentMap):
        ''' 2 params: arg1, passedValue = None '''
        
        returnValue = False
        
        try:
            #See the ConditionSet.test method for a full explanation of this trickery. 
            try:
                passedValue = argumentMap['runtimeVariables'][self.argumentTag]
            except:
                errorMsg = 'Condition %s not called with required argument tag %s among parameters %s!  Evaluation Failed!' % (self.meme, self.argumentTag, argumentMap)
                raise Exceptions.MissingArgumentError(errorMsg)         
                   
            returnValue = self.innerTest(self.valueList, passedValue)
            
        except Exceptions.MissingArgumentError as e:
            raise e
        except Exception as e:
            errorMsg = 'argumentMap = %s, passedValue = %s  Traceback = %s' % (argumentMap, passedValue, e)
            Graph.api.writeError('Condition %s has unknown error: defaulting to False.  %s' %(self.meme, errorMsg))
        return returnValue


    
    
class ConditionStringAAA(ConditionString, AgentAttributeArgument):
    className = "ConditionStringAAA"

    def __init__(self, conditionContainerUUID, path, operator, subjectArgumentPath, valueList = None ):
        try:
            self.initializeCondition(conditionContainerUUID, path, operator, valueList)
            self.initArgument(subjectArgumentPath)
        except Exception as e:
            #Debug statement
            unused_catch = e
        
        
    def execute(self, entityID, argumentMap):
        ''' 2 param2: entityID, argumentMap'''
        returnValue = False
        try:
            #See the ConditionSet.test method for a full explanation of this trickery. 
            try:
                argumentValue = self.getArgumentValue(argumentMap['subjectID'])
            except Exception as e:
                errorMsg = "Condition %s not called with required subject ID!  Condition has no entity for comparison and can't proceed!" % (self.meme)
                raise Exceptions.MissingArgumentError(errorMsg) 
            
            returnValue = self.innerTest(self.valueList, argumentValue)
        except Exception as e:
            errMsg = 'Condition %s failed to evaluate and is defaulting to False.  Traceback = %s' % (self.meme, e)
            Graph.api.writeError(errMsg)
        return returnValue
            
            
            
class ConditionStringMultiA(ConditionString, MultiAgentAttributeArgument):
    className = "ConditionStringMultiA"
    
    def __init__(self, conditionContainerUUID, path, operator, argumentPaths):
        self.initializeCondition(conditionContainerUUID, path, operator)
        self.initArgument(argumentPaths)

        
    def execute(self, entityID, argumentMap):
        ''' 2 param2: entityID, argumentMap'''
        returnValue = False
        
        try:
            try:
                argumentValues = self.getArgumentValues(argumentMap['subjectID'], argumentMap['objectID'])
            except Exception as e:
                errorMsg = "Condition %s not called with required subject and object IDs!  Condition has no entity for comparison and can't proceed!  Traceback = %s" % (self.meme, e)
                raise Exceptions.MissingArgumentError(errorMsg) 
            
            returnValue = self.innerTest([argumentValues[0]], argumentValues[1])
        except Exception as e:
            errMsg1 = 'Condition %s defaulting to False.  MismatchedArgumentPathError while processing:' %(self.meme)
            errMsg2 = ' agents = %s and %s,'  % (argumentMap['subjectID'], argumentMap['objectID'])
            errMsg3 = 'paths = %s and %s, Traceback = %s' % (self.subjectArgumentPath, self.objectArgumentPath, e)
            errMsg = '%s %s %s' %(errMsg1, errMsg2, errMsg3)
            Graph.api.writeError(errMsg)
        return returnValue 




class ConditionNumeric(Condition):
    className = "ConditionNumeric"
    
    def innerTest(self, valueList, passedValue = None):
        ''' return TRUE/FALSE based on the value of the condition  '''
        
        returnValue = False
 
        try:
            if passedValue is not None:
                try:
                    for value in valueList:
                        dValue = decimal.Decimal(value)
                        dArgument = decimal.Decimal(passedValue)
                        if ((self.operator == operatorNumeric.EQUAL) and (dArgument == dValue)) or\
                           ((self.operator == operatorNumeric.NOTEQUAL) and (dArgument != dValue)) or\
                           ((self.operator == operatorNumeric.GREATERTHAN) and (dArgument > dValue)) or\
                           ((self.operator == operatorNumeric.LESSTHAN) and (dArgument < dValue)) or\
                           ((self.operator == operatorNumeric.EQUALORGREATERTHAN) and (dArgument >= dValue)) or\
                           ((self.operator == operatorNumeric.EQUALORLESSTHAN) and (dArgument <= dValue)):
                            returnValue = True
                except Exception as e:
                    raise e
            else:
                exception = 'Call on simple numer condition %s made without argument.  Simple conditions require arguments!' % (self.meme)
                raise Exceptions.MissingArgumentError(exception)
        except Exceptions.MalformedConditionalError as exception:
            Graph.api.writeError('Condition %s defaulting to False. Traceback = %s' % (self.meme, exception))
        except Exceptions.MissingArgumentError:
            errorMsgPart1 = 'Missing argument on call to condition %s!  There needs to be either a stored comparison value set, or one passed from the calling constructor' % self.meme
            errorMsg = 'Condition %s.  defaulting to False.  Traceback = %s' % (self.meme, errorMsgPart1)
            Graph.api.writeError(errorMsg)
        except Exception as e:
            Graph.api.writeError('Condition %s defaulting to False. Traceback = %s' % (self.meme, e))
        return returnValue




class ConditionNumericSimple(ConditionNumeric, SimpleArgument):
    #newCondition = ConditionStringAAA(conditionContainerUUID, path, operator, argumentPaths, values)
    className = "ConditionNumericSimple"
    
    def __init__(self, conditionContainerUUID, path, operator, argumentPaths, valueList = None ):
        self.initializeCondition(conditionContainerUUID, path, operator, valueList)
        self.initArgument(argumentPaths)
        
    def getArgumentValue(self, argumentMap):
        """ self.valueList being called a 'value list' instead of a function list is an artifact of history. 
            the shared inheritance with ConsitionStringSimple of SimpleArgument dates back to early condition
            development, before the Numeric module and it's instantiation by proxy was implemented.  
            When the shift was made, it was easiest to simply override SimpleArgument.getArgumentValue().
        """
        returnVals = []
        for valueEntry in self.valueList:
            try:
                returnVal = Graph.api.evaluateEntity(valueEntry, argumentMap)
                returnVals.extend(returnVal)
            except Exception as e:
                memeType = None
                try:
                    memeType = Graph.api.getEntityMemeType(valueEntry)
                    errorMsg = "Error trying to retrieve argument value from %s meme %s.  Traceback = %s" %(memeType, valueEntry, e)
                    Graph.api.writeError(errorMsg)
                except Exception as e2:
                    errorMsg = "Error trying to retrieve argument value from meme %s of unknown type.  Traceback Chain = %s, %s" %(valueEntry, e2, e)
                    Graph.api.writeError(errorMsg)
        return returnVals

        
    def execute(self, entityID, argumentMap):
        ''' 2 params: arg1, passedValue = None '''

        returnValue = False
        passedValue = None
        try:
            #See the ConditionSet.test method for a full explanation of this trickery. 
            try:
                passedValue = argumentMap['runtimeVariables'][self.argumentTag]
            except:
                errorMsgPart1 = 'Condition %s not called with required argument tag %s among parameters %s!  Evaluation Failed!' % (self.meme, self.argumentTag, argumentMap)
                errorMsg = 'Condition %s has error. %s.  defaulting to False' % (errorMsgPart1, self.meme)
                Graph.api.writeError(errorMsg) 
                raise Exceptions.MissingArgumentError(errorMsg)    
            valueList = self.getArgumentValue(argumentMap)            
            returnValue = self.innerTest(valueList, passedValue)
            
        except Exceptions.MissingArgumentError as e:
            raise e
        except Exception as e:
            errorMsgPart1 = 'argumentMap = %s, passedValue = %s  Traceback = %s' % (argumentMap, passedValue, e)
            errorMsg = 'Condition %s has unknown error: defaulting to False.  %s' %(self.meme, errorMsgPart1)
            Graph.api.writeError(errorMsg)
        return returnValue


    
    
class ConditionNumericAAA(ConditionNumeric, AgentAttributeArgument):
    className = "ConditionNumericAAA"
    
    def __init__(self, conditionContainerUUID, path, operator, argument, valueList = None ):
        self.initializeCondition(conditionContainerUUID, path, operator, valueList)
        self.initArgument(argument)

        
    def execute(self, entityID, argumentMap):
        ''' 2 param2: entityID, argumentMap'''
        returnValue = False
        
        argumentValue = None
        try:
            #See the ConditionSet.test method for a full explanation of this trickery.             
            try:
                argumentValue = self.getArgumentValue(argumentMap['subjectID'])
            except Exception as e:
                fullerror = sys.exc_info()
                errorID = str(fullerror[0])
                errorMsg = str(fullerror[1])
                errorMsg = "Condition %s not called with required subject ID!  Condition has no entity for comparison and can't proceed!  Traceback = %s : %s" % (self.meme, errorID, errorMsg)
                raise Exceptions.MissingArgumentError(errorMsg)      
                #for debugging
                argumentValue = self.getArgumentValue(argumentMap['subjectID'])       
            
            returnValue = self.innerTest(self.valueList, argumentValue)
        except Exception as e:
            fullerror = sys.exc_info()
            errorID = str(fullerror[0])
            errorMsg = str(fullerror[1])
            errMsg = 'Condition %s defaulting to False.  MismatchedArgumentPathError while processing:, params = %s  Traceback = %s : %s' % (self.meme, argumentMap, errorID, errorMsg)
            Graph.api.writeError(errMsg)
        return returnValue         



class ConditionNumericMultiA(ConditionNumeric, MultiAgentAttributeArgument):
    className = "ConditionNumericMultiA"
    
    def __init__(self, conditionContainerUUID, path, operator, argumentPaths):
        self.initializeCondition(conditionContainerUUID, path, operator)
        self.initArgument(argumentPaths)

        
    def execute(self, entityID, argumentMap):
        ''' 2 param2: entityID, argumentMap'''
        returnValue = False
        
        argumentValues = None
        try:
            try:
                argumentValues = self.getArgumentValues(argumentMap['subjectID'], argumentMap['objectID'])
            except Exception as e:
                errorMsg = "Condition %s not called with required subject and object IDs!  Condition has no entity for comparison and can't proceed!  Traceback = %s" % (self.meme, e)
                raise Exceptions.MissingArgumentError(errorMsg) 
            
            returnValue = self.innerTest([argumentValues[0]], argumentValues[1])
        except Exception as e:
            errMsg1 = 'Condition %s defaulting to False.  MismatchedArgumentPathError while processing:' %(self.meme)
            errMsg2 = ' agents = %s and %s,'  % (argumentMap['subjectID'], argumentMap['objectID'])
            errMsg3 = 'paths = %s and %s, Traceback = %s' % (self.subjectArgumentPath, self.objectArgumentPath, e)
            errMsg = '%s %s %s' %(errMsg1, errMsg2, errMsg3)
            Graph.api.writeError(errMsg)
        return returnValue 
            
            

class ConditionScript(object):
    """
        
    """
    className = "ConditionScript"

    def __init__(self, conditionContainerUUID, path, childEntity):
        self.uuid = conditionContainerUUID
        self.meme = path
        self.script = childEntity.execScript
        self.entityLock = threading.RLock()

    
    def execute(self, entityID, argumentMap):
        try:
            returnValue = self.script(entityID, argumentMap) 
        except Exceptions.ScriptError as e:
            raise e           
        except Exception as e:
            errorMsg = "Encountered error when executing script attached to script condition %s.  Traceback = %s" %(self.meme, e)
            Graph.api.writeError(errorMsg)
        return returnValue           
            



    




#globals
#conditionCatalog = conditionCatalog()
moduleName = 'RMLCondition'






            
#Definitions 
def getArgumentTypeFromConditionEntity(conditionContainer):
    ''' Determ,ine if the condition's argument is of one of these two types:
        Graphyne.Condition.SimpleArgument
        Graphyne.Condition.AgentAttributeArgument'''
    #SimpleArgument
    #AgentAttributeArgument
    argument = None
    memberUUIDs = Graph.api.getLinkCounterpartsByMetaMemeType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.SimpleArgument")
    for unused_memID in memberUUIDs:
        argument = argumentType.SIMPLE

    memberUUIDs = Graph.api.getLinkCounterpartsByMetaMemeType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.AgentAttributeArgument")
    for unused_memID in memberUUIDs:
        argument = argumentType.ATTRIBUTE
        
    memberUUIDs = Graph.api.getLinkCounterpartsByMetaMemeType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.MultiAgentAttributeArgument")
    for unused_memID in memberUUIDs:
        argument = argumentType.MULTI_ATTRIBUTE
        
    if argument is None:
        memeType = Graph.api.getEntityMemeType(conditionContainer)
        statement = "CONTENT-WARNING: Unable to get argument from condition %s.  Please check the structure of the meme." %memeType
        memeStructure = Graph.api.getClusterMembers(conditionContainer, 1, False)
        msSatement= "Structure of problem meme = %s" %memeStructure
        Graph.api.writeError(statement)
        Graph.api.writeError(msSatement)

    return argument



def getArgumentsFromConditionEntity(conditionContainer):
    ''' pull the value out of 
        Graphyne.Condition.SimpleArgument:argument
        Graphyne.Condition.AgentAttributeArgument:argument
        
        Note that the value of argument ID will have a different syntax for the two options.
        Simple arguments will have just a key name for lookup in an argument map (dict)
        AA Arguments will have a full blown Member Path
        '''
    conditionMemePath = Graph.api.getEntityMemeType(conditionContainer)
    argumentInfo = {"conditionMemeID" : conditionMemePath}
    memberUUIDs = Graph.api.getLinkCounterpartsByMetaMemeType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.SimpleArgument")
    if len(memberUUIDs) < 1:
        memberUUIDs = Graph.api.getLinkCounterpartsByMetaMemeType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.AgentAttributeArgument")
    if len(memberUUIDs) < 1:
        memberUUIDs = Graph.api.getLinkCounterpartsByMetaMemeType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.MultiAgentAttributeArgument")


    for argumentEntity in memberUUIDs:
        try: 
            argumentInfo["ArgumentTag"] = Graph.api.getEntityPropertyValue(argumentEntity, "ArgumentTag")
        except: pass
        try:
            argumentInfo["subjectArgumentPath"] = Graph.api.getEntityPropertyValue(argumentEntity, "SubjectArgumentPath")
        except: pass
        try: 
            argumentInfo["subjectArgumentPath"] = Graph.api.getEntityPropertyValue(argumentEntity, "SubjectArgumentPath")
            argumentInfo["objectArgumentPath"] = Graph.api.getEntityPropertyValue(argumentEntity, "ObjectArgumentPath")
        except: pass
        
    if len(list(argumentInfo.values())) < 1:
        memeType = Graph.api.getEntityMemeType(conditionContainer)
        statement = "CONTENT-WARNING: Unable to get argument from condition %s.  Please check the structure of the meme." %memeType
        memeStructure = Graph.api.getClusterMembers(conditionContainer, 1, False)
        msSatement= "Structure of problem meme = %s" %memeStructure
        Graph.api.writeError(statement)
        Graph.api.writeError(msSatement)
        raise Exceptions.MalformedConditionalError(msSatement)

    return argumentInfo



def getOperatorFromConditionEntity(conditionContainer):
    ''' pull the the value of the operator property out of ConditionXXX'''
    operator = None
    
    try:
        memberUUIDs = Graph.api.getLinkCounterpartsByType(conditionContainer, "Graphyne.Condition.ConditionSet", 1)
        for entityWithValueUUID in memberUUIDs:
            operatorStr = Graph.api.getEntityPropertyValue(entityWithValueUUID, "SetOperator")
            if operatorStr.upper() == 'AND':
                operator = operatorSet.AND
            elif operatorStr.upper() == 'OR':
                operator = operatorSet.OR
            elif operatorStr.upper() == 'NOT':
                operator = operatorSet.NOT
            else:
                errorMsg = "Graphyne.Condition.ConditionSet meme has invalid SetOperator %s" %operatorStr
                raise Exceptions.MalformedConditionalError(errorMsg)
        if operator is not None: return operator
        
        memberUUIDs = Graph.api.getLinkCounterpartsByType(conditionContainer, "Graphyne.Condition.ConditionString", 1)
        for entityWithValueUUID in memberUUIDs:
            operatorStr = Graph.api.getEntityPropertyValue(entityWithValueUUID, "StringOperator")
            if operatorStr.upper() == 'EQUAL':
                operator = operatorString.EQUAL
            elif operatorStr.upper() == 'NOTEQUAL':
                operator = operatorString.NOTEQUAL
            elif operatorStr.upper() == 'LONGER':
                operator = operatorString.LONGER
            elif operatorStr.upper() == 'SHORTER':
                operator = operatorString.SHORTER
            elif operatorStr.upper() == 'SAMELENGTH':
                operator = operatorString.SAMELENGTH
            elif operatorStr.upper() == 'NOTSAMELENGTH':
                operator = operatorString.NOTSAMELENGTH
            elif operatorStr.upper() == 'STARTSWITH':
                operator = operatorString.STARTSWITH
            elif operatorStr.upper() == 'ENDSWITH':
                operator = operatorString.ENDSWITH
            else:
                errorMsg = "Graphyne.Condition.ConditionString meme has invalid StringOperator %s" %operatorStr
                raise Exceptions.MalformedConditionalError(errorMsg)
        if operator is not None: return operator
        
        memberUUIDs = Graph.api.getLinkCounterpartsByType(conditionContainer, "Graphyne.Condition.ConditionNumeric", 1)
        for entityWithValueUUID in memberUUIDs:
            operatorStr = Graph.api.getEntityPropertyValue(entityWithValueUUID, "NumericOperator")
            if operatorStr.upper() == 'EQUAL':
                operator = operatorNumeric.EQUAL
            elif operatorStr.upper() == 'NOTEQUAL':
                operator = operatorNumeric.NOTEQUAL
            elif operatorStr.upper() == 'GREATERTHAN':
                operator = operatorNumeric.GREATERTHAN
            elif operatorStr.upper() == 'LESSTHAN':
                operator = operatorNumeric.LESSTHAN
            elif operatorStr.upper() == 'EQUALORGREATERTHAN':
                operator = operatorNumeric.EQUALORGREATERTHAN
            elif operatorStr.upper() == 'EQUALORLESSTHAN':
                operator = operatorNumeric.EQUALORLESSTHAN
            else:
                errorMsg = "Graphyne.Condition.ConditionNumeric meme has invalid NumericOperator %s" %operatorStr
                raise Exceptions.MalformedConditionalError(errorMsg)

    except Exceptions.MalformedConditionalError as e:
        Graph.api.writeError(e)
        raise e
    except Exception as e:
        errorMsg = "Problem encountered when determing condition operator.  Traceback = %s" %e
        Graph.api.writeError(errorMsg)
        raise Exceptions.MalformedConditionalError(errorMsg) 
        
    if operator is None:
        memeType = Graph.api.getEntityMemeType(conditionContainer)
        statement = "CONTENT-WARNING: Unable to get operator from condition %s.  Please check the structure of the meme." %memeType
        memeStructure = Graph.api.getClusterMembers(conditionContainer, 1, False)
        msSatement= "Structure of problem meme = %s" %memeStructure
        Graph.api.writeError(statement)
        Graph.api.writeError(msSatement)

    return operator



def getTestValuesFromConditionEntity(conditionContainer):
    ''' pull the list of values out of 
        ConditionXXX.ValueString:value
        ConditionXXX.ValueNumeric:value'''
    values = []
    memberUUIDs = []
    
    try:
        memberUUIDs = []
        memberUUIDs = Graph.api.getLinkCounterpartsByType(conditionContainer, "**::Graphyne.Condition.ValueString")
        if len(memberUUIDs) < 1:
            memberUUIDs = Graph.api.getLinkCounterpartsByMetaMemeType(conditionContainer, "**::Graphyne.Numeric.Formula::Graphyne.Numeric.ValueNumeric")
                    
        for entityWithValueUUID in memberUUIDs:
            entityValue = Graph.api.getEntityPropertyValue(entityWithValueUUID, "Value")
            values.append(entityValue)
    except Exception as e:
        unused = e #For debugging
        
    if len(values) == 0:
        memeType = Graph.api.getEntityMemeType(conditionContainer)
        statement = "CONTENT-WARNING: Unable to get test values from condition %s.  Please check the structure of the meme." %memeType
        memeStructure = Graph.api.getClusterMembers(conditionContainer, 0, False)
        msSatement= "Structure of problem meme = %s" %memeStructure
        Graph.api.writeError(statement)
        Graph.api.writeError(msSatement)
        
    return values
    
       

    
def usage():
    print(__doc__)

    
def main():
    pass
    
if __name__ == "__main__":
    main()

    
    
if __name__ == "__main__":
    pass