#!/usr/bin/env python
# This program is public domain
# Author: Paul Kienzle
"""
Read xpeek stream.

XPeek is a class which captures an xpeek data stream and prepares
it for display.  You interact with the class by inheriting from
it and overriding the the newstream and newpoint methods.

See the following for a description of the XPeek stream::

  http://www.ncnr.nist.gov/programs/reflect/data_reduction/software/xpeek.html

Data lines on the graph are defined by a lineid.  This is usually
the instrument name, though in the case of polarized NG1 and CG1
data, their are multiple lineids associated with the stream.

Here is a simple example which prints a part of the data stream::

    class XPeekPrint(xpeek.XPeek):
        def newdata(self, lineid):
            # Called when there is a new line
            data = self.data[lineid]
            print lineid,"starting",data.filename,"primary",data.primary
        def enddata(self, lineid):
            # Called when the line is complete and a peak has been fitted
            data = self.data[lineid]
            print lineid,"peak",data.peak
        def newpoint(self, lineid):
            # Called when there is a new point for the line
            data = self.data[lineid]
            print lineid,data.timestamp(), \
                "point",len(data.columns['DATA']),\
                data.columns[data.primary][-1],\
                data.columns['DATA'][-1]

Open the stream and process the data::

    xpeek = XPeekPrint(instrument)
    xpeek.process_stream()  # Process the stream [I should call this swim()]

You will need Ctrl-C to break the program since process() loops forever.

In general, newpoint should generate a new plot and display it to
the user each time it is called.  You should display the time
stamp of the last point (self.data[lineid].timestamp()) and the
position in the measurement len(self.data[lineid].columns['DATA'])
and the number of points scheduled (self.data[lineid].points).

See help on Data1D and XPeek for details on the individual fields
and methods.

When subclassing, use logging package to report errors.  These will
show up in the log file for the viewer::

    import logging
    ...
    logging.error("error message")
"""
import math
import socket
import os
import sys
import time
import logging
import traceback
import errno
import thread
import numpy

HOST = "charlotte.ncnr.nist.gov"
#HOST = "jazz.ncnr.nist.gov"
PORT = 1010
BUFFER_SIZE = 1024

NG7_PSD_BEAM_CENTER = 131
NG7_PSD_BEAM_WIDTH = 11
BT7_MOTORS = [ 'E', 'Qx', 'Qy', 'Qz', 'DFM', 'A2', 'A3', 'A4', 'A5', 'A6',
               'Temp', 'magfield' ]

