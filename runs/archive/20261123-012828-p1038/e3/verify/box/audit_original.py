import mpmath as mp
mp.mp.dps=120
K=150
N=2*K+2
q=[(mp.mpf(-10)+mp.mpf('1e-10')*j,mp.mpf(0)) for j in range(K)]
q += [(mp.mpf(0),mp.mpf(1)),(mp.mpf('0.001'),mp.mpf(10))]
q += [(mp.mpf('0.1')+mp.mpf('1e-10')*j,mp.mpf(0)) for j in range(K)]
M=mp.matrix(N,N)
for i in range(N):
 p=[mp.mpf(1)]
 shift=0
 for j in range(N):
  if j==i: continue
  lo,hi=min(i,j),max(i,j)
  dh=q[hi][0]-q[lo][0]
  dw=q[hi][1]-q[lo][1]
  D=dh+mp.sqrt(dh*dh+dw*dw)
  if i<j:
   a,b=mp.mpf(1),-dw/D
  else:
   a,b=dw/D,mp.mpf(1)
  if b==0: continue
  if a==0: shift+=1;continue
  new=[mp.mpf(0)]*(len(p)+1)
  for e,c in enumerate(p):
   new[e]+=a*c
   new[e+1]+=b*c
  p=new
 for e,c in enumerate(p): M[i,e+shift]=c
val=mp.det(M)
print('Strict distinct original-definition matrix determinant:',mp.nstr(val,50))
assert val<0
