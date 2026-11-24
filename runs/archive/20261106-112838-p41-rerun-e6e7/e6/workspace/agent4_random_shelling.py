from itertools import combinations
from pathlib import Path
import random,time,json

def setup(n,d):
    fs=[sum(1<<i for i in c) for c in combinations(range(n),d+1)]
    small=[sum(1<<i for i in c) for sz in range(d+1) for c in combinations(range(n),sz)]
    ids={f:i for i,f in enumerate(small)}
    proper=[]; rb=[]; unions=[]
    for f in fs:
        sub=[g for g in small if g&f==g]
        proper.append(sum(1<<ids[g] for g in sub))
        ridges=[f^(1<<i) for i in range(n) if f>>i&1]
        rb.append([1<<ids[g] for g in ridges])
        masks=[sum(1<<ids[g] for g in sub if g&r==g) for r in ridges]
        unions.append([__import__('functools').reduce(int.__or__,[masks[j] for j in range(d+1) if p>>j&1],0) for p in range(1<<(d+1))])
    return fs,proper,rb,unions

def trial(data,rng,mode):
    fs,p,rb,u=data
    first=rng.randrange(len(fs)); present=p[first]; order=[first]
    todo=set(range(len(fs)));todo.remove(first)
    while todo:
        cand=[]
        for j in todo:
            pattern=sum(1<<i for i,x in enumerate(rb[j]) if present&x)
            if pattern and (present&p[j])==u[j][pattern]:
                cand.append((j,pattern.bit_count()))
        if not cand:return order
        if mode==0:j=rng.choice(cand)[0]
        else:
            score=(min if mode==1 else max)(s for j,s in cand)
            j=rng.choice([j for j,s in cand if s==score])
        order.append(j);todo.remove(j);present|=p[j]
    return order

if __name__=='__main__':
    Path('workspace/agent4_random_shelling.py').write_text(Path(__file__).read_text())
    rng=random.Random(741947);start=time.time();results=[]
    for n,trials in [(7,3000),(8,2000),(9,1000),(10,500),(11,200),(12,100)]:
        data=setup(n,3); best=len(data[0]);bad=None
        for t in range(trials):
            order=trial(data,rng,t%3)
            if len(order)<best:
                best=len(order);bad=[data[0][j] for j in order];break
        results.append((n,t+1,best,len(data[0])))
        print(results[-1], 'seconds',round(time.time()-start,2),flush=True)
        if bad:
            Path('workspace/agent4_shelling_witness.json').write_text(json.dumps({'n':n,'facets':bad}));break
    Path('workspace/agent4_random_results.json').write_text(json.dumps(results))
