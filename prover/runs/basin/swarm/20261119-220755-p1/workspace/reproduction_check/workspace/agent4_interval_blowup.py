"""Certified algebraic constants and rational coefficient field for s4 example.
State order is POSITIVE theta, w[0:4], Z[0:2], unlike shared h=-theta API.
No inverse matrices at runtime. coefficient_formulas accepts generic scalars,
including Sage power series over RBF, and local second-order AD is provided.
"""
import itertools
import sympy as sp
from sage.all import RealIntervalField, RealBallField, matrix, vector

def _pa(a,b):
 n=max(len(a),len(b));z=a[0]*0
 return [(a[i] if i<len(a) else z)+(b[i] if i<len(b) else z) for i in range(n)]
def _ps(a,b):return _pa(a,[-x for x in b])
def _pm(a,b):
 c=[a[0]*0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def _pv(c,t):
 ans=t*0+c[-1]
 for a in c[-2::-1]:ans=ans*t+a
 return ans
def _pdet(M):
 n=len(M);ans=[M[0][0][0]*0]
 for p in itertools.permutations(range(n)):
  sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));term=[M[0][0][0]*0+sign]
  for i in range(n):term=_pm(term,M[i][p[i]])
  ans=_pa(ans,term)
 return ans
def _adj(M):
 n=len(M)
 return [[[(1 if (i+j)%2==0 else -1)*a for a in _pdet([[M[r][c] for c in range(n) if c!=i] for r in range(n) if r!=j])] for j in range(n)] for i in range(n)]
def _mv(A,v):return [sum((a*x for a,x in zip(row,v)),v[0]*0) for row in A]
def _mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),A[0][0]*0) for j in range(len(B[0]))] for i in range(len(A))]

class Jet2:
 """Value, first derivative, second derivative, generic commutative base ring."""
 def __init__(self,v,d=None,dd=None):self.v=v;self.d=v*0 if d is None else d;self.dd=v*0 if dd is None else dd
 def co(self,x):return x if isinstance(x,Jet2) else Jet2(self.v*0+x)
 def __add__(self,x):
  x=self.co(x);return Jet2(self.v+x.v,self.d+x.d,self.dd+x.dd)
 __radd__=__add__
 def __neg__(self):return Jet2(-self.v,-self.d,-self.dd)
 def __sub__(self,x):return self+-self.co(x)
 def __rsub__(self,x):return self.co(x)+-self
 def __mul__(self,x):
  x=self.co(x);return Jet2(self.v*x.v,self.d*x.v+self.v*x.d,self.dd*x.v+2*self.d*x.d+self.v*x.dd)
 __rmul__=__mul__
 def inv(self):return Jet2(1/self.v,-self.d/self.v**2,2*self.d**2/self.v**3-self.dd/self.v**2)
 def __truediv__(self,x):return self*self.co(x).inv()
 def __rtruediv__(self,x):return self.co(x)*self.inv()
 def __pow__(self,n):
  if n<0:return self.inv()**(-n)
  ans=self.co(1)
  for _ in range(n):ans=ans*self
  return ans

