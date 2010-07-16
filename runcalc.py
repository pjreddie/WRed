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
    
    #LOADING THE B MATRIX, UB MATRIX, AND STARS DICTIONARY FROM DJANGO'S CACHE
    Bmatrix = request.session['Bmatrix']
    UBmatrix = request.session['UBmatrix']
    stars = request.session['stars']
    
    response = []
    #wavelength was a string for some reason...
    #wavelength = float(data[0]['wavelength'])
    wavelength = data[0]['wavelength']
    
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
    
    #LOADING THE UB MATRIX AND STARS DICTIONARY FROM DJANGO'S CACHE
    UBmatrix = request.session['UBmatrix']
    stars = request.session['stars'] 
    

    #wavelength was a string for some reason...
    #wavelength = float(data[0]['wavelength'])
    wavelength = data[0]['wavelength']
    response = []    
    chi, phi = calcScatteringPlane ([data[0]['h1'], data[0]['k1'], data[0]['l1']], [data[0]['h2'], data[0]['k2'], data[0]['l2']], UBmatrix, wavelength) #calculate chi and phi (in DEGREES) for the Scattering Plane
    
    #calculations for the desired (h,k,l) vectors
    for i in range(1, data[0]['numrows'] + 1):
        twotheta, theta, omega = calcIdealAngles2([data[i]['h'], data[i]['k'], data[i]['l']], N.radians(chi), N.radians(phi), UBmatrix, wavelength, stars)
        angles = {'twotheta': twotheta, 'theta':theta, 'omega': omega,'chi':chi, 'phi': phi}
        response.append(angles)

    return HttpResponse(simplejson.dumps(response))
    
    
    
    
def calculateUB(request):
    "Calculates the UB matrix and stores it in Django for use in the runcal# methods"
    #requestObject = simplejson.loads(request.POST.keys()[0]) 
    #data = requestObject['data']
    #a, b, c, alpha, beta, gamma, h1, k1, l1, chi1, phi1, h2, k2, l2, chi2, phi2, wavelength = float(data[2]['a']), float(data[2]['b']), float(data[2]['c']), float(data[2]['alpha']), float(data[2]['beta']), float(data[2]['gamma']), float(data[0]['h']), float(data[0]['k']), float(data[0]['l']), float(data[0]['chi']), float(data[0]['phi']), float(data[1]['h']), float(data[1]['k']), float(data[1]['l']), float(data[1]['chi']), float(data[1]['phi']), float(data[2]['wavelength']
   
    #hardcoding in data for test purposes
    a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2, wavelength = 3.9091,3.9091,3.9091,90.,90.,90.,1.,1.,0.,0.,89.62,.001,0.,0.,1.,0.,-1.286,131.063, 2.35916
    
    #data given as  2 sets of {h,k,l,2theta,theta,chi,phi} and numberFields {a, b, c, alpha, beta, gamma, wavelength}
    #UB args: (h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)

    astar,bstar,cstar,alphastar,betastar,gammastar = star(a, b, c, alpha, beta, gamma)
    starDict = {'astar': astar, 'bstar': bstar, 'cstar': cstar, 'alphastar': alphastar, 'betastar': betastar, 'gammastar': gammastar}
    
    Bmatrix = calcB(astar,bstar,cstar,alphastar,betastar,gammastar,c, alpha)
    UBmatrix = calcUB(h1, k1, l1, h2, k2, l2, 0.0, chi1, phi1, 0.0, chi2, phi2, Bmatrix)
    

    #storing the B and UB matricies in the Django cache
    request.session['Bmatrix'] = Bmatrix
    request.session['UBmatrix'] = UBmatrix
    request.session['stars'] = starDict
    return HttpResponse('done')
