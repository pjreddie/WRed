from pylab import *

shape = 'spikes'
if shape is 'spikes':
  t = array([1,1.5,1.8,3,4,7])/10
  x = array([3,2,2.5,4,2,1])
elif shape is 'cosine':
  t = linspace(0,1,10+1)[:-1] 
  x = cos(2*pi*t)
elif shape is 'flat':
  t = linspace(0,1,10+1)[:-1]
  x = ones_like(t)

# Cosine transform of x(t) -> X(w)
w=linspace(0,1,100) 
N=len(w)
X = sqrt(2/pi)/N*sum([xk*cos(2*pi*w*tk) for xk,tk in zip(x,t)],axis=0)

# Inverse transform X(w) -> x(t)
n = len(t)
xp = sqrt(2/pi)/n*sum([Xk*cos(2*pi*wk*t) for Xk,wk in zip(X,w)],axis=0)
plot(t,x,label='x')
plot(t,xp*x[0]/xp[0],label='f(F(x))')
legend()
grid(True)
show()
