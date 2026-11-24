from itertools import combinations
from collections import defaultdict,deque
import random,json,time

def make(n,rng):
    T={(0,1,2)};E={tuple(e) for e in combinations(range(3),2)};m=3
    while True:
        missing=[(u,v) for u,v in combinations(range(m),2) if (u,v) not in E]
        available=[(u,v,[w for w in range(m) if w not in (u,v) and tuple(sorted((u,w))) in E and tuple(sorted((v,w))) in E]) for u,v in missing]
        available=[x for x in available if x[2]]
        if m<n and (not available or rng.random()<0.4):
            u,v=rng.choice(tuple(E));t=tuple(sorted((u,v,m)))
            T.add(t);E.add(tuple(sorted((u,m))));E.add(tuple(sorted((v,m))));m+=1
        elif available:
            u,v,ws=rng.choice(available);w=rng.choice(ws)
            T.add(tuple(sorted((u,v,w))));E.add((u,v))
        else:return T

def closure(T,n):
    T=set(T);count=defaultdict(int);queue=deque()
    def insert(t):
        for w in range(n):
            if w in t:continue
            f=tuple(sorted((*t,w)));count[f]+=1
            if count[f]==3:queue.append(f)
    for t in T:insert(t)
    while queue:
        f=queue.popleft()
        if count[f]!=3:continue
        new=next(t for t in combinations(f,3) if t not in T)
        T.add(new);insert(new)
    return T

def main():
    rng=random.Random(134643)
    for n,trials in [(10,1000),(20,100),(30,10)]:
      tm=time.time()
      for j in range(trials):
        T=make(n,rng);C=closure(T,n)
        if len(C)!=n*(n-1)*(n-2)//6:
            print('PROPER2SHELLABLECLOSURE n',n,'trial',j,'T',len(T),'C',len(C),flush=True)
            json.dump(sorted(T),open('workspace/agent4_2tree'+str(n)+'.json','w'))
            json.dump(sorted(C),open('workspace/agent4_2treeclosure'+str(n)+'.json','w'))
            return
      print('allcomplete',n,trials,'time',time.time()-tm,flush=True)
if __name__=='__main__':main()
