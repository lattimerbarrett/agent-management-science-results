"""Exact core moment functional for shared-two-root/negative-neutral example."""
import sympy as S
x=S.symbols('x')
beta=S.Rational(1,100)
c=S.Rational(1,10)
gamma=S.Rational(1,4)
p=(x*x-1)*(x-c)
q=(x*x-1)*(x+c)
r=x*x-gamma
chi=S.expand(p*q-beta)

def L(f):
    """Sum over six core nodes with weights d_i q_i r_i."""
    return S.rem(S.Poly(S.expand(q*r*f),x),S.Poly(chi,x)).coeff_monomial(x**5)

H=S.Matrix(3,3,lambda j,k:L(x**(j+k)))
e0=S.Matrix([1,0,0])
dp_coeff=-p.subs(x,0)*H.inv()*e0
dp=S.expand(sum(dp_coeff[j]*x**j for j in range(3)))

def dL(f):return S.expand(f).subs(x,0)-L(f)
def L1(f):return L(S.expand(p*p*f))/beta
def dL1(f):return S.factor((dL(S.expand(p*p*f))+2*L(S.expand(p*dp*f)))/beta)

if __name__=='__main__':
    assert L(1)==1
    for j in range(3):assert L(p*x**j)==0
    assert L(p*p)==beta
    assert H.det()>0 and H[:2,:2].det()>0 and H[0,0]>0
    dh=S.factor(dL(p*p)+2*L(p*dp))
    assert dh==0
    dh1=S.factor(dL1(q*q))
    assert dh1==4*beta
    print('core moments0..8:',[L(x**j)for j in range(9)])
    print('Gram H=',H)
    print('dq/depsilon when adding mass at0=',dp)
    print('dF0/depsilon=',dh,'dF1/depsilon=',dh1)
    print('Exact core functional / perturbation checks passed.')