class IntervalBlowup:
 def __init__(self,q1='-289/400',q2='17/10',N='3/50',bits=300,kind='interval'):
  self.bits=bits;self.kind=kind
  self.R=RealIntervalField(bits) if kind=='interval' else RealBallField(bits)
  R=self.R;self.nodes=list(map(R,[-3,-1,0,1,2,3]));S=self.nodes
  q1,q2,NN=map(sp.Rational,[q1,q2,N]);self.params=(q1,q2,NN);self.N=self.ri(NN)
  x=sp.Symbol('x');P=sp.prod(x-a for a in [-3,-1,0,1,2,3])*(x-q1)*(x-q2)
  # SymPy intervals are exact rational Sturm isolations, independent of floats.
  self.root_boxes=[]
  def root(poly):
   pairs=sp.Poly(poly,x).intervals(eps=sp.Rational(1,10**(int(bits*.302)+20)))
   assert len(pairs)==8 and all(k==1 for I,k in pairs)
   out=[]
   for (lo,hi),mult in pairs:
    self.root_boxes.append((lo,hi))
    if kind=='interval':out.append(R(self.ri(lo).lower(),self.ri(hi).upper()))
    else:
     mid=(lo+hi)/2;rad=(hi-lo)/2
     out.append(R(self.ri(mid)).add_error(self.ri(rad)))
   return out
  aa=root(P+NN);bb=root(P+2*NN)
  self.f=[R(1)]
  for i in [0,3,5,6]:self.f=_pm(self.f,[-aa[i],R(1)])
  self.g=[R(1)]
  for i in [1,2,4,7]:self.g=_pm(self.g,[-aa[i],R(1)])
  self.mus=[bb[1],bb[6]]
  self.denroots=[aa[i] for i in [0,3,5,6]]+S+[aa[i] for i in [1,2,4,7]]*2
  self.d=[self.ri(sp.prod(a-b for b in [-3,-1,0,1,2,3] if a!=b)) for a in [-3,-1,0,1,2,3]]
  fv=[_pv(self.f,a) for a in S];self.fv=fv
  self.fm=[_pv(self.f,a) for a in self.mus];self.gm=[-self.N/a for a in self.fm]
  self.V=[[a**j for j in range(4)] for a in S];self.Vm=[[a**j for j in range(4)] for a in self.mus]
  # Both moment matrices affine in positive theta.
  self.M=[[[sum((self.N*S[i]*S[i]**(r+c)/(self.d[i]*fv[i]) for i in range(6)),R(0)),sum((-self.N*S[i]**(r+c)/(self.d[i]*fv[i]) for i in range(6)),R(0))] for c in range(4)] for r in range(4)]
  self.Mp=[[[sum((S[i]*S[i]**(r+c)*fv[i]/self.d[i] for i in range(6)),R(0)),sum((-S[i]**(r+c)*fv[i]/self.d[i] for i in range(6)),R(0))] for c in range(4)] for r in range(4)]
  self.A=_adj(self.M);self.Ap=_adj(self.Mp)
  det=_pdet(self.M);detp=_pdet(self.Mp);self.c=det[-1];self.cp=detp[-1]
  # Christoffel determinant identities detM=c*f(theta), detMp=cp*g(theta).
  # Interval residual inclusion is an independent finite consistency check.
  assert all((det[i]-self.c*self.f[i]).contains_zero() for i in range(5))
  assert all((detp[i]-self.cp*self.g[i]).contains_zero() for i in range(5))
  self.D=[[sum((self.N**2*S[i]*S[i]**j/(self.d[i]*fv[i]**2) for i in range(6)),R(0)),sum((-self.N**2*S[i]**j/(self.d[i]*fv[i]**2) for i in range(6)),R(0))] for j in range(4)]
  self.P=[R(1)]
  for a in S:self.P=_pm(self.P,[-a,R(1)])
  self.prepare_rational()
 def ri(self,q):
  q=sp.Rational(q);return self.R(int(q.p))/int(q.q)
 def prepare_rational(self):
  R=self.R;z=R(0);N=self.N;f0=self.fv[2];g0=N/f0
  DG=[[_pa(_pa(_pm(self.Ap[i][0],self.M[0][j]),_pm(self.Ap[i][1],self.M[1][j])),_pa(_pm(self.Ap[i][2],self.M[2][j]),_pm(self.Ap[i][3],self.M[3][j]))) for j in range(4)] for i in range(4)]
  DG=[[[a*(-1/self.cp) for a in p] for p in row] for row in DG]
  self.nb=[]
  for j in range(4):
   poly=_pa([f0*a for a in DG[0][j]],_pm(_ps([g0 if j==0 else z],self.D[j]),self.g))
   self.nb.append([z]+[a*2/N for a in poly])
  self.nK=[]
  for i in range(4):
   poly=[z]
   for j in range(4):poly=_pa(poly,[z]*j+self.A[i][j])
   self.nK.append([-N*a/(4*self.c) for a in poly])
  self.nF=[[[z] for _ in range(2)] for _ in range(4)]
  for i in range(4):
   for m in range(2):
    poly=[z]
    for j in range(4):poly=_pa(poly,[a*self.Vm[m][j] for a in self.A[i][j]])
    self.nF[i][m]=[-4*self.fm[m]*a/self.c for a in poly]
  self.nL=[]
  for m in range(2):
   row=[]
   for j in range(4):
    poly=_pm(_ps([2*self.Vm[m][j]/self.fm[m]],[2*a/N for a in self.D[j]]),self.g)
    for k in range(4):poly=_pa(poly,[2*self.Vm[m][k]*a/self.gm[m] for a in DG[k][j]])
    row.append(poly)
   self.nL.append(row)
 def transformed(self,W,Zscale):
  """Return same theta-state field with original w=W*wnew, Z=Zscale*Znew.
  Numerators are combined ONCE before evaluation, avoiding interval cancellation.
  W and Zscale must enclose fixed invertible exact constants. If their ball
  enclosures are uncertain, this uniformly encloses all transformations in them.
  """
  import copy
  out=copy.copy(self);R=self.R;W=matrix(R,W);Wi=W.inverse();zs=list(map(R,Zscale));z=R(0)
  def comb(ps,cs):
   ans=[z]
   for p,c in zip(ps,cs):ans=_pa(ans,[a*c for a in p])
   return ans
  out.nb=[comb(self.nb,[W[i,j] for i in range(4)]) for j in range(4)]
  out.nK=[comb(self.nK,[Wi[i,j] for j in range(4)]) for i in range(4)]
  out.nF=[[comb([self.nF[j][m] for j in range(4)],[Wi[i,j]*zs[m] for j in range(4)]) for m in range(2)] for i in range(4)]
  out.nL=[[comb(self.nL[m],[W[i,j] for i in range(4)]) for j in range(4)] for m in range(2)]
  out.D=[comb(self.D,[W[i,j] for i in range(4)]) for j in range(4)]
  return out
 def coefficient_formulas(self,theta):
  """Generic-ring coefficient evaluation, including arbitrary-order PS jets."""
  t=theta;ft=_pv(self.f,t);gt=_pv(self.g,t);pt=_pv(self.P,t)
  return dict(b=[_pv(p,t)/gt for p in self.nb],K=[_pv(p,t)/(ft*pt) for p in self.nK],
    force=[[_pv(p,t)/ft for p in row] for row in self.nF],
    L=[[_pv(p,t)/gt for p in row] for row in self.nL],D=[_pv(p,t) for p in self.D])
 def field_generic(self,y):
  """Generic scalar field; no coercion of input scalars."""
  th=y[0];w=y[1:5];Z=y[5:];co=self.coefficient_formulas(th);zero=th*0
  v=sum((co['b'][i]*w[i] for i in range(4)),zero)
  return [v]+[w[i]-co['K'][i]*v*v+sum((co['force'][i][m]*Z[m] for m in range(2)),zero) for i in range(4)]+[Z[m]*(2+sum((co['L'][m][i]*w[i] for i in range(4)),zero)) for m in range(2)]
 def field_jac_hess(self,box,order=2):
  """Rigorous field/Jacobian/Hessian enclosures on a rectangular box.
  Returns (list7, matrix7x7, list7_of_matrix7x7); unused orders return None.
  Scalars may be interval, ball, or any generic base ring supporting division.
  """
  y=list(box);th=y[0];w=y[1:5];Z=y[5:];zero=th*0;one=zero+1
  co=self.coefficient_formulas(Jet2(th,one,zero));b=co['b'];K=co['K'];F=co['force'];L=co['L']
  v=sum((b[j].v*w[j] for j in range(4)),zero);vt=sum((b[j].d*w[j] for j in range(4)),zero);vtt=sum((b[j].dd*w[j] for j in range(4)),zero)
  vals=[v]+[w[i]-K[i].v*v*v+sum((F[i][m].v*Z[m] for m in range(2)),zero) for i in range(4)]+[Z[m]*(2+sum((L[m][i].v*w[i] for i in range(4)),zero)) for m in range(2)]
  if not order:return vals,None,None
  J=[[zero for _ in range(7)] for _ in range(7)];J[0][0]=vt
  for j in range(4):J[0][j+1]=b[j].v
  for i in range(4):
   J[i+1][0]=-K[i].d*v*v-2*K[i].v*v*vt+sum((F[i][m].d*Z[m] for m in range(2)),zero)
   for j in range(4):J[i+1][j+1]=(one if i==j else zero)-2*K[i].v*v*b[j].v
   for m in range(2):J[i+1][m+5]=F[i][m].v
  for m in range(2):
   J[m+5][0]=Z[m]*sum((L[m][j].d*w[j] for j in range(4)),zero)
   for j in range(4):J[m+5][j+1]=Z[m]*L[m][j].v
   J[m+5][m+5]=2+sum((L[m][j].v*w[j] for j in range(4)),zero)
  if order==1:return vals,J,None
  H=[[[zero for _ in range(7)] for _ in range(7)] for _ in range(7)]
  H[0][0][0]=vtt
  for j in range(4):H[0][0][j+1]=H[0][j+1][0]=b[j].d
  for i in range(4):
   k=i+1
   H[k][0][0]=-K[i].dd*v*v-4*K[i].d*v*vt-2*K[i].v*(vt*vt+v*vtt)+sum((F[i][m].dd*Z[m] for m in range(2)),zero)
   for j in range(4):
    H[k][0][j+1]=H[k][j+1][0]=-2*(K[i].d*v*b[j].v+K[i].v*(vt*b[j].v+v*b[j].d))
    for l in range(4):H[k][j+1][l+1]=-2*K[i].v*b[j].v*b[l].v
   for m in range(2):H[k][0][m+5]=H[k][m+5][0]=F[i][m].d
  for m in range(2):
   k=m+5;H[k][0][0]=Z[m]*sum((L[m][j].dd*w[j] for j in range(4)),zero)
   for j in range(4):
    H[k][0][j+1]=H[k][j+1][0]=Z[m]*L[m][j].d
    H[k][j+1][m+5]=H[k][m+5][j+1]=L[m][j].v
   H[k][0][m+5]=H[k][m+5][0]=sum((L[m][j].d*w[j] for j in range(4)),zero)
  return vals,J,H


