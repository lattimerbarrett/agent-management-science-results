import sympy as s
from agent4_chern_constraints import constraints

def eliminate(ranks,weights=None):
    eq,vs,sub=constraints(ranks,weights)
    while True:
        found=None
        for e in eq:
            for v in reversed(vs):
                d=s.diff(e,v)
                if d!=0 and not d.free_symbols:
                    found=(e,v,d);break
            if found:break
        if not found:break
        e,v,d=found
        val=s.expand(v-e/d)
        eq=[s.expand(f.subs(v,val)) for f in eq]
        eq=list(dict.fromkeys(f for f in eq if f!=0))
        vs.remove(v);sub[v]=val
    return eq,vs,sub

if __name__=='__main__':
    for ranks in [(4,3),(3,4),(2,5),(1,6)]:
        eq,vs,sub=eliminate(ranks)
        gb=s.groebner(eq,*vs,order='grevlex')
        print(ranks,vs,list(gb))
        print('solutions',s.solve(list(gb),vs))
