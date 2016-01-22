"""
   Logger.py: Core Logging Service for Graphyne.  Runs a separate thread for logging in <usr>/Graphyne/
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'



from os.path import expanduser
from time import ctime
import codecs
import os
import threading

from . import Fileutils
from . import Graph


class NoProcConfigError(ValueError):
    pass


class LogLevel(Graph.LogLevel):
    pass
 
logLevel = LogLevel() 
    
    
    
class Logger(threading.Thread):
    ''' The Graphyne logging class.  Intended to run 1x per process.  '''
    className = 'Logger'
    
    def initialize(self, lLevel, codePage, logDir, overwrite = True):
        self._stopevent = threading.Event()
        self._sleepperiod = 5.0
        threading.Thread.__init__(self, name="Logger")

        if logDir is None:
            logRoot =  expanduser("~")
            logDir = os.path.join(logRoot, "Graphyne")
            if not os.path.exists(logDir):
                os.makedirs(logDir)
        logFile = os.path.join(logDir, "Graphyne.log")
        header = ''
        overwrite = True
            
        lLevel = restrictLogLevel(lLevel)
        self.standardLogLevels = LogLevel()
        self.lLevel = lLevel
        self.logFile = logFile
        self.codePage = codePage
        header = header + '\n'
        overwriteAppend = 'w'
        if overwrite == False: 
            overwriteAppend = 'a'
            header = '\n\n\n' + header

        Fileutils.ensureDirectory(logDir)
        fileName = codecs.open( self.logFile, overwriteAppend, self.codePage )
        #file = open(self.logFile, overwriteAppend)
        if header != None :
            fileName.writelines(header)
        fileName.writelines('%s Initialization \n' % ctime() )
        fileName.close
        
        
        
    def run(self):
        while not self._stopevent.isSet():
            try:
                toBeLogged = Graph.logQ.get_nowait()
                #toBeLogged = [contentType : logLevel : method : message]
                
                method = toBeLogged[2]
                statement = toBeLogged[3]
                errorLevel = toBeLogged[1]
                logLevelStr = ''
                if errorLevel == logLevel.ERROR: logLevelStr = ' ERROR: '
                elif errorLevel == logLevel.WARNING: logLevelStr = ' WARNING: '
                elif errorLevel == logLevel.ADMIN: logLevelStr = ' ADMIN: '
                elif errorLevel == logLevel.INFO: logLevelStr = ' INFO: '
                elif errorLevel == logLevel.DEBUG: logLevelStr = ' DEBUG: '
                
                if restrictLogLevel(errorLevel) <= self.lLevel:
                    fileName = codecs.open( self.logFile, "a", self.codePage )
                    #file = open(self.logFile,"a")
                    fileName.writelines('%s: %s %s - %s \n' % (ctime(), logLevelStr, method, statement) )
                    fileName.close
                    
                    # There is a risk of the loglevel affecting the content of the operations
                    # When characters with a non-latin codepage are printed non-latin codepage
                    try:
                        if (errorLevel == logLevel.ERROR) or (errorLevel == logLevel.WARNING) or (errorLevel == logLevel.ADMIN):
                            print(('%s: %s - %s' % (ctime(), method, statement)))
                    except:
                        print(('%s: %s - *** message contains character coding that can not \n               be rendered in the console. Please check your logfile***' % (ctime(), method))) 
                        print(('               Please check your logfile' % (ctime(), method)))
                
            except:
                self._stopevent.wait(self._sleepperiod)
        try:
            fileName = codecs.open( self.logFile, "a", self.codePage )
            fileName.writelines('%s:  %s' % (ctime(), "ADMIN:  Engine has ordered all archive threads to be terminated.  Logger Signing Off.") )
            fileName.close
        except: 
            pass
        print(("%s ends" % (self.getName(),)))
        
        

    def join(self, timeout = 10):
        """
        Stop the thread
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)



#Globals
moduleName = 'Logger'   
            

def restrictLogLevel(level):
    llevel = level
    if level!=0 and level!=1 and level!=2 and level!=3 and level!=4:
        llevel = logLevel.ERROR
    return llevel