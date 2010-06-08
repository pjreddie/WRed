
import numpy as np
import scipy
import matcompat

# if available import pylab (from matlibplot)
try:
    import matplotlib.pylab as plt
except ImportError:
    pass

def findpeaktest():

    # Local Variables: y, x, p
    # Function calls: findpeak, abs, findpeaktest, exp
    x = np.arange(-1., 1.1, .1)
    p = np.array(np.hstack((100., 0., .1)))
    y = np.dot(np.abs(p[0]), np.exp(np.dot(-0.5, matdiv(x-p[1], p[2])**2.)))
    findpeak(x, y, 1.)
    return []
    return 
def findpeak(x, y, npeaks):

    # Local Variables: best_index, no_width, this_max, increment, ymin, yd2, half_height, ymax, width, wh_cross, fwhm, ysupport, n_crossings, ny, npeaks, elevation, F, full_height, yd, xsupport, y, value_sign, max_index, b, incrementr, g, i, no_widthl, n, p, no_widthr, indices, x, diff_sign, incrementl, xpeaks
    # Function calls: min, interp1, max, sgolay, length, abs, zeros, floor, diff, findpeak, find
    clear(p)
    #%This is a program that finds the positions and FWHMs in a set of
    #%data specified by x and y.  The user supplies the number of peaks and
    #%the program returns an array p, where the first entries are the positions of
    #%the peaks and the next set are the FWHMs of the corresponding peaks
    #%The program is adapted from a routine written by Rob Dimeo at NIST and
    #%relies on using a Savit-Golay filtering technique to obtain the derivative
    #%without losing narrow peaks.  The parameter F is the frame size for the smoothing
    #%and is set to 11 pts.  The order of the polynomial for making interpolations to better
    #%approximate the derivate is 4.  I have improved on Dimeo's program by also calculating second
    #%derivate information to better handle close peaks.  If peaks are too close together, there are
    #%still problems because the derivative may not turn over.  I have also added a refinement of going
    #%down both the left and right sides of the peak to determine the FWHMs because of the issue of peaks that
    #%are close together.
    #%William Ratcliff
    F = 11.
    [b, g] = sgolay(4., F)
    #%original
    #%g=sgolay(4,F);
    yd = np.zeros(1., length(x))
    yd2 = np.zeros(1., length(x))
    for n in np.arange((F+1.)/2., (length(x)-(F+1.)/2.)+1):
        yd[int(n)-1] = np.dot(g[:,1].conj().T, y[int(n-(F+1.)/2.+1.)-1:n+(F+1.)/1.0.].conj().T)
        yd2[int(n)-1] = np.dot(g[:,2].conj().T, y[int(n-(F+1.)/2.+1.)-1:n+(F+1.)/1.0.].conj().T)
        
    n_crossings = 0.
    #%npeaks=3;
    ny = length(yd)
    value_sign = 2.*(yd > 0.)-1.
    indices = 0.
    #% Determine the number of zero crossings
    #%diff_sign = value_sign(2:ny)-value_sign(1:ny-1);
    diff_sign = np.array(np.hstack((0., np.diff(value_sign))))
    wh_cross = nonzero(np.logical_and(np.logical_or(diff_sign == 2., diff_sign == -2.), yd2<0.))
    n_crossings = length(wh_cross)
    indices = np.dot(0.5, 2.*wh_cross-1.)
    no_width = 0.
    if n_crossings > 0.:
        #% Ok, now which ones of these are peaks?
    ysupport = np.arange(1., (length(y))+1)
    ymax = interp1(ysupport, y, indices)
    #%  ymax = interpolate(y,indices)
    ymin = matcompat.max(ymax)
    for i in np.arange(0., (npeaks-1.)+1):
        #%this_max = max(ymax,max_index)
        
    indices = best_index
    xsupport = np.arange(1., (length(x))+1)
    xpeaks = interp1(xsupport, x, indices)
    xpeaks = xpeaks[0:npeaks]
    for i in np.arange(1., (npeaks)+1):
        full_height = y[int(np.floor(indices[int(i)-1]))-1]
        half_height = np.dot(0.5, full_height)
        #% Descend down the peak until you get lower than the half height
        elevation = full_height
        incrementr = 0.
        while elevation > half_height:
            #% go down the right side of the peak
            
        #%now go to the left side of the peak
        #% Descend down the peak until you get lower than the half height
        elevation = full_height
        incrementl = 0.
        while elevation > half_height:
            #% go down the right side of the peak
            
        no_width = matcompat.max(no_widthl, no_widthr)
        increment = matcompat.max(np.abs(incrementl), incrementr)
        #%     no_width_found:
        if no_width:
            width = np.dot(2.0, x[int(ny)-1]-xpeaks[int(i)-1])
        else:
            width = np.dot(2.0, x[int((np.floor(indices[int(i)-1])+increment))-1]-xpeaks[int(i)-1])
            
        
        if i == 1.:
            fwhm = width
        else:
            fwhm = np.array(np.hstack((fwhm, width)))
            
        
        #%plot([(xpeaks(i)-fwhm(i)/2) (xpeaks(i)+fwhm(i)/2)],[half_height half_height]); hold on;
        
    #%hold off;
    #%b=length(fwhm);
    #%fwhm=fwhm(b);
    p = np.array(np.hstack((xpeaks, np.abs(fwhm))))
    return []
    
    return [p]
def fp_gaussian(x, area, center, fwhm):

    # Local Variables: center, area, sig, y, x, fwhm
    # Function calls: pi, exp, sqrt, fp_gaussian
    sig = matdiv(fwhm, 2.354)
    y = np.dot(matdiv(area, np.sqrt(np.dot(np.dot(2.0, np.pi), sig**2.))), np.exp(np.dot(-0.5, matdiv(x-center, sig)**2.)))
    return [[p]]
    return [y]