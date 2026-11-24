from pathlib import Path
p=Path('workspace/agent2_endpoint_checks.py')
p.write_text('''"""Independent checks: actual normalized polynomials, canonical ring rows,
Fourier support and positive small-radius endpoint. Run with Python (mpmath).
The proof for arbitrary m is analytic; these finite tests audit conventions.
"""
import mpmath as mp
mp.mp.dps=80

def mul(p,q):
 out=[mp.mpc(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):out[i+j]+=a*b
 return out

def poly(factors):
 p=[mp.mpc(1)]
 for f in factors:p=mul(p,f)
 return p

def check(m,eps):
 K=m; z=mp.exp(2j*mp.pi/m); h=mp.mpf('.001')
 r=eps; R=10*eps
 # clustered axis values only: actual order still defines limiting polynomials
 pts=[(mp.mpf(-10),mp.mpc(0))]*K+[(0,r*z**k) for k in range(m)]+[(h,R*z**k) for k in range(m)]+[(mp.mpf('.1'),mp.mpc(0))]*K
 n=len(pts); factors=[[None]*n for _ in range(n)]
 for i in range(n):
  for j in range(i+1,n):
   dh=pts[j][0]-pts[i][0];dw=pts[j][1]-pts[i][1]
   if not dh and not dw: # limiting oriented axial factors
    factors[i][j]=[1];factors[j][i]=[0,1];continue
   D=dh+mp.sqrt(dh*dh+abs(dw)**2)
   factors[i][j]=[1,-mp.conj(dw)/D];factors[j][i]=[dw/D,1]
 rows=[poly([factors[i][j] for j in range(n) if j!=i]) for i in range(n)]
 rows=[p+[0]*(n-len(p)) for p in rows]
 f=lambda d,s:s/(d+mp.sqrt(d*d+s*s))
 x=f(10,r);y=f(10+h,R);u=f(mp.mpf('.1'),r);v=f(mp.mpf('.1')-h,R)
 F=poly([[1,1j*mp.exp(-mp.pi*1j*k/m)] for k in range(1,m)])
 Ds=[h+mp.sqrt(h*h+r*r+R*R-2*r*R*mp.cos(2*mp.pi*k/m)) for k in range(m)]
 C=poly([[1,-(R*z**(-k)-r)/Ds[k]] for k in range(m)])
 E=poly([[(R-r*z**k)/Ds[k],1] for k in range(m)])
 A=poly([[x,1]]*K+[[1,u]]*K);A=mul(mul(A,F),C)
 B=poly([[y,1]]*K+[[1,v]]*K);B=mul(mul(B,F),E)
 err=mp.mpf(0)
 for offset,base in [(K,A),(K+m,B)]:
  for k in range(m):
   target=[z**(k*K-k*e)*base[e] for e in range(n)]
   ix=max(range(n),key=lambda e:abs(target[e]));scale=rows[offset+k][ix]/target[ix]
   err=max(err,max(abs(rows[offset+k][e]-scale*target[e]) for e in range(n))/max(1,max(map(abs,rows[offset+k]))))
 assert err<mp.mpf('1e-65'),(m,eps,err)
 # Compute residue-zero canonical Schur complement by unit pivots.
 ix=list(range(0,n,m)); aa=[A[e] for e in ix];bb=[B[e] for e in ix]
 low=[rows[j] for j in range(K) if j%m==0]
 high=[rows[K+2*m+j] for j in range(K) if (K+j)%m==0]
 for row in low:
  q=[row[e] for e in ix];pivot=next(i for i,t in enumerate(q) if abs(t)>mp.mpf('1e-75'))
  for p in (aa,bb):
   c=p[pivot]/q[pivot]
   for i in range(len(p)):p[i]-=c*q[i]
 for row in high[::-1]:
  q=[row[e] for e in ix];pivot=max(i for i,t in enumerate(q) if abs(t)>mp.mpf('1e-75'))
  for p in (aa,bb):
   c=p[pivot]/q[pivot]
   for i in range(len(p)):p[i]-=c*q[i]
 i=ix.index(K);j=ix.index(K+m);det=aa[i]*bb[j]-aa[j]*bb[i]
 assert abs(mp.im(det))<mp.mpf('1e-60')
 return err,mp.re(det)

if __name__=='__main__':
 for m in range(1,9):
  err,_=check(m,mp.mpf(1))
  _,d=check(m,mp.mpf('1e-12'))
  assert abs(d-1)<mp.mpf('1e-6'),(m,d)
  print('m=',m,'canonical relative error=',mp.nstr(err,4),'small-radius block det=',mp.nstr(d,16))
''')
exec(compile(p.read_text(),str(p),'exec'))