def _scale(p,c):return [a*c for a in p]
def _psum(ps,z):
 ans=[z]
 for p in ps:ans=_pa(ans,p)
 return ans
def _shift_poly(p,a):
 import math
 z=p[0]*0;pw=[z+1]
 for _ in range(len(p)):pw.append(pw[-1]*a)
 return [sum((p[i]*math.comb(i,j)*pw[i-j] for i in range(j,len(p))),z) for j in range(len(p))]
def _pd(p):return [p[i]*i for i in range(1,len(p))] if len(p)>1 else [p[0]*0]

class BalancedRationalField:
 """Precomputed full common-denominator field in Y=B*r coordinates.
 Both B and physical state Y use POSITIVE theta in the first coordinate.
 Prepare once per B. Call local(ref) for cheaply shifted local q coordinates.
 """
 def __init__(self,ob,B):
  R=ob.R;self.R=R;self.B=matrix(R,B);self.Bi=self.B.inverse();self.ob=ob;z=R(0)
  self.mons=[()]+[(j,) for j in range(7)]+[(j,k) for j in range(7) for k in range(j,7)]
  self.lookup={m:i for i,m in enumerate(self.mons)};n=len(self.mons)
  g2=_pm(ob.g,ob.g);self.den=_pm(_pm(ob.f,ob.P),g2)
  d_over_g=_pm(_pm(ob.f,ob.P),ob.g);d_over_f=_pm(ob.P,g2)
  # r-polynomials are represented by theta-polynomial coefficients per monomial.
  def empty():return [[z] for _ in range(n)]
  def linear(cs):
   out=empty()
   for j in range(7):out[1+j]=cs[j]
   return out
  def add(A,B):return [_pa(a,b) for a,b in zip(A,B)]
  def scale(A,p):return [_pm(a,p) for a in A]
  def prodlinear(A,B):
   out=empty()
   for i,m in enumerate(self.mons[:8]):
    for j,k in enumerate(self.mons[:8]):
     mon=tuple(sorted(m+k));idx=self.lookup[mon];out[idx]=_pa(out[idx],_pm(A[i],B[j]))
   return out
  WW=[linear([_scale([R(1)],self.B[i+1,j]) for j in range(7)]) for i in range(4)]
  ZZ=[linear([_scale([R(1)],self.B[m+5,j]) for j in range(7)]) for m in range(2)]
  VN=empty()
  for i in range(4):VN=add(VN,scale(WW[i],ob.nb[i]))
  V2=prodlinear(VN,VN)
  raw=[scale(VN,d_over_g)]
  for i in range(4):
   out=add(scale(WW[i],self.den),scale(V2,_scale(ob.nK[i],-1)))
   for m in range(2):out=add(out,scale(ZZ[m],_pm(ob.nF[i][m],d_over_f)))
   raw.append(out)
  for m in range(2):
   lw=empty()
   for i in range(4):lw=add(lw,scale(WW[i],ob.nL[m][i]))
   raw.append(add(scale(ZZ[m],_scale(self.den,2)),scale(prodlinear(ZZ[m],lw),d_over_g)))
  self.nums=[]
  for i in range(7):
   out=empty()
   for k in range(7):out=add(out,[ _scale(p,self.Bi[i,k]) for p in raw[k]])
   self.nums.append(out)
 def local(self,ref):return LocalBalancedField(self,ref)

