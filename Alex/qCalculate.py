import numpy as N

def scalar(x1, y1, z1, x2, y2, z2, astar,bstar,cstar,alphastar,betastar,gammastar):
          "calculates scalar product of two vectors"
               a=astar
               b=bstar
               c=cstar
               alpha=N.radians(alphastar)
               beta=N.radians(betastar)
               gamma=N.radians(gammastar)

          s=x1*x2*a**2+y1*y2*b**2+z1*z2*c**2+(x1*y2+x2*y1)*a*b*N.cos(gamma)+(x1*z2+x2*z1)*a*c*N.cos(beta)+(z1*y2+z2*y1)*c*b*N.cos(alpha)
          return s


def modvec(x, y, z, lattice):
          "Calculates modulus of a vector defined by its fraction cell coordinates"
          "or Miller indexes"
          m=N.sqrt(scalar(x, y, z, x, y, z, astar,bstar,cstar,alphastar,betastar,gammastar))
          return m



def calcq(H, K, L):
          "Given reciprocal-space coordinates of a vector, calculate its coordinates in the Cartesian space."
          q=modvec(H, K, L,astar,bstar,cstar,alphastar,N.betastar,gammastar);
          return q
