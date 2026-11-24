import mpmath as mp
from fractions import Fraction as F
mp.mp.dps=80

def mul(a,b):
 c=[mp.mpc(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def ev(a,t):return sum(x*t**i for i,x in enumerate(a))

def core(m):
 al=ep=mp.mpf('.5');be=100/(mp.mpf('.75')+mp.sqrt(10000+mp.mpf(9)/16));de=1/(75+mp.sqrt(5626))
 A=[mp.mpc(1)];B=A.copy()
 for j in range(1,m):
  f=[1,mp.j*mp.exp(-mp.j*mp.pi*j/m)];A=mul(A,f);B=mul(B,f)
 for j in range(m):
  z=mp.exp(2*mp.j*mp.pi*j/m);D=mp.sqrt(10001-200*z.real)
  A=mul(A,[1,-mp.conj((100*z-1)/D)]);B=mul(B,[(100-z)/D,1])
 assert max(abs(x.imag) for x in A+B)<mp.mpf('1e-65')*max(abs(x) for x in A+B)
 return al,be,de,ep,[x.real for x in A],[x.real for x in B]

def certificate(m):
 al,be,de,ep,HA,HB=core(m)
 UA=lambda t:(t+al)*(1+de*t)
 UB=lambda t:(t+be)*(1+ep*t)
 t=1/be;s=mp.sqrt(al/de);eta=t*UA(s)/s
 Cfourier=sum(abs(ev(HA,t*mp.exp(2*mp.j*mp.pi*j/m))) for j in range(1,m))/m
 r=max([abs(UA(t*mp.exp(2*mp.j*mp.pi*j/m)))/UA(t) for j in range(1,m)]+[mp.mpf(0)])
 Ctail=ev(list(map(abs,HA)),s);c=abs(ev(HA,t))/(2*m)
 CA=ev(list(map(abs,HA)),2);CB=ev(HB,t);h0=HB[0]
 ratio=UA(2)*UB(t)/(UA(t)*2*(1+mp.sqrt(be*ep))**2)
 assert ev(HA,t)<0 and min(HB)>0 and r<1 and eta<UA(t) and ratio<1
 for K in range(1,100000):
  k=m*K
  e1=Cfourier*r**k+Ctail*(eta/UA(t))**k
  e2=(k+1)*CA*CB/(c*h0)*ratio**k
  if e1<c and e2<1:return K
 raise RuntimeError('Increase search limit')

def boundary_block(m,K):
 al,be,de,ep,A,B=core(m);k=m*K
 for _ in range(k):A=mul(mul(A,[al,1]),[1,de]);B=mul(mul(B,[be,1]),[1,ep])
 C=mp.matrix(2*K+2)
 for q in range(2*K):
  row=[1,-al**m-be**m,(al*be)**m] if q<K else [(de*ep)**m,-de**m-ep**m,1]
  for j,x in enumerate(row):C[q,q+j]=x
 for q,x in enumerate(A[::m]):C[2*K,q]=x.real
 for q,x in enumerate(B[::m]):C[2*K+1,q]=x.real
 return C

def normalized_det(C):
 C=C.copy()
 for i in range(C.rows):
  s=max(abs(C[i,j]) for j in range(C.cols))
  for j in range(C.cols):C[i,j]/=s
 return mp.det(C)

def direct(m,lows,ups,H,r,R):
 Q=[(mp.mpf(x),0) for x in lows]+[(0,r*mp.exp(2*mp.j*mp.pi*j/m)) for j in range(m)]+[(H,R*mp.exp(2*mp.j*mp.pi*j/m)) for j in range(m)]+[(mp.mpf(x),0) for x in ups]
 n=len(Q);P=[[mp.mpc(1)] for _ in Q]
 for i in range(n):
  for j in range(i+1,n):
   dz=Q[j][0]-Q[i][0];w=Q[j][1]-Q[i][1];D=dz+mp.sqrt(dz*dz+abs(w)**2)
   P[i]=mul(P[i],[1,-mp.conj(w)/D]);P[j]=mul(P[j],[w/D,1])
 return mp.matrix([p+[0]*(n-len(p)) for p in P])

if __name__=='__main__':
 assert F(507,200)*F(199*149,99**2)<8<F(867,100)
 assert F(7,1000)<F(1,2)*F(99,100)**2
 for m in [1,2,3,4,5,7,10,20]:
  K=certificate(m);d=normalized_det(boundary_block(m,K))
  assert abs(d.imag)<mp.mpf('1e-60') and d.real<0
  print('m,K,negative block determinant:',m,K,mp.nstr(d.real,12),flush=True)
 # Entirely independent original-pair calculation at an ADMISSIBLE witness.
 m=1;k=40;e=mp.mpf('1e-9')
 lows=[-mp.mpf('.75')-e*(k-j) for j in range(k)]
 ups=[75+e*j for j in range(k)]
 d=normalized_det(direct(m,lows,ups,e,mp.mpf(1),mp.mpf(100)))
 assert abs(d.imag)<mp.mpf('1e-60') and d.real<0
 print('direct admissible n=82 determinant:',mp.nstr(d.real,16),flush=True)
 with open('workspace/agent1_finalcheck.py','w') as f:f.write(open('scratchpad.py').read())
