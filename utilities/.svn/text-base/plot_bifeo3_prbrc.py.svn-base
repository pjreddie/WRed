import numpy as N
import  pylab
import scipy.sandbox.delaunay as D
#import numpy.core.ma as ma
import matplotlib.numerix.ma as ma
from matplotlib.ticker import NullFormatter, MultipleLocator
from scipy.signal.signaltools import convolve2d
import scriptutil as SU
import re
import readicp
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
import math

from matplotlib.patches import Ellipse
from rescalculator import lattice_calculator
from rescalculator.rescalc import rescalculator
eps=1e-3
pi=N.pi








def ResPlot(H,K,L,W,EXP,myrescal,ax,fig):
     """Plot resolution ellipse for a given scan"""
     center=N.round(H.shape[0]/2)
     if center<1:
          center=0
     if center>H.shape[0]:
          center=H.shape[0]
     #EXP=[EXP[center]]
     Style1=''
     Style2='--'
     
     XYAxesPosition=[0.1, 0.6, 0.3, 0.3]
     XEAxesPosition=[0.1, 0.1, 0.3, 0.3]
     YEAxesPosition=[0.6, 0.6, 0.3, 0.3]
     TextAxesPosition=[0.45, 0.0, 0.5, 0.5]
     GridPoints=101
     
     [R0,RMS]=myrescal.ResMatS(H,K,L,W,EXP)
     #[xvec,yvec,zvec,sample,rsample]=self.StandardSystem(EXP);
     myrescal.lattice_calculator.StandardSystem()
     #print 'shape ',self.lattice_calculator.x.shape
     qx=myrescal.lattice_calculator.scalar(myrescal.lattice_calculator.x[0,:],myrescal.lattice_calculator.x[1,:],myrescal.lattice_calculator.x[2,:],H,K,L,'latticestar')
     qy=myrescal.lattice_calculator.scalar(myrescal.lattice_calculator.y[0,:],myrescal.lattice_calculator.y[1,:],myrescal.lattice_calculator.y[2,:],H,K,L,'latticestar')
     qw=W;
     
     #========================================================================================================
     #find reciprocal-space directions of X and Y axes
     
     o1=myrescal.lattice_calculator.orientation.orient1.T#[:,0] #EXP['orient1']
     o2=myrescal.lattice_calculator.orientation.orient2.T#[:,0] #EXP['orient2']
     pr=myrescal.lattice_calculator.scalar(o2[0,:],o2[1,:],o2[2,:],myrescal.lattice_calculator.y[0,:],myrescal.lattice_calculator.y[1,:],myrescal.lattice_calculator.y[2,:],'latticestar')
     o2[0]=myrescal.lattice_calculator.y[0,:]*pr
     o2[1]=myrescal.lattice_calculator.y[1,:]*pr
     o2[2]=myrescal.lattice_calculator.y[2,:]*pr
     
     if N.abs(o2[0,center])<1e-5:
          o2[0,center]=0.0
     if N.absolute(o2[1,center])<1e-5:
          o2[1,center]=0.0
     if N.absolute(o2[2,center])<1e-5:
          o2[2,center]=0.0
     
     if N.abs(o1[0,center])<1e-5:
          o1[0,center]=0.0
     if N.absolute(o1[1,center])<1e-5:
          o1[1,center]=0.0
     if N.absolute(o1[2,center])<1e-5:
          o1[2,center]=0.0
     
     #%========================================================================================================
     #%determine the plot range
     XWidth=max(myrescal.fproject(RMS,0))
     YWidth=max(myrescal.fproject(RMS,1))
     WWidth=max(myrescal.fproject(RMS,2))
     XMax=(max(qx)+XWidth*1.5)
     XMin=(min(qx)-XWidth*1.5)
     YMax=(max(qy)+YWidth*1.5)
     YMin=(min(qy)-YWidth*1.5)
     WMax=(max(qw)+WWidth*1.5)
     WMin=(min(qw)-WWidth*1.5)
    ##fig=pylab.figure()
    ##%========================================================================================================
    ##% plot XY projection
     proj,sec=myrescal.project(RMS,2)
     (a,b,c)=N.shape(proj)
     mat=N.copy(proj)
     #print 'proj ', proj.shape
     a1=[];b1=[];theta=[];a1_sec=[];b1_sec=[];theta_sec=[];e=[]; e_sec=[]
     for i in range(c):
         matm=N.matrix(mat[:,:,i])
         w,v=N.linalg.eig(matm)
         vm=N.matrix(v)
         vmt=vm.T
         mat_diag=vmt*matm*vm
         a1.append(1.0/N.sqrt(mat_diag[0,0]))
         b1.append(1.0/N.sqrt(mat_diag[1,1]))
         thetar=N.arccos(vm[0,0])
         theta.append(math.degrees(thetar))
 
     mat_sec=N.copy(sec)
     #print 'proj ', proj
     (a,b,c)=N.shape(sec)
     print 'reached'
     for i in range(c):
         rsample='latticestar'
         ascale=myrescal.lattice_calculator.modvec(o1[0],o1[1],o1[2],rsample)[0]
         bscale=myrescal.lattice_calculator.modvec(o2[0],o2[1],o2[2],rsample)[0]
         print 'ascale',ascale
         print 'bscale',bscale
         ascale=1
         bscale=1
         matm_sec=N.matrix(mat_sec[:,:,i])
         w_sec,v_sec=N.linalg.eig(matm_sec)
         vm_sec=N.matrix(v)
         vmt_sec=vm_sec.T
         mat_diag_sec=vmt_sec*matm_sec*vm_sec
         #print 'a',myrescal.lattice_calculator.a[0]
         a1_sec.append(1.0/N.sqrt(mat_diag_sec[0,0])/ascale)
         b1_sec.append(1.0/N.sqrt(mat_diag_sec[1,1])/bscale)
         thetar_sec=N.arccos(vm_sec[0,0]/ascale)
         theta_sec.append(math.degrees(thetar_sec))
         #x0y0=N.array([H[i],K[i]])
         x0y0=N.array([qx[i],qy[i]])
         print 'a1_sec',a1_sec
         print 'b1_sec',b1_sec
         print 'theta_sec',math.degrees(thetar_sec)
         print 'x0y0',x0y0
         #print i,'qx',qx[i]
         #print 'qy',qy[i]
         e.append(Ellipse(x0y0,width=2*a1[i],height=2*b1[i],angle=theta[i]))
         e_sec.append(Ellipse(x0y0,width=2*a1_sec[i],height=2*b1_sec[i],angle=theta_sec[i]))
 
  
 
 
 
     rsample='latticestar'
     oxmax=XMax/myrescal.lattice_calculator.modvec(o1[0],o1[1],o1[2],rsample)
     oxmin=XMin/myrescal.lattice_calculator.modvec(o1[0],o1[1],o1[2],rsample)
     oymax=YMax/myrescal.lattice_calculator.modvec(o2[0],o2[1],o2[2],rsample)
     oymin=YMin/myrescal.lattice_calculator.modvec(o2[0],o2[1],o2[2],rsample)
  
     #make right y-axis
     #ax2 = fig.add_subplot(2,2,1)
     #pylab.subplots_adjust(hspace=0.6,wspace=0.3)
     #ax2.set_ylim(oymin[center], oymax[center])
     #ax2.yaxis.tick_right()
     #ax2.yaxis.set_label_position('right')
     #ax2.xaxis.set_major_formatter(pylab.NullFormatter())
     #ax2.xaxis.set_major_locator(pylab.NullLocator())
     #ylabel=r'Q$_y$' +'(units of ['+str(o2[0,center])+' '+str(o2[1,center])+' '+str(o2[2,center])+'])'
     #ax2.set_ylabel(ylabel)
     #make top x-axis
     #if 1:
         #ax3 = fig.add_axes(ax2.get_position(), frameon=False,label='x-y top')
         #ax3.xaxis.tick_top()
         #ax3.xaxis.set_label_position('top')
         #ax3.set_xlim(oxmin[center], oxmax[center])
         #ax3.yaxis.set_major_formatter(NullFormatter())
         #ax3.yaxis.set_major_locator(pylab.NullLocator())
         #xlabel=r'Q$_x$' +'(units of ['+str(o1[0,center])+' '+str(o1[1,center])+' '+str(o1[2,center])+'])'
         #ax3.set_xlabel(xlabel)
         #ax3.set_zorder(2)
 
     #make bottom x-axis, left y-axis
     if 1:
         #ax = fig.add_axes(ax2.get_position(), frameon=False,label='x-y')
         #ax.yaxis.tick_left()
         #ax.yaxis.set_label_position('left')
         #ax.xaxis.tick_bottom()
         #ax.xaxis.set_label_position('bottom')
         for i in range(c):
             #ax.add_artist(e[i])
             e[i].set_clip_box(ax.bbox)
             e[i].set_alpha(0.5)
             e[i].set_facecolor('red')
             ax.add_artist(e_sec[i])
             e_sec[i].set_clip_box(ax.bbox)
             e_sec[i].set_alpha(0.7)
             e_sec[i].set_facecolor('black')
 
         #ax.set_xlim(XMin, XMax)
         #ax.set_ylim(YMin, YMax)
         #xlabel=r'Q$_x$ ('+r'$\AA^{-1}$)'
         #ax.set_xlabel(xlabel)
         #ylabel=r'Q$_y$ ('+r'$\AA^{-1}$)'
         #ax.set_ylabel(ylabel)
 



















