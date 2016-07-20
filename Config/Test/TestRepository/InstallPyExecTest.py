'''
Created on Jul 14, 2016

@author: David Stocker
'''

import threading

class TestClass(threading.Thread):
    className = "TestClass"
    
    def __init__(self, path):
        self.meme = path
        self.entityLock = threading.RLock()
        
    def execute(self, params):
        ''' 
            Return a string, based on the content of runtimeVariables (params[1])
        '''
        # If param is not empty, then return params[0]
        # Else return the meme path
        
        if len(params[1]) == 0:
            return self.meme
        elif "returnMe" in params[1]:
            return params[1]["returnMe"]
        else:
            raise KeyError
