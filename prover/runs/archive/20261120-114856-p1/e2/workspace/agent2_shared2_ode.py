"""Special shared-two-root n=6 blow-up. Numerical leading field; not proof."""
import numpy as np
class Shared2ODE:
 def __init__(self,eps=.012,richardson=True):
  self.eps=eps; self.richardson=richardson
  self.h=.1
  self.lam=np.sort(np.roots([1.,-1.,-8.,8.,16.,-16.,-.1]).real)
  x=self.lam;self.d=np.array([1/np.prod(x[i]-np.delete(x,i)) for i in range(6)])
  self.X=np.array([np.ones(6),x,x*x]).T;self.x3=x**3
  self.s1=sum(x);self.s2=(self.s1**2-sum(x*x))/2;self.t2=self.s1**2-self.s2
  self.bounds=(self.lam[1],self.lam[2],self.lam[3],self.lam[4])
 def energy(self,U,V,A,B,D):
  return A*A*(-4*U+4*V+16)+A*B*(8*U-2*V-8)+B*B*(-U+V+4)+4*D*V
 def solve_D(self,U,V,A,B):return (1-self.energy(U,V,A,B,0))/(4*V)
 def poly(self,w):
  c=np.linalg.solve(self.X.T@(w[:,None]*self.X),-self.X.T@(w*self.x3))
  p=self.x3+self.X@c;h=w@(p*p)
  return c,p,h
 def finite(self,z,e):
  U,V,A,B,D=z;x=self.lam;z0=e*e*D
  p0=(x-z0)*(x*x-4+e*(A*x+B))
  raw=self.d*(x*x+U*x+V)/p0;w0=raw/sum(raw)
  h0=w0@(p0*p0);w1=w0*p0*p0/h0
  c1,p1,h1=self.poly(w1);w2=w1*p1*p1/h1
  c2,p2,h2=self.poly(w2)
  c0=np.array([z0*(4-e*B),-4+e*B-z0*e*A,e*A-z0]);dc=c2-c0
  # Difference of nearby unshared roots, without subtracting absolute roots.
  val=dc[0]+z0*(dc[1]+z0*dc[2]);der=3*z0*z0+2*c2[2]*z0+c2[1]
  dz=-val/der
  for _ in range(2):
   v=val+der*dz+(3*z0+c2[2])*dz*dz+dz**3
   dz-=v/(der+2*(3*z0+c2[2])*dz+3*dz*dz)
  Adot=(dc[2]+dz)/e**3;Anew=A+e*e*Adot
  Bdot=dc[1]/e**3+z0*Adot+(dz/e**2)*Anew
  Ddot=dz/e**4
  delta=w2*p2-w0*p0;dh=delta@self.x3
  du=(delta@(x**4)-(self.s1+U)*dh)/h2
  dv=(delta@(x**5)-(self.t2+U*self.s1+V)*dh)/h2-self.s1*du
  damp=(w0@((p0*p1-h0)**2)/h0+w1@((p1*p2-h1)**2)/h1)/e**4
  return np.array([du/e**2,dv/e**2,Adot,Bdot,Ddot,damp]),w0,h0
 def data(self,y):
  U,V,A,B=y;D=self.solve_D(U,V,A,B);z=(U,V,A,B,D);e=self.eps
  f=(self.finite(z,e)[0]+self.finite(z,-e)[0])/2
  if self.richardson:
   f2=(self.finite(z,2*e)[0]+self.finite(z,-2*e)[0])/2
   f=(4*f-f2)/3
  f[2]+=f[5]*A/2;f[3]+=f[5]*B/2
  return f,D
 def rhs(self,t,y):return self.data(y)[0][:4]
 def pos(self,y):
  U,V=y[:2];roots=np.sort(np.roots([1,U,V]));return roots
 def event(self,t,y):
  roots=self.pos(y)
  if np.max(abs(roots.imag))>1e-8:return -1
  a,b=roots.real;l,r,L,R=self.bounds
  return min(a-l,r-a,b-L,R-b)-1e-5
 event.terminal=True
 event.direction=-1
 def center(self,A=0.1,B=0.1):
  l,r,L,R=self.bounds;a=(l+r)/2;b=(L+R)/2
  return np.array([-a-b,a*b,A,B])
