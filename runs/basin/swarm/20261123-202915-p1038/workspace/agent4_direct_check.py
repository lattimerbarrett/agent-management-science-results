import numpy as np, mpmath as mp
mp.mp.dps=100
d=np.load('workspace/agent1_negative_m4.npz'); m=int(d['m']); ls=[mp.mpf(float(x)) for x in d['low']]; us=[mp.mpf(float(x)) for x in d['up']]; H=mp.mpf(float(d['H'])); R=mp.mpf(float(d['R'])); rho=int(d['k']); a=len(ls);b=len(us); n=a+b+2*m
Q=[(x,mp.mpc(0)) for x in ls]+[(mp.mpf(0),mp.exp(2j*mp.pi*k/m)) for k in range(m)]+[(H,R*mp.exp(2j*mp.pi*k/m)) for k in range(m)]+[(x,mp.mpc(0)) for x in us]
def mul(p,q):
 z=[mp.mpc(0)]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):z[i+j]+=x*y
 return z
def row(i):
 p=[mp.mpc(1)]
 for j in range(n):
  if i==j: continue
  u,v=sorted((i,j)); h=Q[v][0]-Q[u][0]; w=Q[v][1]-Q[u][1]; D=h+mp.sqrt(h*h+abs(w)**2)
  f=[1,-mp.conj(w)/D] if i==u else [w/D,1]
  p=mul(p,f)
 return p
inds=list(range(rho,a+b,m)); C=mp.matrix(len(inds)+2)
for q,j in enumerate(inds):
 i=j if j<a else j+2*m
 p=row(i)
 vals=p[rho::m];norm=max(abs(z) for z in vals)
 for k,x in enumerate(vals):C[q,k]=x/norm
for ii,i in enumerate([a,a+m]):
 p=row(i);vals=p[rho::m]; phase=next(z/abs(z) for z in vals if abs(z)>mp.mpf('1e-60')); vals=[z/phase for z in vals]; norm=max(abs(z) for z in vals)
 print('row imag',max(abs(mp.im(x)) for x in vals)/norm)
 for k,x in enumerate(vals):C[len(inds)+ii,k]=x/norm
print('direct projected block determinant',mp.nstr(mp.det(C),50))
print('m,n,rho',m,n,rho)
import shutil
shutil.copyfile('scratchpad.py','workspace/agent4_direct_check.py')
