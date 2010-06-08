from mpfit import mpfit
import numpy
import copy

def F(x,p):
    y = ( p[0]*2 + p[1]*x + p[2]*x**2 + p[3]*numpy.sqrt(x) + p[4]*numpy.log(x))
    return y

def myfunct(p, fjac=None, x=None, y=None, err=None):
    # Parameter values are passed in "p"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    model = F(x, p)
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return [status, (y-model)/err]


if __name__=='__main__':
    print 'hi'
    x = numpy.arange(1,100)
    p0 = numpy.array([5.7, 2.2, 500., 1.5, 2000.])
    y = F(x,p0)#( p0[0]*2 + p0[1]*x + p0[2]*x**2 + p0[3]*numpy.sqrt(x) + p0[4]*numpy.log(x))
    err=y*0.1
    p0[1]=2.0
    p0[2]=400
    p0[3]=1.0
    p0[4]=1000.0
    parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
    parinfo=[]
    for i in range(5):
        parinfo.append(copy.deepcopy(parbase))
    print 'initial parinfo',parinfo
    print parinfo[1]
    parinfo[0]['fixed'] = 1
    print parinfo[1]
    parinfo[4]['limited'][0] = 1
    parinfo[4]['limits'][0]  = 50.
    print 'parinfo',parinfo
    values = [5.7, 2.2, 400., 1.5, 1000.]
    for i in range(5): 
        parinfo[i]['value']=p0[i]#values[i]
    fa = {'x':x, 'y':y, 'err':err}
    m = mpfit(myfunct, p0, parinfo=parinfo,functkw=fa)
    print 'status = ', m.status
    if (m.status <= 0): print 'error message = ', m.errmsg
    print 'parameters = ', m.params
    print 'perror',m.perror
    print 'chi',m.fnorm
    print 'covar',m.covar
    