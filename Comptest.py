#!/usr/bin/env python3

"""
   Comptest.py: Regression testing utility for Graphyne.  Performs the full suite of tests frdine in the runTests() method, against a single persistence type.
"""

__author__ = 'David Stocker'
__copyright__ = 'Copyright 2016, David Stocker'   
 
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'David Stocker'
__email__ = 'mrdave991@gmail.com'
__status__ = 'Production'


from Smoketest import publishResults
import sys
import Graphyne.Graph as Graph
import Graphyne.Fileutils as Fileutils


def doDriverSmokeTest(pc):
    #persistenceConstellations.append([persistenceModule1, lLevel, css, 'memory', 'sqllite', True])
    import Smoketest
    try:
        testReport = Smoketest.smokeTestSet(pc[0], pc[1], pc[2], pc[3], pc[4], pc[5], pc[6], pc[7])
        return testReport
    except Exception as e:
        print(("Failure in run %s" %pc[5]))
        testReport = Smoketest.smokeTestSet(pc[0], pc[1], pc[2], pc[3], pc[4], pc[5], pc[6], pc[7])
        raise e
    

   

if __name__ == "__main__":
    ''' This is the test method for the conditional argument module.
        argv[1] = "test_error", "test_warning", "test_info" or "test_debug" '''
        
    print("\nStarting Graphyne Smoke Test")
    
    lLevel = Graph.logLevel.WARNING
    try:
        if sys.argv[1] == "info":
            lLevel = Graph.logLevel.INFO
        elif sys.argv[1] == "debug":
            lLevel = Graph.logLevel.DEBUG
    except:
        pass

    css = Fileutils.defaultCSS()
    
    ####
    # Database Connections
    ####
    from graphyne.DatabaseDrivers import NonPersistent as persistenceModuleNone
    from graphyne.DatabaseDrivers import RelationalDatabase as persistenceModule1
    persistenceConstellations = []
    persistenceConstellations.append([persistenceModuleNone, lLevel, css, "No-Persistence", None, None, False, True])
    persistenceConstellations.append([persistenceModule1, lLevel, css, "sqllite", 'memory', 'sqlite', False, True])

    try:
        if (sys.argv[1] is not None) and (sys.argv[2] is not None):
            from graphyne.DatabaseDrivers import RelationalDatabase as persistenceModuleArg
            persistenceConstellations.append([persistenceModuleArg, lLevel, css, "%s - Reset" %sys.argv[2], sys.argv[1], sys.argv[2], True, False])   
            persistenceConstellations.append([persistenceModuleArg, lLevel, css, "%s - NoReset" %sys.argv[2], sys.argv[1], sys.argv[2], False, False]) 
    except: 
        print("Missing parameters 2 and 3.  Only testing non-persistence and sqlite against :memory:")
    ####
    # End Database Connections
    ####
    
    responses = []
    for persistenceConstellation in persistenceConstellations:
        #Multiprocessing pickles objects and DB connections can't be pickled; therefore we'll just execute the test serially
        localResult = doDriverSmokeTest(persistenceConstellation)
        responses.append(localResult)
  
    titleText = "Graphyne Comprehensive Test Suite - Results"
    publishResults(responses, css, "GraphyneTestResult.html", titleText)