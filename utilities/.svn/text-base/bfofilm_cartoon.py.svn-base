import numpy as N
import pylab
from matplotlib.ticker import NullFormatter, MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator


if __name__=='__main__':
    if 0:
        ax=pylab.subplot(2,2,1)
        #1 1 0
        x1=N.array([1])
        y1=N.array([1])

        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        #-1 -1 0
        x1=N.array([-1])
        y1=N.array([-1])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        #-1 2 0
        x1=N.array([-1])
        y1=N.array([2])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        #1 -2 0
        x1=N.array([1])
        y1=N.array([-2])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        #2 -1 0
        x1=N.array([2])
        y1=N.array([-1])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        #-2 1 0
        x1=N.array([-2])
        y1=N.array([1])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        pylab.xlabel('[1 0 0]')
        pylab.ylabel('[0 1 0]')
        #draw vertical line
        #x1=[0,0]
        #y1=[-2.5,2.5]
        #pylab.plot(x1,y1,linewidth=3.0)
        #draw horizontal line
        #x1=[-2.5,2.5]
        #y1=[0,0]
        #pylab.plot(x1,y1,linewidth=3.0,color='blue')

        #draw line 1 1 0
        x1=[1,-1]
        y1=[1,-1]
        pylab.plot(x1,y1,linewidth=3.0,color='blue')

        #draw line 1 2 0
        x1=[1,-1]
        y1=[-2,2]
        pylab.plot(x1,y1,linewidth=3.0,color='blue')

        #draw line 1 1 0
        x1=[-2,2]
        y1=[1,-1]
        pylab.plot(x1,y1,linewidth=3.0,color='blue')



        s=r'$\delta 2\bar{\delta} 0$'
        pylab.text(1.2,-2,s,fontsize=20)

        s=r'$2\delta \bar{\delta} 0$'
        pylab.text(1.8,-0.7,s,fontsize=20)

        s=r'$\delta \delta 0$'
        pylab.text(1,1.2,s,fontsize=20)

        s=r'$\bar{\delta} \bar{\delta} 0$'
        pylab.text(-1,-1.6,s,fontsize=20)

        s=r'$2\bar{\delta} \delta 0$'
        pylab.text(-2,1.2,s,fontsize=20)

        s=r'$\bar{\delta} 2\delta 0$'
        pylab.text(-.7,2.0,s,fontsize=20)

        pylab.axis([-3.5,3.5,-3.5,3.5])
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())

    if 0:
        ax=pylab.subplot(2,2,2)

        # 1 1 0
        x1=N.array([4])
        y1=N.array([0])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        s=r'$\delta \delta 0$'
        pylab.text(4.8,0.0,s,fontsize=20)

        # -1 -1 0
        x1=N.array([-4])
        y1=N.array([0])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        s=r'$\bar{\delta} \bar{\delta} 0$'
        pylab.text(-6.8,0.0,s,fontsize=20)

        # -1 2 0
        x1=N.array([2])
        y1=N.array([0])
        pylab.plot(x1,y1,'bo',markersize=10,markerfacecolor='white')
        s=r'$\bar{\delta} 2\delta 0$'
        pylab.text(0.5,0.4,s,fontsize=20)

        # 2 -1 0
        #x1=N.array([2])
        #y1=N.array([0])
        #pylab.plot(x1,y1,'bo',markersize=10)
        s=r'$2\delta \bar{\delta} 0$'
        pylab.text(0.5,-1.4,s,fontsize=20)


        # -2 1 0
        x1=N.array([-2])
        y1=N.array([0])
        pylab.plot(x1,y1,'bo',markersize=10,markerfacecolor='white')
        s=r'$2\bar{\delta} \delta 0$'
        pylab.text(-3.5,0.4,s,fontsize=20)

        # 1 -2 0
        #x1=N.array([2])
        #y1=N.array([0])
        #pylab.plot(x1,y1,'bo',markersize=10)
        s=r'$\delta 2\bar{\delta} 0$'
        pylab.text(-3.5,-1.4,s,fontsize=20)



        pylab.axis([-8.0,8.0,-3.5,3.5])
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())

        pylab.xlabel('[1 1 0]')
        pylab.ylabel('[0 0 1]')


    if 1:
        ax=pylab.subplot(2,2,2)

        # 1 1 0
        x1=N.array([4])
        y1=N.array([0])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        s=r'$\delta \delta 0$'
        pylab.text(4.8,0.0,s,fontsize=20)

        # -1 -1 0
        x1=N.array([-4])
        y1=N.array([0])
        pylab.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
        s=r'$\bar{\delta} \bar{\delta} 0$'
        pylab.text(-6.8,0.0,s,fontsize=20)

        # 1 0 1
        x1=N.array([2])
        y1=N.array([4])
        pylab.plot(x1,y1,'bo',markersize=5,markerfacecolor='white')
        s=r'$\delta 0 \delta$'
        pylab.text(0.5,4.4,s,fontsize=20)


        # 0 -1 1
        x1=N.array([-2])
        y1=N.array([4])
        pylab.plot(x1,y1,'bo',markersize=10,markerfacecolor='white')
        s=r'$0 \bar{\delta} \delta$'
        pylab.text(-3.0,4.4,s,fontsize=20)


        # 0 1 -1
        x1=N.array([2])
        y1=N.array([-4])
        pylab.plot(x1,y1,'bo',markersize=10,markerfacecolor='gray')
        s=r'$0 \delta \bar{\delta}$'
        pylab.text(0.5,-6.8,s,fontsize=20)


        # -1 0 -1
        x1=N.array([-2])
        y1=N.array([-4])
        pylab.plot(x1,y1,'bo',markersize=5,markerfacecolor='gray')
        s=r'$\bar{\delta} 0 \bar{\delta}$'
        pylab.text(-3.0,-6.8,s,fontsize=20)


        pylab.axis([-8.0,8.0,-8,8])
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())

        pylab.xlabel('[1 1 0]')
        pylab.ylabel('[0 0 1]')




    if 1:
        pylab.show()



