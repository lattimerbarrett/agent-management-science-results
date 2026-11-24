import itertools, random, json, time
from pathlib import Path

def subsets(f):
    s=f
    while True:
        yield s
        if not s: return
        s=(s-1)&f

def trial(n,d,rng):
    facets=[sum(1<<i for i in c) for c in itertools.combinations(range(n),d+1)]
    ridges={f:tuple((1<<v,f^(1<<v)) for v in range(n) if f>>v&1) for f in facets}
    faces={0}; order=[]; remain=set(facets)
    f=rng.choice(facets)
    faces.update(subsets(f)); order.append(f);remain.remove(f)
    while remain:
        possible=[]
        for f in remain:
            R=sum(v for v,g in ridges[f] if g in faces)
            if R and R not in faces: possible.append(f)
        if not possible:
            # Independently verify every missing facet's intersection has
            # a maximal common face of non-ridge size.
            for f in remain:
                common=[s for s in subsets(f) if s in faces]
                maximal=[s for s in common if not any(s!=g and s&g==s for g in common)]
                assert any(s.bit_count()!=d for s in maximal)
            return order,sorted(remain)
        f=rng.choice(possible)
        faces.update(subsets(f)); order.append(f);remain.remove(f)
    return None

def main():
    rng=random.Random(2718281828)
    start=time.time();report=[]
    for n,count in [(7,10000),(8,10000),(9,5000),(10,2000),(11,1000)]:
        for i in range(count):
            result=trial(n,3,rng)
            if result:
                out={'n':n,'d':3,'order':result[0],'missing':result[1]}
                Path('workspace/agent2_blocked_shelling.json').write_text(json.dumps(out))
                print('BLOCKED',out);return
        report.append((n,count));print('completed',n,count,flush=True)
    print('No blocked shellings',report,'seconds',time.time()-start)
if __name__=='__main__':
    Path('workspace/agent2_random_shellings.py').write_text(Path(__file__).read_text())
    main()
