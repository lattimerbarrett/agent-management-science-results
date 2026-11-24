import sympy as S
x,y=S.symbols('x y')
G=S.groebner([x**4,x**3+x*x*y+x*y*y+y**3],y,x,domain='EX')
def red(f):return G.reduce(S.expand(f))[1]
s=x+y;t=x*y

def comps(n):
 if n==0: yield ()
 else:
  for j in range(1,n+1):
   for q in comps(n-j):yield (j,)+q

def system(comp):
 variables=[];ch=[0]*6
 for i,m in enumerate(comp):
  a=len(comp)-1-i
  cs=[S.Integer(1)]
  for j in range(1,5):
   if j>m: cs.append(S.Integer(0));continue
   if j==1:
    A=S.Symbol('A'+str(i));variables.append(A);cs.append(A*s)
   elif j==2:
    B,C=S.symbols('B%d C%d'%(i,i));variables.extend([B,C]);cs.append(B*s*s+C*t)
   elif j==3:
    D=S.Symbol('D'+str(i));variables.append(D);cs.append(D*s*t)
   else:
    F=S.Symbol('F'+str(i));variables.append(F);cs.append(F*t*t)
  c1,c2,c3,c4=cs[1:]
  p=[m,c1,(c1*c1-2*c2)/2,(c1**3-3*c1*c2+3*c3)/6,(c1**4-4*c1*c1*c2+2*c2*c2+4*c1*c3-4*c4)/24,0]
  for k in range(6):
   ch[k]+=sum(p[j]*(a*x)**(k-j)/S.factorial(k-j) for j in range(min(k,4)+1))
 eq=[]
 for k in range(1,6):
  rr=red(ch[k]); pp=S.Poly(rr,x,y)
  for (ix,iy),v in pp.terms():
   if iy or ix>3: eq.append(v)
 return variables,eq
