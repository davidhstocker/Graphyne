'''
Created on Jul 22, 2014

@author: Dave
'''

#Generates test data

global operators
global paramKeys
operators = ['=', '>', '<', '>=', '<=', '!=', '><', '<>']
paramKeys = ['x', 'y']

#The possible individual values for x,y, and z.  
global traverseParamArray
global nodeParamArray
traverseParamArray = [[4, 5, 6], [1, 2, 3]]
nodeParamArray = [[0, 1, 2]]


x4a = [False, True, False, True, False, True, True, False]
x5a = [False, True, False, True, False, True, True, False]
x6a = [False, True, False, True, False, True, True, False]
x4b = [False, True, False, True, False, True, True, False]
x5b = [False, True, False, True, False, True, True, False]
x6b = [False, True, False, True, False, True, True, False]

y1a = [False, False, True, False, True, True, True, False]
y2a = [False, False, False, True, True, False, True, False]
y3a = [False, True, False, True, False, True, True, False]
y1b = [False, False, True, False, True, True, True, False]
y2b = [False, False, False, True, True, False, True, False]
y3b = [False, True, False, True, False, True, True, False]

traverseParamArrayResultsA = [[x4a, x5a, x6a], [y1a, y2a, y3a]]
traverseParamArrayResultsB = [[x4b, x5b, x6b], [y1b, y2b, y3b]]


global mask
mask = [[False, False], \
        [True, False], \
        [False, True], \
        [True, True]]


def getEachPossibleValue(nestedArrayX, nestedArrayY):
    valueArray = []
    for nestedArrayXValue in nestedArrayX:
        for nestedArrayYValue in nestedArrayY:
            valueArray.append([nestedArrayXValue, nestedArrayYValue])
    return valueArray




traverseParamValues = getEachPossibleValue(traverseParamArray[0], traverseParamArray[1])
nodeParamValues = getEachPossibleValue(nodeParamArray[0], nodeParamArray[1])




def getValueOperatorCombos(paramValues):
    comboArray = []
    for paramValue in paramValues:
        for subMask in mask:
            paramCombo = [None, None]
            if subMask[0] == True: paramCombo[0] = paramValue[0]
            if subMask[1] == True: paramCombo[1] = paramValue[1]
            comboArray.append(paramCombo)
    return comboArray
            
            
            
traverseParamCombos = getValueOperatorCombos(traverseParamValues)
nodeParamCombos = getValueOperatorCombos(traverseParamValues)


#Nodes
A = {'x':1, 'y':2}
B = {'x':3, 'y':2}
C = {'x':1}
D = {'x':3}
theNodes = {'a':A, 'b':B, 'c':C, 'd':D}

def getFilterStatements(paramCombos, openBrace, closeBrace, resultsArray):
    filterStatements = []
    nNth = 0
    for paramCombo in paramCombos:
        nNth = nNth + 1
        for i in operators:
            for j in operators: 
                filterStatement = ""
                trueOrFalse = True
                if paramCombo[0] is not None:
                    currResOuterList = resultsArray[nNth]
                    currResInnerList = currResOuterList[i]
                    filterStatement = "%s%sx %s %s%s" %(filterStatement, openBrace, i, paramCombo[0], closeBrace)
                if paramCombo[1] is not None:
                    if len(filterStatement) > 0:
                        filterStatement = "%s, " %filterStatement
                    filterStatement = "%s%sy %s %s%s" %(filterStatement, openBrace, j, paramCombo[1], closeBrace)
                filterStatements.append(filterStatement)
    return filterStatements

traverseFilterStatements = getFilterStatements(traverseParamCombos, '[', ']')
nodeFilterStatements = getFilterStatements(traverseParamCombos, '(', ')')

traverseFilterString = ""
nodeFilterString = ""

lastStatement = None

for nodeFilterStatement in nodeFilterStatements:
    if len(nodeFilterStatement) > 0:
        if nodeFilterString != lastStatement: 
            lastStatement = nodeFilterString
            nodeFilterString = "%s\n%s" %(nodeFilterString, nodeFilterStatement)   

for traverseFilterStatement in traverseFilterStatements:
    if len(traverseFilterStatement) > 0:
        if traverseFilterStatement != lastStatement: 
            lastStatement = traverseFilterStatement
            traverseFilterString = "%s\n%s" %(traverseFilterString, traverseFilterStatement)
        
     
        
print(traverseFilterString)
print("\n")
print(nodeFilterString)

                        

