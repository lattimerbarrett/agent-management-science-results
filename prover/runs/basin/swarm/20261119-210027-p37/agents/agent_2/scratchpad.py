src='''"""Executed exact upper certificate lambda(8)<=237758434088.

For a maximal intersecting family F on [8] with no singleton, let H be its
3-subsets. H is an intersecting triple family. Let f(H) count 4-sets containing
a member of H, and e(H) count pairs whose every triple superset is in H.
For fixed H there are 2**e(H) choices of pairs and 2**(35-f(H)) middle-level
choices. All other set memberships are forced by complementation/upwardness.
Thus lambda(8)=8+sum_H 2**(35-f(H)+e(H)).

The eligible pairs form an intersecting graph, hence a star or a triangle.
For e eligible star edges, H contains at least 21-C(7-e,2) triples; a triangle
requires 16 triples. Consequently for e=0,...,7 the necessary minimum h values
are 0,6,11,15,18,20,21,21. Replacing e(H) by the resulting emax(|H|) gives
a rigorous upper bound. No EKR theorem is needed.
"""
from itertools import combinations

def lambda8_upper():
    T=[sum(1<<x for x in a) for a in combinations(range(8),3)]
    Q=[sum(1<<x for x in a) for a in combinations(range(8),4)]
    intersect=[sum(1<<j for j,b in enumerate(T) if a&b) for a in T]
    shadow=[sum(1<<j for j,b in enumerate(Q) if a&b==a) for a in T]
    minima=[0,6,11,15,18,20,21,21]
    emax=[max(e for e,v in enumerate(minima) if v<=h) for h in range(57)]
    nodes=0
    def visit(candidates,forced,h):
        nonlocal nodes
        nodes+=1
        total=1<<(35-forced.bit_count()+emax[h])
        while candidates:
            bit=candidates&-candidates
            v=bit.bit_length()-1
            candidates-=bit
            total+=visit(candidates&intersect[v],forced|shadow[v],h+1)
        return total
    answer=8+visit((1<<56)-1,0,0)
    assert answer==237758434088 and nodes==32095507
    assert answer+1<618474403306
    return answer,nodes

if __name__=='__main__':print(lambda8_upper())
'''
open('workspace/agent2_lambda8_bound.py','w').write(src)
exec(compile(src,'workspace/agent2_lambda8_bound.py','exec'))
