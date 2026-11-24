"""Independent interval certificate for finite polynomial graph dilation forms.

SCOPE. Algebraic subcritical jet forms only; this is NOT a proof of Yamabe
compactness or noncompactness. Every asserted positivity uses interval arithmetic
and an explicit infinite-series tail bound. No truncated floating spectrum is
used as evidence.

Let alpha=(n-3)/2+q. A degree-(q+2i) graph h=P_q r^(2i) has spherical
normal displacement whose Gegenbauer/Jacobi radial expansion is the expansion
of g_i(t)=(1-t)^i/(1+t)^(q+i-1). Expand this into powers
 (1+t)^(-s), with c_is=binom(i,j)2^j(-1)^(i-j), s=q-1+j.
The coefficient integral (ignoring the common parity sign) is
 I_s(k)=2^(2alpha-s+1)*(s)_k/k!*B(alpha+k+1,alpha-s+1).
The Jacobi squared norm is
 h_k=2^(2alpha+1)/(2k+2alpha+1)*Gamma(k+alpha+1)^2/
       (Gamma(k+1)Gamma(k+2alpha+1)).
The hemisphere DtN eigenvalue for total angular degree l=k+q is
 D_l=2 Gamma(l/2)Gamma((l+n+1)/2)/
       (Gamma((l-1)/2)Gamma((l+n)/2)).
Terms l<2 are omitted (gauge/Dirichlet-resonance sectors).
Set lambda_l=(l-1)(l+n-1). Then
 Q_ij=sum_k lambda_l^2/D_l/h_k * [sum_s c_is I_s(k)]
                                      *[sum_t c_jt I_t(k)],
 K_ij=(q-1+i+j)Q_ij.
We remove graph gauge directions i<2 at q=0 and i<1 at q=1.

For tail estimates the positive pair summand is a constant times
 (2k+2alpha+1)*Gamma(k+s)Gamma(k+t)Gamma(k+2alpha+1)/
 [Gamma(k+1)Gamma(k+2alpha-s+2)Gamma(k+2alpha-t+2)] *lambda_l^2/D_l.
All displayed Gamma ratios with arguments k+integer reduce to products of
positive linear factors. In even dimension 1/D_l is rational in k.
In odd dimension n=2m+1 put x=(l-1)/2. Gamma log-convexity implies
 [Gamma(x)/Gamma(x+1/2)]^2 <=(x+1/2)/x^2; hence
 1/D_l <=(x+1/2)/(2x^2)*(x)_(m+1)/(x+1/2)_(m+1).
This too is rational. For k>=N, bound numerator factors k+a by
 k*max(1,1+a/N) and denominator factors below by
 k*min(1,1+a/N). Thus T_st(k)<=C_st k^(-p) with p>1.
The remaining sum is bounded by C_st*(N^(-p)+N^(1-p)/(p-1)).
Absolute coefficient sums give entrywise tail enclosures. Interval LDL
with positive lower pivot bounds certifies positivity of the full matrices.

Requires SymPy and mpmath. Run from the project root. Runtime about15sec.
"""
import sympy as s
from mpmath import iv
from collections import Counter
import math,time
iv.dps=40

def iev(e):
 e=s.simplify(s.expand_func(e))
 if e==s.pi:return iv.pi
 if e.is_Rational:return iv.mpf(int(e.p))/int(e.q)
 if e.is_Add:return sum((iev(a) for a in e.args),iv.mpf(0))
 if e.is_Mul:
  v=iv.mpf(1)
  for a in e.args:v*=iev(a)
  return v
 if e.is_Pow:return iev(e.base)**iev(e.exp)
 raise ValueError(e)

def tail(n,q,ss,tt,N):
 alpha=s.Rational(n-3,2)+q
 C=2**(2*alpha-ss-tt+2)*s.gamma(alpha-ss+1)*s.gamma(alpha-tt+1)/(s.gamma(ss)*s.gamma(tt))
 num=[alpha+s.Rational(1,2)]+list(range(ss))+list(range(tt))+list(range(int(2*alpha+1)))+[q-1]*2+[q+n-1]*2
 den=[0]+list(range(int(2*alpha-ss+2)))+list(range(int(2*alpha-tt+2)))
 if n%2==0:
  m=n//2
  num+=list(q+2*r for r in range(m))
  den+=list(q-1+2*r for r in range(m+1))
 else:
  m=(n-1)//2
  num+=[q]+list(q-1+2*r for r in range(m+1))
  den+=[q-1]*2+list(q+2*r for r in range(m+1))
 nc,dc=Counter(num),Counter(den)
 for a in list(nc):
  cancel=min(nc[a],dc[a]);nc[a]-=cancel;dc[a]-=cancel
 degree=sum(dc.values())-sum(nc.values())
 assert degree>1,(n,q,ss,tt,degree)
 factor=s.Rational(1)
 for a,p in nc.items():
  if a>0:factor*=(1+a/s.Integer(N))**p
 for a,p in dc.items():
  if a<0:factor/=(1+a/s.Integer(N))**p
 bound=iev(C*factor)*(iv.mpf(N)**(-degree)+iv.mpf(N)**(1-degree)/(degree-1))
 return bound.b

