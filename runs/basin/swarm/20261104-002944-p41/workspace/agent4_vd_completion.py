"""Construct a vertex-decomposable completion on the original vertex set.
The routine assumes a positive-rank pure VD complex. All returned additions
are original-vertex facets and every prefix is certified directly.
"""
from itertools import combinations
from functools import reduce
import sys
sys.path.insert(0,'workspace')
from agent2_checker import certificate,verify,deletion,link,bits

def vertices(fs):return reduce(int.__or__,fs,0)
def vd_complete(fs,target=None):
    fs=tuple(sorted(fs));q=fs[0].bit_count()
    assert q>=1 and certificate(fs,0) is not None
    if target is None:target=vertices(fs)
    assert vertices(fs)&target==vertices(fs)
    order=[]
    # Any ghost target vertex enters through a simplex on an existing ridge.
    for w in bits(target^vertices(fs)):
        ridge=sum(bits(fs[0])[:q-1]);f=w|ridge
        order.append(f);fs=tuple(sorted((*fs,f)))
    if q==1 or len(fs)==1:return order
    c=certificate(fs,0);v=c[1];assert v.bit_count()==1
    de=deletion(fs,v)
    for f in vd_complete(de,target^v):
        order.append(f);fs=tuple(sorted((*fs,f)))
    li=link(fs,v)
    for h in vd_complete(li,target^v):
        f=v|h;order.append(f);fs=tuple(sorted((*fs,f)))
    assert set(fs)=={sum(c) for c in combinations(bits(target),q)}
    return order

def check(fs):
    order=vd_complete(fs);cur=tuple(sorted(fs));v=vertices(fs);q=fs[0].bit_count()
    for f in order:
        assert f not in cur
        cur=tuple(sorted((*cur,f)))
        c=certificate(cur,0);assert c is not None
        verify(cur,0,c)
    assert set(cur)=={sum(c) for c in combinations(bits(v),q)}
    return len(order)

def main():
    cases=steps=0
    for n in range(1,6):
      for q in range(1,n+1):
        allf=[sum(c) for c in combinations([1<<v for v in range(n)],q)]
        for mask in range(1,1<<len(allf)):
          fs=tuple(f for i,f in enumerate(allf) if mask>>i&1)
          if certificate(fs,0) is not None:
            steps+=check(fs);cases+=1
    print('VDcompletion exhaustive <=5ambientvertices:',cases,'inputs',steps,'certifiedprefixes')
if __name__=='__main__':main()
