import os, time, copy
import simplejson
from collections import deque

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from WRed.display.models import *
from WRed.file_parsing.file_to_json import displayfile

import numpy as N
from WRed.utilities.mpfit import mpfit

from fitting_functions import *


def print_timing(func):
  def wrapper(*arg):
    t1 = time.time()
    res = func(*arg)
    t2 = time.time()
    print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
    return res
  return wrapper



@print_timing
@login_required
def fitting_request_action(request, idNum):
    print 'USERNAME: ', request.user.username
    print 'Authenticated: ', request.user.is_authenticated()
    #print 'Request: ', request.POST
    
    if request.user.is_authenticated() and (request.user.username == str(idNum) or request.user.is_superuser):
        try:
            actionID = request.POST['actionID']
            actionName = request.POST['actionName']
        except (KeyError):
            return HttpResponse('No POST data')

        print 'You are trying to request the following action: ' + actionName + ' [ID: ' + actionID + ']'
        
        
        if actionID == '1':
            data = simplejson.loads(request.POST['data'])
            prevFunctions = simplejson.loads(request.POST['prevFunctions'])
            replaceIndices = simplejson.loads(request.POST['replaceIndices'])
            
            xData = simplejson.loads(request.POST['data'])['x']
            yData = simplejson.loads(request.POST['data'])['y']
            functionID = int(request.POST['functionID'])
            function = getFunctionClass(functionID)()
            
            request.session['replaceIndices'] = replaceIndices
            request.session['xData'] = xData
            request.session['yData'] = yData
            request.session['functionID'] = functionID
            request.session['function'] = function
            
            
            functionGroup = FunctionGroup()
            functionGroup.data = data
            
            if len(prevFunctions):
                for prevFunctionInfo in prevFunctions:
                    prevFunction = getFunctionClass(prevFunctionInfo['functionID'])()
                    prevFunction.functionParams = prevFunctionInfo['functionParams']
                    functionGroup.functions.append(prevFunction)
                    
            functionGroup.functions.append(function)

            request.session['functionGroup'] = functionGroup
            print functionGroup.functions
            print '^^^^^^^^^^^^^^'
            
            addlParams = { 'functionID': functionID, 'actionID': 2 }  # 'xData': xData, 'yData': yData, 
            request.session['addlParams'] = addlParams
            

            nextFitInstruction = function.fitInstructions.popleft()
            
            response = fitInstructionResponse(nextFitInstruction, addlParams)
            return HttpResponse(simplejson.dumps(response))
            
            
        elif actionID == '2':
            xData = request.session['xData']
            yData = request.session['yData']
            function = request.session['function']
            functionGroup = request.session['functionGroup']
            
            
            # Data Types
            if request.POST['dataType'] == 'askPoint':
                request = defPoint(request, functionGroup)
            elif request.POST['dataType'] == 'askDrag':
                request = defPoint(request, functionGroup)

                function.setFunctionParamsFromRequest(request)
                
                # Update most recent function (maybe this is wrong)
                functionGroup.functions[-1] = function
                
                dragFit = functionGroup.createFunction(xData, yData)
                dragFit.update({ 'dataType': 'doingDrag', 'replaceIndices': request.session['replaceIndices'], 'dragMode': request.POST['dragMode'] })
                return HttpResponse(simplejson.dumps(dragFit))
            
            
            if not request.session['function'].fitInstructions:
                function.setFunctionParamsFromRequest(request)
                
                # Update most recent function (maybe this is wrong)
                functionGroup.functions[-1] = function
                
                finishedFunction = functionGroup.createFunction(xData, yData)
                print finishedFunction
                print '############'
                
                response = finishedFunction
                response.update({ 'replaceIndices': request.session['replaceIndices'] })
                
                return HttpResponse(simplejson.dumps(response))
            else:
                #guess width
                #guessWidth = guess_width(xData, yData, peakX, peakY, backgroundY)
                #guessWidth2 = guess_width2(xData, yData, peakX, peakY, backgroundY)
                
                nextFitInstruction = function.fitInstructions.popleft()
                if nextFitInstruction['dataType'] == 'askDrag':
                    nextFitInstruction.update({ 'dragMode': 'before' })
                
                response = fitInstructionResponse(nextFitInstruction, request.session['addlParams'])
                response.update({ 'replaceIndices': request.session['replaceIndices'] })
                return HttpResponse(simplejson.dumps(response))
            
        elif actionID == '3':
            allData = simplejson.loads(request.POST['allData'])
            dataData = allData[0]
            xData = dataData['x']
            yData = dataData['y']
            yErrData = dataData['yerr']
            
            
            #functionData = simplejson.loads(request.POST['functionData']) # Not used at all
            
            allFunctionInfos = simplejson.loads(request.POST['allFunctionInfos'])
            functionGroup = FunctionGroup()
            functionGroup.data = dataData
            
            for functionInfos in allFunctionInfos:
                for functionInfo in functionInfos:
                    print functionInfo
                    functionID = int(functionInfo['functionID'])
                    functionParams = functionInfo['functionParams']
                    function = getFunctionClass(functionID)()
                    function.setFunctionParamsFromDict(functionParams)
                    functionGroup.functions.append(function)
            
            (params, slices) = functionGroup.getFunctionsParamsAsArray()
            
            functkw = { 'xData': xData, 'yData': yData, 'yErr': yErrData, 'functionGroup': functionGroup, 'slices': slices }
            mpfitResult = mpfit(mpfitFunction, params, functkw=functkw,ftol=1e-5)
            
            functionGroup.setFunctionsParamsFromArray(mpfitResult.params, slices)

            finishedFit = functionGroup.createFunction(xData, yData)
            chiSquared = sigfig(functionGroup.chisq(xData, yData, yErrData))
            
            fitFunctionInfos = []
            pointer = 0
            counter = 0
            for function in functionGroup.functions:
                mpfitFunctionResult = dict(params=mpfitResult.params[pointer : pointer + slices[counter]],
                                           perror=mpfitResult.perror[pointer : pointer + slices[counter]])
                
                # Map sigfigs
                fitFunctionParams = function.getFunctionParamsFromArray(map(sigfig, mpfitResult.params))
                fitFunctionParamsErr = function.getFunctionParamsFromArray(map(sigfig, mpfitResult.perror))
                fitFunctionParamsArray = paramsJoin(fitFunctionParams, fitFunctionParamsErr)       
                
                fitFunctionInfo = { 'fitFunctionParams': fitFunctionParams, 'fitFunctionParamsErr': fitFunctionParamsErr,
                                    'fitFunctionParamsArray': fitFunctionParamsArray }
                fitFunctionInfo.update(function.getJSON())
                
                fitFunctionInfos.append(fitFunctionInfo)
                
                pointer += slices[counter]
                counter += 1
            
            print fitFunctionInfos
            print '*****'
            print

            response = finishedFit
            response.update({ 'functionInfos': fitFunctionInfos, 'fitInfo': { 'chisq': chiSquared },
                              'replaceIndices': simplejson.loads(request.POST['replaceIndices']), 'dataType': 'doFit' })
            return HttpResponse(simplejson.dumps(response))
            
        else:
            return HttpResponse('actionID not correct; it was ' + actionID)
            
    else:
        return HttpResponse('Not authenticated.')



