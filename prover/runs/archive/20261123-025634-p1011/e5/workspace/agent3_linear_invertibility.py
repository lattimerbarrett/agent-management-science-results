import sympy as s
import os,shutil,json
n,k,mu=s.symbols('n k mu',positive=True)
c=n*(n-2)/4
rho=(mu-n)/(mu+c)
assert s.simplify(rho.subs(mu,0)+4/(n-2))==0
assert s.simplify(rho.subs(mu,n))==0
assert s.simplify(rho.subs(mu,2*(n+1))-4/(n+4))==0
assert s.simplify(s.diff(rho,mu)-(c+n)/(mu+c)**2)==0
# Exact inequality for k>=2, by k=2+j with j>=0.
j=s.symbols('j',nonnegative=True)
num=s.factor((rho-4/(n+4)).subs(mu,(j+2)*(j+n+1)))
expected=4*j*n*(j+n+3)/((n+4)*(2*j+n+2)*(2*j+n+4))
assert s.simplify(num-expected)==0
# Verify Euclidean Jacobi coefficients under conformal compactification.
assert s.simplify(c-n*(n+2)/4+n)==0
# Kernel generators, using radial derivative identities.
r2,xi=s.symbols('r2 xi',real=True)
a=(n-2)/2
# Translation Z_i/U=-(n-2)xi/(1+r2)=-a*y_i
assert s.simplify(-(n-2)*xi/(1+r2)+a*2*xi/(1+r2))==0
# Dilation Z_0/U=a*(r2-1)/(r2+1)=a*y_last
records=[]
for nv in range(3,101):
 for kv in range(0,101):
  eig=s.Integer(kv)*(kv+nv-1)
  rat=(eig-nv)/(eig+s.Rational(nv*(nv-2),4))
  if kv==1:assert rat==0
  else:assert abs(rat)>=s.Rational(4,nv+4)
 records.append({'n':nv,'inverse_norm_exact':str(s.Rational(nv+4,4))})
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_linear_invertibility.json','w') as f:json.dump({'symbolic_general_dimension_gap_identity':str(num),'dimensions':records},f,indent=2)
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_linear_invertibility.py'):shutil.copyfile(__file__,'workspace/agent3_linear_invertibility.py')
print('Verified exact all-n spectral gap identity:',num)
print('Supplementary 9898 exact rational eigenvalue checks passed.')
