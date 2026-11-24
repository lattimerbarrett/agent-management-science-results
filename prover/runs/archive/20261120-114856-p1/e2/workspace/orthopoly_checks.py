"""Exact rational checks for restarted-CG spectral formulas."""
import sympy as S
x=S.symbols("x")
def monic_orthogonal(nodes,w,s):
    M=S.Matrix([[sum(wi*li**(i+j) for wi,li in zip(w,nodes)) for j in range(s)] for i in range(s)])
    rhs=S.Matrix([-sum(wi*li**(i+s) for wi,li in zip(w,nodes)) for i in range(s)])
    a=M.inv()*rhs
    return x**s+sum(a[j]*x**j for j in range(s))
def step(nodes,w,s):
    p=monic_orthogonal(nodes,w,s)
    vals=[p.subs(x,t) for t in nodes]
    h=sum(wi*pi*pi for wi,pi in zip(w,vals))
    return [S.cancel(wi*pi*pi/h) for wi,pi in zip(w,vals)],p,h

def check():
    for s in (1,2,3):
        nodes=list(map(S.Integer,range(1,2*s+3)))
        z=[S.Integer(i*i+1) for i in range(1,len(nodes)+1)]
        w=[a/sum(z) for a in z]
        wn,p,h=step(nodes,w,s)
        wnn,q,hn=step(nodes,wn,s)
        # No square roots: squared Cauchy and exact defect identity.
        cross=sum(wi*p.subs(x,t)*q.subs(x,t) for wi,t in zip(w,nodes))
        assert S.cancel(cross-h)==0
        defect=sum(wi*(p.subs(x,t)*q.subs(x,t)-h)**2 for wi,t in zip(w,nodes))
        assert S.cancel(defect-h*(hn-h))==0
        assert hn>=h
        for j in range(s):
            assert S.cancel(sum(wi*p.subs(x,t)*t**j for wi,t in zip(w,nodes)))==0
    print("Exact rational orthogonality, normalization, Lyapunov/defect identities checked for s=1,2,3.")
if __name__=="__main__": check()