# --

def defPoint(request, functionGroup):
    xPos = float(request.POST['xPos'])
    yPos = float(request.POST['yPos'])
    
    # We need to subtract the value from rest of the functions
    if len(functionGroup.functions) > 1:
        yPos -= functionGroup.getValueAtX(xPos)
    
    request.session[request.POST['xID']] = xPos
    request.session[request.POST['yID']] = yPos
    return request

def defDrag(request):
    request.session[request.POST['xIDstart']] = float(request.POST['xPosstart'])
    request.session[request.POST['yIDstart']] = float(request.POST['yPosstart'])
    request.session[request.POST['xIDend']]   = float(request.POST['xPosend'])
    request.session[request.POST['yIDend']]   = float(request.POST['yPosend'])
    return request



def getFunctionClass(functionID):
    d = { 1:  Linear,
          2:  LinearDrag,
          11: Gaussian,
          12: GaussianDrag,
          21: Lorentzian,
          22: LorentzianDrag }
    return d[functionID]



def fitInstructionResponse(fitInstruction, addlParams):
#    returnResponse = { 'dataType': fitInstruction['dataType'], 'xID': fitInstruction['xID'], 'yID': fitInstruction['yID'],
#                       'messageTitle': fitInstruction['messageTitle'], 'messageText': fitInstruction['messageText'] }
    returnResponse = fitInstruction
    returnResponse.update(addlParams)
    
    return returnResponse

def objectToArrayPairs(d):
    return [dict(name=key, value=value) for key, value in d.iteritems()]

def paramsJoin(d1, d2):
    n = []
    for (key, value) in d1.items():
        n.append({ 'name': key, 'value': value, 'err': d2[key] })
    return n


# --

# Copied straight from William



def mpfitFunction(params, parinfo=None, fjac=None, xData=None, yData=None, yErr=None, functionGroup=None, slices=None):
    # Parameter values are passed in "params"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default flag.

    functionGroup.setFunctionsParamsFromArray(params, slices)
    yCalc = functionGroup.function(xData, yData)
    
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
