import threading
import decimal
import random
from . import Condition
from . import Graph
from . import Scripting
from . import Exceptions


class ArgumentType(object):
    ArgumentMin = "Memetic.Random.ArgumentMin"
    ArgumentMax = "Memetic.Random.ArgumentMax"
    ArgumentMeanAngle = "Memetic.Random.ArgumentMeanAngle"
    ArgumentConc = "Memetic.Random.ArgumentConc"
    ArgumentShape = "Memetic.Random.ArgumentShape"
    ArgumentScale = "Memetic.Random.ArgumentScale"
    ArgumentMean = "Memetic.Random.ArgumentMean"
    ArgumentStdD = "Memetic.Random.ArgumentStdD"
    
    

class ArgumentDetailType(object):
    ValueMin = "Memetic.Random.ValueMin"
    ValueStandardDeviation = "Memetic.Random.ValueStandardDeviation"    
    ValueMean = "Memetic.Random.ValueMean"
    ValueScale = "Memetic.Random.ValueScale"
    ValueShape = "Memetic.Random.ValueShape"
    ValueConc = "Memetic.Random.ValueConc"
    ValueMeanAngle = "Memetic.Random.ValueMeanAngle"
    ValueMax = "Memetic.Random.ValueMax"                    
    AAAMin = "Memetic.Random.AAAMin"
    AAAStandardDeviation = "Memetic.Random.AAAStandardDeviation"    
    AAAMean = "Memetic.Random.AAAMean"
    AAAScale = "Memetic.Random.AAAScale"
    AAAShape = "Memetic.Random.AAAShape"
    AAAConc = "Memetic.Random.AAAConc"
    AAAMeanAngle = "Memetic.Random.AAAMeanAngle"
    AAAMax = "Memetic.Random.AAAMax"                    
    SAMin = "Memetic.Random.SAMin"
    SAStandardDeviation = "Memetic.Random.SAStandardDeviation"
    SAMean = "Memetic.Random.SAMean"
    SAScale = "Memetic.Random.SAScale"
    SAShape = "Memetic.Random.SAShape"
    SAConc = "Memetic.Random.SAConc"
    SAMeanAngle = "Memetic.Random.SAMeanAngle"
    SAMax = "Memetic.Random.SAMax" 
    


class RandomType(object):
    Linear = "Memetic.Random.Linear"
    LinearInteger = "Memetic.Random.LinearInteger"
    VonMises = "Memetic.Random.VonMises"
    Weibull = "Memetic.Random.Weibull"
    Pareto = "Memetic.Random.Pareto"
    Gamma = "Memetic.Random.Gamma"
    Beta = "Memetic.Random.Beta"
    Exponential = "Memetic.Random.Exponential"
    Gaussian = "Memetic.Random.Gaussian"
    LogNormal = "Memetic.Random.LogNormal"
        
        
        
argumentType = ArgumentType()
argumentDetailType = ArgumentDetailType()
randomType = RandomType()
        



#Argument Classes
class SimpleArgument(object):
    def __init__(self, valueEntityUUID):
        self.tag = Graph.api.getEntityPropertyValue(valueEntityUUID, "ArgumentTag")
        
    def getArgumentValue(self, argumentParams):
        returnValue = argumentParams[self.tag]
        returnValue


        

class AgentAttributeArgument(Condition.AgentAttributeArgument):
    def __init__(self, argumentPaths):
        self.initArgument(argumentPaths)




class ValueArgument(object):
    """ a class for holding fixed value arguments """
    className = "ValueArgument"
    
    def __init__(self, valueEntityUUID):
        entityValue = Graph.api.getEntityPropertyValue(valueEntityUUID, "value")
        self.value = decimal.Decimal(entityValue)
        
    def getArgumentValue(self):
        return self.value
    
    
    
        
