"""Exact checks for the s=1 convergence proof and general two-cycle identity."""
import sympy as sp

def check_s1():
    m2,m3,m4,x=sp.symbols("m2 m3 m4 x")
    q=sp.Poly(sp.expand((x*x-m3*x/m2-m2)**2),x)
    moments={0:1,1:0,2:m2,3:m3,4:m4}
    val=sp.expand(sum(c*moments[k[0]] for k,c in q.terms()))
    assert sp.cancel(val-(m4-m3**2/m2-m2**2))==0
    p,a,b=sp.symbols("p a b")
    mu=p*a+(1-p)*b
    var=sp.expand(p*(a-mu)**2+(1-p)*(b-mu)**2)
    assert sp.cancel(p*(a-mu)**2/var-(1-p))==0
    mu2=(1-p)*a+p*b
    assert sp.expand((a-mu)*(a-mu2)-(b-mu)*(b-mu2))==0
    assert sp.expand((a-mu)*(a-mu2)-p*(1-p)*(a-b)**2)==0

def check_fixed_pair_parameterization():
    # s=2 exact irrational example; parameter H=x-t.
    x,t=sp.symbols("x t")
    nodes=[-3,-1,1,3]
    f=x*x+sp.sqrt(2)*x-4
    g=x*x-sp.sqrt(2)*x-4
    P=sp.prod(x-a for a in nodes)
    N=sp.Integer(7)
    assert sp.expand(f*g-P-N)==0
    d=[sp.prod(a-b for b in nodes if a!=b) for a in nodes]
    p=[sp.cancel(N*(a-t)/(di*f.subs(x,a))) for a,di in zip(nodes,d)]
    assert sp.simplify(sum(p)-1)==0
    for j in range(2):
        assert sp.simplify(sum(pi*a**j*f.subs(x,a) for a,pi in zip(nodes,p)))==0
    pp=[sp.cancel(pi*f.subs(x,a)**2/N) for a,pi in zip(nodes,p)]
    for j in range(2):
        assert sp.simplify(sum(pi*a**j*g.subs(x,a) for a,pi in zip(nodes,pp)))==0
    for a,pi,pip in zip(nodes,p,pp):
        assert sp.simplify(pip*g.subs(x,a)**2/N-pi)==0
    # At t=0 all weights are strictly positive.
    assert all(pi.subs(t,0)>0 for pi in p)

if __name__=="__main__":
    check_s1()
    check_fixed_pair_parameterization()
    print("All exact symbolic checks passed.")
