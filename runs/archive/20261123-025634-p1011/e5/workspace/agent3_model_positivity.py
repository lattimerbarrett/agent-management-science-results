import sympy as s, json, os
x=s.symbols('x')

def gram(n,d):
 a=s.Rational(n,2)
 Ps=[]
 for j in range(d+1):
  p=0
  for h in range(j+1):
   # rising m+1 and m+n+1-h with m=x-a-1
   p+=s.binomial(j,h)*2**h*(-1)**(j-h)*s.rf(x-a,h)*s.rf(x+a+1-h,h)/(s.factorial(h)*s.prod(n+2-2*r-1 for r in range(1,h+1)))
  Ps.append(s.expand(p))
 def moment(i,j):
  target=s.Poly(s.expand(x*Ps[i]*Ps[j]),x)
  poly=0; rem=target.as_expr()
  for h in range(i+j,-1,-1):
   mon=x**(2*h)
   image=s.expand((x+a-2)**2*mon.subs(x,x-1)-(x-a+2)**2*mon.subs(x,x+1))
   coefficient=s.expand(rem).coeff(x,2*h+1)/image.coeff(x,2*h+1)
   poly+=coefficient*mon
   rem=s.expand(rem-coefficient*image)
  assert rem==0
  return s.simplify(s.gamma(s.Rational(3,2))**2/s.gamma(s.Rational(n+1,2))**2*(n-1)**2*poly.subs(x,a)+s.gamma(2)**2/s.gamma(s.Rational(n+2,2))**2*n**2*poly.subs(x,a+1))
 G=s.Matrix(d+1,d+1,moment)
 D=s.Matrix(d+1,d+1,lambda i,j:(1+i+j)*G[i,j])
 return G,D
# Rational, alternating-series Machin enclosure; no floating-point sign tests.
def atan_interval(q,N=24):
 total=sum((-1)**j*s.Rational(1,(2*j+1)*q**(2*j+1)) for j in range(N))
 nxt=(-1)**N*s.Rational(1,(2*N+1)*q**(2*N+1))
 return min(total,total+nxt),max(total,total+nxt)
a5,b5=atan_interval(5);a239,b239=atan_interval(239)
lo,hi=16*a5-4*b239,16*b5-4*a239
def polynomial_interval(expr):
 expr=s.Poly(s.expand(expr),s.pi)
 lower=upper=0
 for (p,),coefficient in expr.terms():
  l,h=lo**p,hi**p
  if coefficient<0:l,h=h,l
  lower+=coefficient*l;upper+=coefficient*h
 return lower,upper
def certify_sign(expr):
 num,den=s.fraction(s.cancel(expr))
 nl,nh=polynomial_interval(num);dl,dh=polynomial_interval(den)
 ns=1 if nl>0 else -1 if nh<0 else 0
 ds=1 if dl>0 else -1 if dh<0 else 0
 assert ns and ds
 return ns*ds
out=[]
for n in range(5,21):
 d=(n-5)//4
 G,D=gram(n,d)
 minors=[s.factor(D[:k,:k].det()) for k in range(1,d+2)]
 values=[float(m.evalf(30)) for m in minors]
 print(n,d,values)
 signs=[certify_sign(m) for m in minors]
 assert signs==([1]*(d+1) if n<=18 else [1]*d+[-1])
 out.append({'n':n,'d':d,'minors':[str(m) for m in minors],'values':values,'rationally_certified_signs':signs})
 # Record signs rather than assuming low-dimensional positivity.
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_model_positivity.json','w') as f:json.dump(out,f,indent=2)
import shutil
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_model_positivity.py'):shutil.copyfile(__file__,'workspace/agent3_model_positivity.py')
