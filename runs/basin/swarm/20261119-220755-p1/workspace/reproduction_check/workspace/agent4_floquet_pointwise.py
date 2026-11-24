"""Rigorous pointwise interval bounds for a Floquet-tube certificate.
Inputs are exact dyadic Hermite data (ordinary float arrays are interpreted as
exact binary rationals), not claims that floating splines are exact ODE orbits.
Physical coordinate convention: POSITIVE theta first, then w4,Z2.
"""
import bisect
import numpy as np
from sage.all import matrix,vector,PolynomialRing

def upper_abs(x):return max(abs(x.lower()),abs(x.upper()))
def norminf(A):
 if hasattr(A,'nrows'):return max(sum(upper_abs(A[i,j]) for j in range(A.ncols())) for i in range(A.nrows()))
 return max(upper_abs(x) for x in A)
def _exact(R,x):
 if isinstance(x,(float,np.floating)):
  p,q=float(x).as_integer_ratio();return R(p)/q
 return R(x)
def _eval(cs,t):
 ans=cs[-1]
 for c in cs[-2::-1]:ans=ans*t+c
 return ans

class HermiteEnclosure:
 """Piecewise-cubic C1 interpolant, exact rational input data, rigorous ranges."""
 def __init__(self,knots,values,derivatives,R,periodic=True):
  self.R=R;self.knots=[_exact(R,x) for x in knots];self.kfloat=list(map(float,knots))
  vv=np.asarray(values);dd=np.asarray(derivatives);assert vv.shape==dd.shape
  assert len(vv)==len(knots);self.ismatrix=(vv.ndim==3);assert vv.ndim in [2,3]
  self.values=[];self.derivatives=[]
  for arr,out in [(vv,self.values),(dd,self.derivatives)]:
   for row in arr:
    if self.ismatrix:out.append(matrix(R,row.shape[0],row.shape[1],lambda i,j:_exact(R,row[i,j])))
    else:out.append(vector(R,[_exact(R,a) for a in row]))
  if periodic:
   self.values[-1]=self.values[0];self.derivatives[-1]=self.derivatives[0]
  self.coeffs=[]
  for k in range(len(knots)-1):
   h=self.knots[k+1]-self.knots[k];a0=self.values[k];a1=self.derivatives[k];dy=self.values[k+1]-a0
   a2=dy*(3/h**2)-(a1*2+self.derivatives[k+1])/h
   a3=dy*(-2/h**3)+(a1+self.derivatives[k+1])/h**2
   self.coeffs.append([a0,a1,a2,a3])
 def centered(self,mid,left=None,right=None):
  mfloat=float(mid);k=min(max(bisect.bisect_right(self.kfloat,mfloat)-1,0),len(self.coeffs)-1)
  if left is not None:
   ll=_exact(self.R,left);rr=_exact(self.R,right)
   assert ll.lower()>=self.knots[k].lower() and rr.upper()<=self.knots[k+1].upper(), 'Bounds must stay inside one Hermite piece'
  d=mid-self.knots[k];a0,a1,a2,a3=self.coeffs[k]
  return [a0+a1*d+a2*d**2+a3*d**3,a1+a2*(2*d)+a3*(3*d**2),a2+a3*(3*d),a3]

