"""Exact incidence checks for width-three rank-seven cases (1,5,1),(1,4,2).
Requires agent1_chern_eliminate.py and agent4_chern_constraints.py alongside.
The geometric boundary-map/descent argument is separate from this script.
"""
import sympy as s
from agent1_chern_eliminate import system

def check_case(ranks):
    eq,vs,sub=system(ranks)
    G=s.groebner(eq,*vs,order='grevlex')
    assert G.is_zero_dimensional
    L=G.fglm('lex')
    assert all(G.reduce(e)[1]==0 for e in eq)
    if ranks==(1,5,1):
        a,v=vs
        expected=[2*a-v**6+3*v**4-3*v**2+v,v*(v*v-1)**3]
        points=[(0,0),(0,1),(1,-1)]
    else:
        a,v,w=vs
        expected=[a+v/2+w*w/2-w,v*v-w*w/3-2*w/3,
                  v*(w-1)**2,w*(w-1)**2]
        points=[(0,0,0),(0,1,1),(1,-1,1)]
    assert {s.expand(e) for e in L}=={s.expand(e) for e in expected}
    top=sub[s.Symbol('c2_10')]
    assert top==-a-v
    for point in points:
        mapping=dict(zip(vs,point))
        assert all(s.expand(e.subs(mapping))==0 for e in eq)
        assert a.subs(mapping)==0 or top.subs(mapping)==0
    # Exhaustiveness follows directly from the displayed triangular basis:
    # case151: v*(v^2-1)^3=0; case142: w*(w-1)^2=0.
    return {'ranks':ranks,'remaining_variables':list(map(str,vs)),
            'lex_basis':list(map(str,L)),'all_reduced_points':points,
            'boundary_c1_product_at_points':[a.subs(dict(zip(vs,P)))*top.subs(dict(zip(vs,P))) for P in points]}

if __name__=='__main__':
    for r in [(1,5,1),(1,4,2)]:
        print(check_case(r))
