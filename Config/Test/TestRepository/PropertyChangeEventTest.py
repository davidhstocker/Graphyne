'''
Created on Oct 16, 2016

@author: David Stocker
'''

import Graphyne.Scripting

class EchoPropDelta(Graphyne.Scripting.StateEventScript):
    """
        This class tests the property change event.  It returns the old and new values.
    """
        
    def execute(self, entityID, params):
        ''' 
            Return a string, based on the content of runtimeVariables (params[2])
        '''
        # If param is not empty, then return params[0]
        # Else return the meme path
        
        if "oldVal" in params:
            oldVal =  params["oldVal"]
        else:
            raise KeyError
        
        if "newVal" in params:
            newVal =  params["newVal"]
        else:
            raise KeyError
        
        return "%s %s" %(oldVal, newVal)
    
    
    
    
class EchoID(Graphyne.Scripting.StateEventScript):
    """
        This class tests the property change event.  It returns the old and new values.
    """
    
    className = "Echo"
        
    def execute(self, entityID, params):
        ''' 
            Return the uuid of the calling entity
        '''
        return "%s" %(entityID)
