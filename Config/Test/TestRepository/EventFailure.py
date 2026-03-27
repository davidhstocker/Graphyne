'''
Created on Nov 11, 2016

@author: d035331
'''

import sys
from pathlib import Path
# Add repo root to sys.path (3 levels up from this file)
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import Graphyne.Scripting


class BrokenScript(Graphyne.Scripting.StateEventScript):
    """
        Do something not allowed and cause an exception
    """
        
    def execute(self, entityID, params):
            aDict = {"a": 1}
            unusedB = aDict["b"] #this should raise an exception
            


class ThrowsException(Graphyne.Scripting.StateEventScript):
    """
        Like BrokenScript, but should catch and raise the exception
    """
        
    def execute(self, entityID, params):
      
        try:
            aDict = {"a": 1}
            unusedB = aDict["b"] #this should raise an exception
        except Exception as e:
            raise e
        
        
class NotAStateEventScript():
    """
        Like BrokenScript, but should catch and raise the exception
    """
        
    def neverUsed(self):
        pass