class Data1D(object):
    """
    Set of data columns from xpeek.

    This data structure maintains the current run for an instrument.

    It is created when a new measurement is started and each time
    a new point is received on the xpeek stream it is added to the
    run.  Everything needed to plot the run is contained herein.

    Attributes::

     *columns*     dictionary of column name, each with a list of values
     *points*      number of points expected in the final dataset
     *independent* list of fields being scanned
     *dependent*   list of dependent fields (used by NSE)
     *primary*     column to plot along the x direction
     *pixels*      number of pixels in the data column
     *comment*     comment field from the file
     *filename*    filename
     *runid*       three digit run number
     *peak*        a fitted peak function, or None if not fitted

    Methods::

     *timestamp*   formatted time of last read point
     *eta*         formatted estimate of run completion time
     *time_remaining* estimate of time required to complete the run

    If any columns are multivalued, then they will have a list of
    values rather than a single value.

    Important columns::

        PT         point number
        DATA       counts (except NSE, NG4)
        TIMESTAMP  time the data was measured (seconds since 1970/01/01)

    Additional columns that may be present::

        BT1: T, M, MON
        BT4, BT9, NG5: QH, QK, QL, ENERGY, T
        BT5: M
        BT7: Temp, Mon, Det, Time, PSDC00..PSDC47
        NG1, CG1: M, A01, A02, A03, A04, A05, A06
        NG4: PSD
        NG7: MON, SC1, QX, QZ, A08, A16, MON
        NSE: PHASECURRENT CHANNEL1..CHANNEL10 RING1..RING6, BSpi(|21|22)[xyz]

    BT7 has issues.  ICE does not provide useful columns to XPeek so it
    has been hacked with primary='PT' and PSDC.. gathered into DATA.
    """
    def __init__(self, instrument, fields):
        """
        Create a new data set.

        Fields should be a list of header fields: NPTS,VARY and FILE.
        The final field should be the comment.
        """
        self.instrument = instrument
        self.peak = None # No peak yet
        # BT7 appears not to have a comment field
        self.comment = fields.pop()
        self.points = 0
        self.independent = []
        self.dependent = []
        self.file = 'unknown'
        self.pixels = 0
        try:
            for f in fields: k,v = f.split('=')  # verify Key=Value pairs
        except:
            raise ValueError("incorrect line format; use tabs to separate FIELD=value pairs")

        for f in fields:
            k,v = f.split('=')
            if k == 'NPTS':
                try:
                    self.points = int(v)
                except ValueError:
                    self.points = 1  # Sometimes records ******** for NPTS
            elif k == 'VARY':
                self.independent = v.split()
            elif k == 'DEPEND':
                self.dependent = v.split()
            elif k == 'FILE':
                self.filename = v
                # runid is filename without directory and extension
                v = os.path.basename(v)
                idx = v.find('.')
                if idx>0: v = v[:idx]
                self.runid = v
            elif k == 'TYPE':
                self.scantype = v
            else:
                logging.error("Unknown start field %s in %s"%(k,fields))
        self.columns = {}
        # Varying defaults to 'PT'
        if self.independent == []: self.independent = ['PT']
        self.primary = self.independent[0]
        if instrument == 'NSE':
            self.primary = 'PT'
        if instrument == 'BT7' and self.primary not in BT7_MOTORS:
            self.primary = 'PT'

    def add_point(self, fields):
        """
        Receive another data point.

        Fields is a list of strings column=value.

        Used by the xpeek stream processor to add another data point.

        You will likely need to specialize this function and the plot 
        function for the particulars of the instruments as new capabilities
        are added for the instruments.
        """
        # Convert fields into numbers or lists, checking for duplicates
        columns = {}
        for f in fields:
            k,v = f.split('=')
            values = [asfloat(d) for d in v.replace(',',' ').split()]
            if len(values) == 1: values = values[0]
            if k in columns:
                raise ValueError,'duplicate field %s'%k
            columns[k] = values

        # BT7 hacks
        # - convert the 48 PSD fields into data list
        if self.instrument == 'BT7' and 'PSDC00' in columns:
            columns['DATA'] = [columns['PSDC%02d'%i] for i in range(48)]
            for i in range(48): del columns['PSDC%02d'%i]

        # NG7 hacks
        # - if PSD, DATA = PSD specular minus background
        # - if SC1, DATA = SC1
        # - DATA is normalized by monitor
        if self.instrument == 'NG7':
            if 'PSD' in self.columns:
                psd = numpy.array(columns['PSD'])
                c,w = NG7_PSD_BEAM_CENTER, NG7_PSD_BEAM_WIDTH
                spec = numpy.sum(psd[c-w:c+w])
                back = numpy.sum(psd[c-2*w:c+2*w])
                columns['DATA'] = 2*spec-back
            elif 'SC1' in self.columns:
                columns['DATA'] = columns['SC1']
            # monitor normalization, protecting against 0 monitor
            if 'MON' in self.columns:
                if columns['MON']>0: columns['DATA'] /= columns['MON']

        # NSE hacks
        # - populate data from the DEPEND field
        if self.instrument == 'NSE':
            columns['DATA'] = columns[self.dependent[0]]

        if self.instrument in ['NG2','NG4'] and 'PSD' in columns:
            columns['DATA'] = columns['PSD']

        # Make sure there is a data column
        if 'DATA' not in columns: columns['DATA'] = 0

        # How big is the detector?
        pixels = 1 if numpy.isscalar(columns['DATA']) else len(columns['DATA'])

        # Update array
        if len(self.columns) == 0:
            # Adding point to new dataset
            for k in columns.keys(): self.columns[k] = [columns[k]]
            self.pixels = pixels
        else:
            # Adding point to existing data set
            if set(columns.keys()) != set(self.columns.keys()):
                raise ValueError,'columns do not match %s'%str(self.columns.keys())
            if pixels != self.pixels:
                raise ValueError,'inconsistent field length DATA'
            for k in columns.keys(): self.columns[k].append(columns[k])

        # Extract environment variables
        self.environment = {}
        for k,v in self.columns.items():
            if k.lower() in ['t','temp', 'temperatur', 'temperature']:
                self.environment['Temp.'] = v[-1]
            elif k.lower() in ['h','magfield']:
                self.environment['Field'] = v[-1]


    def time_remaining(self, drop=2):
        """
        Returns the estimated time remaining in the run.

        Time estimates are tricky since not all points require the same
        flux and since the flux is not constant.

        For now we use the simple assumption that every point takes the
        same amount of time.

        To account for the occasional reactor scram, we fit twice, once
        with all the points, and again with the two worst points removed
        (this is the *drop* parameter).  There are various reasons why
        this may still be wrong, such as when the reactor is running on
        reduced power for a significant portion of the run, or when counting
        against measured counts over a dynamic scattering kernel, so don't use
        the estimate for anything significant.

        We tried to model the rate of measurement by modeling with
        constant, linear, quadratic and power models [power(x) = p1+p2*x^p3].
        """
        times = self.time_per_point(drop=drop)
        return numpy.sum(times[len(self.columns['PT']):])

    def time_per_point(self,drop=2):
        import wsolve
        if self.columns is {}: return 0
        if not ('PT' in self.columns and 'TIMESTAMP' in self.columns): return 0
        # Measurement point
        current_point = self.columns['PT'][-1]
        all_points = numpy.arange(self.points)
        if current_point < 2: return 0*all_points
        # Time steps
        t = numpy.asarray(self.columns['TIMESTAMP'])
        dt = t[1:]-t[:-1]
        pt = numpy.arange(1,len(t))

        # If you don't have many points to go on, assume the time is constant
        if len(pt) < 5:
            return numpy.mean(dt[0])*numpy.ones_like(all_points)

        # Weight more recent points more strongly
        weight = 1./numpy.arange(len(dt))

        # Constant,linear,quadratic models, with two worst residuals removed
        models = []
        bics = []
        for degree in range(3):
            fn = wsolve.wpolyfit(pt,dt,dy=weight,degree=degree)
            if drop > 0:
                idx = numpy.argsort(abs(fn(pt)-dt))[:-drop]
                fn = wsolve.wpolyfit(pt[idx], dt[idx], dy=weight[idx], degree=degree)
                BIC_p = BIC(k=degree+1, fx=fn(pt[idx]), y=dt[idx])
            else:
                BIC_p = BIC(k=degree+1, fx=fn(pt), y=dt)
            models.append(fn)
            bics.append(BIC_p)

        if True:
            logfn = wsolve.wpolyfit(pt,numpy.log(dt-dt[0]+20),
                                    dy=weight, degree=1)
            fn = lambda pt: numpy.exp(logfn(pt))+dt[0]-20
            BIC_p = BIC(k=2, fx=fn(pt), y=dt)
            models.append(fn)
            bics.append(BIC_p)
        #print "bics",bics

        # Exponential model
        if self.instrument in ['BT4']:
            pars,BIC_p = fit_exp(pt,dt,dy=weight,drop=drop)
            models.append(lambda x,p=pars: exponential(p,x))
            bics.append(BIC_p)

        # Power model
	if False and self.instrument in ['NG7']:
            pars,BIC_p = robust_fit(power, [0,1,2], pt, dt, 
                                    dy=weight, drop=drop)
            models.append(lambda x,p=pars: power(p,x))
            bics.append(BIC_p)

        # Toss model and associated bic if the model predicts negative measurement time
        models,bics = zip(*[(m,b) for m,b in zip(models,bics) 
                            if (m(all_points)>0).all()])
        best = numpy.argmin(bics) # Choose lowest BIC
        # BIC is too accepting - be selective in its use
        if self.instrument == 'BT4':
            if self.points>20 and bics[best] < 2*bics[-1]: 
                 idx = -1
            else:
                 idx = best
            idx = -1
        elif self.instrument == 'NG7' and 'QZ' in self.columns:
            idx = best
        else:
            # For other scans use the constant approximation
            idx = 0
        model = models[idx]

        # If measurement estimate is for more than one day, then reject
        times = models[idx](all_points)
        if sum(times) > 60*60*24*2:
            times = models[0](all_points)

        # Finally, compute the predicted duration
        return times

    def timestamp(self, format="%m/%d %H:%M"):
        """
        Returns the timestamp as a string for the last datapoint, or an
        empty string if the time stamp column isn't available.
        """
        if 'TIMESTAMP' in self.columns:
            t = self.columns['TIMESTAMP'][-1]
            return time.strftime(format,time.localtime(t))
        else:
            return ""

    def eta(self, format="%m/%d %H:%M"):
        """
        Returns the estimated time to completion as a formated string.

        This is just the time of the last point plus the estimated time remaining.

        Returns the empty string if there is no estimated time remaining.
        """
        dt = self.time_remaining()
        if dt <= 0: 
            return ""

        t = self.columns['TIMESTAMP'][-1] + dt
        return time.strftime(format, time.localtime(t))