class ValueNumeric(Scripting.StateEventScript):
    className = "ValueNumeric"

    def execute(self, entityUUID, unusedParams):
        entityValue = Graph.api.getEntityPropertyValue(entityUUID, "Value")
        return [entityValue]
    
    
class RandomLinear(threading.Thread):
    """ An abstract class for defining the twp types of linear random generators, static and AA """
    className = "RandomLinear"
    entityLock = threading.RLock()
    
    def __init__(self, randomElements):
        try:
            pass
            minEntity = None
            maxEntity = None
            for randomElement in randomElements:
                if randomElement["RType"] == argumentDetailType.ValueMin:
                    minEntity = randomElement["RID"]
                elif randomElement["RType"] == argumentDetailType.ValueMax:
                    maxEntity = randomElement["RID"]
                else:
                    pass #raise an exception
            self.minVal = decimal.Decimal(minVal)
            self.maxVal = decimal.Decimal(maxVal)
        except Exception as e:
            raise Exceptions.GeneratorError(e)

    def execute(self, params):
        return random.uniform(self.minVal, self.maxVal)
    
    

class RandomLinearFlex(threading.Thread, AgentAttributeArgument):
    className = "RandomLinearFlex"
    entityLock = threading.RLock()

    def __init__(self, functionContainerUUID, path, operator, subjectArgumentPath, valueList = None ):
        try:
            self.initializeCondition(functionContainerUUID, path, operator, valueList)
            self.initArgument(subjectArgumentPath)
        except Exception as e:
            #Debug statement
            unused_catch = e
        
        
    def execute(self, params):
        """ 2 param2: entityID, argumentMap"""
        returnValue = False
        argumentMap = None
        argumentValue = None
        try:
            #See the ConditionSet.test method for a full explanation of this trickery. 
            if type({}) == type(params[1]): 
                argumentMap = params[1]
            else:
                errorMsg = 'Condition %s not called with required parameter format [uuid, {}]!  Parameters were %s' % (self.meme, params)
                raise Exceptions.MissingArgumentError(errorMsg)
           
            try:
                argumentValue = self.getArgumentValue(argumentMap['subjectID'])
            except:
                errorMsg = "Condition %s not called with required subject ID!  Condition has no entity for comparison and can't proceed!" % (self.meme)
                raise Exceptions.MissingArgumentError(errorMsg) 
            
            returnValue = self.innerTest(self.valueList, argumentValue)
        except Exception as e:
            errMsg = 'Condition %s failed to evaluate and is defaulting to False.  Traceback = %s' % (self.meme, e)
            Graph.api.writeError(errMsg)
        return returnValue
            
            
class RandomBeta(threading.Thread):
    className = "RandomBeta"
    entityLock = threading.RLock()
    

class RandomGamma(threading.Thread):
    className = "RandomGamma"
    entityLock = threading.RLock()
    

class RandomLinearInteger(threading.Thread):
    className = "RandomLinearInteger"
    entityLock = threading.RLock()
    

class RandomVonMises(threading.Thread):
    className = "RandomVonMises"
    entityLock = threading.RLock()
    

class RandomWeibull(threading.Thread):
    className = "RandomWeibull"
    entityLock = threading.RLock()
    

class RandomPareto(threading.Thread):
    className = "RandomPareto"
    entityLock = threading.RLock()
    

class RandomExponential(threading.Thread):
    className = "RandomExponential"
    entityLock = threading.RLock()


class RandomGaussian(threading.Thread):
    className = "RandomGaussian"
    entityLock = threading.RLock()


class RandomLogNormal(threading.Thread):
    className = "RandomLogNormal"
    entityLock = threading.RLock()



