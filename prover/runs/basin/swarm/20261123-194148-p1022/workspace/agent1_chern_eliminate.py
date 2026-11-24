import sys
sys.path.insert(0,'workspace')
import sympy as s
from agent4_chern_constraints import constraints

def eliminate(eq, vs):
    eq=list(eq); vs=list(vs); sub={}
    while True:
        found=False
        for e in eq:
            for v in vs[::-1]:
                p=s.Poly(e,v)
                if p.degree()==1 and p.coeff_monomial(v).is_number:
                    val=-p.coeff_monomial(1)/p.coeff_monomial(v)
                    sub[v]=val; vs.remove(v)
                    eq=[s.expand(f.subs(v,val)) for f in eq]
                    eq=[f for f in eq if f!=0]
                    found=True;break
            if found:break
        if not found: break
    return eq,vs,sub

def system(ranks, weights=None):
    eq, vs, sub0=constraints(ranks,weights)
    eq,vs,sub=eliminate(eq,vs)
    return eq,vs,sub0|sub

if __name__=='__main__':
    for ranks in [(6,1),(5,2),(4,3),(3,4),(2,5),(1,6)]:
        eq,vs,sub=system(ranks)
        g=s.groebner(eq,*vs,order='grevlex') if vs else eq
        print(ranks,'remaining',len(vs),'GB',list(g),flush=True)