def power(p,x): 
    """
    Powerlaw model used by NG7 for monitor counts
    """
    return p[0]+p[1]*x**p[2]
power.deriv = lambda p,x: (1, x**p[2], p[1]*x**p[2]*numpy.log(x))

def exponential(p,x):
    return p[0] + p[1]*numpy.exp(p[2]*x)
exponential.deriv = lambda p,x: (1, numpy.exp(p[2]*x), p[1]*numpy.exp(p[2]*x)*x)

def fit_exp(x,y,dy=None,drop=2):
    # Generate initial guess for p0,p1,p2 using y[0],y[k],y[n]
    # by first solving the shifted equation:
    #   g(x) = p1'*exp(p2*(x-x0)) + p0
    n,k = len(y)-1,int(len(y)/2)
    if y[n] > y[0] and y[k] > y[0]:
        p2 = math.log((y[n]-y[0])/(y[k]-y[0]))/(x[n]-x[k])
    else:
        p2 = 0
    p1 = (y[n]-y[0])/(math.exp(p2*(x[n]-x[0])) - 1)
    p0 = (y[0]-p1)
    # then remove the shift:
    #   g(x) = p1'*exp(-p2*x0) * exp(p2*x) + p0
    p1 *= math.exp(-p2*x[0])
    return robust_fit(exponential, (p0,p1,p2), x, y, dy=dy, drop=drop)
    #return (p0,p1,p2),0

