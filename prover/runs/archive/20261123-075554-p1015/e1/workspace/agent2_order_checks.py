"""Finite exhaustive checks of order-theoretic lemmas used in skip arguments.
These certify finite identities, not infinite effective-existence theorems.
"""
from itertools import product

def subset(x,y):
    return (x & ~y)==0

def run_checks():
    n=3; universe=range(1<<n)
    comparable=[(x,y) for x in universe for y in universe if subset(x,y)]
    monotone_truth_tables=[]
    for table in range(1<<(1<<n)):
        if all(not ((table>>x)&1) or ((table>>y)&1) for x,y in comparable):
            monotone_truth_tables.append(table)
    assert len(monotone_truth_tables)==20
    checked=0
    for coordinates in product(monotone_truth_tables,repeat=n):
        # Complementing a monotone map produces an antitone map H.
        def H(x):
            return sum((1-((table>>x)&1))<<i for i,table in enumerate(coordinates))
        assert all(subset(H(y),H(x)) for x,y in comparable)
        fixed=[x for x in universe if H(x)==x]
        assert all(x==y or not subset(x,y) for x in fixed for y in fixed)
        checked+=1
    # Standard total codes contain exactly one token for each bit.
    for width in range(1,7):
        codes=[sum(1<<(2*i+((bits>>i)&1)) for i in range(width))
               for bits in range(1<<width)]
        assert all(x==y or not subset(x,y) for x in codes for y in codes)
    return {"antitone_maps_checked": checked,"monotone_boolean_tables":20,
            "total_code_widths_checked":6}

if __name__=='__main__':
    print(run_checks())
