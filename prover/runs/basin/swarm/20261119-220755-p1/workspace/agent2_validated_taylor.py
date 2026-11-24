"""Interval Taylor integration, generic ball local-coordinate vector fields.
Builder(ref) must return object with field(q), jac(q); all generic PS-compatible.
Coordinates are physical Y=ref+S q. No unchecked quadrature error estimates.
"""
from sage.all import *

def upper_abs(a):return abs(a).upper()
def horner(cc,x):
 ans=x*0
 for c in cc[::-1]:ans=ans*x+c
 return ans

class ValidatedTaylor:
 def __init__(self,K,S,builder):self.K=K;self.S=S;self.Si=S.inverse();self.builder=builder
 def jets(self,local,q0,degree,variational=False,M0=None):
  K=self.K;R=PowerSeriesRing(K,'t',default_prec=degree+1);qc=[[K(a)] for a in q0]
  mc=[[[K(i==j) if M0 is None else M0[i,j]] for j in range(7)] for i in range(7)]
  for n in range(degree):
   q=[R(cc,prec=n+1) for cc in qc];f=local.field(q)
   for i in range(7):qc[i].append(R(f[i])[n]/(n+1))
   if variational:
    J=local.jac(q);MM=matrix(R,7,7,lambda i,j:R(mc[i][j],prec=n+1));dm=matrix(R,J)*MM
    for i in range(7):
     for j in range(7):mc[i][j].append(dm[i,j][n]/(n+1))
  return qc,mc if variational else None
 def step(self,ref,rad,h,degree=24,variational=True):
  K=self.K;local=self.builder(ref);q0=[K(0).add_error(K(r)) for r in rad];f0=local.field(q0);rr=[K(upper_abs(h*f0[i]))*K('1.2')+abs(h)**2 for i in range(7)]
  for attempt in range(30):
   tube=[K(0).add_error(rr[i]+K(rad[i])) for i in range(7)];fb=local.field(tube);needed=[upper_abs(h*fb[i]) for i in range(7)]
   if all(needed[i]<rr[i].lower() for i in range(7)):break
   rr=[K(max(float(rr[i]),float(needed[i])))*K('1.2') for i in range(7)]
  else:raise ArithmeticError('Picard enclosure did not close')
  # At this point tube is a strict invariant Picard tube, hence the unique flow exists.
  J=local.jac(tube);L=max(sum(upper_abs(a) for a in row) for row in J);L=K(L);mrad=(L*abs(h)).exp()-1
  Mbox=matrix(K,7,7,lambda i,j:K(i==j).add_error(mrad))
  center,cm=self.jets(local,q0,degree-1,variational)
  rem,rm=self.jets(local,tube,degree,variational,Mbox)
  out=[horner(center[i],h)+rem[i][degree]*h**degree for i in range(7)]
  MM=None
  if variational:MM=matrix(K,7,7,lambda i,j:horner(cm[i][j],h)+rm[i][j][degree]*h**degree)
  shift=vector(K,[a.mid() for a in out]);newexact=vector(K,ref)+self.S*shift;newref=vector(K,[a.mid() for a in newexact]);roundoff=self.Si*(newexact-newref);newrad=[K(out[i].rad())+K(upper_abs(roundoff[i])) for i in range(7)]
  return list(newref),newrad,MM,dict(picard=tube,L=L,remainder=max(upper_abs(rem[i][degree]*h**degree) for i in range(7)))
 def flow(self,ref,span,substeps,degree=24,variational=True,verbose=False):
  K=self.K;ref=list(ref);rad=[K(0)]*7;MM=identity_matrix(K,7);maxrem=K(0).upper();maxL=K(0).upper()
  for j in range(substeps):
   ref,rad,M,info=self.step(ref,rad,span/substeps,degree,variational)
   if variational:MM=M*MM
   maxrem=max(maxrem,info['remainder']);maxL=max(maxL,info['L'].upper())
   if verbose:print('substep',j,'radius',max(float(a) for a in rad),'remainder',float(info['remainder']),flush=True)
  return ref,rad,MM,dict(max_remainder=maxrem,max_L=maxL)