def chisq(fx,y,dy=1): 
    """
    sum squared weighted residuals (unnormalized)
    """
    return numpy.sum(((y-fx)/dy)**2)

def dchisq(f,p,x,y,dy=1):
    fx = f(p,x)
    dfx = f.deriv(p,x)
    C = 2*(fx-y)/dy**2
    return numpy.array([numpy.sum(C*v) for v in dfx])

def robust_fit(curve,p0,x,y,dy=1,drop=2):
    """
    Fit then refit with worst points removed.

    *curve*(p,x) is the theory function
    *p0* is the initial point
    *x* is the measurement points
    *y* is the measured values
    *dy* is the measurement uncertainty (1-sigma)
    *drop* is the number of points to remove

    Returns the fit parameters *p* and the estimated *BIC*.
    """
    if 1:
        from scipy.optimize import fmin_bfgs
        def fmin(f,x0,fprime): 
            try:
                return fmin_bfgs(f=f,x0=x0,fprime=fprime,disp=0)
            except:
                return x0
    else:
        from quasinewton import quasinewton
        def fmin(f,x0,fprime):
            try:
                return quasinewton(fn=f,x0=x0,grad=fprime)['x']
            except:
                return x0

    p0 = numpy.asarray(p0)
    dy *= numpy.ones_like(y)
    f = lambda p: chisq(curve(p,x),y,dy)
    fp = lambda p: dchisq(curve,p,x,y,dy)
    p = fmin(f=f,x0=p0,fprime=fp)
    if drop > 0:
        idx = numpy.argsort(abs(curve(p,x)-y)/dy)[:-drop]
        f = lambda p: chisq(curve(p,x[idx]),y[idx],dy[idx])
        fp = lambda p: dchisq(curve,p,x[idx],y[idx],dy[idx])
        p = fmin(f=f,x0=p,fprime=fp)
        k = len(p)
        n = len(y)-drop
        BIC_p = BIC(len(p), curve(p,x[idx]), y[idx], dy[idx])
    else:
        BIC_p = BIC(len(p), curve(p,x), y, dy)
    return p,BIC_p

