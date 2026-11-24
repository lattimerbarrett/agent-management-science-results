import sympy as S,json
from pathlib import Path
r,x,c=S.symbols('r x c',positive=True)
lam=r-1+c*x*x
expr=S.exp(x)/(lam+S.exp(x))+S.exp(-x)/(lam+S.exp(-x))+(r-2)/(lam+1)-1
coef=S.simplify(S.diff(expr,x,2).subs(x,0)/2)
cv=S.factor(S.solve(coef,c)[0]);print('lambda s2 coefficient',cv)
assert S.simplify(cv-(r-1)*(r-2)/r**2)==0
sigma=S.factor(2*cv/(r-1));assert S.simplify(sigma-2*(r-2)/r**2)==0
hess=S.factor(r-r**2/(r-2));assert S.simplify(hess+2*r/(r-2))==0
# Exact covariance summation from Markov spectral eigenvalue
for R in range(3,21):
 eig=-S.Rational(1,R-1)
 sig=S.Rational(1,R)*(1+eig)/(1-eig)
 assert sig==S.Rational(R-2,R*R)
 print(R,'cov eigen',sig,'cycle imbalance coefficient',S.Rational(R,R-2))
Path('workspace/agent2_uniform_imbalance_checks.json').write_text(json.dumps({'lambda_second_coefficient':str(cv),'covariance_direction_norm2':str(sigma),'rate_hessian':str(hess),'checked_r':list(range(3,21))},indent=2))
Path('workspace/agent2_uniform_imbalance_checks.py').write_text(Path(__file__).read_text())
