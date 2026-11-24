import sympy as s
p=s.diag(1,0)
v=s.Matrix([s.Rational(7,25),s.Rational(24,25)])
q=v*v.T
assert p*p==p and q*q==q and p*q!=q*p
n=0
for den in range(5,40):
    for num in range(den//2+1,den):
        t=s.Rational(num,den)
        if t*s.Rational(32,25)>1: continue
        S=t*(p+q); D=2*(1-t)
        assert D<1
        assert all(z>=0 for z in (s.eye(2)-S).eigenvals())
        assert s.Matrix.hstack(s.Matrix([1,0]),v).rank()==2
        assert all(z>=0 for z in (S-(1-D)*s.eye(2)).eigenvals())
        n+=1
print("Exact noncommuting weighted join certificates:",n)