def plot_nodes(tri):
    for nodes in tri.triangle_nodes:
        D.fill(x[nodes],y[nodes],'b')
    pylab.show()

def plot_data(xa,ya,za,fig,nfig,colorflag=False):

    cmap = pylab.cm.jet
    cmap.set_bad('w', 1.0)
    myfilter=N.array([[0.1,0.2,0.1],[0.2,0.8,0.2],[0.1,0.2,0.1]],'d') /2.0
    zout=convolve2d(za,myfilter,mode='same')
    zima = ma.masked_where(N.isnan(zout),zout)


    ax=fig.add_subplot(1,1,nfig)
    pc=ax.pcolormesh(xa,ya,zima,shading='interp',cmap=cmap)  # working good!
#    pc=ax.imshow(zima,interpolation='bilinear',cmap=cmap)
    pc.set_clim(0.0,660.0)



    if colorflag:
        g=pylab.colorbar(pc,ticks=N.arange(0,675,100))
        print g
        #g.ticks=None
        #gax.yaxis.set_major_locator(MultipleLocator(40))
        #g.ticks(N.array([0,20,40,60,80]))

    return ax,g

def prep_data(filename):
#    Data=pylab.load(r'c:\resolution_stuff\1p4K.iexy')
    Data=pylab.load(filename)
    xt=Data[:,2]
    yt=Data[:,3]
    zorigt=Data[:,0]
    x=xt[:,zorigt>0.0]
    y=yt[:,zorigt>0.0]
    z=zorigt[:,zorigt>0.0]
