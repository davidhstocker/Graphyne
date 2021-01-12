"""
   Exceptions.py: Graphyne specific Exceptions
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'


#classes
class TagError(ValueError):
    pass

class TraverseFilterError(ValueError):
    pass

class EmptyFileError(ValueError):
    '''File contains no data  '''
    pass


class UndefinedPersistenceError(ValueError):
    ''' No persistence has been defined '''
    pass

class PersistenceQueryError(ValueError):
    ''' Invalid Relational Query to persistence '''
    pass

class EnhancementError(ValueError):
    pass


class EventScriptFailure(ValueError):
    pass


class XMLSchemavalidationError(ValueError):
    pass


class UndefinedValueListError(ValueError):
    pass

class DuplicateValueListError(ValueError):
    pass

class UndefinedOperatorError(ValueError):
    pass

class DisallowedCloneError(ValueError):
    pass


class UndefinedUUIDError(ValueError):
    pass

class TemplatePathError(ValueError):
    pass

class MetaMemePropertyNotDefinedError(ValueError):
    """A given metameme does not have a property that its memes claims that it has"""

class MemePropertyValidationError(ValueError):
    """A meme has an invalid property"""
    pass

class MemePropertyValueError(ValueError):
    """A meme has a property with an invalid value"""
    pass

class MemePropertyValueTypeError(ValueError):
    """A meme's property has been asked to assign a value of the wrong type"""
    pass

class MemePropertyValueOutOfBoundsError(ValueError):
    """A meme property with constrained bounds has been asked to assign a value outside those bounds"""
    pass

class MemeMembershipValidationError(ValueError):
    """A meme has an invalid member"""
    pass

class NonInstantiatedSingletonError(ValueError):
    """This error should only occur if the meme is a singleton, but no entity has been instantiated.  It means that there
    is a technical problem with the meme loader in that it did not instantiate singleton memes"""
    pass

class MemeMemberCardinalityError(ValueError):
    """A meme's membership roll violates the cardinality rules of its parent metameme"""
    pass

class EntityPropertyMissingValueError(ValueError):
    """An entity has been asked to provide a value for a property that it does not have"""
    pass

class EntityPropertyValueTypeError(ValueError):
    """An entity's property has been asked to assign a value of the wrong type"""
    pass

class EntityPropertyDuplicateError(ValueError):
    """An entity's property has been asked to assign a value of the wrong type"""
    pass

class EntityPropertyValueOutOfBoundsError(ValueError):
    """An entity property with constrained bounds has been asked to assign a value outside those bounds"""
    pass

class EntityMemberDuplicateError(ValueError):
    """An entity may not have a unique member more than 1x"""
    pass

class EntityMemberMissingError(ValueError):
    """An entity may not have a unique member more than 1x"""
    pass

class EntityInitializationError(ValueError):
    """An entity can't initialize"""
    pass

class UnknownLinkError(ValueError):
    """A reference between two entities is missing"""
    pass

class UnanchoredReferenceError(ValueError):
    """There is no matched pair of an outboud link on one entity and an inbound on another"""
    pass

class UndefinedReferenceDirectionalityError(ValueError):
    """Thrown by LinkRepository.getCounterparts, when it was called with a value other than 0, 1 or 2"""
    pass

class UndefinedReferenceValueComparisonOperator(ValueError):
    """references may be filtered by attribute values.  If they are, then the value comparison operator must be one of 0-5"""
    pass

class ScriptError(ValueError):
    """A script error"""
    pass

class GeneratorError(ValueError):
    """General error for random numbers """
    pass


class StateEventScriptInitError(ValueError):
    """An error initializing a state event script"""
    pass

class SourceMemeManipulationError(ValueError):
    """An error in manipulating a source meme"""
    pass

class EntityNotInLinkError(ValueError):
    """The link does not have the prescribed entity"""
    pass

class EntityLinkFailureError(ValueError):
    """The link could not be created"""
    pass

class EntityDuplicateLinkError(ValueError):
    """The link already exists"""
    pass

class QueueError(ValueError):
    """ We have a problem with an engine comm queue"""
    pass

class NoSuchZoneError(ValueError):
    """The entity repository is called using an invalid zone filter parameter"""
    pass

class NoSuchEntityError(ValueError):
    """The entity repository is called using an invalid entity uuid"""
    pass

class MissingImlpicitMemeDatabase(ValueError):
    """There is an implicit meme, but no design time database connection string has been given"""
    pass   

class UndefinedSQLSyntax(Exception):
    """No SQL Syntax has been defined"""
    pass

class InconsistentPersistenceArchitecture(Exception): 
    """The constellation of persistence configuration options don't work together """
    def __init__(self, persistenceType, persistenceArg, nestedTraceback = None):
        self.persistenceType = persistenceType
        self.persistenceArg = persistenceArg
        if nestedTraceback is not None:
            self.enumeration = "Error while trying to set up backend persistence.  persistenceType=%s, (connection string) persistenceArg =%s, nested traceback = %s" %(persistenceType, persistenceArg, nestedTraceback)
        else:
            if self.persistenceType == "sqlite":
                errorMsg = "When the backend persistence type (persistenceType) is set to 'sqlite', then "
                errorMsg = "%s the 'persistenceArg' argument must conform to one of three patterns: " %errorMsg
                errorMsg = "%s(1) - It contains a valid filename, ending in '.sqlite'.  If it is an existing file, then that will be used.  Otherwise, it will be created. " %errorMsg
                errorMsg = "%s(2) - It is 'memory', in which case the sqlite3 database will be started with the :memory: connection option. " %errorMsg
                errorMsg = "%s(3) - It is None, in which case the sqlite3 database will be started with the :memory: connection option as default. " %errorMsg
                errorMsg = "%sThe provided value %s for 'persistenceArg' does not fit this pattern" %(errorMsg, persistenceArg)
                self.enumeration = errorMsg
            elif (self.persistenceType == "mssql"):
                self.enumeration = "Backend persistence type (persistenceType) is set to '%s', the provided connection string argument (persistenceArg) of %s is inconsistent.  Please provide a valid connection string." %(persistenceType, persistenceArg)
            else:
                self.enumeration = "Unsupported persistence type (persistenceType) argument %s." %persistenceType
    def __str__(self):
        return repr(self.enumeration)
    
class MalformedArgumentPathError(ValueError):
    '''Parsing a conditional argument path via regular expressions yields a zero length array.  
        This means that the argument path does not follow the xPath style  '''
    pass

class MismatchedArgumentPathError(ValueError):
    '''Walking down an agent's attributes using th3e argumen path yields an error.
        This indicated that the agent does not have the desired arguent path available '''
    pass

class MissingArgumentError(ValueError):
    '''A conditional that requires argument X has been called without that argument  '''
    pass

class MissingAgentPathError(ValueError):
    '''A conditional that requires an agent with an attribute at path X has been called without that agent/attribute  combo'''
    pass

class MissingAgentError(ValueError):
    '''A conditional that requires a reference agent has been called without one'''
    pass

class MalformedConditionalError(ValueError):
    ''' A conditional is somehow malformed and can not be processed'''
    pass
    
class UtilityError(Exception):
    """ Generic Problem Exception in the testing utility suite """
    pass


    