class LocalBalancedField:
 """q'=B^-1 F(ref+Bq), all common-denominator numerators collected and shifted.
 Supports generic PS and analytic full Jacobian/Hessian boxes.
 """
 def __init__(self,balanced,ref):
  self.balanced=balanced;self.R=balanced.R;R=self.R;self.ref=list(map(R,ref));self.theta_ref=self.ref[0]
  self.B=balanced.B;self.Bi=balanced.Bi;self.row=[self.B[0,j] for j in range(7)]
  r0=list(self.Bi*vector(R,self.ref));z=R(0);lookup=balanced.lookup;self.mons=balanced.mons
  self.denroots=balanced.ob.denroots
  self.den=_shift_poly(balanced.den,self.theta_ref);self.dden=_pd(self.den);self.ddden=_pd(self.dden)
  self.nums=[]
  for out in balanced.nums:
   tmp=[list(p) for p in out]
   # Translate r=r0+q while holding the theta coefficient argument independent.
   const=list(out[0]);lins=[list(out[1+j]) for j in range(7)]
   for j in range(7):const=_pa(const,_scale(out[1+j],r0[j]))
   for idx,(j,k) in enumerate(self.mons[8:],8):
    poly=out[idx];const=_pa(const,_scale(poly,r0[j]*r0[k]))
    lins[j]=_pa(lins[j],_scale(poly,r0[k]));lins[k]=_pa(lins[k],_scale(poly,r0[j]))
   tmp[0]=const
   for j in range(7):tmp[1+j]=lins[j]
   self.nums.append([_shift_poly(p,self.theta_ref) for p in tmp])
  self.dnums=[[_pd(p) for p in row] for row in self.nums]
  self.ddnums=[[_pd(p) for p in row] for row in self.dnums]
  self.bytheta=[]
  for row in self.nums:
   degree=max(len(p) for p in row)
   self.bytheta.append([[p[r] if r<len(p) else z for p in row] for r in range(degree)])
 def _eval(self,ps,dt,q,zero):
  pp=[_pv(p,dt) for p in ps];out=pp[0]
  for j in range(7):out+=pp[1+j]*q[j]
  for idx,(j,k) in enumerate(self.mons[8:],8):out+=pp[idx]*q[j]*q[k]
  return out,pp
 def _den(self,dt):
  # Expanded-polynomial interval evaluation can spuriously cross zero. Tighten
  # the constant coefficient by direct outward interval product of real factors.
  val=_pv(self.den,dt);isps=hasattr(dt,'list') and hasattr(dt,'prec')
  c0=dt[0] if isps else dt
  IR=RealIntervalField(self.balanced.ob.bits);th=IR(self.theta_ref)+IR(c0);prod=IR(1)
  for root in self.denroots:prod*=th-IR(root)
  tight=self.R(prod)
  if isps:
   try:n=int(val.prec())
   except TypeError:n=int(val.parent().default_prec())
   coeff=[val[i] for i in range(n)];coeff[0]=tight
   return val.parent()(coeff).add_bigoh(n)
  return tight
 def _monomials(self,q):
  return [q[0]*0+1]+list(q)+[q[j]*q[k] for j,k in self.mons[8:]]
 def _transposed(self,bytheta,dt,mons):
  out=dt*0
  for cs in bytheta[::-1]:
   cr=sum((mons[k]*c for k,c in enumerate(cs)),dt*0)
   out=out*dt+cr
  return out
 def field(self,q):
  zero=q[0]*0;dt=sum((q[j]*self.row[j] for j in range(7)),zero);den=self._den(dt);mons=self._monomials(q)
  return [self._transposed(row,dt,mons)/den for row in self.bytheta]
 def numerator_data(self,q,jacobian=True):
  """Exact generic polynomial compositions: returns (N,D,JN), F=N/D,
  DF=JN/D^2. No division or interval evaluation in input q is performed.
  Useful for composing a whole defect with a polynomial trajectory BEFORE
  interval evaluation, retaining all cancellation.
  """
  zero=q[0]*0;one=zero+1;dt=sum((q[j]*self.row[j] for j in range(7)),zero)
  den=_pv(self.den,dt);den1=_pv(self.dden,dt);mons=self._monomials(q)
  NN=[];JN=[]
  for bytheta in self.bytheta:
   N=zero;Nt=zero;Nq=[zero]*7
   for cs in bytheta[::-1]:
    cr=sum((mons[k]*c for k,c in enumerate(cs)),zero)
    if jacobian:
     cg=[one*cs[1+j] for j in range(7)]
     for idx,(j,k) in enumerate(self.mons[8:],8):
      cg[j]+=q[k]*cs[idx];cg[k]+=q[j]*cs[idx]
     Nt=Nt*dt+N;Nq=[Nq[j]*dt+cg[j] for j in range(7)]
    N=N*dt+cr
   NN.append(N)
   if jacobian:JN.append([(Nq[j]+Nt*self.row[j])*den-N*den1*self.row[j] for j in range(7)])
  return NN,den,(JN if jacobian else None)
 def _field_jac_fast(self,q):
  zero=q[0]*0;one=zero+1;dt=sum((q[j]*self.row[j] for j in range(7)),zero);den=self._den(dt);den1=_pv(self.dden,dt)
  mons=self._monomials(q);vals=[];JJ=[]
  for bytheta in self.bytheta:
   N=zero;Nt=zero;Nq=[zero]*7
   for cs in bytheta[::-1]:
    cr=sum((mons[k]*c for k,c in enumerate(cs)),zero)
    cg=[one*cs[1+j] for j in range(7)]
    for idx,(j,k) in enumerate(self.mons[8:],8):
     cg[j]+=q[k]*cs[idx];cg[k]+=q[j]*cs[idx]
    Nt=Nt*dt+N;N=N*dt+cr
    Nq=[Nq[j]*dt+cg[j] for j in range(7)]
   vals.append(N/den)
   JJ.append([(Nq[j]+Nt*self.row[j])/den-N*den1*self.row[j]/den**2 for j in range(7)])
  return vals,JJ,None
 field_generic=field
 def field_jac_hess(self,q,order=2):
  if order==1:return self._field_jac_fast(q)
  zero=q[0]*0;dt=sum((q[j]*self.row[j] for j in range(7)),zero)
  den=self._den(dt);den1=_pv(self.dden,dt);den2=_pv(self.ddden,dt)
  vals=[];JJ=[];HH=[]
  for i in range(7):
   N,pp=self._eval(self.nums[i],dt,q,zero);vals.append(N/den)
   if not order:continue
   Nt,ppt=self._eval(self.dnums[i],dt,q,zero)
   Nq=[pp[1+j] for j in range(7)];Nqt=[ppt[1+j] for j in range(7)]
   Nqq=[[zero for _ in range(7)] for _ in range(7)]
   for idx,(j,k) in enumerate(self.mons[8:],8):
    Nq[j]+=pp[idx]*q[k];Nq[k]+=pp[idx]*q[j]
    Nqt[j]+=ppt[idx]*q[k];Nqt[k]+=ppt[idx]*q[j]
    Nqq[j][k]+=pp[idx];Nqq[k][j]+=pp[idx]
   Ns=[Nq[j]+Nt*self.row[j] for j in range(7)]
   Ds=[den1*self.row[j] for j in range(7)]
   JJ.append([Ns[j]/den-N*Ds[j]/den**2 for j in range(7)])
   if order==1:continue
   Ntt,_=self._eval(self.ddnums[i],dt,q,zero)
   Hij=[]
   for j in range(7):
    row=[]
    for k in range(7):
     Njk=Nqq[j][k]+Nqt[j]*self.row[k]+Nqt[k]*self.row[j]+Ntt*self.row[j]*self.row[k]
     Djk=den2*self.row[j]*self.row[k]
     row.append(Njk/den-(Ns[j]*Ds[k]+Ns[k]*Ds[j]+N*Djk)/den**2+2*N*Ds[j]*Ds[k]/den**3)
    Hij.append(row)
   HH.append(Hij)
  return vals,(JJ if order else None),(HH if order==2 else None)
 def field_jac(self,q):
  f,j,_=self.field_jac_hess(q,1);return f,j

def _local_transform(self,B,ref):
 cache=getattr(self,'_balanced_cache',None)
 if cache is None or cache[0] is not B:
  cache=(B,BalancedRationalField(self,B));self._balanced_cache=cache
 return cache[1].local(ref)
IntervalBlowup.local_transform=_local_transform
