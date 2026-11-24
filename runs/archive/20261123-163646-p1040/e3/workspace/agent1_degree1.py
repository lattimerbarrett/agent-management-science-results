import sys,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_tensor import *

def ia_generators(n):
    """Magnus generators (name, changed input, its output word)."""
    for i in range(1,n+1):
        for j in range(1,n+1):
            if i != j: yield ('K',i,j), i, (j,i,-j)
        for j in range(1,n+1):
            for k in range(j+1,n+1):
                if i not in (j,k):
                    yield ('C',i,j,k),i,(i,j,k,-j,-k)

def check_degree_one(n):
    basis={(i,j,k) for i in range(1,n+1) for j in range(1,n+1) for k in range(j+1,n+1)}
    seen=set()
    for name,i,w in ia_generators(n):
        displacement=homogeneous(magnus(w+(-i,),2),2)
        positive=[(word,c) for word,c in displacement.items() if word[0]<word[1]]
        assert len(positive)==1
        (j,k),c=positive[0]
        assert abs(c)==1 and displacement=={(j,k):c,(k,j):-c}
        key=(i,j,k)
        assert key in basis and key not in seen
        seen.add(key)
    assert seen==basis
    return {'n':n,'rank':len(basis),'signed_permutation_verified':True}

