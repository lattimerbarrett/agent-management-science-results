"""Exact interval-AD consistency checks; independent multivariate Taylor seeds."""
import sys,numpy as np,time
sys.path.insert(0,'workspace')
from agent4_interval_blowup import IntervalBlowup
from sage.all import PowerSeriesRing
D=np.load('workspace/agent1_GENUINE_s4_periodic.npz');rng=np.random.default_rng(417)
for kind in ['interval','ball']:
 ob=IntervalBlowup(kind=kind,bits=320);R=ob.R;PS=PowerSeriesRing(R,'t',default_prec=5);t=PS.gen()
 for ix in [0,1000,2000,3000,4000]:
  yy=D['y'][:,ix].copy();yy[0]*=-1;y=list(map(R,yy));F,J,H=ob.field_jac_hess(y)
  for repeat in range(3):
   direction=list(map(R,rng.integers(-3,4,size=7)));yp=[PS(y[i])+t*direction[i] for i in range(7)];fp=ob.field_generic(yp)
   for i in range(7):
    linear=sum((J[i][j]*direction[j] for j in range(7)),R(0))
    quad=sum((H[i][j][k]*direction[j]*direction[k] for j in range(7) for k in range(7)),R(0))/2
    assert (fp[i][0]-F[i]).contains_zero()
    assert (fp[i][1]-linear).contains_zero()
    assert (fp[i][2]-quad).contains_zero(),(kind,ix,i,fp[i][2],quad)
 print(kind,'field/Jac/Hessian Taylor identities PASS at5phases x3integerdirections')
# Check interval boxes exclude all denominators and contain sample-corner values.
ob=IntervalBlowup(bits=300);R=ob.R;ix=2500;y=D['y'][:,ix].copy();y[0]*=-1
width=np.array([1e-5,1e-8,1e-8,1e-8,1e-8,1e-10,1e-10]);box=[R(a-b,a+b) for a,b in zip(y,width)]
FB,JB,HB=ob.field_jac_hess(box)
for _ in range(20):
 sample=[R(float(a+b*rng.choice([-1,1]))) for a,b in zip(y,width)];FS,JS,HS=ob.field_jac_hess(sample)
 for i in range(7):
  assert FB[i].lower()<=FS[i].lower()<=FS[i].upper()<=FB[i].upper()
  for j in range(7):
   assert JB[i][j].lower()<=JS[i][j].lower()<=JS[i][j].upper()<=JB[i][j].upper()
   for k in range(7):assert HB[i][j][k].lower()<=HS[i][j][k].lower()<=HS[i][j][k].upper()<=HB[i][j][k].upper()
print('20corner samples all enclosed for field/Jac/Hess')
# Test the newer rational q1=-143/200 constants too.
other=IntervalBlowup(q1='-143/200',kind='ball');print('newerparameterroots',other.mus)
print('ALL intervalfieldfinitechecks PASSED')

# Independent whitening cross-check and actual order16 dynamic Taylor jet.
from agent2_taylor_generic import WhiteGenericField
ob=IntervalBlowup(kind='ball',bits=300);ww=WhiteGenericField(bits=300)
tr=ob.transformed(ww.W,ww.Zscale)
y=ww.white(list(map(ww.K,D['y'][:,2500])));yt=list(y);yt[0]*=-1
F=tr.field_generic(yt);Fw=ww.field(y);Fw[0]*=-1
assert max(float(abs(F[i]-Fw[i])) for i in range(7))<1e-70
PS=PowerSeriesRing(ob.R,'t',default_prec=18);t=PS.gen();YY=[PS(a) for a in yt]
for j in range(16):
 ff=tr.field_generic(YY)
 for i in range(7):YY[i]+=ff[i][j]/(j+1)*t**(j+1)
assert max(float(a[16].rad()) for a in YY)<1e-40
print('Independent whitened field agreement and order16 dynamic PS enclosure PASS')

# Full B-mixing, local reference, common-denominator collection and AD check.
from sage.all import matrix,vector
BB=D['B'].copy();BB[0]*=-1;B=matrix(ob.R,BB)
ref=list(map(ob.R,D['y'][:,2500]));ref[0]*=-1
local=ob.local_transform(B,ref);q=list(map(ob.R,rng.normal(size=7)*.001))
F=local.field(q);direct=list(B.inverse()*vector(ob.R,ob.field_generic(list(vector(ob.R,ref)+B*vector(ob.R,q)))))
assert max(float(abs(F[i]-direct[i])) for i in range(7))<1e-60
PS=PowerSeriesRing(ob.R,'t',default_prec=5);t=PS.gen();dr=list(map(ob.R,rng.integers(-2,3,7)))
fp=local.field([PS(q[i])+t*dr[i] for i in range(7)]);F,J,H=local.field_jac_hess(q)
for i in range(7):
 assert (fp[i][0]-F[i]).contains_zero()
 assert (fp[i][1]-sum(J[i][j]*dr[j] for j in range(7))).contains_zero()
 assert (fp[i][2]-sum(H[i][j][k]*dr[j]*dr[k] for j in range(7) for k in range(7))/2).contains_zero()
print('Full B-local common polynomial field and independent AD directional identities PASS')
