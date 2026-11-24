"""Exact QQ certificate for P4 rank7 splitting multiplicities (2,3,2)."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import sympy as s
from agent1_chern_eliminate import system

def check():
    es,vs,_=system((2,3,2))
    weights=[1,2,2,1,2]
    def order(m):
        return(sum(w*a for w,a in zip(weights,m)),tuple(-a for a in m[::-1]))
    G=s.groebner(es,*vs,order=order)
    a,u,b,v,w=vs
    expected=[w*w-w,a*w+v/2-w/2,v*w-v,a*a+v/2-w/2,
              a/3+u+v/6-w/6,b,a*v-v/2+w/2,v*v-w]
    assert list(G)==expected
    assert G.reduce(a*(a+v))[1]==0
    print('Exact weighted Groebner basis:',list(G))
    print('bottom_c1 * top_c1 = 0: verified')
    return list(G)

if __name__=='__main__': check()
