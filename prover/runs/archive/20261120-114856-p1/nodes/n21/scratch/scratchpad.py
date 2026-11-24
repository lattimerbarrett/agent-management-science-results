import numpy as np
lam=np.array([1.,2.,4.,9.,20.]); s=2
w=np.array([1.,4.,1.,9.,4.]);w/=sum(w)
shifts=[-10.,0.,.9,21.,40.]
previous=None
for k in range(8):
 V=np.column_stack([lam**j for j in range(s)])
 c=np.linalg.solve(V.T@(w[:,None]*V),-V.T@(w*lam**s))
 q=lam**s+V@c; H=w@(q*q); wn=w*q*q/H
 vals=[]
 for t in shifts:
  qt=t**s+sum(c[j]*t**j for j in range(s))
  M=w@(1/abs(lam-t)); Mn=wn@(1/abs(lam-t))
  vals.append(np.sqrt(H*Mn/M)/abs(qt))
 vals=np.array(vals)
 print(k,'H',H,'shifted contractions',vals)
 if previous is not None: assert np.min(vals-previous)>-1e-10
 previous=vals; w=wn