#Numeric Classes
class InitValueNumeric(Scripting.StateEventScript):
        
    def execute(self, valueNumericEntityUUID, unusedParams):

        """
        An instantiation by proxy class.  See the documentation of InitRandom of Graphyne.Condition.InitCondition for an
        explanation behind instantiation by proxy classes.

        This method is the state event script executed on creation of the Function's child, ValueNumeric.  Since this child
            entity links one and only one Function's, it builds the relevant callable object and then installs that as the
            parent Function's executor.  

        valueNumericEntityUUID is the uuid of the child entity
        functionContainerUUID is the uuid of the parent Function
        """        
        path = None

        # Determine the parent condition UUID (randomContainerUUID)
        valueNumericEntity = Graph.api.getEntity(valueNumericEntityUUID)
        
        try:
            functionContainerUUID = None
            propertyValue = Graph.api.getEntityPropertyValue(valueNumericEntityUUID, "Value")
            functionContainerUUIDSet = Graph.api.getLinkCounterpartsByMetaMemeType(valueNumericEntityUUID, "Graphyne.Numeric.Formula")
            for functionContainerUUIDSetEntry in functionContainerUUIDSet:
                functionContainerUUID = functionContainerUUIDSetEntry
            if functionContainerUUID is None:
                warningMsg = "VlaueNumeric Meme %s has no parent Graphyne.Numeric.Formula." %valueNumericEntity.memePath.fullTemplatePath
                Graph.api.writeError(warningMsg)
            else:
                newValueNumeric = ValueNumeric()
                Graph.api.installPythonExecutor(functionContainerUUID, newValueNumeric)
                Graph.api.setEntityPropertyValue(functionContainerUUID, "Value", propertyValue)
                uuidAsStr = str(functionContainerUUID)
                logStatement = "Added executor object to %s Function %s" %(path, uuidAsStr)
                Graph.api.writeLog(logStatement)
        except Exception as e:
            #debugger aid
            functionContainerUUIDSet = Graph.api.getEntityCounterparts(valueNumericEntityUUID)
            unusedDebug = e