def certify(n,q,J,N=2000,verbose=True):
 alpha=s.Rational(n-3,2)+q
 start={0:2,1:1}.get(q,0);inds=list(range(start,J+1));sz=len(inds)
 if not sz:return
 sslist=list(range(max(1,q-1),q+J))
 I={ss:iev(2**(2*alpha-ss+1)*s.gamma(alpha+1)*s.gamma(alpha-ss+1)/s.gamma(2*alpha-ss+2)) for ss in sslist}
 h=iev(2**(2*alpha+1)/(2*alpha+1)*s.gamma(alpha+1)**2/s.gamma(2*alpha+1))
 D=[]
 k0=max(0,2-q)
 for kk in [k0,k0+1]:
  l=s.Integer(q+kk)
  D.append(iev(2*s.gamma(l/2)*s.gamma((l+n+1)/2)/(s.gamma((l-1)/2)*s.gamma((l+n)/2))))
 M=[[iv.mpf(0) for j in inds] for i in inds]
 coeff={i:{q-1+j:s.binomial(i,j)*2**j*(-1)**(i-j) for j in range(i+1) if q-1+j>0} for i in inds}
 for k in range(N):
  if k>=k0:
   # coefficients at k>=k0: nonpositive s terms are supported only at l<2, omitted.
   vals=[sum((int(c)*I[ss] for ss,c in coeff[i].items()),iv.mpf(0)) for i in inds]
   l=k+q
   w=iv.mpf((l-1)**2*(l+n-1)**2)/D[(k-k0)%2]/h
   for a in range(sz):
    for b in range(a,sz):M[a][b]+=w*vals[a]*vals[b]
   D[(k-k0)%2]*=iv.mpf(l*(l+n+1))/((l-1)*(l+n))
  # advance I,h from k to k+1
  for ss in sslist:I[ss]*=iev((k+ss)*(k+alpha+1)/((k+1)*(k+2*alpha-ss+2)))
  h*=iev((2*k+2*alpha+1)/(2*k+2*alpha+3)*(k+alpha+1)**2/((k+1)*(k+2*alpha+1)))
 for a,i in enumerate(inds):
  for b,j in enumerate(inds):
   if b<a:continue
   err=iv.mpf(0)
   for ss,ci in coeff[i].items():
    for tt,cj in coeff[j].items():err+=abs(int(ci*cj))*tail(n,q,ss,tt,N)
   e=math.nextafter(float(err.b),math.inf)
   v=M[a][b]+iv.mpf([-e,e])
   M[a][b]=M[b][a]=v*(q-1+i+j)
 # scale entries using central diagonal to aid reading
 scale=[math.sqrt(float(M[a][a].b)) for a in range(sz)]
 A=[[M[a][b]/scale[a]/scale[b] for b in range(sz)] for a in range(sz)]
 piv=[]
 LL=[[iv.mpf(0) for b in range(sz)] for a in range(sz)]
 for a in range(sz):
  pivot=A[a][a]-sum((LL[a][c]**2*piv[c] for c in range(a)),iv.mpf(0))
  assert float(pivot.a)>0,(n,q,J,N,a,pivot)
  piv.append(pivot);LL[a][a]=iv.mpf(1)
  for b in range(a+1,sz):LL[b][a]=(A[b][a]-sum((LL[b][c]*LL[a][c]*piv[c] for c in range(a)),iv.mpf(0)))/pivot
 if verbose:print('CERTIFIED',n,q,J,N,[(float(v.a),float(v.b)) for v in piv],flush=True)
 return piv

if __name__=='__main__':
 t=time.time()
 for n in range(3,19):
  for q in range(0,(n-1)//2+1):
   J=(n-1-2*q)//4
   if J<{0:2,1:1}.get(q,0):continue
   certify(n,q,J,N=2000)
 print('time',time.time()-t)
 from pathlib import Path
 Path('workspace/agent4_interval_jet_forms.py').write_text(Path(__file__).read_text())
