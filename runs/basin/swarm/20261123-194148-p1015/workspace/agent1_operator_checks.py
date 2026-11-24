from itertools import combinations, product
from pathlib import Path
import json

def subsets(n):
    return list(range(1<<n))
def monotone_tables(n):
    dom=subsets(n)
    return [tuple(t) for t in product((0,1), repeat=1<<n)
            if all(not(t[a] and not t[b]) for a in dom for b in dom if a&b==a)]
def rules(t,n):
    return tuple(a for a in subsets(n) if t[a] and not any(t[b] for b in subsets(n) if b!=a and b&a==b))
def evaluate(rs,a):
    return int(any(f&a==f for f in rs))
counts={}
for n in range(1,4):
    ts=monotone_tables(n)
    rs=[rules(t,n) for t in ts]
    assert all(evaluate(r,a)==t[a] for t,r in zip(ts,rs) for a in subsets(n))
    # Negative universal evaluation: for any finite positive operator,
    # its output complement is the selected coordinate of U^-(A).
    for a in subsets(n):
        neg_u=tuple(1-t[a] for t in ts)
        for i,t in enumerate(ts):
            assert neg_u[i]==1-evaluate(rs[i],a)
    counts[n]={'monotone_predicates':len(ts),'canonical_rule_evaluations':len(ts)*(1<<n)}
# Composition of all two-input/two-output positive operators, checking
# a finite s-m-n construction: substitute each input singleton condition
# into the output rule and distribute finite conjunctions over disjunctions.
ts=monotone_tables(2)
ops=list(product(ts,repeat=2))
composition_cases=0
for inner in ops:
    for outer in ops:
        comp=[]
        for out in outer:
            out_rules=rules(out,2)
            new=[]
            for need in out_rules:
                choices=[rules(inner[j],2) for j in range(2) if need>>j&1]
                for picked in product(*choices):
                    union=0
                    for f in picked: union|=f
                    new.append(union)
            comp.append(new)
        for a in subsets(2):
            mid=sum(inner[j][a]<<j for j in range(2))
            for j in range(2):
                assert evaluate(comp[j],a)==outer[j][mid]
                # Complementing preserves a computable index translation.
                assert 1-evaluate(comp[j],a)==1-outer[j][mid]
                composition_cases+=1
report={'finite_universality':counts,'composition_output_cases':composition_cases,
        'meaning':'Finite exhaustive analogues of canonical positive rules, composition and uniform complement indexing; not substitutes for the infinitary proofs.'}
Path('workspace/agent1_operator_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent1_operator_checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
