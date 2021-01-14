'''
Created on Dec 13, 2016

@author: David Stocker
'''

import Graphyne.Scripting
import Graphyne.Graph

class OnInitialize(Graphyne.Scripting.StateEventScript):
    """
        This class tests the initialize event.  As this event has no return mechanism, we'll test it
        by adding a property.  The EventInitRemove.InitRemoveEventTest entity that this script will
        be attached to has no properties.  So we'll add a property during script execution, which we
        can then check for later.
    """
        
    def execute(self, selfUUID, params):
        Graphyne.Graph.api.addEntityStringProperty(selfUUID, "AProp", "Hello")
    
    
    
    
class OnDelete(Graphyne.Scripting.StateEventScript):
    """
        This class tests the terminate event.  It echos 'Hello World' back.
    """

        
    def execute(self, selfUUID, params): 
        ''' 
           Echo the string "Hello World", where the "Hello" part comes from the AProp property added in the OnInitialize script.
           
        '''
        hello = Graphyne.Graph.api.getEntityPropertyValue(selfUUID, "AProp")
        return "%s World" %(hello)


