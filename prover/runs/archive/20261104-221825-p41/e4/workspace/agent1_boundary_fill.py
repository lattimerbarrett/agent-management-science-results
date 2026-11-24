"""Construct a k-decomposition after filling one entire present facet boundary."""
from agent3_checker import subsets,deletion_link,certificate,verify

def fill_certificate(facets,k,cert,F):
    facets=tuple(sorted(facets))
    rank=facets[0].bit_count()
    assert F.bit_count()==rank and F not in facets
    # Every codimension-one face of F must already be in the complex.
    assert all(any(g&f==g for f in facets) for g in subsets(F,rank-1))
    if cert[0]=='simplex':
        assert rank==1
        return ('shed',F,cert,('simplex',0))
    _,s,dc,lc=cert
    de,li=deletion_link(facets,s)
    if F&s==s:
        return ('shed',s,dc,fill_certificate(li,k,lc,F^s))
    return ('shed',s,fill_certificate(de,k,dc,F),lc)

def test(nmax=5):
    from itertools import combinations
    count=0
    for n in range(1,nmax+1):
      for rank in range(1,n+1):
        universe=tuple(subsets((1<<n)-1,rank))
        for mask in range(1,1<<len(universe)):
          fs=tuple(sorted(f for i,f in enumerate(universe) if mask>>i&1))
          for k in sorted(set([0,1,rank-1])):
            cert=certificate(fs,k)
            if cert is None:continue
            for F in universe:
              if F in fs:continue
              if not all(any(g&f==g for f in fs) for g in subsets(F,rank-1)):continue
              new=fill_certificate(fs,k,cert,F)
              verify(tuple(sorted(fs+(F,))),k,new)
              count+=1
    return count
if __name__=='__main__':print('Directly constructed and independently verified full-boundary fills:',test())
