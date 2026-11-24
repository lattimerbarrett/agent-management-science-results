from itertools import combinations, product
import json, os

def check_system(cores, groups, k, target):
    cores=list(map(frozenset,cores)); groups=[[frozenset(f) for f in g] for g in groups]
    assert len(cores)==len(groups)==target
    assert all(cores) and all(groups)
    assert all(not a&b for a,b in combinations(cores,2))
    flat=[f for g in groups for f in g]
    assert len(set(flat))==len(flat)
    assert all(len(f)==k for f in flat)
    assert all(x<=f for x,g in zip(cores,groups) for f in g)
    assert all(a&b for a,b in combinations(flat,2))
    vertices=set().union(*flat)
    forbidden=0
    for C in combinations(vertices,target-1):
        C=set(C)
        assert any(not C&f for f in flat), ('small cover',C)
        forbidden+=1
    assert all(any(x&f for x in cores) for f in flat)
    return {'k':k,'t':target,'edges':len(flat),'vertices':len(vertices),'tested_small_covers':forbidden,'total_deficit':sum(k-len(x) for x in cores)}

def cycle3(k):
    cores=[{(i,j) for j in range(k-1)} for i in range(3)]
    groups=[[cores[i]|{v} for v in cores[(i+1)%3]] for i in range(3)]
    return check_system(cores,groups,k,3)

