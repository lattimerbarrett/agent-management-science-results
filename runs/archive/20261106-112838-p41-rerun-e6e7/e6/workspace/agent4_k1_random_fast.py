import sys,time,json,random
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_fastdec import dec
from agent4_random_shelling import setup
rng=random.Random(481952)
start=time.time()
Path('workspace/agent4_k1_random_fast.py').write_text(Path(__file__).read_text())
for n,trials in [(8,100),(9,100),(10,50),(11,20)]:
    data=setup(n,3);fs,p,rb,u=data
    for t in range(trials):
        dec.cache_clear()
        j=rng.randrange(len(fs));current={j};present=p[j];todo=set(range(len(fs)))-current
        order=[fs[j]];failedchecks=0
        while todo:
            cand=[]
            for j in todo:
                pattern=sum(1<<i for i,x in enumerate(rb[j]) if present&x)
                if pattern and (present&p[j])==u[j][pattern]:cand.append(j)
            rng.shuffle(cand)
            valid=None
            for j in cand:
                fac=tuple(sorted([fs[h] for h in current]+[fs[j]]))
                if dec(fac,1):valid=j;break
                failedchecks+=1
            if valid is None:
                print('FOUND',n,t,len(current),failedchecks,flush=True)
                Path('workspace/agent4_k1_obstruction.json').write_text(json.dumps({'n':n,'d':3,'k':1,'facets':order}));raise SystemExit
            j=valid;current.add(j);todo.remove(j);order.append(fs[j]);present|=p[j]
        if t%10==0:print(n,t,'failedchecks',failedchecks,'seconds',time.time()-start,'cache',dec.cache_info().currsize,flush=True)
    print('COMPLETE',n,trials,flush=True)
