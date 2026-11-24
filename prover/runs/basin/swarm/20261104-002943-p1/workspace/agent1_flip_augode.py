import numpy as np
from scipy.optimize import root
D=np.load('workspace/agent1_flip_cycle.npz');x=D['lam'];w0=D['w0'];p=D['p'];q=D['q'];C=float(D['C']);s=4;n=8;V=x[:,None]**np.arange(s);offs=np.array([6,7])

def weightjet(ws,ref):
 order=len(ws)-1;Ms=[V.T@(w[:,None]*V) for w in ws];ps=[ref]+[None]*order;cs=[np.zeros(s)]
 for j in range(1,order+1):
  rhs=V.T@(ws[j]*ref)
  for l in range(1,j):rhs+=Ms[l]@cs[j-l]
  cs.append(-np.linalg.solve(Ms[0],rhs));ps[j]=V@cs[j]
 raw=[np.zeros(n) for j in range(order+1)]
 for j in range(order+1):
  for a in range(j+1):
   for b in range(j-a+1):raw[j]+=ws[a]*ps[b]*ps[j-a-b]
 den=[r.sum() for r in raw];out=[]
 for j in range(order+1):
  v=raw[j].copy()
  for l in range(1,j+1):v-=den[l]*out[j-l]
  out.append(v/den[0])
 return out

def ode(t,z):
 w=z[:n];hc=z[n:n+s];amps=z[n+s:];h=V@hc;u=w*p*h
 w2=np.zeros(n);w2[offs]=amps*amps;w2-=sum(amps*amps)*w
 out=weightjet(weightjet([w,u,w2,np.zeros(n)],p),q);b=out[1]-u
 G=V.T@((w*p*p)[:,None]*V);hd=np.linalg.solve(G,V.T@(p*(out[2]-w2-b*p*h)))
 ad=np.divide(out[3][offs],2*amps,out=np.zeros(len(offs)),where=amps!=0)
 return np.r_[b,hd,ad]