#    zorig=ma.array(zorigt)
    print 'reached'
    threshold=0.0;
#    print zorigt < threshold
#    print N.isnan(zorigt)
#    z = ma.masked_where(zorigt < threshold , zorigt)
    print 'where masked ', z.shape
#should be commented out--just for testing
##    x = pylab.randn(Nu)/aspect
##    y = pylab.randn(Nu)
##    z = pylab.rand(Nu)
##    print x.shape
##    print y.shape
    # Grid
    xi, yi = N.mgrid[-5:5:100j,-5:5:100j]
    xi,yi=N.mgrid[x.min():x.max():.05,y.min():y.max():.05]
    # triangulate data
    tri = D.Triangulation(x,y)
    print 'before interpolator'
    # interpolate data
    interp = tri.nn_interpolator(z)
    print 'interpolator reached'
    zi = interp(xi,yi)
    # or, all in one line
    #    zi = Triangulation(x,y).nn_interpolator(z)(xi,yi)
#    return x,y,z
    return xi,yi,zi





def prep_data2(xt,yt,zorigt):
#    Data=pylab.load(r'c:\resolution_stuff\1p4K.iexy')
    #Data=pylab.load(filename)
    #xt=Data[:,2]
    #yt=Data[:,3]
    #zorigt=Data[:,0]
    x=xt[:,zorigt>0.0]
    y=yt[:,zorigt>0.0]
    z=zorigt[:,zorigt>0.0]
#    zorig=ma.array(zorigt)
    print 'reached'
    threshold=0.0;