class InitRandom(object):

    def __init__(self, dtParams = None, rtParams = None):
        self.dtParams = dtParams
        self.rtParams = rtParams   
        
    def execute(self, randomEntityUUID):

        """
        On first sight, this method engages in a bit of voodoo.  When Memetic entities In Memetic are instantiated, 
            only directly linked StateEventScript entities are installed on the entity.  This is to prevent distantly 
            linked state event scripts  with n degrees of separation from spamming themselves everywhere.  The downside
            is that in the case of RandomNumber (and formulas in general), we are using a switch meme to act as a proxy 
            that gives a single point of entry.  Because the RandomNumber is a switch, we can't actually directly link 
            StateEventScript, so it is installed at one degree of separation from the perspective of the RandomNumber.
            
        (incidentally, this technique was pioneered on conditions and is known as 'instantiation by proxy')

        This method is the state event script executed on creation of the Function's grandchild, RandomNumber's child entity; 
            and of Distribution's extenders..  Since this child entity links one and only one RandomNumber, which in turn is 
            linked to only one Function, it builds the relevant callable object and then installs that as the grandparent
            Finction's executor.  

        randomEntityUUID is the uuid of the grandchild/child entity
        functionContainerUUID is the uuid of the grandparent Function
        """        
        path = None

        # Determine the parent condition UUID (randomContainerUUID)
        randomEntity = Graph.api.getEntity(randomEntityUUID)
        randomEntityType = Graph.api.getEntityMetaMemeType(randomEntityUUID)
        
        #todo 
        randomContainerUUID = None
        randomContainerUUIDSet = Graph.api.getLinkCounterpartsByMetaMemeType(randomEntityUUID, "Graphyne.Numeric.RandomNumber")
        for randomContainerUUIDSetEntry in randomContainerUUIDSet:
            randomContainerUUID = randomContainerUUIDSetEntry
        if randomContainerUUID is None:
            warningMsg = "Distribution Meme %s has no parent Graphyne.Numeric.RandomNumber." %randomEntity.memePath.fullTemplatePath
            Graph.api.writeError(warningMsg)
        else:            
            functionContainerUUID = None
            functionContainerUUIDSet = Graph.api.getLinkCounterpartsByMetaMemeType(functionContainerUUID, "Graphyne.Numeric.Formula")
            for functionContainerUUIDSetEntry in functionContainerUUIDSet:
                functionContainerUUID = functionContainerUUIDSetEntry
            
            if functionContainerUUID is None:
                warningMsg = "Distribution Meme %s has no grandparentparent Graphyne.Numeric.Formula." %randomEntity.memePath.fullTemplatePath
                Graph.api.writeError(warningMsg)
            else:        
                try:
                    randomElements = [] #list containing one or more dicts
                    
                    argumentEntry = self.getRandomElement(randomEntityUUID, argumentType.ArgumentMin, argumentDetailType.ValueMin, argumentDetailType.AAAMin, argumentDetailType.SAMin)
                    if len(argumentEntry) > 0: randomElements.append(argumentEntry)
                    
                    argumentEntry = self.getRandomElement(randomEntityUUID, argumentType.ArgumentMax, argumentDetailType.ValueMax, argumentDetailType.AAAMax, argumentDetailType.SAMax)
                    if len(argumentEntry) > 0: randomElements.append(argumentEntry)
                    
                    argumentEntry = self.getRandomElement(randomEntityUUID, argumentType.ArgumentConc, argumentDetailType.ValueConc, argumentDetailType.AAAConc, argumentDetailType.SAConc)
                    if len(argumentEntry) > 0: randomElements.append(argumentEntry)
                    
                    argumentEntry = self.getRandomElement(randomEntityUUID, argumentType.ArgumentMean, argumentDetailType.ValueMean, argumentDetailType.AAAMean, argumentDetailType.SAMean)
                    if len(argumentEntry) > 0: randomElements.append(argumentEntry)
                    
                    argumentEntry = self.getRandomElement(randomEntityUUID, argumentType.ArgumentMeanAngle, argumentDetailType.ValueMeanAngle, argumentDetailType.AAAMeanAngle, argumentDetailType.SAMeanAngle)
                    if len(argumentEntry) > 0: randomElements.append(argumentEntry)
                    
                    argumentEntry = self.getRandomElement(randomEntityUUID, argumentType.ArgumentScale, argumentDetailType.ValueScale, argumentDetailType.AAAScale, argumentDetailType.SAScale)
                    if len(argumentEntry) > 0: randomElements.append(argumentEntry)
                    
                    argumentEntry = self.getRandomElement(randomEntityUUID, argumentType.ArgumentShape, argumentDetailType.ValueShape, argumentDetailType.AAAShape, argumentDetailType.SAShape)
                    if len(argumentEntry) > 0: randomElements.append(argumentEntry)
                    
                    argumentEntry = self.getRandomElement(randomEntityUUID, argumentType.ArgumentStdD, argumentDetailType.ValueStandardDeviation, argumentDetailType.AAAStandardDeviation, argumentDetailType.SAStandardDeviation)
                    if len(argumentEntry) > 0: randomElements.append(argumentEntry)
                    
                    if randomEntityType == randomType.Beta:
                        newRandom = RandomBeta(randomElements)
                    elif randomEntityType == randomType.Gamma:
                        newRandom = RandomGamma(randomElements)
                    elif randomEntityType == randomType.Linear:
                        newRandom = RandomLinear(randomElements)
                    elif randomEntityType == randomType.LinearInteger:
                        newRandom = RandomLinearInteger(randomElements)
                    elif randomEntityType == randomType.VonMises:
                        newRandom = RandomVonMises(randomElements)
                    elif randomEntityType == randomType.Weibull:
                        newRandom = RandomWeibull(randomElements)
                    elif randomEntityType == randomType.Pareto:
                        newRandom = RandomPareto(randomElements)
                    elif randomEntityType == randomType.Exponential:
                        newRandom = RandomExponential(randomElements)
                    elif randomEntityType == randomType.Gaussian:
                        newRandom = RandomGaussian(randomElements)
                    elif randomEntityType == randomType.LogNormal:
                        newRandom = RandomLogNormal(randomElements)
                    else:
                        pass #raise an exception
                    
                except:
                    pass
                Graph.api.installPythonExecutor(functionContainerUUID, newRandom)
                
                uuidAsStr = str(functionContainerUUID)
                logStatement = "Added executor object to %s Function %s" %(path, uuidAsStr)
                Graph.api.writeLog(logStatement)
            
            
    def getRandomElement(self, randomEntityUUID, argType, val, aaa, sa):
        """ 
            given the randomEntityUUID and a constellation of possible random entities, construct an argument dict
            getRandomElement(self, randomEntityUUID, 
                                argumentType.ArgumentMin, 
                                argumentDetailType.ValueMin, 
                                argumentDetailType.AAAMin, 
                                argumentDetailType.SAMin)
        """
        randomElement = {}
        randomRootUUIDs = Graph.api.getLinkCounterpartsByType(randomEntityUUID, argType)
        if len(randomRootUUIDs) > 0:
            randomUUIDs = []
            for randomRootUUID in randomRootUUIDs:
                randomElement = {"BaseType" : argType, "BaseID" : randomRootUUID}
                randomUUIDs = Graph.api.getLinkCounterpartsByType(randomRootUUID, val)
                if len(randomUUIDs) > 0:
                    randomElement["RType"] = val
                    for randomUUID in randomUUIDs:
                        randomElement["RID"] = randomUUID
                else:
                    randomUUIDs = Graph.api.getLinkCounterpartsByType(randomRootUUID, aaa)
                    if len(randomUUIDs) > 0:
                        randomElement["RType"] = aaa
                        for randomUUID in randomUUIDs:
                            randomElement["RID"] = randomUUID      
                    else:
                        randomUUIDs = Graph.api.getLinkCounterpartsByType(randomRootUUID, sa)
                        if len(randomUUIDs) > 0:
                            randomElement["RType"] = sa
                            for randomUUID in randomUUIDs:
                                randomElement["RID"] = randomUUID                    
        return randomElement




