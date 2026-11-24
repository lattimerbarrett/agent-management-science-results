"""Exact all-k confluent m1 formula, independently checked for k0..10.
Analytic proof: quotient by Q=(1-xT)(1-yT), evaluate at1/x,1/y.
This does not establish nonconfluent configurations.
"""
import sympy as s

def check(max_k=10):
    x,y,c,T=s.symbols('x y c T');U=(1+x*x)*(1+y*y);V=(1+x*y)**2
    for k in range(max_k+1):
        A=s.Poly((1-c*T)*(T+x)**k,T);B=s.Poly((T+c)*(T+y)**k,T)
        aa=[A.nth(i) for i in range(k+2)];bb=[B.nth(i) for i in range(k+2)]
        for i in range(k):
            for Z in (aa,bb):
                z=Z[i];Z[i+1]=s.expand(Z[i+1]+(x+y)*z);Z[i+2]=s.expand(Z[i+2]-x*y*z)
        D=s.expand(aa[k]*bb[k+1]-aa[k+1]*bb[k])
        positive=(1+c*c)*U**k+(y-c)*(x-y)*(1+c*x)*sum(U**(k-1-j)*V**j for j in range(k))
        assert s.expand(D-positive)==0
    return max_k+1

if __name__=='__main__':print('Exact symbolic confluent formulas checked:',check())
