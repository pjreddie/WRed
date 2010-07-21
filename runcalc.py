import os
import simplejson
import numpy as N
import csv #(Commma Separated Values)

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from Alex.ubmatrix import *


def runcalc1(request):
    "Calculations for omega = 0 mode"
    #print request.POST
    #Strangely, data is sent as a dictionary, where all data is the key and the dictionary's value is random characters.
    #Therefore, extracting data from dictionary key
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
    stars = request.session['stars'] #TODO check float 
    

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
    requestObject = simplejson.loads(request.POST.keys()[0]) 
    data = requestObject['data']
    a, b, c, alpha, beta, gamma, h1, k1, l1, twotheta1, theta1, chi1, phi1, h2, k2, l2, twotheta2, theta2, chi2, phi2 = float(data[2]['a']), float(data[2]['b']), float(data[2]['c']), float(data[2]['alpha']), float(data[2]['beta']), float(data[2]['gamma']), float(data[0]['h']), float(data[0]['k']), float(data[0]['l']), float(data[0]['twotheta']), float(data[0]['theta']), float(data[0]['chi']), float(data[0]['phi']), float(data[1]['h']), float(data[1]['k']), float(data[1]['l']), float(data[1]['twotheta']), float(data[1]['theta']), float(data[1]['chi']), float(data[1]['phi'])

    #hardcoding in data for test purposes
    a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2, wavelength, twotheta1, theta1, twotheta2, theta2 = 3.9091,3.9091,3.9091,90.,90.,90.,1.,1.,0.,0.,89.62,.001,0.,0.,1.,0.,-1.286,131.063, 2.35916, 50.522, 27.116, 35.125, 17.563
    
    #data given as  2 sets of {h,k,l,2theta,theta,chi,phi} and numberFields {a, b, c, alpha, beta, gamma, wavelength}
    #UB args: (h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)
    omega1 = theta1 - twotheta1/2
    omega2 = theta2 - twotheta2/2
    
    astar, bstar, cstar, alphastar, betastar, gammastar = star(a, b, c, alpha, beta, gamma)
    starDict = {'astar': astar, 'bstar': bstar, 'cstar': cstar, 'alphastar': alphastar, 'betastar': betastar, 'gammastar': gammastar}
    
    Bmatrix = calcB(astar,bstar,cstar,alphastar,betastar,gammastar,c, alpha)
    UBmatrix = calcUB(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)
    

    #storing the B and UB matricies in the Django cache
    request.session['Bmatrix'] = Bmatrix
    request.session['UBmatrix'] = UBmatrix
    request.session['stars'] = starDict
    return HttpResponse([UBmatrix[0][0],', ', UBmatrix[0][1],', ', UBmatrix[0][2],', ', UBmatrix[1][0],', ', UBmatrix[1][1],', ', UBmatrix[1][2],', ', UBmatrix[2][0],', ', UBmatrix[2][1],', ', UBmatrix[2][2]])
    
    #return HttpResponse(simplejson.dumps(UBmatrix)) #not working atm
    #return HttpResponse(UBmatrix)
    
    
    
    
def makeSaveFile (request):
    requestObject = simplejson.loads(request.POST.keys()[0]) 
    data = requestObject['data']
    dataWriter = csv.writer(open('savedata.txt'), delimiter= ', ', quoting=csv.QUOTE_NONE)
    dataWriter.writerow(['#Data input file for angleCalculator'])
    dataWriter.writerow(['#File downloaded from angleCalculator: (DATE HERE)'])
    dataWriter.writerow(['#WARNING: editing this file may result in a loss of data when loaded)'])
    
    dataWriter.writerow(['#mode'])
    dataWriter.writerow([data[0]['mode']])
    
    dataWriter.writerow(['#a b c alpha beta gamma wavelength'])
    dataWriter.writerow([data[0]['a'], data[0]['b'], data[0]['c'], data[0]['alpha'], data[0]['beta'], data[0]['gamma'], data[0]['wavelength']])
    
    dataWriter.writerow(['#observations h k l twotheta theta chi phi'])
    dataWriter.writerow([data[1]['h'], data[1]['k'], data[1]['l'], data[1]['twotheta'], data[1]['theta'], data[1]['chi'], data[1]['phi']])
    dataWriter.writerow([data[2]['h'], data[2]['k'], data[2]['l'], data[2]['twotheta'], data[2]['theta'], data[2]['chi'], data[2]['phi']])
    
    dataWriter.writerow(['#UBmatrix'])
    dataWriter.writerow([data[0]['ub'][0], data[0]['ub'][1], data[0]['ub'][2], data[0]['ub'][3], data[0]['ub'][4], data[0]['ub'][5], data[0]['ub'][6], data[0]['ub'][7], data[0]['ub'][8]])
    
    
    dataWriter.writerow(['#Scattering Plane Vectors h k l'])
    dataWriter.writerow([data[0]['h1'], data[0]['k1'], data[0]['l1']])
    dataWriter.writerow([data[0]['h1'], data[0]['k2'], data[0]['l2']])

    dataWriter.writerow(['#desired h k l twotheta theta omega chi phi'])
    for i in range(3, data[0]['numrows'] + 3):
        dataWriter.writerow([data[i]['h'], data[i]['k'], data[i]['l'], data[i]['twotheta'], data[i]['theta'], data[i]['omega'], data[i]['chi'], data[i]['phi']])
    
'''
------- A sample file...... ----------
#Data input file for angleCalculator
#File downloaded from angleCalculator: (DATE HERE)
#WARNING: editing this file may result in a loss of data when loaded

#mode
Scattering Plane

#a b c alpha beta gamma wavelength
3.9091, 3.9091, 3.9091, 90, 90, 90, 2.35916 

#observations h k l twotheta theta chi phi
1, 1, 0, 50.522, 27.116, 89.62, 0.001
0, 0, 1, 35.125, 17.563, -1.286, 131.063

#UBmatrix
-0.8495486120866541, 0.8646150711829229, -1.055554030805845, -0.7090402876860106, 0.7826211792587279, 1.211714627203656, 1.165768160358335, 1.106088263216144, -0.03224481098900243

#Scattering Plane Vectors h k l
1, 0, 0
0, 1, 1

#desired h k l twotheta theta omega chi phi
1, 1, 1, 666, -126.83, 666, -59.948, -12.5967
'''
