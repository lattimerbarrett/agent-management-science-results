from itertools import combinations
from agent2_decomp import witness, skeleton, prefix_order

def masks(vertices, rank):
    return [sum(c) for c in combinations(vertices,rank)]

def complete_facets(fs,k,vertices,buffers):
    """Return a certified-by-theorem facet-addition ordering. Pure rank >=3, k>=1.
    vertices and buffers are lists of distinct bit masks, not vertex indices.
    All input vertices must occur in fs. Uses exactly rank(fs)-3 buffers.
    """
    r=next(iter(fs)).bit_count()
    assert len(buffers)==r-3 and r>=3 and k>=1
    current=set(fs); result=[]
    def add(f):
        assert f not in current
        current.add(f);result.append(f)
    if r==3:
        edges=set(skeleton(fs,2))
        while len(edges)<len(vertices)*(len(vertices)-1)//2:
            f=next((a|b|c for a,b in combinations(vertices,2) if a|b not in edges
                    for c in vertices if c not in (a,b) and a|c in edges and b|c in edges),None)
            assert f is not None,'input graph disconnected'
            add(f)
            edges.update(x for x in masks(vertices,2) if x&f==x)
        for f in masks(vertices,3):
            if f not in current:add(f)
    else:
        a=buffers[0]; rest=buffers[1:]
        L=skeleton(fs,r-1)
        for g in prefix_order(L,k):add(a|g)
        for h in complete_facets(L,k,vertices,rest):add(a|h)
        for f in masks(vertices+rest,r):
            if f not in current:add(f)
    final=set(masks(vertices+buffers,r))
    assert current==final
    return result
