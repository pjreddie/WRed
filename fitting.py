import os
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

import time

 

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
    print 
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
            x = simplejson.loads(request.POST['x'])
            y = simplejson.loads(request.POST['y'])
            functionID = int(request.POST['functionID'])
            request.session['x'] = x
            request.session['y'] = y
            request.session['functionID'] = functionID
            
            addlParams = { 'x': x, 'y': y, 'functionID': functionID, 'actionID': 2 }
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
                dragFit = createFit(request)
                dragFit.update({ 'dataType': 'doingDrag' })
                return HttpResponse(simplejson.dumps(dragFit))
            
            
            if not request.session['fitInstructions']:
                finishedFit = createFit(request)
                return HttpResponse(simplejson.dumps(finishedFit))
            else:
                #guess width
                #guessWidth = guess_width(x, y, peakX, peakY, backgroundY)
                #guessWidth2 = guess_width2(x, y, peakX, peakY, backgroundY)
                
                nextFitInstruction = request.session['fitInstructions'].popleft()
                
                response = fitInstructionResponse(nextFitInstruction, request.session['addlParams'])
                return HttpResponse(response)
            
            
        else:
            return HttpResponse('actionID not correct; it was ' + actionID)
            
    else:
        return HttpResponse('Not authenticated.')




def createFit(request):
      x = request.session['x']
      y = request.session['y']
      functionID = request.session['functionID']
      
      functionParams = getFunctionParams(functionID, request)
      print functionParams
      
      functionDomain = N.arange(x[0], x[-1], abs(x[-1] - x[0]) / 180)
      
      print x
      print functionDomain
      
      thefunction = getFunction(functionID)
      functionRange = thefunction(functionDomain, functionParams)
      functionData = zip(functionDomain, functionRange)
      
      functionY = thefunction(x, functionParams)
      functionResiduals = N.subtract(functionY, y)
      functionResidualData = zip(x, functionResiduals)
      

      print
      print functionRange
      print functionY
      print
      print '--------'
      print
      
      JSONobj = dict(fit=functionData, resid=functionResidualData)
      return JSONobj




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
                              { 'dataType': 'askPoint', 'xID': 'X1', 'yID': 'Y1',
                                'messageTitle': 'Step 1', 'messageText': 'Please click on the first point' },
                              { 'dataType': 'askDrag', 'xIDstart': 'X2', 'yIDstart': 'Y2', 'xIDend': 'X3', 'yIDend': 'Y3',
                                'messageTitle': 'Step 2', 'messageText': 'Please drag on the second point' }
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


def generateLinearFunction(domain, params):
    (X1, Y1, X2, Y2) = (params['X1'], params['Y1'], params['X2'], params['Y2'])
    slope = N.divide(Y2 - Y1, X2 - X1)
    return slope * N.subtract(domain, X1) + Y1
    
def generateGaussianFunction(domain, params):
    (peakX, peakY, backgroundY, stdDev) = (params['peakX'], params['peakY'], params['backgroundY'], params['stdDev'])
    return backgroundY + (peakY - backgroundY) * N.exp(- N.power(N.subtract(domain, peakX), 2) / 2 / N.power(stdDev, 2))
    
def generateLorentzianFunction(domain, params):
    (peakX, peakY, backgroundY, gamma) = (params['peakX'], params['peakY'], params['backgroundY'], params['gamma'])
    return backgroundY + (peakY - backgroundY) * N.divide(N.power(gamma, 2), N.power(N.subtract(domain, peakX), 2) + N.power(gamma, 2))


def getFunctionParams(functionID, request):
    functionParams = {}
    
    if functionID == 1:
        functionParams = { 'X1': request.session['X1'],
                           'Y1': request.session['Y1'],
                           'X2': request.session['X2'],
                           'Y2': request.session['Y2'] }
    elif functionID == 2:
        functionParams = { 'X1': request.session['X2'],
                           'Y1': request.session['Y2'],
                           'X2': request.session['X3'],
                           'Y2': request.session['Y3'] }
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
