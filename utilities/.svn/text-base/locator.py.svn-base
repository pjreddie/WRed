import numpy as N

class locator:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        return
    def inside(self,xt,yt):
        inds=N.array([])
        for i in range(xt.shape[0]):
            indx=N.where(self.x==xt[i])[0]
            indy=N.where(self.y==yt[i])[0]
            ind=N.intersect1d(indx,indy)
            inds=N.concatenate((inds,ind))
        #print indx[0]
        #print indy[0]
        #ind=indx
        #print N.ravel(inds)
        return N.ravel(inds)


if __name__=="__main__":
    #x=N.arange(1,7,1)
    #y=N.arange(2,8,1)
    x=N.array([1,2,3,4,5,9,11,11,11])
    y=N.array([2,4,5,6,5,8,8,8,7])
    data=N.zeros((x.shape[0],2))
    data[:,0]=x
    data[:,1]=y
    
    print data
    mylocator=locator(x,y)
    xt=N.array([11,3])
    yt=N.array([8,5])
    ind=mylocator.inside(xt,yt)