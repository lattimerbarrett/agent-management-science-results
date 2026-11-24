import sympy as s
import mpmath as mp
mp.mp.dps=35
p=s.symbols('p', positive=True)
q=p/(p-1)
U=lambda t: 1+1/(t*(t-1))
assert s.simplify(U(q)/(p-1)-U(p))==0
print('Duality identity checked symbolically.')
# For w_delta(x)=|x|^(delta-1), f=1_(0,1), integrate
# only x<exp(-2), so the absolute logarithm has a fixed sign.
# Report delta * (restricted weighted H norm)/(weighted f norm).
# The substitution u=-delta*log(x) removes the singular endpoint.
for pp in [mp.mpf('1.5'),mp.mpf('3')]:
    target=mp.gamma(pp+1)**(1/pp)/mp.pi
    print('p =',pp,'limiting value =',mp.nstr(target,12))
    errors=[]
    for dd in [mp.mpf('.1'),mp.mpf('.03'),mp.mpf('.01')]:
        def integrand(u):
            a=u+dd*mp.log1p(-mp.exp(-u/dd))
            return mp.exp(-u)*a**pp
        integral=mp.quad(integrand,[2*dd,1,mp.inf])
        scaled=integral**(1/pp)/mp.pi
        errors.append(abs(scaled-target))
        print('delta =',dd,'scaled ratio =',mp.nstr(scaled,12))
    assert all(errors[i+1]<errors[i] for i in range(len(errors)-1))
print('The numerical checks verify only these scalar test computations, not a sharp matrix lower bound.')
