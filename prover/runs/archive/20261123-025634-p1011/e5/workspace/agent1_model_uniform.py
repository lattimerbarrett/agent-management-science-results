"""Verified dimension-family certificate for a spectral MODEL only.
This is not a construction of boundary Yamabe solutions.
"""
import sys,json
from pathlib import Path
import sympy as s
import numpy as np
sys.path.insert(0,'workspace')
from agent1_spectral_exact import gram

def atan_bounds(q,N=32):
    q=s.Rational(q)
    a=sum((-1)**j*q**(2*j+1)/s.Integer(2*j+1) for j in range(N))
    b=a+(-1)**N*q**(2*N+1)/s.Integer(2*N+1)
    return min(a,b),max(a,b)
a,b=atan_bounds(s.Rational(1,5)); c,d=atan_bounds(s.Rational(1,239))
PILO,PIHI=16*a-4*d,16*b-4*c
assert PILO>s.Rational(314,100) and PIHI<s.Rational(22,7)

def interval(e):
    e=s.sympify(e)
    if e==s.pi:return PILO,PIHI
    if e.is_Rational:return e,e
    if e.is_Add:
        vals=[interval(a) for a in e.args]
        return sum(a for a,b in vals),sum(b for a,b in vals)
    if e.is_Mul:
        lo=hi=s.Integer(1)
        for arg in e.args:
            a,b=interval(arg); v=[lo*a,lo*b,hi*a,hi*b];lo,hi=min(v),max(v)
        return lo,hi
    if e.is_Pow and e.exp.is_Integer:
        lo,hi=interval(e.base);power=int(e.exp)
        if power<0:
            assert lo*hi>0
            vals=[1/lo,1/hi];lo,hi=min(vals),max(vals);power=-power
        vals=[lo**power,hi**power]
        if lo<=0<=hi and power%2==0:vals.append(s.Integer(0))
        return min(vals),max(vals)
    raise ValueError(e)

certs={}
for n in range(21,33):
    G=gram(n,2)
    D=s.Matrix(3,3,lambda i,j:(2+2*i+2*j)*G[i,j])
    _,V=np.linalg.eigh(np.array(D.evalf(),float))
    v0=V[:,0]/V[0,0]
    for denom in [100,1000,10000,100000]:
        v=s.Matrix([s.Rational(float(t)).limit_denominator(denom) for t in v0])
        expr=s.factor((v.T*D*v)[0]);lo,hi=interval(expr)
        if hi<0:break
    assert hi<0
    certs[str(n)]={'vector':[str(t) for t in v], 'quadratic':str(expr), 'upper':str(hi)}
    print(n,list(v),float(expr),flush=True)

# Uniform n>=33 proof of a negative degree1 dilation determinant.
n,x=s.symbols('n x')
c0=n**5-14*n**4-339*n**3+3852*n**2-13068*n+12960
c1=-2*(3*n**5-42*n**4+659*n**3-4216*n**2+12036*n-13248)
c2=9*n**5-126*n**4-195*n**3+4836*n**2-13820*n+11488
assert all(c<0 for c in s.Poly(c1.subs(n,n+33),n).all_coeffs())
assert all(c>0 for c in s.Poly(c2.subs(n,n+33),n).all_coeffs())
# Gamma log convexity gives 2/(n+1)<=Gamma((n+1)/2)^2/Gamma((n+2)/2)^2<=2/n.
L=8*n**2/(s.Rational(22,7)*(n-1)**2*(n+1))
U=8*n/(s.Rational(314,100)*(n-1)**2)
num,den=s.fraction(s.factor(c0+c1*U+c2*L**2))
assert all(c>0 for c in s.Poly(num.subs(n,n+33),n).all_coeffs())
assert all(c>0 for c in s.Poly(den.subs(n,n+33),n).all_coeffs())
print('PASS: uniform spectral MODEL determinant certificate for every n>=33.')
print('WARNING: not a proof of the PDE construction or of sharp compactness.')
Path('workspace/agent1_model_uniform.py').write_text(Path(__file__).read_text())
Path('workspace/agent1_model_uniform.json').write_text(json.dumps(certs,indent=2))