def BIC(k,fx,y,dy=1):
    """
    Bayesian information criterion[1] for selecting between models.

    Returns log(chi^2/dof) + k*log(n)/n.

    k is the number of model parameters
    fx is the model f applied at the observation points
    y is the observed values (assumed to be normally distributed)
    dy is the uncertainty in the observations.

    The value we return is correct up to an additive constant, so it
    cannot be used in a more general Bayesian framework.  However,
    it preserves the ordering for the purposes of comparing fitted
    curves to otherwise equally probable models with differing
    numbers of parameters.

    [1] http://en.wikipedia.org/wiki/Bayesian_information_criterion
    """
    n = len(y)
    chi = chisq(fx,y,dy)
    if n==0 or n==k or chi==0: 
        return numpy.inf
    else:
        return math.log(chi/(n-k)) + k*math.log(n)/n


class GaussPeak(object):
    """Gaussian peak fitter result"""
    # ICP fit functions
    #
    # FindPeak scan
    #
    # p1 = constant  bkgnd
    # p2 = linear    bkgnd
    # p3 = quadratic bkgnd
    # p4 = height
    # p5 = position
    # p6 = width
    #BT5:END TYPE=FP FIT_P1=3.29 FIT_P2= 0.0 ... TIMESTAMP=...
    _vars = dict(FIT_P1='constant', FIT_P2='linear', FIT_P3='quadratic',
                 FIT_P4='height', FIT_P5='position', FIT_P6='width')
    def __init__(self, fields):
        self.timestamp = ""
        for f in fields:
            k,v = f.split('=')
            if k == 'TIMESTAMP':
                self.timestamp = time.ctime(float(v))
            else:
                setattr(self,self._vars[k],asfloat(v))
    def __call__(self, x):
        bkg = numpy.polyval([self.quadratic,self.linear,self.constant],x)
        g = numpy.exp( -((x-self.position)*1.665109/self.width)**2 )
        return self.height*g+bkg
    def __str__(self):
        bkgd = []
        if abs(self.quadratic)>1e-5: bkgd.append("%gx^2"%self.quadratic)
        if abs(self.linear)>1e-5: bkgd.append("%gx"%self.linear)
        if abs(self.constant)>1e-5: bkgd.append("%g"%self.constant)
        if bkgd != []:
            bkgd = "\nbkgd="+"+".join(bkgd)
        else:
            bkgd = ""

        return ("center=%.5f\nwidth=%.5f\nscale=%.0f%s"
                %(self.position,self.width,self.height,bkgd))

class CosPeak(object):
    """Cosine peak fitter result"""
    # Iscan
    #
    # p1 = constant bkgnd
    # p2 = amplitude
    # p3 = frequency
    # p4 = phase
    _vars = dict(FIT_P1='background', FIT_P2='amplitude',
                 FIT_P3='frequency', FIT_P4='phase')
    def __init__(self, fields):
        self.timestamp = ""
        for f in fields:
            k,v = f.split('=')
            if k == 'TIMESTAMP':
                self.timestamp = time.ctime(float(v))
            else:
                setattr(self,self._vars[k],asfloat(v))
    def __call__(self, x):
        g = numpy.cos(x*self.frequency+self.phase)
        return self.amplitude*g+self.background
    def __str__(self):
        if abs(self.background) > 1e-5:
            bkgd = "\nbkgd=%g"%self.background
        else:
            bkgd = ""
        return ("freq=%.5f\nphase=%.5f\nscale=%.0f%s"
                %(self.frequency,self.phase,self.amplitude,bkgd))

class NoPeak(object):
    def __init__(self, fields):
        self.timestamp = ""
        for f in fields:
            k,v = f.split('=')
            if k == 'TIMESTAMP':
                self.timestamp = time.ctime(float(v))
            else:
                raise KeyError,"Unknown END field %s"%k
    def __call__(self,x):
        return x
    def __str__(self):
        return "No peak"

