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
                [0.0000,   0.5000,   .5-xas],
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


@mlab.show
def test_den():
    #P = np.random.random((10,10))
    #P=np.load(r'c:\maxdenP.np.npy')
    #myfilestr=r'c:\structfactors_density.dat'
    #x,y,z=np.loadtxt(myfilestr).T
    #P=z.reshape((101,101))
    #print P.shape
    fig=mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))    
    x,y,z=np.array([[1,0,1],
                    [0,-1,1],
                    [-1,0,-1],
                    [0,1,-1],
                    [1,1,0],
                    [-1,-1,0]
                    ],'float64').T
    #view along z-axis
    pts_as=mlab.points3d(x,y,z,color=(1,0,0),colormap='gist_rainbow',figure=fig,scale_factor=.3)
    #x,y,z=gen_fe()  
    print 'x',x,x.shape
    print 'y',y,y.shape
    print 'z',z,z.shape
    x,y,z=np.array([[0,1,1],
                    [0,-1,-1],
                    ],'float64').T
    pts_FE=mlab.points3d(x,y,z,color=(0,1,0),colormap='gist_rainbow',figure=fig,scale_factor=.3)
    mlab.text3d(0, 1, 1,'011',scale=.2,color=(1,1,0))
    mlab.text3d(1, 1, 0,'110',scale=.2)
    mlab.text3d(-1, -1, 0,'-1-10',scale=.2)
    mlab.text3d(1, 0, 1,'101',scale=.2)
    mlab.text3d(0, -1, 1,'0-11',scale=.2)
    mlab.text3d(-1, 0, -1,'-10-1',scale=.2)
    mlab.text3d(0, 1, -1,'01-1',scale=.2)
    
    
    #pts_fe=mlab.points3d(x,y,z-.125,color=(0,1,0),colormap='gist_rainbow',figure=fig,scale_factor=.02)
    #x,y,z=gen_sr()  
    #print 'x',x,x.shape
    #pts_sr=mlab.points3d(x,y,z-.125,color=(0,0,1),colormap='gist_rainbow',figure=fig)
    #outline=mlab.outline(figure=fig,extent=[0,1,0,1,-1,0])
    outline=mlab.outline(figure=fig)
    mlab.orientation_axes(figure=fig,xlabel='a',ylabel='b',zlabel='c')
    #print 'shape',P.shape
    #P = P[:,:, np.newaxis]
    #print 'after',P.shape
    #src = mlab.pipeline.scalar_field(P)
    #src = mlab.pipeline.array2d_source(P)
    #surf = mlab.pipeline.surface(src,figure=fig,extent=[0,1,0,1,-1,0],name='surf2',opacity=0.4)
    #surf.transform.GetTransform().RotateX(90)
    print 'done'


if __name__=='__main__':
    test_den()