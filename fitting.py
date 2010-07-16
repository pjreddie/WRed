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
            function = getFunctionClass(functionID)()
            
            request.session['xData'] = xData
            request.session['yData'] = yData
            request.session['functionID'] = functionID
            request.session['function'] = function
            
            addlParams = { 'xData': xData, 'yData': yData, 'functionID': functionID, 'actionID': 2 }
            request.session['addlParams'] = addlParams
            

            nextFitInstruction = function.fitInstructions.popleft()
            
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
                function = request.session['function']
                function.setFunctionParamsFromRequest(request)
                
                dragFit = createFunction(xData, yData, function)
                dragFit.update({ 'dataType': 'doingDrag' })
                return HttpResponse(simplejson.dumps(dragFit))
            
            
            if not request.session['function'].fitInstructions:
                xData = request.session['xData']
                yData = request.session['yData']
                function = request.session['function']
                function.setFunctionParamsFromRequest(request)
                
                finishedFunction = createFunction(xData, yData, function)
                return HttpResponse(simplejson.dumps(finishedFunction))
            else:
                #guess width
                #guessWidth = guess_width(xData, yData, peakX, peakY, backgroundY)
                #guessWidth2 = guess_width2(xData, yData, peakX, peakY, backgroundY)
                
                nextFitInstruction = request.session['function'].fitInstructions.popleft()
                
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
            function = getFunctionClass(functionID)()
            function.setFunctionParamsFromRequest(request)
            params = function.getFunctionParamsAsArray()
            
            
            functkw = { 'xData': xData, 'yData': yData, 'yErr': yErrData, 'function': function }
            mpfitResult = mpfit(mpfitFunction, params, functkw=functkw)
            
            function.functionParams = function.getFunctionParamsFromArray(mpfitResult.params)

            finishedFit = createFunction(xData, yData, function)
            chiSquared = sigfig(chisq(xData, yData, yErrData, function))
            
            # Map sigfig 
            fitFunctionParams = function.getFunctionParamsFromArray(map(sigfig, mpfitResult.params))
            fitFunctionParamsErr = function.getFunctionParamsFromArray(map(sigfig, mpfitResult.perror))
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




def createFunction(xData, yData, function):
      functionDomain    = N.arange(min(xData), max(xData), abs(max(xData) - min(xData)) / 180.)
      functionDataRange = N.arange(min(yData), max(yData), abs(max(yData) - min(yData)) / 180.)
      
      functionRange = function.function(functionDomain, functionDataRange)
      functionData = zip(functionDomain, functionRange)
      
      functionY = function.function(xData, yData)
      functionResiduals = N.subtract(functionY, yData)
      functionResidualData = zip(xData, functionResiduals)

      

      print
      print functionRange
      print functionY
      print
      print '--------'
      print
      
      JSONobj = dict(fit=functionData, resid=functionResidualData, functionID=function.functionID, functionParams=function.functionParams)
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
    
    return simplejson.dumps(returnResponse)

def objectToArrayPairs(d):
    return [dict(name=key, value=value) for key, value in d.iteritems()]

def paramsJoin(d1, d2):
    n = []
    for (key, value) in d1.items():
        n.append({ 'name': key, 'value': value, 'err': d2[key] })
    return n


# --

# Copied straight from William
def chisq(xData, yData, yErr, function):
    yCalc = function.function(xData, yData)
    
    yErr_temp = copy.deepcopy(yErr)
#    zero_loc = N.where(yErr == 0)[0]
#    if len(zero_loc) != 0:
#        yErr_temp[zero_loc] = 1.0
    chi = ((yData - yCalc) / yErr_temp) ** 2
    
    return chi.sum() / (len(yData) - len(function.functionParams))


def mpfitFunction(params, parinfo=None, fjac=None, xData=None, yData=None, yErr=None, function=None):
    # Parameter values are passed in "params"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default flag.
    
    function.functionParams = function.getFunctionParamsFromArray(params)
    yCalc = function.function(xData, yData)
    
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