def parse_peak(fields):
    """
    Process peak parameters.

    Fields should be:
        ['TYPE=type', 'FIT_P1=v1', ..., 'FIT_Pn=vn' 'TIMESTAMP=epoch']
    Optional COMMAND=nnn which we ignore.
    Returns NoPeak if no type and fit fields
    """
    # Seems to be an extra tab in the peak output, so strip the empty fields
    while '' in fields: fields.remove('')
    for f in fields: k,v = f.split('=')  # verify Key=Value pairs
    # Strip the 'COMMAND' field from ICE output
    fields = [f for f in fields if not f.startswith('COMMAND=')]
    #logging.info('END fields '+str(fields))
    if len(fields)>1:
        k,v=fields[0].split('=')
        v = v.strip() # BT7 uses TYPE= FP rather than TYPE=FP
        if k!='TYPE':
            raise KeyError,"Unknown END field %s"%k
        if v=='FP':
            return GaussPeak(fields[1:])
        elif v=='ISCAN':
            return CosPeak(fields[1:])
        elif v=='NOCONV':
            return NoPeak(fields[1:])
        else:
            raise ValueError,"Unknown peak type %s"%v
    else:
        return NoPeak(fields)

class XPeek(object):
    """
    XPeek data stream.

    This is an abstract base class which is only useful if you inherit
    from it.  The following fields are useful to the subclasses:

      instrument: the instrument this stream is listening to
      data: dictionary of data objects for each data line in the scan
      newdata(): abstract method called when a data START is encountered
      newpoint(): abstract method called when a point is received

    See xpeek.Data1D for details on the data line representation.

    Note that some instruments have multiple data lines present
    simultaneously, so plot each line.

    Note: handling of polarized data is incorrect if the A cross
    section is not measured first since starting the A cross section
    deletes the other polarization cross sections.

    Once the data processor is set up use the following:

        s = XPeek(instrument): connect to the instrument
        s.process(): method to call to process the stream.
    """
    def __init__(self, instrument, address=(HOST,PORT), echo=False):
        """Connect to the socket and subscribe to instrument"""
        self.instrument = instrument
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        self.socket.send('subscribe '+instrument)
        self.socket_buffer = ""
        self.data = {}
        self.lock = thread.allocate_lock()
        self.echo = echo # Echo lines to stdout as they come in.

    def readline(self):
        """Get the next line from the socket, blocking until it is received"""
        while '\n' not in self.socket_buffer:
            # Interruptible
            try:
                self.socket_buffer += self.socket.recv(BUFFER_SIZE)
            except socket.error,msg:
                if msg[0] == errno.EINTR:
                    raise KeyboardInterrupt
                else:
                    raise
        idx = self.socket_buffer.find('\n')
        line = self.socket_buffer[:idx]
        self.socket_buffer = self.socket_buffer[idx+1:]
        logging.debug('READ '+line)
        return line

    def parseline(self,line):
        """Get the next line from readline and parse it"""
        self.lastline = line # Remember this for errors
        if self.echo: print line
        fields = line.split('\t')
        lineid = line[:line.find(':')] # LineID is everything to the first ':'
        if fields[0].endswith('END'):
            # This is the end of a find_peek run.
            peak = parse_peak(fields[1:])
            self.data[lineid].peak = peak
            self.enddata(lineid)
        elif fields[0].endswith('FINISH'):
            # Done this section ... most sources aren't reporting this?
            pass
        elif fields[0].endswith('START'):
            # NG1/CG1 polarized data hack
            # If measuring a polarized dataset, the A cross section will
            # be started first.  If we don't match [CN][BCD]1 then reset
            if not (lineid[0] in 'CN'
                    and lineid[1] in 'BCD'
                    and lineid[2] == '1'):
                self.data = {}

            self.data[lineid] = Data1D(self.instrument, fields[1:])
            self.newdata(lineid) # subclassing hook
        elif lineid in self.data:
            self.data[lineid].add_point(fields[1:])
            self.newpoint(lineid)
        else:
            logging.warn("Missing START for "+lineid)

            self.data[lineid] = Data1D(self.instrument,
                                       ['NPTS=0','FILE=unknown','VARY=',
                                        'xpeek START not provided'])

    def newdata(self, lineid): """operate on new data line"""
    def newpoint(self, lineid): """operate on new point"""
    def enddata(self, lineid): """close data line"""

    def process_stream(self):
        """Process lines using parseline() forever"""
        # Catch-all so we know why the process died.
        while True:
            # Read the next line
            try:
                line = self.readline()
                print line
            except KeyboardInterrupt:
                thread.interrupt_main()
            except:
                logging.error("%s failed with %s"
                              % (self.instrument, traceback.format_exc()))
                continue

            # Interpret the next line
            try:
                self.lock.acquire()
                self.parseline(line)
            except KeyboardInterrupt:
                thread.interrupt_main()
            except:
                logging.error("%s failed with %s\nLine: %s"
                              % (self.instrument,
                                 traceback.format_exc(),
                                 self.lastline))
            finally:
                self.lock.release()

    def close(self):
        """close the connection"""
        self.socket.close()

