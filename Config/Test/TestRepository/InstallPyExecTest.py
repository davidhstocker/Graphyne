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
        
    def execute(self, entityID, params):
        ''' 
            Return a string, based on the content of runtimeVariables (params["runtimeVariables"])
        '''
        # If param is not empty, then return params[0]
        # Else return the meme path
        
        if len(params['runtimeVariables']) == 0:
            return self.meme
        elif "returnMe" in params['runtimeVariables']:
            return params['runtimeVariables']["returnMe"]
        else:
            raise KeyError
