"""Exact Chern-equation elimination for uniform rank7 on P4, widths (1,3,3)."""
import sys
sys.path.insert(0,'workspace')
import sympy as s
from agent1_chern_eliminate import system

def check():
    eq,vs,sub=system((1,3,3),(0,1,2))
    assert list(map(str,vs))==['c0_10','c1_10','c1_20','c1_21','c1_30']
    weights=(1,1,2,3,3)
    def weighted(m):
        return (sum(a*b for a,b in zip(weights,m)),tuple(-a for a in m[::-1]))
    gb=s.groebner(eq,*vs,order=weighted,domain=s.QQ)
    a,v,w,z,t=vs
    expected=[w*w-w-2*a*v-v*v+v,a*v*v+a*v,v**3-3*v*v+2*v-6*a*v,a*(v+w),v*w-w-v*v+v-4*a*v,z-a*v-v*v/2+v/2,t+v*v-v-w,a*a-a*v-2*a]
    assert all(gb.reduce(e)[1]==0 for e in expected)
    g2=s.groebner(expected,*vs,order=weighted,domain=s.QQ)
    assert all(g2.reduce(e)[1]==0 for e in eq)
    points=s.solve(list(gb),vs)
    expected_points={(0,0,0,0,0),(0,1,0,0,0),(0,2,2,1,0),(0,1,1,0,1),(1,-1,1,0,-1),(2,0,0,0,0)}
    assert set(points)==expected_points
    assert all(all(e.subs(dict(zip(vs,p)))==0 for e in eq) for p in points)
    remaining=[p for p in points if p[0]!=0 and p[0]+p[1]!=0]
    assert remaining==[(2,0,0,0,0)]
    print({'case':(1,3,3),'reduced_points':len(points),'nonconstant_boundary_point':remaining[0]})
    return True
if __name__=='__main__':
    check()
