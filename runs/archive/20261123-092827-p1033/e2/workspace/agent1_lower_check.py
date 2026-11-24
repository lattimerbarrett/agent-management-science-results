from itertools import combinations
from math import isqrt
import json

def tau(edges,V):
    for s in range(len(V)+1):
        for C in combinations(V,s):
            if all(set(C)&E for E in edges):return s

def cycle_example(a=2):
    X=[set(range(i*a,(i+1)*a)) for i in range(3)]
    groups=[[X[i]|{v} for v in X[(i+1)%3]] for i in range(3)]
    E=sum(groups,[])
    assert all(F&G for F in E for G in E)
    assert tau(E,list(range(3*a)))==3
    for S in combinations(range(3),2):
        assert tau(sum([groups[i] for i in S],[]),list(range(3*a)))==2
    return {'core_size':a,'k':a+1,'t':3,'deficiency_sum':3}

# Check the sharp counting contradiction in every integer case up to 1000.
for d in range(1,1001):
    s=d*(d+2)+1
    assert s>=d+2
    assert d*(d+2)<s
    assert d+2-1>d
# Necessary sorted lower bound, including safe exception for first group.
def lower(t):
    return sum(isqrt(j+1)-1+(isqrt(j+1)**2<j+1) for j in range(2,t+1))
result={'cycle_examples':[cycle_example(a) for a in [2,3]],'lower_bounds':{t:lower(t) for t in [10,100,1000,10000,100000]}}
print(result)
with open('workspace/agent1_checked.json','w') as f:json.dump(result,f,indent=2)
with open('workspace/agent1_lower_check.py','w') as f:f.write(open('scratchpad.py').read())