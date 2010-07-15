import os, time, copy
import simplejson
from collections import deque

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from WRed.display.models import *
from WRed.display.fileToJson import displayfile

import numpy as N
from WRed.utilities.mpfit import mpfit


def print_timing(func):
  def wrapper(*arg):
    t1 = time.time()
    res = func(*arg)
    t2 = time.time()
    print '%s took %0.3f ms' % (func.func_name, (t2 - t1) * 1000.0)
    return res
  return wrapper



@print_timing
@login_required
def fitting_request_action(request, idNum):
    print 'USERNAME: ', request.user.username
    print 'Authenticated: ', request.user.is_authenticated()
    print 'Request: ', request.POST
    
    if request.user.is_authenticated() and (request.user.username == str(idNum) or request.user.is_superuser):
        try:
            actionID = request.POST['actionID']
            actionName = request.POST['actionName']
        except (KeyError):
            return HttpResponse('No POST data')

        print 'You are trying to request the following action: ' + actionName + ' [ID: ' + actionID + ']'
        
        
        if actionID == '1':
            xData = simplejson.loads(request.POST['xData'])
            yData = simplejson.loads(request.POST['yData'])
            functionID = int(request.POST['functionID'])
            request.session['xData'] = xData
            request.session['yData'] = yData
            request.session['functionID'] = functionID
            
            addlParams = { 'xData': xData, 'yData': yData, 'functionID': functionID, 'actionID': 2 }
            request.session['addlParams'] = addlParams
            
            fitInstructions = getFitInstructions(functionID)
            nextFitInstruction = fitInstructions.popleft()
            request.session['fitInstructions'] = fitInstructions
            
            response = fitInstructionResponse(nextFitInstruction, addlParams)
            return HttpResponse(response)
            
            
        elif actionID == '2':
            # Data Types
            if request.POST['dataType'] == 'askPoint':
                request = defPoint(request)
            elif request.POST['dataType'] == 'askDrag':
                request = defPoint(request)

                xData = request.session['xData']
                yData = request.session['yData']
                functionID = request.session['functionID']
                functionParams = getFunctionParams(functionID, request)
                
                dragFit = createFunction(xData, yData, functionID, functionParams)
                dragFit.update({ 'dataType': 'doingDrag' })
                return HttpResponse(simplejson.dumps(dragFit))
            
            
            if not request.session['fitInstructions']:
                xData = request.session['xData']
                yData = request.session['yData']
                functionID = request.session['functionID']
                functionParams = getFunctionParams(functionID, request)
                
                finishedFunction = createFunction(xData, yData, functionID, functionParams)
                return HttpResponse(simplejson.dumps(finishedFunction))
            else:
                #guess width
                #guessWidth = guess_width(xData, yData, peakX, peakY, backgroundY)
                #guessWidth2 = guess_width2(xData, yData, peakX, peakY, backgroundY)
                
                nextFitInstruction = request.session['fitInstructions'].popleft()
                
                response = fitInstructionResponse(nextFitInstruction, request.session['addlParams'])
                return HttpResponse(response)
            
        elif actionID == '3':
            dataData = simplejson.loads(request.POST['dataData'])
            xData = dataData['x']
            yData = dataData['y']
            yErrData = dataData['yerr']
            
            functionData = simplejson.loads(request.POST['functionData'])
            functionID = int(request.POST['functionID'])
            functionParams = simplejson.loads(request.POST['functionParams'])
            params = paramsDictToArray(functionID, functionParams)
            
            
            functkw = { 'xData': xData, 'yData': yData, 'yErr': yErrData, 'functionID': functionID }
            mpfitResult = mpfit(mpfitFunction, params, functkw=functkw)
            
            fitFunctionParams = paramsArrayToDict(functionID, mpfitResult.params)

            finishedFit = createFunction(xData, yData, functionID, fitFunctionParams)            
            chiSquared = sigfig(chisq(xData, yData, yErrData, functionID, fitFunctionParams))
            
            # Map sigfig 
            fitFunctionParams = paramsArrayToDict(functionID, map(sigfig, mpfitResult.params))
            fitFunctionParamsErr = paramsArrayToDict(functionID, map(sigfig, mpfitResult.perror))
            fitFunctionParamsArray = paramsJoin(fitFunctionParams, fitFunctionParamsErr)       
            
            functionInfo = { 'fitFunctionParams': fitFunctionParams, 'fitFunctionParamsErr': fitFunctionParamsErr, 'chisq': chiSquared,
                             'fitFunctionParamsArray': fitFunctionParamsArray }


            response = finishedFit
            response.update({ 'legendIndex': request.POST['legendIndex'], 'functionInfo': functionInfo, 'dataType': 'doFit' })
            return HttpResponse(simplejson.dumps(response))
            
        else:
            return HttpResponse('actionID not correct; it was ' + actionID)
            
    else:
        return HttpResponse('Not authenticated.')




