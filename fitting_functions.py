import os, copy
import numpy as N
import simplejson
from collections import deque

class FunctionParamGroup(object):
    def __init__(self, paramNames=None):
        self.params = {}
        
        if paramNames is None:
            paramNames = []
        for paramName in paramNames:
            self.params.update({ paramName: FunctionParam(paramName) })
    
    def get(self, paramName):
        return self.params[paramName].value
    
    def set(self, paramName, value):
        self.params[paramName].value = value
    
    def __repr__(self):
        repr = str(self.params)
        return repr
        

class FunctionParam(object):
    def __init__(self, paramName = '', initValue=0):
        self.paramName = paramName
        self.value = initValue
        self.error = 0
        self.upperLimit = 0
        self.lowerLimit = 0
    
    def __repr__(self):
        return str(self.value)
    
    def getJSON(self):
        return { 'paramName': self.paramName, 'value': self.value, 'error': self.error, 'upperLimit': self.upperLimit, 'lowerLimit': self.lowerLimit }
        
        

class FunctionGroup(object):
    def __init__(self):
        self.functions = []
        self.data = {}
        
    def __repr__(self):
        foo = "["
        for function in self.functions:
            foo += function.__repr__() + ", "
        return foo + "]"
    
    def foo(self):
        f1 = Linear()
        f2 = Linear()
        f1.functionParams.params = { 'X1': FunctionParam('X1', 0), 'X2': FunctionParam('X2', 1),
                                     'Y1': FunctionParam('Y1', 2), 'Y2': FunctionParam('Y2', 2) }
        f2.functionParams.params = { 'X1': FunctionParam('X1', 0), 'X2': FunctionParam('X2', 1),
                                     'Y1': FunctionParam('Y1', 3), 'Y2': FunctionParam('Y2', 3) }
        self.functions = [f1, f2]
    
    def getValueAtX(self, X):
        functionYs = []
        for function in self.functions:
            value = function.function(X, None)
            if value:
                functionYs.append(value)
        
        return sum(functionYs)
    
    def function(self, Domain, Range):
        functionRanges = []
        for function in self.functions:
            functionRanges.append(function.function(Domain, Range))
        
        functionRange = sum(N.array(functionRanges))
        return functionRange
    
    def chisq(self, xData, yData, yErr):
        yCalc = self.function(xData, yData)
        
        yErr_temp = copy.deepcopy(yErr)
    #    zero_loc = N.where(yErr == 0)[0]
    #    if len(zero_loc) != 0:
    #        yErr_temp[zero_loc] = 1.0
        chi = ((yData - yCalc) / yErr_temp) ** 2
        
        return chi.sum() / (len(yData) - self.countFunctionParams())
    
    def countFunctionParams(self):
        count = 0
        for function in self.functions:
            count += len(function.functionParams.params)
        return count
            

    def createFunction(self, xData, yData):
        functionDomain    = N.arange(min(xData), max(xData), abs(max(xData) - min(xData)) / 200.)
        functionDataRange = N.arange(min(yData), max(yData), abs(max(yData) - min(yData)) / 200.)

        print self

        functionRanges = []
        functionYs = []
        functionInfos = []
        for function in self.functions:
            functionRanges.append(function.function(functionDomain, functionDataRange))
            functionYs.append(function.function(xData, yData))
            functionInfos.append(function.getJSON())
        
        functionRange = sum(N.array(functionRanges))
        functionData = zip_(functionDomain, functionRange)
        
        functionY = sum(N.array(functionYs))
        functionResiduals = N.subtract(functionY, yData)
        functionResidualData = zip_(xData, functionResiduals)

        print
        print functionRange
        print functionY
        print
        print functionData
        print functionResidualData
        print
        print '--------'
        print
        
        functionObj = dict(fit=functionData, resid=functionResidualData, functionInfos=functionInfos)
        return functionObj
    
    
    def getFunctionsParamsAsArray(self):
        functionsParamsArray = []
        functionsParamsArraySlices = []
        for function in self.functions:
            functionParamsArray = function.getFunctionParamsAsArray()
            functionsParamsArray.extend(functionParamsArray)
            functionsParamsArraySlices.append(len(functionParamsArray))
        return (functionsParamsArray, functionsParamsArraySlices)
    
    def setFunctionsParamsFromArray(self, params, slices):
        pointer = 0
        counter = 0
        for counter in range(len(slices)):
            functionParamsArray = params[pointer : pointer + slices[counter]]
            self.functions[counter].setFunctionParamsFromArray(functionParamsArray)
            pointer += slices[counter]
            counter += 1
        
    def getFunctionsParamsFromArray(self, params, slices):
        functionsParams = []
        
        pointer = 0
        counter = 0
        for counter in range(len(slices)):
            functionParamsArray = params[pointer : pointer + slices[counter]]
            functionsParams.append(self.functions[counter].getFunctionParamsFromArray(functionParamsArray))
            pointer += slices[counter]
            counter += 1
        
        return functionsParams
    

