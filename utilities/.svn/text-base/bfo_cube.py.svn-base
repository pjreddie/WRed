import numpy as np
from enthought.mayavi import mlab
pi=np.pi



def gen_as():
    xas=0.361
    a=-pi/2; b=-pi/2; c=-pi/2
    rx=np.array([[1,0,0],[0,np.cos(a),np.sin(a)],[0,-np.sin(a),np.cos(b)]],'Float64')
    ry=np.array([[np.cos(b),0,-np.sin(b)],[0,1,0],[np.sin(a),0,np.cos(b)]],'Float64')
    rz=np.array([[np.cos(c),np.sin(c),0],[-np.sin(c),np.cos(c),0],[0,0,1]],'Float64')
    pos_at=np.array([[0.0000,   0.0000,   1-xas],\
                [0.0000,   0.0000,   xas],\
                [0.0000,   0.5000,   .5-xas],\
                [0.0000,   0.5000,   .5+xas],\
                [0.5000,   0.0000,   .5-xas],\
                [0.5000,   0.0000,   .5+xas],\
                [0.5000,   0.5000,   1-xas],\
                [0.5000,   0.5000,   xas],
                #[0.0000,   0.0000,   2-xas],\
                #[0.0000,   0.0000,   1-xas],\
                #[0.0000,   0.5000,   1+.5-xas],
                #[0.0000,   0.5000,   1+.5+xas],\
                #[0.5000,   0.0000,   1+.5-xas],\
                #[0.5000,   0.0000,   1+.5+xas],\
                #[0.5000,   0.5000,   1+1-xas],\
                #[0.5000,   0.5000,   1+xas],\
                #[0.0000,   0.0000,   -1-xas],\
                #[0.0000,   0.0000,   -1-xas],\
                #[0.0000,   0.5000,   -1+.5-xas],
                #[0.0000,   0.5000,   -1+.5+xas],\
                #[0.5000,   0.0000,   -1+.5-xas],\
                #[0.5000,   0.0000,   -1+.5+xas],\
                #[0.5000,   0.5000,   -1+1-xas],\
                #[0.5000,   0.5000,   -1+xas],\
                ]) 
    pos_at=np.dot(pos_at,rx)
    x=pos_at[:,0]
    y=pos_at[:,1]
    z=pos_at[:,2]
    return x,y,z

def gen_fe():
    a=-pi/2; b=-pi/2; c=-pi/2
    rx=np.array([[1,0,0],[0,np.cos(a),np.sin(a)],[0,-np.sin(a),np.cos(b)]],'Float64')
    ry=np.array([[np.cos(b),0,-np.sin(b)],[0,1,0],[np.sin(a),0,np.cos(b)]],'Float64')
    rz=np.array([[np.cos(c),np.sin(c),0],[-np.sin(c),np.cos(c),0],[0,0,1]],'Float64')
    pos_at=np.array([[0.2500,   0.2500,   0.2500],\
                [0.7500,   0.7500,   0.2500],\
                [0.7500,   0.2500,   0.7500],
                [0.2500,   0.7500,   0.7500],\
                [0.7500,   0.7500,   0.7500],\
                [0.2500,   0.2500,   0.7500],\
                [0.2500,   0.7500,   0.2500],\
                [0.7500,   0.2500,   0.2500]])   
    pos_at=np.dot(pos_at,rx)
    x=pos_at[:,0]
    y=pos_at[:,1]
    z=pos_at[:,2]
    return x,y,z


def gen_sr():
    a=-pi/2; b=-pi/2; c=-pi/2
    rx=np.array([[1,0,0],[0,np.cos(a),np.sin(a)],[0,-np.sin(a),np.cos(b)]],'Float64')
    ry=np.array([[np.cos(b),0,-np.sin(b)],[0,1,0],[np.sin(a),0,np.cos(b)]],'Float64')
    rz=np.array([[np.cos(c),np.sin(c),0],[-np.sin(c),np.cos(c),0],[0,0,1]],'Float64')
    pos_at=np.array([[0.0000,   0.0000,   0.0000],\
                [0.0000,   0.5000,   0.5000],\
                [0.5000,   0.0000,   0.5000],
                [0.5000,   0.5000,   0.0000]\
                ])      
    
    pos_at=np.dot(pos_at,rx)
    x=pos_at[:,0]
    y=pos_at[:,1]
    z=pos_at[:,2]
    return x,y,z


def genvec(vec,fig,color=None):
    vmag=np.sqrt(vec[0]**2+vec[1]**2+vec[2]**2); vec=vec/vmag
    u=[vec[0]];v=[vec[1]];w=[vec[2]]
    mlab.quiver3d([0],[0],[0],u,v,w,line_width=3, scale_factor=1,figure=fig,color=color)

