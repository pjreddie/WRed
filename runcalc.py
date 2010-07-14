import os
import simplejson

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from Alex.ubmatrix import *

def runcalc(request):
    print request.POST
    requestObject = simplejson.loads(request.POST.keys()[0])
    data = requestObject['data']
    Bmatrix, UBmatrix = convertData(data)
    omega = 0
    twotheta, theta, omega, chi, phi = calcIdealAngles([data[2]['h'], data[2]['k'], data[2]['l']], UBmatrix,omega,Bmatrix)

    response = {'twotheta': twotheta, 'theta':theta, 'omega': omega,'chi':chi, 'phi': phi }
    
    return HttpResponse(simplejson.dumps(response))

def convertData(data): 
    "Given a long list of data from the frontend, calculates the UBmatrix and returns it to runcalc"
    #data given as 2 sets of {h,k,l,2theta,theta,chi,phi} and numberFields {a, b, c, alpha, beta, gamma}
    #UB args: (h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)

    astar,bstar,cstar,alphastar,betastar,gammastar = star(data[2]['a'],data[2]['b'],data[2]['c'],data[2]['alpha'],data[2]['beta'],data[2]['gamma'])
   
    Bmatrix = calcB(astar,bstar,cstar,alphastar,betastar,gammastar,data[2]['c'], data[2]['alpha'])
    
    #print (data[0]['h'], data[0]['k'], data[0]['l'], data[1]['h'], data[1]['k'], data[1]['l'], 0, data[0]['chi'], data[0]['phi'], 0, data[1]['chi'], data[1]['phi'])

    UBmatrix = calcUB(data[0]['h'], data[0]['k'], data[0]['l'], data[1]['h'], data[1]['k'], data[1]['l'], 0, data[0]['chi'], data[0]['phi'], 0, data[1]['chi'], data[1]['phi'], Bmatrix)

    return Bmatrix, UBmatrix
