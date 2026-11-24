from pathlib import Path
Path('workspace/agent2_comb_characteristic.md').write_text(r'''# Uniform dyadic characteristic of the asymmetric-jump comb

Fix p>2, q=p/(p-1), v=1/(p-1), Q>=max(2,2^(p-1)), and let
t=Q^-1, s=Q^-v, r=2-t, z=2-s, k=Q^(v/p).
Thus 0<t<=s<=1/2 and 3/2<=z<=r<2.

At each active node with state(a,c,h), first take the two equal-probability rotation children h'=h+-k/c. At each rotation child, take the equal-probability stretch children (ra,zc,h') and (ta,sc,h'). The latter absorbs, the former continues. Swapping stretch labels after a rotation changes only placement, not any estimate below. Stop all surviving paths after L cycles. Put
M(a,c,h)=[[a^(1/p),a^(1/p)h],[0,a^(1/p)/c]].
The characteristic considered is the dyadic version of the question's mixed root-kernel characteristic; the reduction to full real-interval characteristic and Hilbert transform is NOT established by this lemma.

The scalar processes a,c,ah,ch are martingales, and Ea_T=1 at root(1,1,0). Under probability mu with density a_T, exitage n<L has mass (t/2)(r/2)^n, and then a_T=t r^n,c_T=s z^n. Surviving terminal ageL has mu mass(r/2)^L and values a_T=r^L,c_T=z^L. Moreover |h_T|<=k sum_{j>=0}z^-j<=3k. The same bound holds when starting immediately before a stretch (with the first rotation omitted), and for any signs or stretch-label swaps.

Let R=c/a. Direct geometric sums give
E_mu a_T^-q <= 2 Q^v,
E_mu c_T^-p <= C_p Q^v,
E_mu R_T^q <= 2 Q^(v(1-v)).
Indeed the first absorbed contribution is
(t^(1-q)/2) sum_{n<L}(r^(1-q)/2)^n,
whose ratio is<=1/2, plus survivor contribution(r^(1-q)/2)^L<=1.
The second is
(t s^-p/2) sum_{n<L}(r/(2z^p))^n,
whose ratio is<=(2/3)^p, plus survivor contribution<=1; and t s^-p=Q^v.
The third is
(t/2)(s/t)^q sum_{n<L} H^n,
where H=z^q/(2r^(q-1))<=z/2=1-s/2. It is at most(s/t)^(q-1), plus survivorH^L<=1. Since(s/t)^(q-1)=Q^(v(1-v))>=1, the claimed bound follows.

For any vector e=(e1,e2), elementary l2/lp equivalence gives
(E|M e|^p)^(1/p)<=C_p (|e1|+Q^(v/p)|e2|).
Also M^(-*)e=(a^(-1/p)e1,c a^(-1/p)(e2-h e1)), so
(E|M^(-*)e|^q)^(1/q)
<=C_p[(E_mu a^-q+k^q E_mu R^q)^(1/q)|e1|+(E_mu R^q)^(1/q)|e2|]
<=C_p[Q^(1/p)|e1|+Q^((1-v)/p)|e2|].
We used v/q=1/p and k^q Q^(v(1-v))=Q^v.
Thus positive diagonal envelope matrices can be taken as
B=diag(1,Q^(v/p)), C=diag(Q^(1/p),Q^((1-v)/p)),
and BC=Q^(1/p)I.

To pass from these envelopes to the precise interval characteristic, use the elementary two-column norm estimate. For each x,
(E_y||M(x)M(y)^-1||^q)^(1/q)
=(E_y||M(y)^(-*)M(x)*||^q)^(1/q)
<=C_p||C M(x)*||=C_p||M(x) C||.
Taking the outer Lp norm and applying the primal envelope to its two columns bounds the characteristic's pth root by C_p||BC||<=C_pQ^(1/p). Hence the interval characteristic is<=C_pQ.

This is UNIFORM AT EVERY DYADIC NODE, not merely the root. At any active state(a0,c0,h0), common right normalization gives exactly
M(a,c,h) M(a0,c0,h0)^-1
=M(a/a0,c/c0,c0(h-h0)).
The normalized future process is the same comb with fewer cycles. At a rotation child the first rotation is absent, but all moment bounds remain valid; an absorbed leaf is constant. Common right normalization leaves pair kernels exactly unchanged. Therefore the supremum of all dyadic interval characteristics is<=C_pQ, uniformly in L.

This proves the characteristic half of the discrete comb proposal. It does not yet prove the Petermichl-shift lower identity or a full-interval/Hilbert transference theorem.
''')
import numpy as np

def moments(p,Q,L):
 q=p/(p-1);v=1/(p-1);t=Q**-1;s=Q**-v;r=2-t;z=2-s
 n=np.arange(L)
 mu=t/2*(r/2)**n
 aa=t*r**n;cc=s*z**n
 ma=np.sum(mu*aa**-q)+(r**(1-q)/2)**L
 mc=np.sum(mu*cc**-p)+(r/(2*z**p))**L
 mr=np.sum(mu*(cc/aa)**q)+(z**q/(2*r**(q-1)))**L
 assert abs(np.sum(mu)+(r/2)**L-1)<1e-10
 assert ma<=2*Q**v*(1+1e-10)
 assert mc<=(1+1/(2*(1-(2/3)**p)))*Q**v*(1+1e-10)
 assert mr<=2*Q**(v*(1-v))*(1+1e-10)
 return ma,mc,mr

for p in [2.05,2.2,2.5,3,4,6,10]:
 for Q in [max(10,2**p),max(100,2**p),10000]:
  for L in [1,2,10,100,1000]:moments(p,Q,L)
print('105 actual finite-comb moment-sum tests passed.')
# Actual mixed characteristic of finite terminal laws, not merely moments.
for p in [2.2,3.,5.]:
 Q=max(20,2**p);q=p/(p-1);v=1/(p-1);k=Q**(v/p)
 t=Q**-1;s=Q**-v;r=2-t;z=2-s
 active=[(1.,1.,0.,1.)];leaves=[]
 for level in range(6):
  nxt=[]
  for aa,cc,hh,prob in active:
   for sign in [-1,1]:
    H=hh+sign*k/cc
    leaves.append((t*aa,s*cc,H,prob/4))
    nxt.append((r*aa,z*cc,H,prob/4))
  active=nxt
 leaves+=active
 aa,cc,hh,prob=np.array(leaves).T
 d1=aa**(1/p);d2=d1/cc
 bx=d1[:,None]/d1[None,:]
 bz=d2[:,None]/d2[None,:]
 by=d1[:,None]/d2[None,:]*(hh[:,None]-hh[None,:])
 tr=bx*bx+by*by+bz*bz;det=bx*bz
 norm=np.sqrt((tr+np.sqrt(np.maximum(0,tr*tr-4*det*det)))/2)
 A=np.sum(prob*(norm**q@prob)**(p-1))
 ma,mc,mr=moments(p,Q,6)
 print('p=',p,'Q=',Q,'atoms=',len(leaves),'actualmixedcharacteristic=',A,'A/Q=',A/Q)
 assert np.isfinite(A)
Path('workspace/agent2_comb_characteristic_checks.py').write_text(Path(__file__).read_text())