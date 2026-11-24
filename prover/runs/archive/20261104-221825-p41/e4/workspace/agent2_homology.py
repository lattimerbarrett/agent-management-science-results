"""Exact GF(2) reduced homology and Cohen-Macaulay necessary checks."""
from agent3_checker import subsets

def binary_rank(columns):
    pivots={}
    for x in columns:
        while x:
            p=x.bit_length()-1
            if p not in pivots:
                pivots[p]=x;break
            x^=pivots[p]
    return len(pivots)

def reduced_betti(facets):
    facets=tuple(facets)
    assert facets and len({f.bit_count() for f in facets})==1
    rank=facets[0].bit_count()
    faces=[sorted({s for f in facets for s in subsets(f,j)})
           for j in range(rank+1)]
    boundary=[0]*(rank+2)
    for j in range(1,rank+1):
        idx={x:i for i,x in enumerate(faces[j-1])}
        columns=[]
        for face in faces[j]:
            col=0
            for v in subsets(face,1):col^=1<<idx[face^v]
            columns.append(col)
        boundary[j]=binary_rank(columns)
    return {j-1:len(faces[j])-boundary[j]-boundary[j+1]
            for j in range(rank+1)}

def cm_obstruction(facets):
    """None iff pure input is CM over GF2; else return bad link/betti."""
    facets=tuple(facets)
    assert facets and len({f.bit_count() for f in facets})==1
    rank=facets[0].bit_count()
    faces=sorted({s for f in facets for s in subsets(f)},
                 key=lambda s:(s.bit_count(),s))
    for s in faces:
        link=tuple(sorted({f^s for f in facets if f&s==s}))
        betti=reduced_betti(link)
        for j in range(-1,rank-s.bit_count()-1):
            if betti[j]:return s,j,betti[j]
    return None
