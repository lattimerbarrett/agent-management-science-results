"""Finite verification of enumeration-operator composition and quantifier duality."""
from itertools import product
from pathlib import Path
import json

def monotone_tables(n):
    masks=range(1<<n)
    for bits in product((0,1),repeat=1<<n):
        if all(not bits[a] or bits[b] for a in masks for b in masks if a&b==a):
            yield tuple(bits)

def apply(rules,B):
    return sum(1<<x for x,row in enumerate(rules) if any(F&B==F for F in row))

def compose(left,right,n):
    out=[set() for _ in range(n)]
    for x in range(n):
        for F in left[x]:
            parts=[right[y] for y in range(n) if F>>y&1]
            for selections in product(*parts):
                U=0
                for support in selections: U|=support
                out[x].add(U)
    return tuple(tuple(sorted(row)) for row in out)

def main():
    totals={}
    for n in (1,2):
        tables=list(monotone_tables(n))
        ops=[tuple(tuple(i for i,b in enumerate(t) if b) for t in rows)
             for rows in product(tables,repeat=n)]
        monotone_count=composition_count=0
        for op in ops:
            for B in range(1<<n):
                for C in range(1<<n):
                    if B&C==B:
                        assert apply(op,B)&apply(op,C)==apply(op,B)
                        monotone_count+=1
        for left in ops:
            for right in ops:
                comp=compose(left,right,n)
                for B in range(1<<n):
                    assert apply(comp,B)==apply(left,apply(right,B))
                    composition_count+=1
        totals[n]={'operators':len(ops),'monotonicity_checks':monotone_count,
                   'composition_checks':composition_count}
    checks=0
    for n in range(1,4):
        for bits in product((False,True),repeat=n*n):
            forall_exists=all(any(bits[x*n+y] for y in range(n)) for x in range(n))
            exists_forall_neg=any(all(not bits[x*n+y] for y in range(n)) for x in range(n))
            assert forall_exists == (not exists_forall_neg)
            checks+=1
    report={'finite_operator_checks':totals,'quantifier_duality_checks':checks,
            'scope':'Finite tests validate formulas only, not infinite theorem.'}
    print(json.dumps(report,indent=2))
    Path('workspace/agent4_finite_checks.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__': main()

