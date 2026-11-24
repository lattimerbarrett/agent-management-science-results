from itertools import combinations
import random,time,json

def run(n,rng):
    T={frozenset((0,1,2))};E={frozenset(e) for e in combinations(range(3),2)};m=3;multi=0
    while True:
        available=[]
        for u,v in combinations(range(m),2):
            if frozenset((u,v)) in E:continue
            W={w for w in range(m) if w not in (u,v) and frozenset((u,w)) in E and frozenset((v,w)) in E}
            if W:available.append((u,v,W))
        if m<n and (not available or rng.random()<0.45):
            sample=rng.sample(tuple(E),min(20,len(E)))
            degree={v:sum(v in e for e in E) for v in range(m)}
            a,b=min(sample,key=lambda e:sum(degree[v] for v in e))
            T.add(frozenset((a,b,m)));E.add(frozenset((a,m)));E.add(frozenset((b,m)));m+=1
        elif available:
            choices=[]
            for u,v,W in rng.sample(available,min(25,len(available))):
                remaining=set(W);cc=[]
                while remaining:
                    comp={remaining.pop()};todo=list(comp)
                    while todo:
                        x=todo.pop()
                        yy={y for y in remaining if frozenset((u,x,y)) in T and frozenset((v,x,y)) in T}
                        remaining-=yy;comp|=yy;todo.extend(yy)
                    cc.append(comp)
                if len(cc)>1:multi+=1
                comp=min(cc,key=len)
                choices.append((len(W)-len(comp),-len(comp),rng.random(),u,v,comp))
            _,_,_,u,v,comp=max(choices)
            E.add(frozenset((u,v)))
            T.update(frozenset((u,v,w)) for w in comp)
        else:return T,multi

def main():
    rng=random.Random(183891)
    for n,reps in [(20,1000),(40,100)]:
        tm=time.time();mult=0
        for i in range(reps):
            T,mm=run(n,rng);mult+=mm
            if len(T)!=n*(n-1)*(n-2)//6:
                print('PROPER CLOSED SHELLABLE2',n,i,len(T),'components',mult,flush=True)
                json.dump([sorted(t) for t in T],open('workspace/agent4_2closed'+str(n)+'.json','w'))
                return
        print('allfull',n,reps,'multicomponentcount',mult,'time',time.time()-tm,flush=True)
if __name__=='__main__':main()
