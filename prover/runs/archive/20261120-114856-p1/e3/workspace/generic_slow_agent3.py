import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp
class GenericSlow:
 def __init__(self,a,b,c,d,H,xi,eta):
  mp.mp.dps=60
  self.a=np.longdouble(str(a));self.b=np.longdouble(str(b))
  pc=[1,a+c,b+d+a*c,a*d+b*c,b*d-H]
  roots=sorted(mp.polyroots([mp.mpf(str(x)) for x in pc],maxsteps=1000),key=float)
  self.roots=np.array([str(x) for x in roots],dtype=np.longdouble);self.l=np.r_[self.roots,np.longdouble(str(xi)),np.longdouble(str(eta))]
  V=mp.matrix([[x**j for x in roots] for j in range(4)]);iv=V**-1
  self.iv=np.array([[str(iv[i,j]) for j in range(4)]for i in range(4)],dtype=np.longdouble)
 def weights(self,m,h,z,w1,w2):
  m,h,z,w1,w2=map(np.longdouble,[m,h,z,w1,w2]);M2=-self.a*m-self.b+h;M3=-self.a*M2-self.b*m+z
  mom=np.array([1,m,M2,M3],dtype=np.longdouble)-np.array([[self.l[4]**j,self.l[5]**j]for j in range(4)])@np.array([w1,w2])
  return np.r_[self.iv@mom,w1,w2]
 def step(self,w):
  l=self.l;M=[sum(w*l**j)for j in range(4)];aa=(M[1]*M[2]-M[3])/(M[2]-M[1]**2);bb=-M[2]-aa*M[1];pp=l*l+aa*l+bb;ww=w*pp*pp;return ww/sum(ww)
 def moments(self,w):
  m=w@self.l;M2=w@(self.l**2);M3=w@(self.l**3)
  return m,M2+self.a*m+self.b,M3+self.a*M2+self.b*m,w[4],w[5]
 def finite(self,y,r):
  m,p,q1,q2=map(np.longdouble,y);r=np.longdouble(r);w=self.weights(m,-r,p*r,q1*r*r,q2*r*r);nw=self.step(self.step(w));mm,hh,zz,e1,e2=self.moments(nw)
  A=(mm-m)/r;B=(hh+r)/(r*r);C=(zz-p*r)/(r*r)
  return np.array([A,C+p*B,(e1-q1*r*r)/r**3+2*q1*B,(e2-q2*r*r)/r**3+2*q2*B,B],dtype=float)
 def rhsfull(self,y):
  e=1e-4
  x=(self.finite(y,e)+self.finite(y,-e))/2
  y2=(self.finite(y,e/2)+self.finite(y,-e/2))/2
  return (4*y2-x)/3
 def rhs(self,t,y):return self.rhsfull(y)[:4]

 def normmonic(self,w):
  l=self.l;M=[sum(w*l**j)for j in range(4)];a=(M[1]*M[2]-M[3])/(M[2]-M[1]**2);b=-M[2]-a*M[1];p=l*l+a*l+b;return sum(w*p*p)
 def jacapply(self,w,dw):
  l=self.l;M=[sum(w*l**j)for j in range(4)];D=[sum(dw*l**j)for j in range(4)];var=M[2]-M[1]**2;N=M[1]*M[2]-M[3];a=N/var;b=-M[2]-a*M[1]
  da=((D[1]*M[2]+M[1]*D[2]-D[3])*var-N*(D[2]-2*M[1]*D[1]))/var**2;db=-D[2]-da*M[1]-a*D[1];p=l*l+a*l+b;dp=da*l+db;H=sum(w*p*p);dH=sum(dw*p*p);nw=w*p*p/H;ndw=(dw*p*p+2*w*p*dp)/H-nw*dH/H;return nw,ndw
 def Acoeff(self,m):
  w=self.weights(m,0,0,0,0);dwh=np.r_[self.iv@np.array([0,0,1,-self.a],dtype=np.longdouble),0,0];dwz=np.r_[self.iv@np.array([0,0,0,1],dtype=np.longdouble),0,0]
  w1,h1=self.jacapply(w,dwh);w2,h2=self.jacapply(w1,h1);_,z1=self.jacapply(w,dwz);_,z2=self.jacapply(w1,z1)
  return h2@self.l,z2@self.l
 def setenergy(self,c,d,H):
  self.c=np.longdouble(str(c));self.d=np.longdouble(str(d));self.H=np.longdouble(str(H))
 def energyfinite(self,y,r):
  m,p,q1,q2=map(np.longdouble,y);r=np.longdouble(r);Ah,Az=self.Acoeff(m);eh=self.b-self.d;ez=self.a-self.c;det=eh*Az-ez*Ah;hh=(-Az-ez*p)*r/det;zz=(eh*p+Ah)*r/det
  w=self.weights(m,hh,zz,q1*r*r,q2*r*r);nw=self.step(self.step(w));mm,hn,zn,e1,e2=self.moments(nw);rn=-((self.b-self.d)*hn+(self.a-self.c)*zn);Ahn,Azn=self.Acoeff(mm);pn=(Ahn*hn+Azn*zn)/rn;yn=np.array([mm,pn,e1/rn**2,e2/rn**2],dtype=np.longdouble)
  return np.r_[(yn-np.array(y,dtype=np.longdouble))/r,(r-rn)/r**2].astype(float)
 def energyrhsfull(self,y):
  e=1e-4;x=(self.energyfinite(y,e)+self.energyfinite(y,-e))/2;y2=(self.energyfinite(y,e/2)+self.energyfinite(y,-e/2))/2;return (4*y2-x)/3
 def energyrhs(self,t,y):return self.energyrhsfull(y)[:4]

 def extrafinite(self,y,r):
  m,p,eta,k=map(np.longdouble,y);r=np.longdouble(r);Ah,Az=self.Acoeff(m);eh=self.b-self.d;ez=self.a-self.c;det=eh*Az-ez*Ah;hh=(eta*Az-ez*p)*r/det;zz=(eh*p-Ah*eta)*r/det
  w=self.weights(m,hh,zz,(1-k)*r*r,k*r*r);nw=self.step(self.step(w));mm,hn,zn,e1,e2=self.moments(nw);rn=np.sqrt(e1+e2)*np.sign(r);Ahn,Azn=self.Acoeff(mm);pn=(Ahn*hn+Azn*zn)/rn;en=((self.b-self.d)*hn+(self.a-self.c)*zn)/rn;kn=e2/(e1+e2);yn=np.array([mm,pn,en,kn],dtype=np.longdouble)
  return np.r_[(yn-np.array(y,dtype=np.longdouble))/r,(rn-r)/r**2].astype(float)
 def extrarhsfull(self,y):
  e=1e-4;x=(self.extrafinite(y,e)+self.extrafinite(y,-e))/2;y2=(self.extrafinite(y,e/2)+self.extrafinite(y,-e/2))/2;return (4*y2-x)/3
 def extrarhs(self,t,y):return self.extrarhsfull(y)[:4]
