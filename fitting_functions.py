import os
import numpy as N
from collections import deque

class FunctionGroup(object):
    def __init__(self):
        self.functions = []

    

class Function(object):
    def __init__(self, functionID=0):
        self.functionID = functionID
        self.fitInstructions = deque()
        self.functionParams = {}
    
    def __repr__(self):
        foo = str(self.functionID) + ": ["
        for (key, value) in self.functionParams.items():
            foo += key + ":" + str(value) + ", "
        foo += "]"
        return foo
        
    def function(self, Domain, Range):
        return None
    
    def setFunctionParamsFromRequest(self, request):
        for (key, value) in self.functionParams.items():
            if request.session.has_key(key):
                self.functionParams.update({ key: request.session[key] })
    
    def getFunctionParamsAsArray(self):
        pass
    
    def getFunctionParamsFromArray(self, params):
        pass
        


# LINEAR

class Linear(Function):
    def __init__(self):
        super(Linear, self).__init__()
        self.functionID = 1
        self.fitInstructions  = deque([
                                    { 'dataType': 'askPoint', 'xID': 'X1', 'yID': 'Y1',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the first point' },
                                    { 'dataType': 'askPoint', 'xID': 'X2', 'yID': 'Y2',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the second point' }
                                ])
        self.functionParams = { 'X1': None, 'Y1': None, 'X2': None, 'Y2': None }

    def function(self, Domain, Range):
        (X1, Y1, X2, Y2) = (self.functionParams['X1'], self.functionParams['Y1'], self.functionParams['X2'], self.functionParams['Y2'])
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
        self.fitInstructions  = deque([
                                    { 'dataType': 'askDrag', 'xIDstart': 'X1', 'yIDstart': 'Y1', 'xIDend': 'X2', 'yIDend': 'Y2',
                                      'messageTitle': 'Step 1', 'messageText': 'Please drag from the first point to the second point' }
                                ])


# GAUSSIAN

class Gaussian(Function):
    def __init__(self):
        super(Gaussian, self).__init__()
        self.functionID = 11
        self.fitInstructions  = deque([
                                    { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'widthX', 'yID': 'widthY',
                                      'messageTitle': 'Step 3', 'messageText': 'Please click on the width of the data' }
                                ])
        self.functionParams = { 'peakX': None, 'peakY': None, 'backgroundY': None, 'FWHM': None }

    def function(self, Domain, Range):
        (peakX, peakY, backgroundY, FWHM) = (self.functionParams['peakX'], self.functionParams['peakY'], \
                                             self.functionParams['backgroundY'], self.functionParams['FWHM'])
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
        self.fitInstructions  = deque([
                                    { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askDrag', 'xIDstart': 'widthYst', 'yIDstart': 'widthYst', 'xIDend': 'widthX', 'yIDend': 'widthY',
                                      'messageTitle': 'Step 3', 'messageText': 'Please drag on the width of the data' }
                                ])


# LORENTZIAN

class Lorentzian(Function):
    def __init__(self):
        super(Lorentzian, self).__init__()
        self.functionID = 21
        self.fitInstructions  = deque([
                                    { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'widthX', 'yID': 'widthY',
                                      'messageTitle': 'Step 3', 'messageText': 'Please click on the width of the data' }
                                ])
        self.functionParams = { 'peakX': None, 'peakY': None, 'backgroundY': None, 'FWHM': None }

    def function(self, Domain, Range):
        (peakX, peakY, backgroundY, FWHM) = (self.functionParams['peakX'], self.functionParams['peakY'], \
                                              self.functionParams['backgroundY'], self.functionParams['FWHM'])
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
        self.fitInstructions  = deque([
                                    { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                      'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
                                    { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                      'messageTitle': 'Step 2', 'messageText': 'Please click on the peak of the data' },
                                    { 'dataType': 'askDrag', 'xIDstart': 'widthYst', 'yIDstart': 'widthYst', 'xIDend': 'widthX', 'yIDend': 'widthY',
                                      'messageTitle': 'Step 3', 'messageText': 'Please drag on the width of the data' }
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
