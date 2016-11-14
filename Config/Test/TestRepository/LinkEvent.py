'''
Created on Nov 6, 2016

@author: David Stocker
'''

import Graphyne.Scripting

class LinkAdded(Graphyne.Scripting.StateEventScript):
    """
        This class tests the property change event.  It returns the old and new values.
    """
        
    def execute(self, params):
        ''' 
           Echo the string "Added <uuid> as link <source/target> for <counterpartUUID>"
           
        '''
        selfUUID = params[0]
        sourceEntityID = None
        targetEntityID = None
        st = "source"
        counterpart = None
        
        
        if "sourceEntityID" in params[1]:
            sourceEntityID =  params[1]["sourceEntityID"]
            
        else:
            raise KeyError
        
        if "targetEntityID" in params[1]:
            targetEntityID =  params[1]["targetEntityID"]
            if selfUUID == targetEntityID:
                st = "target"
        else:
            raise KeyError
        
        if selfUUID == sourceEntityID:
            counterpart = targetEntityID
        elif selfUUID == targetEntityID:
            counterpart = sourceEntityID
        
        return "Added %s as link %s for %s" %(selfUUID, st, counterpart)
    
    
    
    
class LinkRemoved(Graphyne.Scripting.StateEventScript):
    """
        This class tests the property change event.  It returns the old and new values.
    """
    
    className = "Echo"
        
    def execute(self, params): 
        ''' 
           Echo the string "Removed <uuid> as link <source/target> for <counterpartUUID>"
           
        '''
        selfUUID = params[0]
        sourceEntityID = None
        targetEntityID = None
        st = "source"
        counterpart = None
        
        
        if "sourceEntityID" in params[1]:
            sourceEntityID =  params[1]["sourceEntityID"]
            
        else:
            raise KeyError
        
        if "targetEntityID" in params[1]:
            targetEntityID =  params[1]["targetEntityID"]
            if selfUUID == targetEntityID:
                st = "target"
        else:
            raise KeyError
        
        if selfUUID == sourceEntityID:
            counterpart = targetEntityID
        elif selfUUID == targetEntityID:
            counterpart = sourceEntityID
        
        return "Removed %s as link %s for %s" %(selfUUID, st, counterpart)

