import os
import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from WRed.display.models import *
from WRed.display.fileToJson import displayfile

import numpy as N


@login_required
def fitting_request_action(request, idNum):
    print 'USERNAME: ', request.user.username
    print 'Authenticated: ', request.user.is_authenticated()
    
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
            background = float(request.POST['backgroundX'])
            request.session['x'] = x
            request.session['y'] = y
            request.session['background'] = background
            
            return HttpResponse('X: ' + str(x) + "\n" + 'Y: ' + str(y))
            
        elif actionID == '2':
            peakX = float(request.POST['peakX'])
            peakY = float(request.POST['peakY'])
            request.session['peakX'] = peakX
            request.session['peakY'] = peakY
            
            #guess width
            x = request.session['x']
            y = request.session['y']
            background = request.session['background']
            guessWidth = guess_width(x, y, peakX, peakY, background)
            guessWidth2 = guess_width2(x, y, peakX, peakY, background)
            
            
            return HttpResponse('Peak X: ' + str(peakX) + "\n" + 'Peak Y: ' + str(peakY) + "\n" + 'Guess width: ' + str(guessWidth) + "\n" + 'Guess width 2: ' + str(guessWidth2))
            
        elif actionID == '3':
            widthX = float(request.POST['widthX'])
            widthY = float(request.POST['widthY'])
            request.session['widthX'] = widthX
            request.session['widthY'] = widthY
            
            x = request.session['x']
            y = request.session['y']
            background = request.session['background']
            peakX = request.session['peakX']
            peakY = request.session['peakY']
            
            width = 2 * N.abs(widthX - peakX)
            request.session['width'] = width
            
            stdDev = width / 2 / N.sqrt(2 * N.log(2))
            
            gaussianDomain = N.arange(x[0], x[-1], abs(x[-1] - x[0]) / 100)
            gaussianFunction = generateGaussianFunction(gaussianDomain, peakX, peakY, background, stdDev)
            gaussianData = zip(gaussianDomain, gaussianFunction)
            
            
            gaussianResiduals = N.subtract(generateGaussianFunction(x, peakX, peakY, background, stdDev), x)
            print gaussianResiduals
            gaussianResidualData = zip(x, gaussianResiduals)
            
            JSONobj = dict(fit=gaussianData, resid=gaussianResidualData)
            
            
            #return HttpResponse('Width: ' + str(width))
            return HttpResponse(simplejson.dumps(JSONobj))
        
        
        
        else:
            return HttpResponse('actionID not correct; it was ' + actionID)
            
    else:
        return HttpResponse('Not authenticated.')


def guess_width(x, y, peakX, peakY, background):
    halfMax = (peakY - background) / 2.
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

def guess_width2(x, y, peakX, peakY, background):
    stddev = N.std(x)
    print stddev
    guessWidth = 2 * N.sqrt(2 * N.log(2)) * stddev
    return guessWidth
    
def generateGaussianFunction(domain, peakX, peakY, background, stdDev):
    return background + (peakY - background) * N.exp(- N.power(N.subtract(domain, peakX), 2) / 2 / N.power(stdDev, 2))
