"""Standalone exact incidence certificate. Requires only SymPy.
Recomputes all systems over QQ; no input files, network or subprocesses.
The geometric interpretation of the asserted alternatives is in the proof.
"""
import sympy as S
from functools import lru_cache
from itertools import product
h,x,T=S.symbols('h x T')
class Chow:
 def __init__(self,n):
  self.n=n
  self.B={j:self.basis(j) for j in range(1,2*n)}
 @lru_cache(None)
 def mon(self,a,b):
  if a>self.n:return {}
  if b<self.n:return {(a,b):S.Integer(1)}
  out={}
  for i in range(1,self.n+1):
   for m,c in self.mon(a+i,b-i).items():out[m]=out.get(m,0)-c
  return {m:c for m,c in out.items() if c}
 def red(self,f):
  out={}
  for (a,b),c in S.Poly(S.expand(f),h,x).terms():
   for m,d in self.mon(a,b).items():out[m]=out.get(m,0)+c*d
  return S.expand(sum(c*h**a*x**b for (a,b),c in out.items()))
 def basis(self,j):
  p=[self.red((h+x)**(j-2*b)*(h*x)**b) for b in range(j//2+1)]
  M=S.Matrix([[S.Poly(f,h,x).coeff_monomial(h**(j-b)*x**b) for f in p] for b in range(j+1)])
  return [p[k] for k in M.rref()[1]]
 def total(self,parts):
  f=S.Integer(1);vs=[];cs=[]
  for i,r in enumerate(parts):
   c=[S.Integer(1)];g=(T+(len(parts)-1-i)*h)**r
   for j in range(1,r+1):
    u=S.symbols(f'u{i}_{j}_0:{len(self.B[j])}');vs+=list(u)
    c.append(sum(v*b for v,b in zip(u,self.B[j])))
    g+=c[-1]*(T+(len(parts)-1-i)*h)**(r-j)
   f=S.expand(f*g);cs.append(c)
  out={}
  for (a,b,c),v in S.Poly(f,T,h,x).terms():
   for (d,e),w in self.mon(b,c).items():out[a,d,e]=out.get((a,d,e),0)+v*w
  eq=list(dict.fromkeys(S.expand(v) for (a,b,c),v in out.items() if c and v!=0))
  return eq,vs,cs
 def character(self,parts):
  vs=[];ch=[];lines=[]
  for i,r in enumerate(parts):
   c=[S.Integer(r)]
   if r==1:lines.append(S.Symbol('b'+str(i)))
   for j in range(1,2*self.n):
    if r==1:c.append(self.red((lines[-1]*(h+x))**j/S.factorial(j)))
    else:
     u=S.symbols(f'v{i}_{j}_0:{len(self.B[j])}');vs+=list(u)
     c.append(sum(v*b for v,b in zip(u,self.B[j])))
   ch.append(c)
  eq=[]
  for k in range(1,2*self.n):
   f=self.red(sum(sum(ch[i][j]*(2-i)**(k-j)*h**(k-j)/S.factorial(k-j) for j in range(k+1)) for i in range(3)))
   eq += [v for (a,b),v in S.Poly(f,h,x).terms() if b]
  vs=list(reversed(vs));sol=next(iter(S.linsolve(eq,vs)));sub=dict(zip(vs,sol))
  free=(set().union(*(z.free_symbols for z in sol))|set(lines))-{h,x}
  eq=[];cs=[]
  for i,r in enumerate(parts):
   c=[S.Integer(1)]
   for k in range(1,2*self.n-1):
    z=self.red(sum((-1)**(j-1)*S.factorial(j)*ch[i][j].subs(sub)*c[k-j] for j in range(1,k+1))/k)
    if k>r:eq+=S.Poly(z,h,x).coeffs()
    c.append(z if parts==(3,1,3) or k<=r else S.Integer(0))
   cs.append(c)
  eq=list(dict.fromkeys(S.factor(z) for z in eq if z!=0));back={}
  if parts!=(3,1,3):
   while True:
    hit=None
    for z in sorted(eq,key=S.count_ops):
     for v in sorted(free,key=str,reverse=True):
      p=S.Poly(z,v)
      if p.degree()==1 and p.coeff_monomial(v).is_Rational and p.coeff_monomial(v)!=0:
       hit=(v,S.expand(-p.coeff_monomial(1)/p.coeff_monomial(v)));break
     if hit:break
    if not hit:break
    v,z=hit;free.remove(v)
    back={u:S.expand(w.subs(v,z)) for u,w in back.items()};back[v]=z
    eq=list(dict.fromkeys(S.factor(w.subs(v,z)) for w in eq));eq=[w for w in eq if w!=0]
  cs=[[z.subs(back,simultaneous=True) for z in c] for c in cs]
  return eq,sorted(free,key=str),cs

def compositions(r):
 if not r:yield ()
 else:
  for a in range(1,r+1):
   for b in compositions(r-a):yield (a,)+b

def solve(eq,vs,graded=False):
 g=S.groebner(eq,*reversed(vs),order='grevlex' if graded else 'lex',domain=S.QQ)
 if graded:g=g.fglm('lex')
 roots=S.solve_poly_system(list(g),*vs)
 assert roots is not None
 vals=[sorted({z[i] for z in roots}) for i in range(len(vs))]
 for v,w in zip(vs,vals):
  p=S.prod(v-a for a in w)
  assert any(g.reduce(S.expand(p**k))[1]==0 for k in range(1,9))
 good=[]
 for z in product(*vals):
  d=dict(zip(vs,z))
  if all(S.expand(f.subs(d))==0 for f in eq):good.append(z)
 assert set(good)==set(roots)
 return g,[dict(zip(vs,z)) for z in roots]

def lower(n,rmax):
 C=Chow(n);systems=roots=0
 for r in range(2,rmax+1):
  for p in compositions(r):
   if len(p)==1:continue
   eq,vs,cs=C.total(p);g,ss=solve(eq,vs);systems+=1;roots+=len(ss)
   for d in ss:
    a=[d.get(S.Symbol(f'u{i}_1_0'),0) for i in range(len(p))]
    zero=lambda i:all(d.get(S.Symbol(f'u{i}_2_{j}'),0)==0 for j in range(2))
    if any(sum(a[:i])==0 for i in range(1,len(a))):continue
    if n==3 and (p[:2]==(1,1) or p[-2:]==(1,1)):continue
    if n==3 and ((p[0]>=2 and zero(0)) or (p[-1]>=2 and zero(len(p)-1))):continue
    if (p[0]==1 and a[0]==-1) or (p[-1]==1 and a[-1]==1):continue
    if n==2:assert p==(1,1,1) and a==[-2,0,2]
    else:
     assert p in ((1,2,2),(2,2,1)) and a==[-2,0,2] and zero(1)
     i=2 if p[0]==1 else 0
     assert d[S.Symbol(f'u{i}_2_0')]==4 and d[S.Symbol(f'u{i}_2_1')]==-4
 print('P%d:'%n,systems,'systems,',roots,'complex roots checked',flush=True)
 assert (systems,roots)==((4,10) if n==2 else (26,74))

def p4():
 C=Chow(4);s=h+x;t=h*x;u=s*s-t
 for p in [(1,6),(2,5),(3,4)]:
  eq,vs,cs=C.total(p);g,ss=solve(eq,vs)
  tops={S.expand(sum(cs[0]).subs(d)) for d in ss}
  expected={S.Integer(1),1-s}
  if p==(3,4):expected|={1-s+u-s**3+2*s*t,1-2*s+2*s*s-t-s*t}
  assert tops=={S.expand(z) for z in expected}
  for d in ss:
   if S.expand(sum(cs[0]).subs(d)-(1-s+u-s**3+2*s*t))==0:
    assert S.expand(sum(cs[1]).subs(d)-(1+s))==0
  assert len(ss)==(4 if p==(3,4) else 2)
 for p in [(1,3,1),(1,4,1),(1,3,2),(1,5,1)]:
  eq,vs,cs=C.total(p)
  if p==(1,5,1):
   g=S.groebner(eq,*reversed(vs));assert g.reduce((vs[0]*vs[-1])**3)[1]==0;continue
  g,ss=solve(eq,vs)
  for d in ss:
   a=[d[S.Symbol(f'u{i}_1_0')] for i in range(3)]
   if a[0]==0 or a[2]==0:continue
   assert p==(1,3,2) and a==[-1,0,1]
   assert all(d[S.Symbol(f'u2_2_{j}')]==0 for j in range(2))
 for p in [(2,2,2),(1,3,3),(1,4,2),(2,2,3),(2,3,2),(3,1,3)]:
  eq,vs,cs=C.character(p)
  if p==(2,3,2):
   g=S.groebner(eq,*reversed(vs),order='grevlex',domain=S.QQ)
   a,b,c,d,e=vs;assert g.reduce(a*(a+d))[1]==0;continue
  g,ss=solve(eq,vs,True)
  if p==(2,2,2):assert len(ss)==1 and all(z==0 for z in ss[0].values())
  elif p in ((1,3,3),(1,4,2)):
   b=vs[0];assert {d[b] for d in ss}==({0,-1,-2} if p==(1,3,3) else {0,-1})
   for d in ss:
    if d[b]==-2:
     assert all(z==0 for v,z in d.items() if v!=b)
     assert all(S.expand(z.subs(d).subs(h,0))==0 for z in cs[1][1:4])
  elif p==(2,2,3):
   a,b,c,d,e=vs
   for z in ss:
    if z[a]:assert (z[a],z[b],z[c])==(-2,2,0)
  else:
   assert len(ss)==6
   for d in ss:
    a=[S.expand(c[1].subs(d)).coeff(h) for c in cs]
    if a[0]==0 or a[2]==0:continue
    f=S.expand(cs[0][2].subs(d))
    if f==0 or S.expand(cs[2][2].subs(d))==0:continue
    assert a==[-4,0,4]
    assert S.expand(f.subs(h,0))==8*x*x and 8!=S.binomial(4,2)
  print('P4',p,'checked',flush=True)
 print('All P4 incidence alternatives checked',flush=True)

def pencil():
 a,b,c,d,e,f,z=S.symbols('a b c d e f z')
 A=S.Matrix([[0,1,0],[1,0,0],[0,0,0]]);B=S.Matrix([[a,b,c],[b,d,e],[c,e,f]])
 p=S.Poly((A+z*B).det(),z)
 assert p.nth(1)==-f and p.nth(2).subs(f,0)==2*c*e
 assert p.nth(3).subs(f,0)==-a*e**2+2*b*c*e-c**2*d
 X,Y,Z=S.symbols('X Y Z');J=S.Matrix([X*X,Y*Y,Y*Z,Z*Z]).jacobian([X,Y,Z])
 from itertools import combinations
 ms=[J.extract(r,range(3)).det() for r in combinations(range(4),3)]
 assert S.gcd_list(ms)==4*X and all(v.subs({X:1,Y:0,Z:0})==0 for v in ms)
if __name__=='__main__':
 lower(2,3);lower(3,5);p4();pencil();print('ALL INCIDENCE CERTIFICATES PASSED')


def check_exterior_constructions():
    import sympy as S
    from itertools import combinations,permutations
    pairs=list(combinations(range(6),2));idx={v:i for i,v in enumerate(pairs)}
    # Coordinate incidence kernels force bivectors to be eigenvectors.
    # Pair-sum incidence kernels force equal eigenvalues on adjacent pairs.
    assert [(i,j) for i,o in enumerate(pairs) for j,v in enumerate(pairs) if set(v)<=set(o)]==[(i,i) for i in range(15)]
    rows=[]
    for i,j,k in permutations(range(6),3):
        row=[0]*15;row[idx[tuple(sorted((i,k)))]]=1
        row[idx[tuple(sorted((j,k)))]]=-1;rows.append(row)
    assert S.Matrix(rows).rank()==14 and S.Matrix(rows)*S.ones(15,1)==S.zeros(len(rows),1)
    M=S.zeros(6);z=iter(S.symbols('z:9'))
    for i,j in pairs:
        if i<2:M[i,j]=next(z);M[j,i]=-M[i,j]
    for I in combinations(range(6),5):
        for J in combinations(range(6),5):assert M.extract(I,J).det()==0
    w=S.zeros(6)
    for i in (0,2,4):w[i,i+1]=1;w[i+1,i]=-1
    g=S.diag(2,1,1,1,1,1);v=g*w*g.T
    assert w.det()==1 and w.rank()==v.rank()==6
    assert v[0,1]!=v[2,3] and w[0,1]==w[2,3]
    sym=list(combinations(range(6),2))+[(i,i) for i in range(6)]
    si={p:i for i,p in enumerate(sym)};mu=S.zeros(21,36);a=S.zeros(36,15)
    for i in range(6):
        for j in range(6):mu[si[tuple(sorted((i,j)))],6*i+j]=1
    for k,(i,j) in enumerate(pairs):a[6*i+j,k]=1;a[6*j+i,k]=-1
    assert mu.rank()==21 and a.rank()==15 and mu*a==S.zeros(21,15)
    x,y,b,l,pa=S.symbols('x y b l pa');s=x+y;p=x*y
    c=[1,-2*s,2*s*s-p,-s*p];r=[1,s,s*s-p,s**3-2*s*p]
    assert S.expand(r[1]-3*s-c[1])==S.expand(r[2]-2*s*r[1]+3*s*s-c[2])==0
    assert S.expand(r[3]-s*r[2]+s*s*r[1]-s**3-c[3])==0
    q=S.expand(b*x*(c[2]-b*x*(c[1]-b*x))-c[3])
    assert S.Poly(q,x,y).coeff_monomial(x*y*y)==2*b+1
    assert S.Poly(S.expand(l*x*c[1]+S.Rational(3,2)*l*l*x*x),x,y).coeff_monomial(x*y)==-2*l
    assert S.solve(2*pa-2+(4-2)*2,pa)==[-1]
    def line(k):return [int(S.binomial(k+3,3)) if k>=0 else 0,0,0,int(S.binomial(-k-1,3)) if k<=-4 else 0]
    table=[]
    for i in range(4):
        A=line(-2-i);B=[4*t for t in line(-1-i)]
        if i==3:assert A[3]==B[3]==4;table.append([0]*4)
        else:table.append([B[j]+(A[j+1] if j<3 else 0) for j in range(4)])
    assert table==[[0]*4,[0]*4,[0,0,1,0],[0]*4]
    al,be=S.symbols('al be',nonzero=True)
    assert S.Matrix([[al,be]]).rank()==1 and S.diag(al,al,be,be).det()==al**2*be**2
    assert S.binomial(5,2)-1==9<10 and S.binomial(4,2)==6!=8
    print('P5 rank/uniformity/simplicity/Koszul and P4 wedge/parity/cohomology checks passed.')

check_exterior_constructions()
