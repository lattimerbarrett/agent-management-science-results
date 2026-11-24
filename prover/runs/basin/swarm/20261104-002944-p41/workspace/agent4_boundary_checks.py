"""Independent finite checks of boundary filling and two-dimensional completion.
Run from repository root: import sys;sys.path.insert(0,'workspace');import agent4_boundary_checks
"""
from itertools import combinations
from functools import reduce
import sys
sys.path.insert(0,'workspace')
from agent2_checker import certificate, verify, bits, maximal

def boundary_present(fs,f):
    return all(any((f^v)&g==(f^v) for g in fs) for v in bits(f))

def complete2(fs):
    fs=tuple(sorted(fs)); vertex=reduce(int.__or__,fs,0)
    vertices=bits(vertex)
    target=[sum(c) for c in combinations(vertices,3)]
    order=[]
    while True:
        edges={sum(c) for f in fs for c in combinations(bits(f),2)}
        missing=[sum(c) for c in combinations(vertices,2) if sum(c) not in edges]
        if not missing:break
        chosen=None
        for uv in missing:
            u,v=bits(uv)
            for w in vertices:
                if w&uv==0 and u|w in edges and v|w in edges:
                    chosen=uv|w;break
            if chosen is not None:break
        assert chosen is not None, 'one-skeleton disconnected'
        fs=tuple(sorted((*fs,chosen)));order.append(chosen)
    for f in target:
        if f not in fs:
            fs=tuple(sorted((*fs,f)));order.append(f)
    return order

def run():
    count=0; boundary_checks=0; completion_checks=0
    for n in range(1,6):
      for q in range(1,n+1):
        target=[sum(c) for c in combinations([1<<i for i in range(n)],q)]
        for mask in range(1,1<<len(target)):
          fs=tuple(f for i,f in enumerate(target) if mask>>i&1)
          for k in range(q):
            c=certificate(fs,k)
            if c is None:continue
            verify(fs,k,c);count+=1
            for f in target:
              if f not in fs and boundary_present(fs,f):
                nex=tuple(sorted((*fs,f)))
                nc=certificate(nex,k)
                assert nc is not None,(fs,k,f)
                verify(nex,k,nc);boundary_checks+=1
            if q==3 and k>=1:
              cur=fs
              for f in complete2(fs):
                cur=tuple(sorted((*cur,f)))
                nc=certificate(cur,k)
                assert nc is not None,(fs,k,f)
                verify(cur,k,nc);completion_checks+=1
    print(dict(certified_complexes=count,boundary_fill_checks=boundary_checks,base2_prefix_checks=completion_checks))
if __name__=='__main__':run()