#    print zorigt < threshold
#    print N.isnan(zorigt)
#    z = ma.masked_where(zorigt < threshold , zorigt)
    print 'where masked ', z.shape
#should be commented out--just for testing
##    x = pylab.randn(Nu)/aspect
##    y = pylab.randn(Nu)
##    z = pylab.rand(Nu)
##    print x.shape
##    print y.shape
    # Grid
    xi, yi = N.mgrid[-5:5:100j,-5:5:100j]
    xi,yi=N.mgrid[x.min():x.max():.001,y.min():y.max():.001]
    # triangulate data
    tri = D.Triangulation(x,y)
    print 'before interpolator'
    # interpolate data
    interp = tri.nn_interpolator(z)
    print 'interpolator reached'
    zi = interp(xi,yi)
    # or, all in one line
    #    zi = Triangulation(x,y).nn_interpolator(z)(xi,yi)
#    return x,y,z
    return xi,yi,zi



def readmeshfiles(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readicp.datareader()
    Qx=N.array([])
    Qy=N.array([])
    Qz=N.array([])
    Counts=N.array([])
    a=N.array([3.943],'d')
    b=N.array([2.779],'d')
    for currfile in flist:
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        Qx=N.concatenate((Qx,N.array(mydata.data['Qx'])*2*pi/a[0]))
        Qy=N.concatenate((Qy,N.array(mydata.data['Qy'])*2*pi/b[0]))
        Qz=N.concatenate((Qz,N.array(mydata.data['Qz'])))
        Counts=N.concatenate((Counts,N.array(mydata.data['Counts'])))
    xa,ya,za=prep_data2(Qx,Qy,Counts);
    print 'xa',xa.min(),xa.max()
    print 'qx',Qx.min(),Qx.max()
    print 
    return xa,ya,za







if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    mydirectory=r'c:\bifeo3xtal\dec7_2007'
    myfilebase='cmesh'
    myend='bt9'
    if 1:
        xc,yc,zc=readmeshfiles(mydirectory,'cmesh',myend) #Rm temp
    if 1:
        xd,yd,zd=readmeshfiles(mydirectory,'dmesh',myend) #0
    if 0:
        xe,ye,ze=readmeshfiles(mydirectory,'emesh',myend) #-1.3
    if 0:
        xf,yf,zf=readmeshfiles(mydirectory,'fmesh',myend) #0
    if 0:
        xg,yg,zg=readmeshfiles(mydirectory,'gmesh',myend) #1.3
    if 0:
        xh,yh,zh=readmeshfiles(mydirectory,'hmesh',myend) #0
    if 0:
        xi,yi,zi=readmeshfiles(mydirectory,'imesh',myend) #-1.3
    if 0:
        xj,yj,zj=readmeshfiles(mydirectory,'jmesh',myend) #0
    print 'matplotlib'

    if 1:

        fig=pylab.figure(figsize=(8,8))
        ylim=(.485,.515)
        xlim=(.485,.515)
        #ylabel='E (meV)'
        #xlabel=r'Q$ \ \ (\AA^{-1}$)'
        ylabel='(1 1 0)'
        xlabel='(1 -1 -2)'


    if 1:
        ax,g=plot_data(xd,yd,zd,fig,1,colorflag=True)
        ##ax.text(.98,.20,'E=0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        #ax.xaxis.set_major_formatter(NullFormatter())
        #ax.set_ylim(ylim); ax.set_xlim(xlim)
        ##g.ax.ticks=N.arange(0,100,20)

    if 0:
        ax,g=plot_data(xe,ye,ze,fig,2,colorflag=True)
        ax.text(.98,.20,'E=-1.3 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)

    if 0:
        ax,g=plot_data(xf,yf,zf,fig,3,colorflag=True)
        ax.text(.98,.20,'0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
    if 0:
        ax,g=plot_data(xg,yg,zg,fig,4,colorflag=True)
        ax.text(.98,.20,'1.3 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
    if 0:
        ax,g=plot_data(xh,yh,zh,fig,5,colorflag=True)
        ax.text(.98,.20,'0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        fmt = FormatStrFormatter('%0.3g')  # or whatever
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_locator(MaxNLocator(5))
    if 0:
        ax,g=plot_data(xi,yi,zi,fig,6,colorflag=True)
        ax.text(.98,.20,'-1.3 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_xlabel(xlabel)
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        fmt = FormatStrFormatter('%0.3g')  # or whatever
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_locator(MaxNLocator(5))

    if 0:
        ax,g=plot_data(xf,yf,zf,fig,6,colorflag=True)
        ax.text(.98,.20,'0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_xlabel(xlabel)
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        #fmt = FormatStrFormatter('%1.4g')  # or whatever
        #ax.yaxis.set_major_formatter(fmt)


    if 1:
        print 'gca ', fig.gca()
        for im in fig.gca().get_images():
            print im
            im.set_clim(0.0,660.0)
        #pylab.show()
    if 0:
        print 'saving'
        pylab.savefig(r'c:\sqltest\demo.pdf',dpi=150)
        print 'saved'


    if 1:
        a=N.array([3.943],'d')
        b=N.array([2.779],'d')
        c=N.array([13.86],'d')
        alpha=N.array([90],'d')
        beta=N.array([90],'d')
        gamma=N.array([90],'d')
 #       orient1=N.array([[0,1,1]],'d')
        orient1=N.array([[1,0,0]],'d')
        orient2=N.array([[0,1,0]],'d')
        orientation=lattice_calculator.Orientation(orient1,orient2)
        mylattice=lattice_calculator.Lattice(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,\
                               orientation=orientation)
        delta=.0045
        hc=.5035
        kc=.5
        #x-axis is cubic, y-axis is 110
        sq3=N.sqrt(3)
        H=N.array([hc,
                   hc,
                   hc+3*delta/2,
                   hc-3*delta/2,
                   hc-3*delta/2,
                   hc+3*delta/2,
                   ],'d');
        K=N.array([kc+delta,
                   kc-delta,
                   kc+delta/2,
                   kc-delta/2,
                   kc+1*delta/2,
                   kc-delta/2
                   ],'d');
        L=N.array([0,0,0,0,0,0],'d');
        W=N.array([0,0,0,0,0,0],'d')
        #H=N.array([.5,.5+2*delta],'d');K=N.array([0.5+delta,.5+delta/2],'d');L=N.array([0,0],'d');W=N.array([0,0],'d')
        #H=N.array([hc],'d');K=N.array([kc],'d');L=N.array([0],'d');W=N.array([0],'d')
        EXP={}
        EXP['ana']={}
        EXP['ana']['tau']='pg(002)'
        EXP['mono']={}
        EXP['mono']['tau']='pg(002)';
        EXP['ana']['mosaic']=25
        EXP['mono']['mosaic']=25
        EXP['sample']={}
        EXP['sample']['mosaic']=0#15
        EXP['sample']['vmosaic']=0#15
        EXP['hcol']=N.array([40, 10.7, 40, 80],'d')
        EXP['vcol']=N.array([120, 120, 120, 240],'d')
        EXP['infix']=-1 #positive for fixed incident energy
        EXP['efixed']=14.7
        EXP['method']=0
        setup=[EXP]
        myrescal=rescalculator(mylattice)
        newinput=lattice_calculator.CleanArgs(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,orient1=orient1,orient2=orient2,\
                            H=H,K=K,L=L,W=W,setup=setup)
        neworientation=lattice_calculator.Orientation(newinput['orient1'],newinput['orient2'])
        mylattice=lattice_calculator.Lattice(a=newinput['a'],b=newinput['b'],c=newinput['c'],alpha=newinput['alpha'],\
                        beta=newinput['beta'],gamma=newinput['gamma'],orientation=neworientation,\
                        )
        myrescal.__init__(mylattice)
        Q=myrescal.lattice_calculator.modvec(H,K,L,'latticestar')
        R0,RM=myrescal.ResMat(Q,W,setup)
        print 'RM '
        print RM.transpose()
        print 'R0 ',R0
        #exit()
        R0,RMS=myrescal.ResMatS(H,K,L,W,setup)
        widths=myrescal.CalcWidths(H,K,L,W,setup)
        print 'YBwidth',widths['YBWidth']
        print 'XBwidth',widths['XBWidth']
        ResPlot(H, K, L, W, setup,myrescal,ax,fig)




    
    
    
    
    if 1:
        pylab.show()