def asfloat(str):
    """
    Convert to float, returning NaN if it is not a valid float
    """
    try:
        return float(str)
    except:
        return numpy.NaN

def demo(instrument):
    class XPeekPrint(XPeek):
        def enddata(self, lineid):
            print lineid,"ending peak",self.data[lineid].peak
        def newdata(self, lineid):
            data = self.data[lineid]
            print lineid,"starting",data.filename,"primary",data.primary
        def newpoint(self, lineid):
            data = self.data[lineid]
            print lineid,data.timestamp("%y/%m/%d %H:%M:%S"),\
                "point",len(data.columns['DATA']),\
                data.columns[data.primary][-1],\
                data.columns['DATA'][-1]

    xpeek = XPeekPrint(instrument)
    xpeek.process_stream()

def debug_eta(instrument):
    from numpy import log10
    import pylab
    class XPeekEta(XPeek):
        def enddata(self, lineid):
            #print ">>>> end",lineid, len(self.data[lineid].columns['TIMESTAMP'])
            #self.plot(lineid)
            pass
        def newdata(self, lineid):
            self.etas = []
            self.models = []
            #print ">>>> new",lineid, len(self.data[lineid].columns['TIMESTAMP'])
        def newpoint(self, lineid):
            line = self.data[lineid]
            eta = line.columns['TIMESTAMP'][-1] + line.time_remaining()
            self.etas.append(eta)
            self.models.append(line.time_per_point())
            #print ">>>>  add",lineid, len(line.columns['TIMESTAMP']),len(self.etas)
            #if len(self.etas)%k == k-1: self.plot(lineid)
        def plot(self, lineid):
            line = self.data[lineid]
            t = numpy.array(line.columns['TIMESTAMP'])
            eta = (numpy.array(self.etas)-t[0])/60.
            t = (t-t[0])
            dt = (t[1:]-t[:-1])/60.
            pt = numpy.arange(len(dt))
            all_pt = numpy.arange(line.points)

            pylab.clf()
            pylab.subplot(211)
            if line.instrument != 'BT4':
                pylab.plot(pt,eta[1:],'-x')
            else:
                pylab.plot(t[1:]/3600,eta[1:],'-x')
                pylab.xlabel('measurement time (hours)')
            pylab.ylabel('estimated run time (min)') 
            lo,hi=min(eta[1:]),max(eta[1:])
            pylab.ylim(lo-(hi-lo)*0.5,hi+(hi-lo)*0.5)
            pylab.subplot(212)
            #pylab.axis([pt[0],pt[-1],dt[0],dt[-1]])
            #pylab.plot(pt,log10(dt),'xg',pt[1:],log10(self.models[-1][1:len(pt)]),'-g')
            pylab.plot(pt[1:],dt[1:],'xg',
                       pt[1:],self.models[-1][1:len(pt)]/60.,'-g')
            #for k in range(65,75):
            #    pylab.plot(pt[1:],self.models[k][1:len(pt)]/60.,'-b',alpha=0.7,hold=True)
            #pylab.xscale('symlog')
            #pylab.yscale('symlog')
            pylab.ylabel('dt (min)')
            pylab.xlabel('Point number')
            lo,hi=min(dt),max(dt)
            pylab.ylim(lo-(hi-lo)*0.5,hi+(hi-lo)*0.5)
            #pylab.axis('auto')
            #pylab.subplot(313)
            #pylab.pcolormesh(numpy.array(self.models))


    xpeek = XPeekEta(instrument)
    thread.start_new_thread(xpeek.process_stream,())
    time.sleep(5)
    while True:
        lineids = xpeek.data.keys()
        xpeek.lock.acquire()
        xpeek.plot(lineids[0])
        xpeek.lock.release()
        pylab.waitforbuttonpress()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    debug_eta(sys.argv[1] if len(sys.argv)>1 else 'NG1')