def createFunction(xData, yData, functionID, functionParams):
      functionDomain    = N.arange(min(xData), max(xData), abs(max(xData) - min(xData)) / 180.)
      functionDataRange = N.arange(min(yData), max(yData), abs(max(yData) - min(yData)) / 180.)
      
      thefunction = getFunction(functionID)
      functionRange = thefunction(functionDomain, functionDataRange, functionParams)
      functionData = zip(functionDomain, functionRange)
      
      functionY = thefunction(xData, yData, functionParams)
      functionResiduals = N.subtract(functionY, yData)
      functionResidualData = zip(xData, functionResiduals)

      

      print
      print functionRange
      print functionY
      print
      print '--------'
      print
      
      JSONobj = dict(fit=functionData, resid=functionResidualData, functionID=functionID, functionParams=functionParams)
      return JSONobj


#def createFit(


# --

def defPoint(request):
    request.session[request.POST['xID']] = float(request.POST['xPos'])
    request.session[request.POST['yID']] = float(request.POST['yPos'])
    return request

def defDrag(request):
    request.session[request.POST['xIDstart']] = float(request.POST['xPosstart'])
    request.session[request.POST['yIDstart']] = float(request.POST['yPosstart'])
    request.session[request.POST['xIDend']]   = float(request.POST['xPosend'])
    request.session[request.POST['yIDend']]   = float(request.POST['yPosend'])
    return request


def getFunction(functionID):
    if functionID == 1 or functionID == 2:
        return generateLinearFunction
    elif functionID == 11 or functionID == 12:
        return generateGaussianFunction
    elif functionID == 21 or functionID == 22:
        return generateLorentzianFunction


