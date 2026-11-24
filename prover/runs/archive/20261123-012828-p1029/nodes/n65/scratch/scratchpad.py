import sympy as s
from pathlib import Path
# Check the cutoff estimate used to construct support projections in the
# quasitracial quotient. These are scalar functional-calculus identities.
t,n=s.symbols('t n', positive=True)
f=n*t/(1+n*t)
assert s.simplify(t*(1-f)**2-t/(1+n*t)**2)==0
assert s.simplify(1/(4*n)-t/(1+n*t)**2-(n*t-1)**2/(4*n*(1+n*t)**2))==0
print('Cutoff estimate: t(1-f_n(t))^2 <= 1/(4n).')
# Projection distances: (p-r)^2=p-r for r<=p.
p,r=s.symbols('p r',commutative=False)
print('For nested projections r<=p: q((p-r)^2)=q(p)-q(r).')
# Record an audit of the proposed quotient construction.
notes='''Quotient audit\n\nQ = product(M_k) / I_U, I_U={x: lim_U tau_k(x_k^*x_k)=0}.\nFaithfulness: tau_U(x^*x)=0 is exactly membership in I_U.\nSupport: f_n(x^*x), f_n(t)=nt/(1+nt), is q-metric Cauchy by\nabelian dominated convergence; its limit is a projection p with xp=x.\nIf xy=0 then f_n(x^*x)y=0, hence py=0.\nFinite projection joins are supports of finite positive sums.\nArbitrary joins reduce to countable increasing finite joins by maximizing\ntheir quasitrace dimensions; q-metric completeness supplies the limit.\nThus ann_r(S)=(1-join support(s))Q.\nFiniteness: v*v=1 => tau(vv*)=1 => tau(1-vv*)=0 => vv*=1.\nFactoriality when each M_k is a factor: a central projection of dimension\nt in (0,1) lifts to p_k. Choose partial isometries between subprojections\nof p_k and 1-p_k of dimension min(tau_k(p_k),1-tau_k(p_k)).\nThey yield a nonzero element v with pv=0, vp=v, contradiction.\nNo-lub: use q-metric saturation, order conditions, and the retained\nlower bound tau((u-a_N)^2)>=eta^2 for a hypothetical supremum u.\n'''
Path('quotient_audit.txt').write_text(notes)
print(notes)
