import sys,itertools,random,time
from pathlib import Path
sys.path.insert(0,'workspace')
from agent2_structural_checks import kd_order, subfaces,skel

def vertices(fs):
    out=0
    for f in fs: out|=f
    return [i for i in range(out.bit_length()) if out>>i&1]
def allfacets(vs,size):
    return [sum(1<<i for i in c) for c in itertools.combinations(vs,size)]
def completion(fs,d,k,new):
    fs=tuple(sorted(fs));vs=vertices(fs)
    assert len(new)==max(0,d-2)
    if d==2:
        current=set(fs); faces=set().union(*(set(subfaces(f)) for f in fs));order=[]
        # Every connected noncomplete graph has an induced 2-edge path.
        while True:
            found=False
            for t in allfacets(vs,3):
                es=[s for s in subfaces(t) if s.bit_count()==2]
                old=[e for e in es if e in faces]
                if len(old)==2:
                    assert t not in current
                    current.add(t);order.append(t);faces.update(subfaces(t));found=True;break
            if not found:break
        assert all(e in faces for e in allfacets(vs,2))
        order += [t for t in allfacets(vs,3) if t not in current]
        return order
    a=new[0];b=new[1:];ab=1<<a
    link=skel(fs,d)
    initial=kd_order(link,k)
    assert initial is not None
    order=[ab|g for g in initial]
    order.extend(ab|g for g in completion(link,d-1,k,b))
    current=set(fs)|set(order)
    # Full a-star is now present; all non-a facets can be arbitrary.
    order.extend(f for f in allfacets(vs+b,d+1) if f not in current)
    return order

def verify(fs,d,k,new):
    current=set(fs);assert kd_order(tuple(sorted(current)),k) is not None
    order=completion(fs,d,k,new)
    for f in order:
        assert f not in current
        assert f.bit_count()==d+1
        current.add(f)
        assert kd_order(tuple(sorted(current)),k) is not None,(fs,d,k,new,f)
    assert current==set(allfacets(vertices(fs)+new,d+1))
    return len(order)

def main():
    start=time.time();runs=steps=0
    # Exhaustive base on 5 labels and exhaustive d=3 on 5 labels.
    for n,d,k in [(5,2,1),(5,3,1)]:
        fac=allfacets(list(range(n)),d+1)
        for state in range(1,1<<len(fac)):
            fs=tuple(sorted(f for i,f in enumerate(fac) if state>>i&1))
            if kd_order(fs,k) is None:continue
            steps+=verify(fs,d,k,list(range(n,n+d-2)));runs+=1
    # Higher-dimensional random test cases; exact verification throughout.
    rng=random.Random(314159)
    for n,d,count in [(6,3,150),(6,4,50),(7,4,30)]:
        fac=allfacets(list(range(n)),d+1)
        for _ in range(count):
            fs=tuple(sorted(rng.sample(fac,rng.randrange(1,len(fac)+1))))
            if kd_order(fs,1) is None:continue
            steps+=verify(fs,d,1,list(range(n,n+d-2)));runs+=1
    print({'initial_complexes':runs,'exact_intermediate_checks':steps,'seconds':time.time()-start})
if __name__=='__main__':
    Path('workspace/agent2_upper_completion.py').write_text(Path(__file__).read_text())
    main()