class Function(object):
    def __init__(self, functionID=0):
        self.functionID = functionID
        self.functionName = ''
        self.fitInstructions = deque()
        self.functionParams = FunctionParamGroup()
    
    def __repr__(self):
        return str(self.functionID) + ": " + str(self.functionParams)
        
    def function(self, Domain, Range):
        return None
    
    def getJSON(self):
        return { 'functionID': self.functionID, 'functionName': self.functionName, 'functionParams': self.functionParams.params }
    
    def setFunctionParamsFromRequest(self, request):
        for (paramName, value) in self.functionParams.params.items():
            if request.session.has_key(paramName):
                self.functionParams.set(paramName, request.session[paramName])
                
    def setFunctionParamsFromDict(self, functionParamsDict):
        for (paramName, value) in self.functionParams.params.items():
            if functionParamsDict.has_key(paramName):
                self.functionParams.set(paramName, functionParamsDict[paramName])
    
    def setFunctionParamsFromArray(self, functionParamsArray):
        functionParamsDict = self.getFunctionParamsFromArray(functionParamsArray)
        self.setFunctionParamsFromDict(functionParamsDict)
    
    def getFunctionParamsAsArray(self):
        pass
    
    def getFunctionParamsFromArray(self, params):
        pass
        

    def createFunction(self, xData, yData):
        functionDomain    = N.arange(min(xData), max(xData), abs(max(xData) - min(xData)) / 200.)
        functionDataRange = N.arange(min(yData), max(yData), abs(max(yData) - min(yData)) / 200.)
        
        functionRange = self.function(functionDomain, functionDataRange)
        functionData = zip_(functionDomain, functionRange)
        
        functionY = self.function(xData, yData)
        functionResiduals = N.subtract(functionY, yData)
        functionResidualData = zip_(xData, functionResiduals)

        print
        print functionRange
        print functionY
        print
        print '--------'
        print
        
        functionObj = dict(fit=functionData, resid=functionResidualData,
                           functionID=self.functionID, functionName=self.functionName, functionParams=self.functionParams)
        return functionObj
          
    def chisq(self, xData, yData, yErr):
        yCalc = self.function(xData, yData)
        
        yErr_temp = copy.deepcopy(yErr)
    #    zero_loc = N.where(yErr == 0)[0]
    #    if len(zero_loc) != 0:
    #        yErr_temp[zero_loc] = 1.0
        chi = ((yData - yCalc) / yErr_temp) ** 2
        
        return chi.sum() / (len(yData) - len(self.functionParams))
        


# LINEAR

