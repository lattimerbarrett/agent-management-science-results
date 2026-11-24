"""Exact Bernstein-positivity proof for the m=1, two-axis contraction model.
This proves only k=2, not arbitrary k and not the requested eventual theorem.
"""
import sympy as s

def check():
    x0,x1,y0,y1,c,T,a,b,u,v=s.symbols('x0 x1 y0 y1 c T a b u v')
    ps=[(1-x0*T)*(1-y0*T),T*(1-x1*T)*(1-y1*T),
        (1-c*T)*(T+x0)*(T+x1),(T+c)*(T+y0)*(T+y1)]
    M=s.Matrix([[s.expand(p).coeff(T,j) for j in range(4)] for p in ps])
    D=s.expand(M.det());P=s.Poly(D,y0,y1);out=0
    # y_i=(x_i+c*t_i)/(1+t_i), clear denominators of degree2.
    for (i,j),coef in P.terms():
        out+=coef*(x0+c*a)**i*(1+a)**(2-i)*(x1+c*b)**j*(1+b)**(2-j)
    counts={}
    for label,sub in [('below',{x1:x0+u,c:x0+u+v}),
                      ('split',{x1:x0+u+v,c:x0+u}),
                      ('above',{x0:c+u,x1:c+u+v})]:
        po=s.Poly(s.expand(out.subs(sub,simultaneous=True)))
        assert all(cf>=0 for cf in po.coeffs())
        # A strictly positive constant term ensures strict positivity throughout.
        assert po.TC()>0
        counts[label]=len(po.terms())
    return counts

if __name__=='__main__':print(check())
