import sympy as s
from pathlib import Path
k=s.symbols('k',integer=True,nonnegative=True)
def exact_sum(a,r):
    # For integer a the gamma ratio is an explicit reciprocal polynomial.
    T=s.prod((k+3+2*t)*(k+2*a-3-2*t) for t in range(r))
    expr=s.cancel((k+a)*T/s.prod((k+3+2*j)/2 for j in range(a-2))**2)
    parts=s.apart(expr,k)
    out=0;residue=0
    for term in s.Add.make_args(parts):
        num,den=s.fraction(term)
        factors=s.factor_list(den,k)[1]
        assert len(factors)==1,(term,factors)
        base,p=factors[0]
        slope=s.diff(base,k);b=s.simplify(base.subs(k,0)/slope)
        c=s.simplify(term*(k+b)**p)
        assert not c.has(k)
        if p==1:
            residue+=c;out-=c*s.polygamma(0,b)
        else:out+=c*(-1)**p/s.factorial(p-1)*s.polygamma(p-1,b)
    assert s.simplify(residue)==0
    return s.simplify(s.expand_func(out))
def formula(a,r):
    return s.simplify(4**r/s.Integer(a-3-r)*(s.gamma(s.Rational(3,2))*s.gamma(s.Rational(3,2)+r)/(s.gamma(a-s.Rational(3,2))*s.gamma(a-s.Rational(3,2)-r))+s.gamma(2)*s.gamma(2+r)/(s.gamma(a-1)*s.gamma(a-1-r))))
count=0
for a in range(4,11):
 for r in range(a-3):
    lhs=exact_sum(a,r);rhs=formula(a,r)
    assert s.simplify(lhs-rhs)==0,(a,r,lhs,rhs)
    count+=1
print('PASS:',count,'exact rational-series sums independently verify moment formula')
Path('workspace/agent4_exact_moments.py').write_text(Path('scratchpad.py').read_text())
