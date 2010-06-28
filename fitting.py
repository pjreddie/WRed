import os
from django.http import HttpResponse, HttpResponseRedirect
import simplejson
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from WRed.display.models import *
from WRed.display.fileToJson import displayfile


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
            return HttpResponse('Go ahead')
        elif actionID == '2':
            data = request.POST['data']
            x=0
            y=0
            height = request.POST['height']
            center = request.POST['center']
            # Calculate width here
            width = find_width(x, y, height, center)
            print width
            return HttpResponse('Height: ' + height + "\n" + 'Center: ' + center + "\n" + 'Width: ' + str(width))
        
        
        
        
        else:
            return HttpResponse('actionID not correct; it was ' + actionID)
            
    else:
        return HttpResponse('Not authenticated.')


def find_width(x, y, height, center):
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