class Linear(Function):
    def __init__(self):
        super(Linear, self).__init__()
        self.functionID = 1
        self.functionName = 'Linear'
        self.fitInstructions  = deque([
                                    { 'dataType': 'askPoint', 'xID': 'X1', 'yID': 'Y1',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the first point' },
                                    { 'dataType': 'askPoint', 'xID': 'X2', 'yID': 'Y2',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the second point' }
                                ])
        self.functionParams = FunctionParamGroup([ 'X1', 'Y1', 'X2', 'Y2' ])

    def function(self, Domain, Range):
        (X1, Y1, X2, Y2) = (self.functionParams.get('X1'), self.functionParams.get('Y1'), self.functionParams.get('X2'), self.functionParams.get('Y2'))
        if X1 is None or X2 is None:
            pass
        else:
            slope = N.divide(Y2 - Y1, X2 - X1)
            return slope * N.subtract(Domain, X1) + Y1
    
    def getFunctionParamsAsArray(self):
        return [ self.functionParams.get('X1'), self.functionParams.get('X2'), self.functionParams.get('Y1'), self.functionParams.get('Y2') ]
    
    def getFunctionParamsFromArray(self, params):
        return { 'X1': params[0], 'X2': params[1], 'Y1': params[2], 'Y2': params[3] }

class LinearDrag(Linear):
    def __init__(self):
        super(LinearDrag, self).__init__()
        self.functionID = 2
        self.functionName = 'Linear drag'
        self.fitInstructions  = deque([
                                    { 'dataType': 'askDrag', 'xIDstart': 'X1', 'yIDstart': 'Y1', 'xIDend': 'X2', 'yIDend': 'Y2',
                                      'messageTitle': 'Step 1', 'messageText': 'Please drag from the first point to the second point' }
                                ])


# GAUSSIAN

class Gaussian(Function):
    def __init__(self):
        super(Gaussian, self).__init__()
        self.functionID = 11
        self.functionName = 'Gaussian'
        self.fitInstructions  = deque([
                                #   { 'dataType': 'askPoint', 'xID': 'bkgdX', 'yID': 'bkgdY',
                                #     'messageTitle': 'Step 1', 'messageText': 'Please click on the bkgd of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'widthX', 'yID': 'widthY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the width of the data' }
                                ])
        self.functionParams = FunctionParamGroup([ 'peakX', 'peakY', 'bkgdY', 'FWHM' ])

    def function(self, Domain, Range):
        (peakX, peakY, bkgdY, FWHM) = (self.functionParams.get('peakX'), self.functionParams.get('peakY'), \
                                       self.functionParams.get('bkgdY'), self.functionParams.get('FWHM'))
        if peakX is None or bkgdY is None or FWHM is None:
            pass
        else:
            stdDev = FWHM / 2 / N.sqrt(2 * N.log(2))
            return bkgdY + (peakY - bkgdY) * N.exp(- N.power(N.subtract(Domain, peakX), 2) / 2 / N.power(stdDev, 2))
    
    def getFunctionParamsAsArray(self):
        return [ self.functionParams.get('peakX'), self.functionParams.get('peakY'),
                 self.functionParams.get('bkgdY'), self.functionParams.get('FWHM') ]
        
    def getFunctionParamsFromArray(self, params):
        return { 'peakX': params[0], 'peakY': params[1], 'bkgdY': params[2], 'FWHM': params[3] }
    
    def setFunctionParamsFromRequest(self, request):
        super(Gaussian, self).setFunctionParamsFromRequest(request)
        
        if request.session.has_key('widthX'):
            FWHM = 2 * N.abs(request.session['widthX'] - request.session['peakX'])
        self.functionParams.set('FWHM', FWHM)
        
class GaussianDrag(Gaussian):
    def __init__(self):
        super(GaussianDrag, self).__init__()
        self.functionID = 12
        self.functionName = 'Gaussian drag'
        self.fitInstructions  = deque([
                                #   { 'dataType': 'askPoint', 'xID': 'bkgdX', 'yID': 'bkgdY',
                                #     'messageTitle': 'Step 1', 'messageText': 'Please click on the bkgd of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askDrag', 'xIDstart': 'widthYst', 'yIDstart': 'widthYst', 'xIDend': 'widthX', 'yIDend': 'widthY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please drag on the width of the data' }
                                ])


# LORENTZIAN

class Lorentzian(Function):
    def __init__(self):
        super(Lorentzian, self).__init__()
        self.functionID = 21
        self.functionName = 'Lorentzian'
        self.fitInstructions  = deque([
                                #   { 'dataType': 'askPoint', 'xID': 'bkgdX', 'yID': 'bkgdY',
                                #     'messageTitle': 'Step 1', 'messageText': 'Please click on the bkgd of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'widthX', 'yID': 'widthY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the width of the data' }
                                ])
        self.functionParams = FunctionParamGroup([ 'peakX', 'peakY', 'bkgdY', 'FWHM' ])

    def function(self, Domain, Range):
        (peakX, peakY, bkgdY, FWHM) = (self.functionParams.get('peakX'), self.functionParams.get('peakY'), \
                                       self.functionParams.get('bkgdY'), self.functionParams.get('FWHM'))
        if peakX is None or bkgdY is None or FWHM is None:
            pass
        else:
            gamma = FWHM
            return bkgdY + (peakY - bkgdY) * N.divide(N.power(gamma, 2), N.power(N.subtract(Domain, peakX), 2) + N.power(gamma, 2))

    def getFunctionParamsAsArray(self):
        return [ self.functionParams.get('peakX'), self.functionParams.get('peakY'),
                 self.functionParams.get('bkgdY'), self.functionParams.get('FWHM') ]
        
    def getFunctionParamsFromArray(self, params):
        return { 'peakX': params[0], 'peakY': params[1], 'bkgdY': params[2], 'FWHM': params[3] }
        
    def setFunctionParamsFromRequest(self, request):
        super(Lorentzian, self).setFunctionParamsFromRequest(request)
        
        if request.session.has_key('widthX'):
            FWHM = N.abs(request.session['widthX'] - request.session['peakX'])
        self.functionParams.set('FWHM', FWHM)

class LorentzianDrag(Lorentzian):
    def __init__(self):
        super(LorentzianDrag, self).__init__()
        self.functionID = 22
        self.functionName = 'Lorentzian drag'
        self.fitInstructions  = deque([
                                #   { 'dataType': 'askPoint', 'xID': 'bkgdX', 'yID': 'bkgdY',
                                #     'messageTitle': 'Step 1', 'messageText': 'Please click on the bkgd of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askDrag', 'xIDstart': 'widthYst', 'yIDstart': 'widthYst', 'xIDend': 'widthX', 'yIDend': 'widthY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please drag on the width of the data' }
                                ])





def getFunctionParams(functionID, request):
    if functionID == 1 or functionID == 2:
        functionParams = { 'X1': request.session['X1'],
                           'Y1': request.session['Y1'],
                           'X2': request.session['X2'],
                           'Y2': request.session['Y2'] }
    elif functionID == 11 or functionID == 12:
        widthX = request.session['widthX']
        peakX = request.session['peakX']
        peakY = request.session['peakY']
        bkgdY = request.session['bkgdY']
        
        width = 2 * N.abs(widthX - peakX)
        stdDev = width / 2 / N.sqrt(2 * N.log(2))
        
        functionParams = { 'peakX': peakX, 'peakY': peakY, 'bkgdY': bkgdY, 'stdDev': stdDev }
    elif functionID == 21 or functionID == 22:
        widthX = request.session['widthX']
        peakX = request.session['peakX']
        peakY = request.session['peakY']
        bkgdY = request.session['bkgdY']
        
        gamma = N.abs(widthX - peakX)
        
        functionParams = { 'peakX': peakX, 'peakY': peakY, 'bkgdY': bkgdY, 'gamma': gamma }
        
    return functionParams

def zip_(l1, l2):
    return [list(elem) for elem in zip(l1, l2)]
