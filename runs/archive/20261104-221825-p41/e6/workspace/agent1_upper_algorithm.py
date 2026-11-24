from itertools import combinations
from functools import reduce
from operator import or_
from agent2_decomp import witness, prefix_order, skeleton

def vertices(fs):
    return reduce(or_,fs,0)
def subsets_of_rank(vs,r):
    bits=[1<<i for i in range(vs.bit_length()) if vs>>i&1]
    return [sum(z) for z in combinations(bits,r)]
def missing_edge_path(fs,vs):
    edges=skeleton(fs,2)
    bits=subsets_of_rank(vs,1)
    for u,v,w in combinations(bits,3):
        for a,b,c in [(u,v,w),(u,w,v),(v,u,w)]:
            if a|b in edges and b|c in edges and a|c not in edges:
                return a|b|c
    return None

def completion(fs,k,buffers):
    # Input buffers are distinct single-bit fresh labels, exactly rank(fs)-3.
    fs=frozenset(fs)
    rank=next(iter(fs)).bit_count()
    assert rank>=3 and len(buffers)==rank-3
    vs=vertices(fs)
    assert not any(vs&a for a in buffers)
    out=[]
    def add(f):
        nonlocal fs
        assert f not in fs and f.bit_count()==rank
        fs=fs|{f}
        assert witness(fs,k) is not None
        out.append(f)
    if rank==3:
        while len(skeleton(fs,2))<len(subsets_of_rank(vs,2)):
            f=missing_edge_path(fs,vs)
            assert f is not None
            add(f)
        for f in subsets_of_rank(vs,3):
            if f not in fs:add(f)
    else:
        a,*rest=buffers
        L=skeleton(fs,rank-1)
        for g in prefix_order(L,k):add(a|g)
        for h in completion(L,k,rest):add(a|h)
        oldvs=vs|sum(rest)
        for f in subsets_of_rank(oldvs,rank):
            if f not in fs:add(f)
    assert fs==frozenset(subsets_of_rank(vs|sum(buffers),rank))
    return out

def check():
    instances=steps=0
    for n in range(3,6):
      for rank in range(3,n+1):
       allfs=subsets_of_rank((1<<n)-1,rank)
       for flags in range(1,1<<len(allfs)):
        fs=frozenset(f for j,f in enumerate(allfs) if flags>>j&1)
        for k in (1,2,3):
         if witness(fs,k) is None:continue
         v=vertices(fs).bit_length()
         additions=completion(fs,k,[1<<(v+i) for i in range(rank-3)])
         instances+=1;steps+=len(additions)
    return instances,steps

if __name__=='__main__':print(check())