def getFitInstructions(functionID):
    fitInstructions = deque([])
    if functionID == 1:
        fitInstructions = deque([
                              { 'dataType': 'askPoint', 'xID': 'X1', 'yID': 'Y1',
                                'messageTitle': 'Step 1', 'messageText': 'Please click on the first point' },
                              { 'dataType': 'askPoint', 'xID': 'X2', 'yID': 'Y2',
                                'messageTitle': 'Step 2', 'messageText': 'Please click on the second point' }
                          ])
    if functionID == 2:
        fitInstructions = deque([
                              { 'dataType': 'askDrag', 'xIDstart': 'X1', 'yIDstart': 'Y1', 'xIDend': 'X2', 'yIDend': 'Y2',
                                'messageTitle': 'Step 1', 'messageText': 'Please drag from the first point to the second point' }
                          ])
    elif functionID == 11 or functionID == 21:
        fitInstructions = deque([
                              { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
                              { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                'messageTitle': 'Step 2', 'messageText': 'Please click on the peak of the data' },
                              { 'dataType': 'askPoint', 'xID': 'widthX', 'yID': 'widthY',
                                'messageTitle': 'Step 3', 'messageText': 'Please click on the width of the data' }
                          ])
    elif functionID == 12 or functionID == 22:
        fitInstructions = deque([
                              { 'dataType': 'askPoint', 'xID': 'backgroundX', 'yID': 'backgroundY',
                                'messageTitle': 'Step 1', 'messageText': 'Please click on the background of the data' },
                              { 'dataType': 'askPoint', 'xID': 'peakX', 'yID': 'peakY',
                                'messageTitle': 'Step 2', 'messageText': 'Please click on the peak of the data' },
                              { 'dataType': 'askDrag', 'xIDstart': 'widthYstart', 'yIDstart': 'widthYstart', 'xIDend': 'widthX', 'yIDend': 'widthY',
                                'messageTitle': 'Step 3', 'messageText': 'Please drag on the width of the data' }
                          ])
    return fitInstructions

def fitInstructionResponse(fitInstruction, addlParams):
#    returnResponse = { 'dataType': fitInstruction['dataType'], 'xID': fitInstruction['xID'], 'yID': fitInstruction['yID'],
#                       'messageTitle': fitInstruction['messageTitle'], 'messageText': fitInstruction['messageText'] }
    returnResponse = fitInstruction
    returnResponse.update(addlParams)
    
    return simplejson.dumps(returnResponse)


def generateLinearFunction(Domain, Range, params):
    (X1, Y1, X2, Y2) = (params['X1'], params['Y1'], params['X2'], params['Y2'])
    slope = N.divide(Y2 - Y1, X2 - X1)
    return slope * N.subtract(Domain, X1) + Y1
    
def generateGaussianFunction(Domain, Range, params):
    (peakX, peakY, backgroundY, stdDev) = (params['peakX'], params['peakY'], params['backgroundY'], params['stdDev'])
    return backgroundY + (peakY - backgroundY) * N.exp(- N.power(N.subtract(Domain, peakX), 2) / 2 / N.power(stdDev, 2))
    
def generateLorentzianFunction(Domain, Range, params):
    (peakX, peakY, backgroundY, gamma) = (params['peakX'], params['peakY'], params['backgroundY'], params['gamma'])
    return backgroundY + (peakY - backgroundY) * N.divide(N.power(gamma, 2), N.power(N.subtract(Domain, peakX), 2) + N.power(gamma, 2))


def paramsDictToArray(functionID, functionParams):
    if functionID == 1 or functionID == 2:
        params = [ functionParams['X1'], functionParams['X2'], functionParams['Y1'], functionParams['Y2'] ]
    if functionID == 11 or functionID == 12:
        params = [ functionParams['peakX'], functionParams['peakY'], functionParams['backgroundY'], functionParams['stdDev'] ]
    if functionID == 21 or functionID == 22:
        params = [ functionParams['peakX'], functionParams['peakY'], functionParams['backgroundY'], functionParams['gamma'] ]

    return params

def paramsArrayToDict(functionID, params):
    if functionID == 1 or functionID == 2:
        functionParams = { 'X1': params[0], 'X2': params[1], 'Y1': params[2], 'Y2': params[3] }
    if functionID == 11 or functionID == 12:
        functionParams = { 'peakX': params[0], 'peakY': params[1], 'backgroundY': params[2], 'stdDev': params[3] }
    if functionID == 21 or functionID == 22:
        functionParams = { 'peakX': params[0], 'peakY': params[1], 'backgroundY': params[2], 'gamma': params[3] }

    return functionParams

def objectToArrayPairs(d):
    return [dict(name=key, value=value) for key, value in d.iteritems()]

def paramsJoin(d1, d2):
    n = []
    for (key, value) in d1.items():
        n.append({ 'name': key, 'value': value, 'err': d2[key] })
    return n


def getFunctionParams(functionID, request):
    functionParams = {}
    
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

# --

# Copied straight from William
def chisq(xData, yData, yErr, functionID, functionParams):
    thefunction = getFunction(functionID)
    yCalc = thefunction(xData, yData, functionParams)
    
    yErr_temp = copy.deepcopy(yErr)
#    zero_loc = N.where(yErr == 0)[0]
#    if len(zero_loc) != 0:
#        yErr_temp[zero_loc] = 1.0
    chi = ((yData - yCalc) / yErr_temp) ** 2
    
    return chi.sum() / (len(yData) - len(functionParams))


def mpfitFunction(params, parinfo=None, fjac=None, xData=None, yData=None, yErr=None, functionID=None):
    # Parameter values are passed in "params"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default flag.
    
    functionParams = paramsArrayToDict(functionID, params)
    thefunction = getFunction(functionID)
    yCalc = thefunction(xData, yData, functionParams)
    
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    
    status = 0
    return [status, (yData - yCalc) / yErr]
    
    


def guess_width(x, y, peakX, peakY, backgroundY):
    halfMax = (peakY - backgroundY) / 2.
    print halfMax
    print
    
    x_i = 0
    while x_i < len(x) and y[x_i] <= peakY and y[x_i] < halfMax:
        print str(x_i) + ' (' + str(x[x_i]) + ', ' + str(y[x_i]) + ')'
        x_i += 1
    leftGreater = y[x_i]
    leftLesser = y[x_i - 1]
    leftPercent = (halfMax - leftLesser) / (leftGreater - leftLesser)
    leftX = x[x_i - 1] + (leftPercent * (x[x_i] - x[x_i - 1]))
    print leftX
    print
    
    x_i = len(x) - 1
    while x_i >= 0 and y[x_i] <= peakY and y[x_i] < halfMax:
        print str(x_i) + ' (' + str(x[x_i]) + ', ' + str(y[x_i]) + ')'
        x_i -= 1
    rightGreater = y[x_i]
    rightLesser = y[x_i - 1]
    rightPercent = (halfMax - rightLesser) / (rightGreater - rightLesser)
    rightX = x[x_i - 1] + (rightPercent * (x[x_i] - x[x_i - 1]))
    print rightX
    print
    
    guessWidth = (abs(leftX - peakX) + abs(rightX - peakX))
    print guessWidth
    print
    return guessWidth

def guess_width2(x, y, peakX, peakY, backgroundY):
    stddev = N.std(x)
    print stddev
    guessWidth = 2 * N.sqrt(2 * N.log(2)) * stddev
    return guessWidth

def sigfig(x, n=6):
     if n < 1:
         raise ValueError("number of significant digits must be >= 1")
     return "%.*e" % (n - 1, x)
