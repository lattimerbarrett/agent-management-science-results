from pathlib import Path
import sympy as s
source=Path('workspace/agent1_exactmoments.py').read_text()
exec(source.split('for n in [17,18,19]:')[0])
a=s.Matrix([1,-s.Rational(46284,100000),s.Rational(5655,100000),-s.Rational(1408,1000000)])
pilo=s.Rational('3.14159265358979323846264338327950288419716939937510')
pihi=s.Rational('3.14159265358979323846264338327950288419716939937511')
# Machin identity pi=16 atan(1/5)-4 atan(1/239),
# certified using exact rational alternating-series bounds.
def atan_bounds(q,N=40):
    lo=sum((-1)**k*s.Rational(1,(2*k+1)*q**(2*k+1)) for k in range(N))
    return lo,lo+s.Rational(1,(2*N+1)*q**(2*N+1))
a5,b5=atan_bounds(5);a239,b239=atan_bounds(239)
assert pilo<16*a5-4*b239 and 16*b5-4*a239<pihi
for n in range(19,33):
    C=Cexact(n)
    D=s.Matrix(4,4,lambda i,j:2*(1+i+j)*C[i,j])
    value=s.factor((a.T*D*a)[0])
    wexact=s.simplify(8*s.Rational(n+4,(n+1)**2)/s.pi*s.gamma(s.Rational(n+3,2))**2/(s.gamma(s.Rational(n+2,2))*s.gamma(s.Rational(n+4,2))))
    candidates=[value.subs(w,wexact.subs(s.pi,p)) for p in [pilo,pihi]]
    assert all(v<0 for v in candidates)
    print(n, 'certified dilation-negative range',*[float(v) for v in candidates])
