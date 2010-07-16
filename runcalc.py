import os
import simplejson
import numpy as N

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from Alex.ubmatrix import *


def runcalc1(request):
    "Calculations for omega = 0 mode"
    #print request.POST
    #Extracting data from dictionary key
    requestObject = simplejson.loads(request.POST.keys()[0]) 
    data = requestObject['data']
    
    #LOADING THE B AND UB MATRIX FROM DJANGO'S CACHE
    Bmatrix = request.session['Bmatrix']
    UBmatrix = request.session['UBmatrix']
    stars = request.session['stars']
    
    response = []
    wavelength = float(data[0]['wavelength'])
    
    #rest of the calculations
    for i in range(1, data[0]['numrows'] + 1):
        twotheta, theta, omega, chi, phi = calcIdealAngles([data[i]['h'], data[i]['k'], data[i]['l']], UBmatrix,Bmatrix, wavelength, stars)
        angles = {'twotheta': twotheta, 'theta':theta, 'omega': omega,'chi':chi, 'phi': phi}
        response.append(angles)

    return HttpResponse(simplejson.dumps(response))




def runcalc2(request):
    "Calculations for scattering plane mode"
    requestObject = simplejson.loads(request.POST.keys()[0])
    data = requestObject['data']
    
    #LOADING THE B AND UB MATRIX FROM DJANGO'S CACHE
    Bmatrix = request.session['Bmatrix']
    UBmatrix = request.session['UBmatrix']
    omega = 0
    
    #first calculation
    chi, phi, theta1, omega1, theta2, omega2 = calcIdealAngles2([data[0]['h1'], data[0]['k1'], data[0]['l1']], [data[0]['h2'], data[0]['k2'], data[0]['l2']], UBmatrix, data[0]['wavelength'])
    response = {'chi': chi, 'phi': phi, 'theta1': theta1, 'omega1': omega1,'theta2': theta2, 'omega2': omega2}
    
    #rest of the calculations
    #get code to calculate the 2theta
    '''for i in (data[0]['numrows']-1):
        twotheta, theta, omega, chi, phi = calcIdealAngles([data[i+2]['h'], data[i+2]['k'], data[i+2]['l']], UBmatrix, omega,Bmatrix)
        response = response + {'twotheta': twotheta, 'theta':theta, 'omega': omega,'chi':chi, 'phi': phi }
    '''
    return HttpResponse(simplejson.dumps(response))
    
    
    
    
def calculateUB(request):
    "Calculates the UB matrix and stores it in Django for use in the runcal# methods"
    #requestObject = simplejson.loads(request.POST.keys()[0]) 
    #data = requestObject['data']
    
    #hardcoding in data for test purposes
    a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2, wavelength = 3.9091,3.9091,3.9091,90,90,90,1,1,0,0,89.62,.001,0,0,1,0,-1.286,131.063, 2.35916
    data = {'h': h1, 'k': k1, 'l': l1, 'omega': omega1, 'chi': chi1, 'phi': phi1}, {'h': h2, 'k': k2, 'l': l2, 'omega': omega2, 'chi': chi2, 'phi': phi2}, {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma, 'wavelength': wavelength}
    
    #data given as  2 sets of {h,k,l,2theta,theta,chi,phi} and numberFields {a, b, c, alpha, beta, gamma, wavelength}
    #UB args: (h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)

    astar,bstar,cstar,alphastar,betastar,gammastar = star(data[2]['a'],data[2]['b'],data[2]['c'],data[2]['alpha'],data[2]['beta'],data[2]['gamma'])
    starDict = {'astar': astar, 'bstar': bstar, 'cstar': cstar, 'alphastar': alphastar, 'betastar': betastar, 'gammastar': gammastar}
    
    Bmatrix = calcB(astar,bstar,cstar,alphastar,betastar,gammastar,data[2]['c'], data[2]['alpha'])
    
    #print (data[0]['h'], data[0]['k'], data[0]['l'], data[1]['h'], data[1]['k'], data[1]['l'], 0, data[0]['chi'], data[0]['phi'], 0, data[1]['chi'], data[1]['phi'])

    UBmatrix = calcUB(data[0]['h'], data[0]['k'], data[0]['l'], data[1]['h'], data[1]['k'], data[1]['l'], 0, data[0]['chi'], data[0]['phi'], 0, data[1]['chi'], data[1]['phi'], Bmatrix)
    


    #storing the B and UB matricies in the Django cache
    request.session['Bmatrix'] = Bmatrix
    request.session['UBmatrix'] = UBmatrix
    request.session['stars'] = starDict
    return HttpResponse('done')