@mlab.show
def test_den():
    P = np.random.random((10,10))
    #P=np.load(r'c:\maxdenP.np.npy')
    #myfilestr=r'c:\structfactors_density.dat'
    #x,y,z=np.loadtxt(myfilestr).T
    #P=z.reshape((101,101))
    #print P.shape
    fig=mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))
    x,y,z=gen_as()   
    #view along z-axis
    #pts_as=mlab.points3d(x,y,z-.125,color=(1,0,0),colormap='gist_rainbow',figure=fig,scale_factor=.1)
    x,y,z=gen_fe()  
    print 'x',x
    print 'y',y
    print 'z',z
    #pts_fe=mlab.points3d(x,y,z-.125,color=(0,1,0),colormap='gist_rainbow',figure=fig,scale_factor=.02)
    x,y,z=gen_sr()  
    #pts_sr=mlab.points3d(x,y,z-.125,color=(0,0,1),colormap='gist_rainbow',figure=fig)
    
   
    if 1:
        #112
        vec=np.array([1,1,-2],'Float64')
        genvec(vec,fig,color=(1,0,0))   
        vec=np.array([-2,1,1],'Float64')
        genvec(vec,fig,color=(1,0,0))   
        vec=np.array([1,-2,1],'Float64')
        genvec(vec,fig,color=(1,0,0))  
        
        #111
        vec=np.array([1,1,1],'Float64')
        genvec(vec,fig, color=(0,0,1))
    
    if 0: 
        #111
        vec=np.array([1,1,1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([1,1,-1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([1,-1,1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([-1,1,1],'Float64')
        genvec(vec,fig, color=(0,0,1))
    
        vec=np.array([1,-1,-1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([-1,1,-1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([-1,-1,1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([-1,-1,-1],'Float64')
        genvec(vec,fig, color=(0,0,1))
    
    
    if 0:
        #scattering plane:
        vec=np.array([1,1,0],'Float64')
        genvec(vec,fig, color=(0,1,0)) 
        vec=np.array([1,1,1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([1,1,-2],'Float64')
        genvec(vec,fig,color=(1,0,0))   
        vec=np.array([0,0,1],'Float64')
        genvec(vec,fig,color=(0,0,0))   
        

    if 0:
        #110 scattering plane:
        vec=np.array([1,1,0],'Float64')
        genvec(vec,fig, color=(0,1,0)) 
        vec=np.array([1,1,1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([1,1,-2],'Float64')
        genvec(vec,fig,color=(1,0,0))   
        vec=np.array([0,0,1],'Float64')
        genvec(vec,fig,color=(0,0,0)) 
        
    if 1:
        #110 scattering plane variations normal to 111
        vec=np.array([1,-1,0],'Float64')
        genvec(vec,fig, color=(0,1,0)) 
        vec=np.array([1,1,1],'Float64')
        genvec(vec,fig, color=(0,0,1))
        vec=np.array([0,1,-1],'Float64')
        genvec(vec,fig,color=(0,1,0))   
        vec=np.array([-1,0,1],'Float64')
        genvec(vec,fig,color=(0,1,0))

        
    
    if 0:
        #1 1 0
        vec=np.array([1,1,0],'Float64')
        genvec(vec,fig, color=(0,1,0)) 
        vec=-np.array([1,1,0],'Float64')
        genvec(vec,fig, color=(0,1,0)) 
        
        vec=np.array([1,0,1],'Float64')
        genvec(vec,fig, color=(0,1,0))
        vec=-np.array([1,0,1],'Float64')
        genvec(vec,fig, color=(0,1,0))
        
        vec=np.array([0,1,-1],'Float64')
        genvec(vec,fig, color=(0,1,0)) 
        vec=-np.array([0,1,-1],'Float64')
        genvec(vec,fig, color=(0,1,0)) 
        #outline=mlab.outline(figure=fig)
    outline=mlab.outline(figure=fig,extent=[-1,1,-1,1,-1,1])
    mlab.orientation_axes(figure=fig,xlabel='a',ylabel='b',zlabel='c')
        #print 'shape',P.shape
    #P = P[:,:, np.newaxis]
    #print 'after',P.shape
    #src = mlab.pipeline.scalar_field(P)
    #src = mlab.pipeline.array2d_source(P)
    #surf = mlab.pipeline.surface(src,figure=fig,extent=[0,1,0,1,-1,0],name='surf2',opacity=0.4)
    #surf.transform.GetTransform().RotateX(90)
    print 'done'
    if 0:
        mlab.view(45, 45,focalpoint=(2,2,2))


if __name__=='__main__':
    test_den()