#globals
#conditionCatalog = conditionCatalog()
moduleName = 'RMLCondition'



            
#Definitions 
def getArgumentTypeFromrandomEntity(conditionContainer):
    """ Determ,ine if the condition's argument is of one of these two types:
        Memetic.SimpleArgument
        Memetic.AgentAttributeArgument"""
    #SimpleArgument
    #AgentAttributeArgument
    argument = None
    randomRootUUIDs = Graph.api.getLinkCounterpartsByType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.SimpleArgument")
    for unused_memID in randomRootUUIDs:
        argument = argumentType.SIMPLE

    randomRootUUIDs = Graph.api.getLinkCounterpartsByType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.AgentAttributeArgument")
    for unused_memID in randomRootUUIDs:
        argument = argumentType.ATTRIBUTE
        
    randomRootUUIDs = Graph.api.getLinkCounterpartsByType(conditionContainer, "*::Graphyne.Condition.Argument::Graphyne.Condition.MultiAgentAttributeArgument")
    for unused_memID in randomRootUUIDs:
        argument = argumentType.MULTI_ATTRIBUTE
        
    if argument is None:
        memeType = Graph.api.getEntityMemeType(conditionContainer)
        statement = "CONTENT-WARNING: Unable to get argument from condition %s.  Please check the structure of the meme." %memeType
        memeStructure = Graph.api.getClusterMembers(conditionContainer, 1, False)
        msSatement= "Structure of problem meme = %s" %memeStructure
        Graph.api.writeError(statement)
        Graph.api.writeError(msSatement)

    return argument





    
    
    
def usage():
    print(__doc__)

    
def main():
    pass
    
if __name__ == "__main__":
    main()

    
    
if __name__ == "__main__":
    pass