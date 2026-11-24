import mpmath as mp
import numpy as np

def verify(filename,dps=100):
 mp.mp.dps=dps
 f=np.load(filename);m=int(f['m']);lows=[mp.mpf(float(t)) for t in f['low']];ups=[mp.mpf(float(t)) for t in f['up']];H=mp.mpf(float(f['H']));R=mp.mpf(float(f['R']));r=mp.mpf(1)
 Q=[(z,mp.mpc(0)) for z in lows]+[(mp.mpf(0),r*mp.exp(2j*mp.pi*k/m)) for k in range(m)]+[(H,R*mp.exp(2j*mp.pi*k/m)) for k in range(m)]+[(z,mp.mpc(0)) for z in ups]
 n=len(Q);P=[[mp.mpc(1)] for _ in Q]
 def mul(p,a,b):
  q=[mp.mpc(0)]*(len(p)+1)
  for j,v in enumerate(p):q[j]+=a*v;q[j+1]+=b*v
  return q
 for i in range(n):
  for j in range(i+1,n):
   h=Q[j][0]-Q[i][0];w=Q[j][1]-Q[i][1];D=h+mp.sqrt(h*h+abs(w)**2)
   P[i]=mul(P[i],1,-w.conjugate()/D);P[j]=mul(P[j],w/D,1)
 for i in range(n):
  P[i]+=[0]*(n-len(P[i]));scale=max(abs(v) for v in P[i]);P[i]=[v/scale for v in P[i]]
 return mp.det(mp.matrix(P))
