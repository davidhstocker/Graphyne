'''
Created on Nov 6, 2016

@author: David Stocker
'''

import Graphyne.Scripting

class LinkAdded(Graphyne.Scripting.StateEventScript):
    """
        This class tests the property change event.  It returns the old and new values.
    """
        
    def execute(self, selfUUID, params):
        ''' 
           Echo the string "Added <uuid> as link <source/target> for <counterpartUUID>"
           
        '''
        sourceEntityID = None
        targetEntityID = None
        st = "source"
        counterpart = None
        
        
        if "sourceEntityID" in params:
            sourceEntityID =  params["sourceEntityID"]
            
        else:
            raise KeyError
        
        if "targetEntityID" in params:
            targetEntityID =  params["targetEntityID"]
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
        
    def execute(self, selfUUID, params): 
        ''' 
           Echo the string "Removed <uuid> as link <source/target> for <counterpartUUID>"
           
        '''
        sourceEntityID = None
        targetEntityID = None
        st = "source"
        counterpart = None
        
        
        if "sourceEntityID" in params:
            sourceEntityID =  params["sourceEntityID"]
            
        else:
            raise KeyError
        
        if "targetEntityID" in params:
            targetEntityID =  params["targetEntityID"]
            if selfUUID == targetEntityID:
                st = "target"
        else:
            raise KeyError
        
        if selfUUID == sourceEntityID:
            counterpart = targetEntityID
        elif selfUUID == targetEntityID:
            counterpart = sourceEntityID
        
        return "Removed %s as link %s for %s" %(selfUUID, st, counterpart)

