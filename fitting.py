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
        
        if actionID == '0':
            x = simplejson.loads(request.POST['x'])
            y = simplejson.loads(request.POST['y'])
            request.session['x'] = x
            request.session['y'] = y
            # FIXME
            background = 0
            request.session['background'] = background
            
            return HttpResponse('X: ' + str(x) + "\n" + 'Y: ' + str(y))
        elif actionID == '1':
            peakX = float(request.POST['peakX'])
            peakY = float(request.POST['peakY'])
            request.session['peakX'] = peakX
            request.session['peakY'] = peakY
            
            return HttpResponse('Peak X: ' + str(peakX) + "\n" + 'Peak Y: ' + str(peakY))
        elif actionID == '2':
            widthX = float(request.POST['widthX'])
            widthY = float(request.POST['widthY'])
            request.session['widthX'] = widthX
            request.session['widthY'] = widthY
            
            x = request.session['x']
            background = request.session['background']
            peakX = request.session['peakX']
            peakY = request.session['peakY']
            
            width = 2 * N.abs(widthX - peakX)
            request.session['width'] = width
            
            stdDev = width / 2 / N.sqrt(2 * N.log(2))
            
            gaussianFunction = (peakY - background) * N.exp(- N.power(N.subtract(x, peakX), 2) / 2 * stdDev)
            
            return HttpResponse('Width: ' + str(width))
        
        
        
        else:
            return HttpResponse('actionID not correct; it was ' + actionID)
            
    else:
        return HttpResponse('Not authenticated.')


def find_area(x, y, height, center, width, background):
    width = 0
    return width









def foo():
        try:
            md5 = DataFile.objects.get(id = idNum).md5
            all_objects = displayfile('db/' + md5 + '.file')
            data = simplejson.dumps(all_objects)
            return HttpResponse(data)
        except ObjectDoesNotExist:
            return HttpResponse('Oops! Datafile Does Not Exist')

