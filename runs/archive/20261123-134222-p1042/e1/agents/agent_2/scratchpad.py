import sympy as s,json
m=s.symbols('m',integer=True,positive=True)
C=lambda x,k:s.prod(x-j for j in range(k))/s.factorial(k)
c=[1,3,9,24,54]
r=[s.expand(c[a]*C(m,a)*C(m-a-1,4-a)) for a in range(5)]
chi=s.factor(sum((-1)**a*r[a] for a in range(5)))
a=m*(m-1)*(m-2)*(m-7)/24
b=s.factor(chi+a)
expected=(m**4+2*m**3+11*m**2+10*m+12)/12
assert s.expand(b-expected)==0
print('rank polynomials',r,'chi',chi,'b',b)
open('workspace/agent2_euler.json','w').write(json.dumps({'D_ranks':list(map(str,r)),'chi':str(chi),'a':str(a),'b':str(b)},indent=2))
open('workspace/agent2_euler.py','w').write(open(__file__).read())
