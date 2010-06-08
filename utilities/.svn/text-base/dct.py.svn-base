# This program is public domain
# Author: Paul Kienzle
"""
Documentation by William
"""
from numpy import sqrt, exp, pi, real
from numpy.fft import fft
import numpy

def dct(x,n=None):
  """y = dct (x, n)
Computes the discrete cosine transform of x.  If n is given, then
x is padded or trimmed to length n before computing the transform.
If x is a matrix, compute the transform along the columns of the
The matrix. The transform is faster if x is real-valued and even
length.

The discrete cosine transform X of x can be defined as follows:
           N-1
X[k] = w(k) sum x[n] cos (pi (2n-1) k / 2N ),  k = 0, ..., N-1
           n=0

with w(0) = sqrt(1/N) and w(k) = sqrt(2/N), k = 1, ..., N-1.  There
are other definitions with different scaling of X[k], but this form
is common in image processing.

See also: idct, dct2, idct2, dctmtx

From Discrete Cosine Transform notes by Brian Evans at UT Austin,
http://www.ece.utexas.edu/~bevans/courses/ee381k/lectures/09_DCT/lecture9/
the discrete cosine transform of x at k is as follows:
          N-1
   X[k] = sum 2 x[n] cos (pi (2n-1) k / 2N )
          n=0

which can be computed using:
   y = [ x ; flipud (x) ]
   Y = fft(y)
   X = exp( -j pi [0:N-1] / 2N ) .* Y

or for real, even length x

   y = [ even(x) ; flipud(odd(x)) ]
   Y = fft(y)
   X = 2 real { exp( -j pi [0:N-1] / 2N ) .* Y }

 Scaling the result by w(k)/2 will give us the desired output. """


  realx = numpy.isreal(x).all()

  axis=-1  # Careful if you change this --- may not work with middle axes
  xlen = x.shape[axis]
  if n is None: n = xlen
  if n > xlen:
    # n is too short --- zero pad
    zshape = x.shape.copy()
    zshape[axis] = xlen-n
    # Zero pad in the fastest dimension.
    x = numpy.concatenate((x,numpy.zeros(zshape)),axis=axis)
  elif n < xlen:
    x = x[...,:n]

  w = numpy.hstack(([sqrt(1./4./n)], 
                    sqrt(1./2./n)*exp((-1j*pi/2/n)*numpy.arange(1,n))))

  if realx and n%2 == 0:
    x = numpy.concatenate( (x[...,::2], x[...,::-2]), axis=axis)
    y = fft (x, axis=axis)
    y = 2 * real( w * y );
  else:
    x = numpy.concatenate( (x, x[...,::-1]), axis=axis)
    y = fft (x, axis=axis)
    y = w * y[...,:n]
    if realx: y = real(y)

  return y

def dct2(x,m=None,n=None):

  if m is None: m = x.shape[0]
  if n is None: n = x.shape[1]

  # TODO: use dct(dct(x,m,axis=0),n,axis=1) to avoid extra transpose
  # TODO: requires dct(...,axis=k) to work first, obviously.
  y = dct(dct(x, m).T, n).T
  return y  

if __name__=="__main__":
    x=numpy.arange(7)
    y=dct(x)
    print y