class FloquetPointwiseBounds:
 def __init__(self,ob,knots,gamma,gamma_deriv,frame,frame_deriv,T,D,periodic=True):
  self.ob=ob;self.R=ob.R;R=self.R;assert 'Interval' in str(R),'Use kind=interval'
  self.gamma=HermiteEnclosure(knots,gamma,gamma_deriv,R,periodic)
  self.frame=HermiteEnclosure(knots,frame,frame_deriv,R,periodic)
  self.knots=list(knots);self.T=_exact(R,T)
  d=np.asarray(D);self.D=matrix(R,d.shape[0],d.shape[1],lambda i,j:_exact(R,d[i,j]))
 def bound(self,left,right,hessian=True,rho=0):
  R=self.R;a=_exact(R,left);b=_exact(R,right);mid=(a+b)/2;t=R(-(b-a).upper()/2,(b-a).upper()/2)
  gc=self.gamma.centered(mid,left,right);pc=self.frame.centered(mid,left,right)
  # Freeze a single invertible exact dyadic frame and exact reference point.
  B=matrix(R,7,7,lambda i,j:R(pc[0][i,j].center()));Bi=B.inverse()
  ref=vector(R,[R(gc[0][i].center()) for i in range(7)])
  local=self.ob.local_transform(B,ref)
  qc=[Bi*(gc[0]-ref)]+[Bi*c for c in gc[1:]]
  cc=[Bi*c for c in pc]
  q=_eval(qc,t);C=_eval(cc,t);Ci=C.inverse()
  # Compose every residual as an exact interval-coefficient polynomial in the
  # common time parameter BEFORE evaluating an interval time. This preserves
  # cancellations in gamma'-T F(gamma) and TF'(gamma)P-P'-PD.
  PR=PolynomialRing(R,'u');u=PR.gen()
  qp=vector(PR,[PR([c[j] for c in qc]) for j in range(7)])
  Cp=matrix(PR,7,7,lambda i,j:PR([c[i,j] for c in cc]))
  gp=vector(PR,[PR([gc[1][j],gc[2][j]*2,gc[3][j]*3]) for j in range(7)])
  gp=matrix(PR,Bi)*gp
  Cprime=Cp.derivative()
  NN,DP,JN=local.numerator_data(qp,True);NN=vector(PR,NN);JN=matrix(PR,JN)
  # Tight exact factor-product interval for denominator on this time segment.
  dt=_eval([gc[0][0]-ref[0],gc[1][0],gc[2][0],gc[3][0]],t);DV=local._den(dt)
  ndelta=gp*DP-self.T*NN
  vd=vector(R,[_eval(list(p),t) if p else R(0) for p in ndelta])
  defect=Ci*vd/DV
  NE=self.T*JN*Cp-(Cprime+Cp*matrix(PR,self.D))*DP**2
  ve=matrix(R,7,7,lambda i,j:_eval(list(NE[i,j]),t) if NE[i,j] else R(0))
  E=Ci*ve/DV**2
  # Tangent-coordinate cancellation: a=P^-1 gamma'=e0+P^-1(gamma'-P0).
  nac=gp-Cp.column(0)
  vac=vector(R,[_eval(list(p),t) if p else R(0) for p in nac])
  acorr=Ci*vac
  Cpv=matrix(R,7,7,lambda i,j:_eval(list(Cprime[i,j]),t) if Cprime[i,j] else R(0))
  bmat=Ci*Cpv
  nr=_exact(R,rho);etas=vector(R,[R(0)]+[R(-nr.upper(),nr.upper())]*6)
  qtube=q+C*etas
  physical_tube=_eval(gc,t)+_eval(pc,t)*etas
  H=None
  if hessian:_,_,H=local.field_jac_hess(qtube,2)
  result={'delta':norminf(defect),'E':norminf(E[:,1:]),'E_full':norminf(E),'defect_vector':defect,'E_matrix':E,
          'C_norm':norminf(C),'Ci_norm':norminf(Ci),'q_radius':norminf(q),
          'B':B,'ref':ref,'local':local,'theta_range':ref[0]+dt,
          'a0_lower':(R(1)+acorr[0]).lower(),'a_normal':norminf(acorr[1:]),'b':norminf(bmat[:,1:]),'b_full':norminf(bmat),
          'physical_tube':physical_tube,'rho':rho}
  if hessian:
   # Contract the tensor BEFORE taking absolute values, retaining output and
   # phase/normal cancellation. Only normal input columns occur in the theorem.
   CN=C[:,1:]
   inp=[CN.transpose()*matrix(R,H[i])*CN for i in range(7)]
   transformed=[]
   for i in range(7):
    hh=matrix(R,6,6)
    for j in range(7):hh+=Ci[i,j]*inp[j]
    transformed.append(hh)
   result['H']=abs(self.T).upper()*max(sum(upper_abs(hh[j,k]) for j in range(6) for k in range(6)) for hh in transformed)
  return result
 def bound_all(self,subdivisions=1,hessian=True,rho=0):
  out=[]
  for a,b in zip(self.knots[:-1],self.knots[1:]):
   for j in range(subdivisions):
    left=a if j==0 else float(a)+(float(b)-float(a))*j/subdivisions;right=b if j+1==subdivisions else float(a)+(float(b)-float(a))*(j+1)/subdivisions
    out.append(self.bound(left,right,hessian,rho))
  return out
