import os
import simplejson
import numpy as N
import csv #(Commma Separated Values)
import datetime

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
    #a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2, wavelength, twotheta1, theta1, twotheta2, theta2 = 3.9091,3.9091,3.9091,90.,90.,90.,1.,1.,0.,0.,89.62,.001,0.,0.,1.,0.,-1.286,131.063, 2.35916, 50.522, 27.116, 35.125, 17.563
    
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
    "Saves the current data in a text file named 'savedata.txt', overwriting the previous text file so there is minimal data storage. Then lets user download the file."
    
    requestObject = simplejson.loads(request.POST.keys()[0]) 
    data = requestObject['data']
    
    #today = datetime.datetime.now()
    #datafile = 'savedata' +today.month + today.day + today.year + '.txt'
    
    #http://docs.python.org/tutorial/inputoutput.html - section 7.2 has information on opening files;
    # open ('filename', 'letter') where letter = 'w' (overwrite), 'r' (read), 'r+' (read and write), 'a' (append, not overwrite)
    #dataWriter = csv.writer(open(datafile, 'w'), delimiter= ',', escapechar ='', quoting=csv.QUOTE_NONE)
    dataWriter = csv.writer(open('savedata.txt', 'w'), delimiter= ',', escapechar ='', quoting=csv.QUOTE_NONE)
    
    dataWriter.writerow(['#Data input file for angleCalculator.'])
    #dataWriter.writerow(['#File downloaded from angleCalculator: '])
    #dataWriter.writerow([theDate])
    dataWriter.writerow(['#WARNING: editing this file may result in a loss of data when loaded.'])
    dataWriter.writerow([' '])
    
    dataWriter.writerow(['#mode'])
    dataWriter.writerow([data[0]['mode']])
    dataWriter.writerow([' '])
    
    dataWriter.writerow(['#a b c alpha beta gamma wavelength'])
    dataWriter.writerow([data[0]['a'], data[0]['b'], data[0]['c'], data[0]['alpha'], data[0]['beta'], data[0]['gamma'], data[0]['wavelength']])
    dataWriter.writerow([' '])
    
    dataWriter.writerow(['#observations h k l twotheta theta chi phi'])
    dataWriter.writerow([data[1]['h'], data[1]['k'], data[1]['l'], data[1]['twotheta'], data[1]['theta'], data[1]['chi'], data[1]['phi']])
    dataWriter.writerow([data[2]['h'], data[2]['k'], data[2]['l'], data[2]['twotheta'], data[2]['theta'], data[2]['chi'], data[2]['phi']])
    dataWriter.writerow([' '])
    
    dataWriter.writerow(['#UBmatrix'])
    dataWriter.writerow([data[0]['ub'][0], data[0]['ub'][1], data[0]['ub'][2], data[0]['ub'][3], data[0]['ub'][4], data[0]['ub'][5], data[0]['ub'][6], data[0]['ub'][7], data[0]['ub'][8]])
    dataWriter.writerow([' '])
    
    dataWriter.writerow(['#Scattering Plane Vectors h k l'])
    dataWriter.writerow([data[0]['h1'], data[0]['k1'], data[0]['l1']])
    dataWriter.writerow([data[0]['h2'], data[0]['k2'], data[0]['l2']])
    dataWriter.writerow([' '])
    
    dataWriter.writerow(['#desired h k l twotheta theta omega chi phi'])
    for i in range(3, data[0]['numrows'] + 3):
        dataWriter.writerow([data[i]['h'], data[i]['k'], data[i]['l'], data[i]['twotheta'], data[i]['theta'], data[i]['omega'], data[i]['chi'], data[i]['phi']])
    dataWriter.writerow(['#End desired'])
    
    return HttpResponse('saved.')
    
    
    
def downloadFile (request):
    
    data = file('savedata.txt')
    response = HttpResponse(data, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + rFile.name
    return HttpResponse(response)
    

def uploadFile (request):
    #TODO PLAY W/ THIS
    filename = 'savedata.txt'
    #filename = request.FILES['file'] # not working properly yet - ERROR OCCURING HERE WHEN LOAD BUTTON PUSHED FOR THIS LINE
    response = []

    #open(filename, letter) --> letter defaults to 'r' (read only)
    dataReader = csv.reader(open(filename), delimiter=',')
    data = []
    for row in dataReader:
        data.append(', '.join(row)) #making an array of row Strings.
        
    modenum = data.index('#mode')  
    latticenum = data.index('#a b c alpha beta gamma wavelength')
    observationsnum = data.index('#observations h k l twotheta theta chi phi')
    scatteringnum = data.index('#Scattering Plane Vectors h k l')
    desirednum = data.index('#desired h k l twotheta theta omega chi phi')
    enddesirednum = data.index('#End desired')
    
    if (modenum < 0 or latticenum < 0 or observationsnum < 0 or scatteringnum < 0 or desirednum < 0):
        #if any of the data titles aren't found, input fails
        #TODO make sure it fails here; bellow line counts as success, I think
        return HttpResponse('failed')
    else:
        #getting the lattice data
        latticearr = data[latticenum+1].split(',')
        thelattice = []
        for x in latticearr:
            thelattice.append(float(x))
        
        #getting the scattering plane vectors
        thespvectors = []
        sparr1 = data[scatteringnum+1].split(',')
        for x in sparr1:
            thespvectors.append(float(x))
        
        sparr2 = data[scatteringnum+2].split(',')
        for x in sparr2:
            thespvectors.append(float(x))    

        #putting the mode data, lattice data, and scattering plane vectors into response[0]
        response0 = {'mode': data[modenum+1], 'a': thelattice[0], 'b': thelattice[1], 'c': thelattice[2], 'alpha': thelattice[3], 'beta': thelattice[4], 'gamma': thelattice[5], 'wavelength': thelattice[6], 'h1': thespvectors[0], 'k1': thespvectors[1],'l1': thespvectors[2], 'h2': thespvectors[3], 'k2': thespvectors[4], 'l2': thespvectors[5]}
        response.append(response0)
        
        #getting observation data
        theobservations = []
        obsarr1 = data[observationsnum+1].split(',')
        for x in obsarr1:
            theobservations.append(float(x)) #indicies 0-6
            
        obsarr2 = data[observationsnum+2].split(',')
        for x in obsarr2:
            theobservations.append(float(x)) #indicies 7-13
            
        response1 = {'h': theobservations[0], 'k': theobservations[1], 'l': theobservations[2], 'twotheta': theobservations[3], 'theta': theobservations[4], 'chi': theobservations[5], 'phi': theobservations[6]}
        response.append(response1)
        
        response2 = {'h': theobservations[7], 'k': theobservations[8], 'l': theobservations[9], 'twotheta': theobservations[10], 'theta': theobservations[11], 'chi': theobservations[12], 'phi': theobservations[13]}
        response.append(response2)
        
        #getting the ideal data
        theidealdata = [] #going to be re-filled for each new row of data
        for i in range(desirednum+1, enddesirednum):
            idealarr = data[i].split(',')
            
            for x in idealarr:
                theidealdata.append(float(x))
            
            desiredresponses = {'h': theidealdata[0], 'k': theidealdata[1], 'l': theidealdata[2], 'twotheta': theidealdata[3], 'theta': theidealdata[4], 'omega': theidealdata[5], 'chi': theidealdata[6], 'phi': theidealdata[7]}
            response.append(desiredresponses)
            
        return HttpResponse(simplejson.dumps(response))

