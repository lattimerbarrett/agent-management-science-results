"""Exact P3 rank-five width-three Chern and ramification checks."""
import sympy as s
from agent2_p3_chern_constraints import constraints
from agent1_chern_eliminate import eliminate

def check():
    results=[]
    for ranks in [(1,3,1),(1,2,2)]:
        eq,vs,sub=constraints(ranks)
        eq,vs,sub1=eliminate(eq,vs);sub.update(sub1)
        G=s.groebner(eq,*vs,order='grevlex')
        assert G.is_zero_dimensional
        points=s.solve(list(G),vs)
        if ranks==(1,3,1):
            assert set(points)=={(0,0),(0,1),(1,-1)}
        else:
            assert set(points)=={(0,0,0,0),(0,1,0,0),(0,1,0,1),(1,-1,0,1),(2,0,0,0)}
        a,v=vs[:2];top=-a-v
        residual=[]
        for P in points:
            S=dict(zip(vs,P))
            assert all(s.expand(e.subs(S))==0 for e in eq)
            if a.subs(S)!=0 and top.subs(S)!=0:residual.append(P)
        assert residual==([] if ranks==(1,3,1) else [(2,0,0,0)])
        results.append((ranks,points,residual))
    # Normal derivative syzygy for a conic in P2.
    x,y,z=s.symbols('x y z')
    a,b,c,d,e,f=s.symbols('a b c d e f')
    g0=a*x+b*y;g1=c*x+d*y;g2=e*x+f*y
    syz=s.Poly(y*y*g0-2*x*y*g1+x*x*g2,x,y)
    solved=s.solve(syz.coeffs(),(a,b,e,f),dict=True)
    assert solved==[{a:2*d,b:0,e:0,f:2*c}]
    # Binary-pencil restriction case: exact Jacobian determinant.
    q=[x*x+z*(a*x+b*y),y*y+z*(d*x+e*y),z*z]
    jac=s.Matrix([[s.diff(qi,var) for var in (x,y,z)] for qi in q]).det()
    expected=2*z*((2*x+a*z)*(2*y+e*z)-b*d*z*z)
    assert s.expand(jac-expected)==0
    assert s.expand((expected/(2*z)).subs(z,0))==4*x*y
    return results

if __name__=='__main__':
    print(check())
