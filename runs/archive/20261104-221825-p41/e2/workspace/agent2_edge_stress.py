import itertools,random
from agent4_checker import dec

def run(sizes=(3,3,2,2),trials=1000,seed=281):
    random.seed(seed)
    parts=[];n=0
    for s in sizes:
        parts.append(list(range(n,n+s)));n+=s
    initial={sum(1<<v for v in c) for c in itertools.product(*parts)}
    tests=0
    for trial in range(trials):
        D=set(initial)
        while True:
            triangles={f^(1<<i) for f in D for i in range(n) if f>>i&1}
            oldedges={sum(1<<v for v in c) for f in D for c in itertools.combinations([i for i in range(n) if f>>i&1],2)}
            options=[]
            for u,v in itertools.combinations(range(n),2):
                sigma=(1<<u)|(1<<v)
                if sigma in oldedges:continue
                common=[(x,y) for x,y in itertools.combinations([i for i in range(n) if i not in (u,v)],2) if ((1<<u)|(1<<x)|(1<<y)) in triangles and ((1<<v)|(1<<x)|(1<<y)) in triangles]
                if common:options.append((sigma,common))
            if not options:break
            sigma,edges=random.choice(options)
            e=random.choice(edges);chosen=[e];verts=set(e)
            for j in range(random.randrange(len(edges)+1)):
                available=[e for e in edges if e not in chosen and set(e)&verts]
                if not available:break
                e=random.choice(available);chosen.append(e);verts.update(e)
            # sigma was absent, its two boundary stars are covered by D,
            # and chosen is a connected graph; hence sigma is an exact
            # edge-decomposition witness for the enlarged complex.
            D.update(sigma|sum(1<<v for v in e) for e in chosen)
            sk=tuple(sorted({f^(1<<i) for f in D for i in range(n) if f>>i&1}))
            assert dec(sk,0),(n,tuple(sorted(D)))
            tests+=1
    return tests

if __name__=='__main__':
    for sizes in [(2,2,2,2),(3,3,2,2),(3,3,3,3)]:
        print(sizes,run(sizes),flush=True)
