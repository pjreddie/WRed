import os, copy
import numpy as N
import simplejson
from collections import deque

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
        f1.functionParams = {'X1': 0, 'X2': 1,'Y1': 2, 'Y2': 2}
        f2.functionParams = {'X1': 0, 'X2': 1,'Y1': 3, 'Y2': 3}
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
            count += len(function.functionParams)
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
        functionData = zip(functionDomain, functionRange)
        
        functionY = sum(N.array(functionYs))
        functionResiduals = N.subtract(functionY, yData)
        functionResidualData = zip(xData, functionResiduals)

        print
        print functionRange
        print functionY
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
            self.functions[counter].functionParams = self.functions[counter].getFunctionParamsFromArray(functionParamsArray)
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
        self.functionParams = {}
    
    def __repr__(self):
        return str(self.functionID) + ": " + simplejson.dumps(self.functionParams)
        
    def function(self, Domain, Range):
        return None
    
    def getJSON(self):
        return { 'functionID': self.functionID, 'functionName': self.functionName, 'functionParams': self.functionParams }
    
    def setFunctionParamsFromRequest(self, request):
        for (key, value) in self.functionParams.items():
            if request.session.has_key(key):
                self.functionParams.update({ key: request.session[key] })
                
    def setFunctionParamsFromDict(self, functionParamsDict):
        for (key, value) in self.functionParams.items():
            if functionParamsDict.has_key(key):
                self.functionParams.update({ key: functionParamsDict[key] })
    
    def getFunctionParamsAsArray(self):
        pass
    
    def getFunctionParamsFromArray(self, params):
        pass
        

    def createFunction(self, xData, yData):
        functionDomain    = N.arange(min(xData), max(xData), abs(max(xData) - min(xData)) / 200.)
        functionDataRange = N.arange(min(yData), max(yData), abs(max(yData) - min(yData)) / 200.)
        
        functionRange = self.function(functionDomain, functionDataRange)
        functionData = zip(functionDomain, functionRange)
        
        functionY = self.function(xData, yData)
        functionResiduals = N.subtract(functionY, yData)
        functionResidualData = zip(xData, functionResiduals)

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
        self.functionParams = { 'X1': None, 'Y1': None, 'X2': None, 'Y2': None }

    def function(self, Domain, Range):
        (X1, Y1, X2, Y2) = (self.functionParams['X1'], self.functionParams['Y1'], self.functionParams['X2'], self.functionParams['Y2'])
        if X1 is None or X2 is None:
            pass
        else:
            slope = N.divide(Y2 - Y1, X2 - X1)
            return slope * N.subtract(Domain, X1) + Y1
    
    def getFunctionParamsAsArray(self):
        return [ self.functionParams['X1'], self.functionParams['X2'], self.functionParams['Y1'], self.functionParams['Y2'] ]
    
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
                                #   { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                #     'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'widthX', 'yID': 'widthY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the width of the data' }
                                ])
        self.functionParams = { 'peakX': None, 'peakY': None, 'backgroundY': 0, 'FWHM': None }

    def function(self, Domain, Range):
        (peakX, peakY, backgroundY, FWHM) = (self.functionParams['peakX'], self.functionParams['peakY'], \
                                             self.functionParams['backgroundY'], self.functionParams['FWHM'])
        if peakX is None or backgroundY is None or FWHM is None:
            pass
        else:
            stdDev = FWHM / 2 / N.sqrt(2 * N.log(2))
            return backgroundY + (peakY - backgroundY) * N.exp(- N.power(N.subtract(Domain, peakX), 2) / 2 / N.power(stdDev, 2))
    
    def getFunctionParamsAsArray(self):
        return [ self.functionParams['peakX'], self.functionParams['peakY'], self.functionParams['backgroundY'], self.functionParams['FWHM'] ]
        
    def getFunctionParamsFromArray(self, params):
        return { 'peakX': params[0], 'peakY': params[1], 'backgroundY': params[2], 'FWHM': params[3] }
    
    def setFunctionParamsFromRequest(self, request):
        super(Gaussian, self).setFunctionParamsFromRequest(request)
        
        if request.session.has_key('widthX'):
            FWHM = 2 * N.abs(request.session['widthX'] - request.session['peakX'])
        self.functionParams.update({ 'FWHM': FWHM })
        
class GaussianDrag(Gaussian):
    def __init__(self):
        super(GaussianDrag, self).__init__()
        self.functionID = 12
        self.functionName = 'Gaussian drag'
        self.fitInstructions  = deque([
                                #   { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                #     'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
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
                                #   { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                #     'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'widthX', 'yID': 'widthY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the width of the data' }
                                ])
        self.functionParams = { 'peakX': None, 'peakY': None, 'backgroundY': 0, 'FWHM': None }

    def function(self, Domain, Range):
        (peakX, peakY, backgroundY, FWHM) = (self.functionParams['peakX'], self.functionParams['peakY'], \
                                              self.functionParams['backgroundY'], self.functionParams['FWHM'])
        if peakX is None or backgroundY is None or FWHM is None:
            pass
        else:
            gamma = FWHM
            return backgroundY + (peakY - backgroundY) * N.divide(N.power(gamma, 2), N.power(N.subtract(Domain, peakX), 2) + N.power(gamma, 2))

    def getFunctionParamsAsArray(self):
        return [ self.functionParams['peakX'], self.functionParams['peakY'], self.functionParams['backgroundY'], self.functionParams['FWHM'] ]
        
    def getFunctionParamsFromArray(self, params):
        return { 'peakX': params[0], 'peakY': params[1], 'backgroundY': params[2], 'FWHM': params[3] }
        
    def setFunctionParamsFromRequest(self, request):
        super(Lorentzian, self).setFunctionParamsFromRequest(request)
        
        if request.session.has_key('widthX'):
            FWHM = N.abs(request.session['widthX'] - request.session['peakX'])
        self.functionParams.update({ 'FWHM': FWHM })

class LorentzianDrag(Lorentzian):
    def __init__(self):
        super(LorentzianDrag, self).__init__()
        self.functionID = 22
        self.functionName = 'Lorentzian drag'
        self.fitInstructions  = deque([
                                #   { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                #     'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
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
        backgroundY = request.session['backgroundY']
        
        width = 2 * N.abs(widthX - peakX)
        stdDev = width / 2 / N.sqrt(2 * N.log(2))
        
        functionParams = { 'peakX': peakX, 'peakY': peakY, 'backgroundY': backgroundY, 'stdDev': stdDev }
    elif functionID == 21 or functionID == 22:
        widthX = request.session['widthX']
        peakX = request.session['peakX']
        peakY = request.session['peakY']
        backgroundY = request.session['backgroundY']
        
        gamma = N.abs(widthX - peakX)
        
        functionParams = { 'peakX': peakX, 'peakY': peakY, 'backgroundY': backgroundY, 'gamma': gamma }
        
    return functionParams
