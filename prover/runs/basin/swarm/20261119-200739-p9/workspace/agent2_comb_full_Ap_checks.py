from pathlib import Path
Path('workspace/agent2_comb_full_Ap.md').write_text(r'''# Full real-interval Ap bound for the inner-good-quarter comb

Use the parameters and finite-horizon L>=1 comb of agent2_comb_characteristic.md. Place children in spatial order
B_minus, G_minus, G_plus, B_plus,
where B absorbs and G continues; the two rotation signs are minus on the first pair and plus on the second. Each child has one quarter the parent's length. Every active interval thus has constant outer bad quarters. Each good child, unless terminal, itself has constant outer bad quarters, of length one sixteenth of its grandparent.

For an interval I, let nu_I denote the probability distribution of terminal roots M(x) for x uniform on I. If nu_I<=C nu_J as measures on matrices, positivity and homogeneity in the problem's exact characteristic give
A_I<=C^p A_J.
Indeed the inner q-average increases by at most C and the outer integral by at most C, giving C^(p-1)C.

Take any I subset[0,1]. Descend active intervals as long as I lies in one good child. If it lies in a constant leaf, its characteristic is1. Otherwise reach an active J on which I intersects at least two child quarters. If |I|>=|J|/16 then nu_I<=16 nu_J trivially. If |I|<|J|/16 it crosses only one child boundary. Both sides of that boundary are constant on strips of width at least |J|/16: the strip is either a bad child quarter or an outer bad quarter inside a good child. At the last cycle, all children are constant, and the strips are even wider. Thus nu_I is supported on at most two values each occurring in J on length at least |J|/16, whence again nu_I<=16nu_J. Consequently
sup_{I subset[0,1]} A_I <=16^p sup_{active J} A_J <=C_p Q.
No comparison of adjacent matrices, no small-step approximation, and no generic remodeling theorem is needed.

Extend M to the negative half-line by its leftmost bad-quarter value M_minus, and to(1,infinity) by its rightmost bad-quarter value M_plus. Any interval meeting[0,1] and of length<1/4 is either contained[0,1] or meets an endpoint on which both pieces are the same constant root. If |I|>=1/4, its inside-root distribution is bounded by4nu_root, and its outside distribution is bounded by4nu_root because each outside value already has root mass1/4. Therefore nu_I<=8nu_root and A_I<=8^p A_root<=C_pQ. Intervals contained in an exterior half-line are constant. Hence the extended genuine matrix weight
W(x)=(M(x)*M(x))^(p/2)
has the problem's FULL real-interval characteristic <=C_pQ, uniformly in finite horizon L. It is bounded and uniformly positive definite for each fixed Q,L, so all smooth density issues are ordinary weighted/unweighted equivalences.
''')
import numpy as np
rng=np.random.default_rng(3419)
maxdom=0.;maxchar=0.
for p in [2.2,3.,5.]:
 Q=max(20,2**p);q=p/(p-1);v=1/(p-1);k=Q**(v/p)
 t=Q**-1;s=Q**-v;r=2-t;z=2-s;leaves=[];nodes=[]
 def build(a,c,h,x,length,left):
  if left==0:
   leaves.append((x,x+length,a,c,h));return
  nodes.append((x,x+length))
  d=length/4
  leaves.append((x,x+d,t*a,s*c,h-k/c))
  build(r*a,z*c,h-k/c,x+d,d,left-1)
  build(r*a,z*c,h+k/c,x+2*d,d,left-1)
  leaves.append((x+3*d,x+4*d,t*a,s*c,h+k/c))
 build(1.,1.,0.,0.,1.,5)
 ar=np.array(leaves);starts,ends,aa,cc,hh=ar.T;lengths=ends-starts
 d1=aa**(1/p);d2=d1/cc
 bx=d1[:,None]/d1[None,:];bz=d2[:,None]/d2[None,:]
 by=d1[:,None]/d2[None,:]*(hh[:,None]-hh[None,:])
 tr=bx*bx+by*by+bz*bz;det=bx*bz
 K=np.sqrt((tr+np.sqrt(np.maximum(0,tr*tr-4*det*det)))/2)**q
 def characteristic(prob):return np.sum(prob*(K@prob)**(p-1))
 for _ in range(2000):
  x=rng.uniform(0,1);y=min(1,x+10**rng.uniform(-10,0))
  if y==x:continue
  prob=np.maximum(0,np.minimum(y,ends)-np.maximum(x,starts))/(y-x)
  jx,jy=min((n for n in nodes if n[0]<=x and n[1]>=y),key=lambda n:n[1]-n[0])
  parent=np.maximum(0,np.minimum(jy,ends)-np.maximum(jx,starts))/(jy-jx)
  good=prob>0
  dom=np.max(prob[good]/parent[good]);maxdom=max(maxdom,dom)
  assert dom<=16*(1+1e-10)
  if rng.random()<.05:
   ratio=characteristic(prob)/characteristic(parent);maxchar=max(maxchar,ratio)
   assert ratio<=16**p*(1+1e-8)
print('6000 actual nonaligned interval probability-domination checks passed; maxdensityratio=',maxdom)
print('Actual mixed characteristic comparisons passed; maxratio=',maxchar)
Path('workspace/agent2_comb_full_Ap_checks.py').write_text(Path(__file__).read_text())