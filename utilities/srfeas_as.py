import numpy as N
import pylab
from matplotlib.ticker import NullFormatter, MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator




def gen_as():
  xas=0.36
  aspos=N.array([[0.0000,   0.0000,1-xas],   
                 [0.0000,   0.0000,xas],    
                 [0.0000,   0.5000,.5-xas],    
                 [0.0000,   0.5000,.5+xas],       
                 [0.5000,   0.0000,.5-xas],  
                 [0.5000,   0.0000,.5+xas],    
                 [0.5000,   0.5000,1-xas],   
                 [0.5000,   0.5000,xas],
                 [1.0000,   0.0000,1-xas],   
                 [1.0000,   0.0000,xas],  
                 [1.0000,   0.5000,.5-xas],    
                 [1.0000,   0.5000,.5+xas]
                 ],'Float64')
  return aspos

def plot_as(ax,fig):
  aspos=gen_as()
  xn=aspos[N.where(aspos[:,1]==0)[0],0]
  zn=aspos[N.where(aspos[:,1]==0)[0],2]
  xp=aspos[N.where(aspos[:,1]==0.5)[0],0]
  zp=aspos[N.where(aspos[:,1]==0.5)[0],2]
  
  for x,z in zip(xn,zn):
    print x,z
    x1=N.array([x])
    y1=N.array([z])
    ax.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
    
  for x,z in zip(xp,zp):
    print x,z
    x1=N.array([x])
    y1=N.array([z])
    ax.plot(x1,y1,'ro',markersize=10,markerfacecolor='red',markeredgecolor='red')
    
    #ax.yaxis.set_major_formatter(NullFormatter())
    #ax.xaxis.set_major_formatter(NullFormatter())
    #s=r'$\bar{\delta} \bar{\delta} 0$'
    #ax.text(-7.2,0.0,s,fontsize=20)

if __name__=="__main__":
  fig=pylab.figure(figsize=(8,8))
  ax=fig.add_subplot(2,1,2)
  plot_as(ax,fig)
  ax.set_aspect(1./ax.get_data_ratio())
  ax.set_xlim(0,1)
  ax.set_ylim(0,1)
  pylab.show()
  
