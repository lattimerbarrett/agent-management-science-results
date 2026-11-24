from itertools import combinations
import z3,time,json
from math import comb

def search(n,seconds=180):
    fs=list(combinations(range(n),4));N=len(fs)
    R={f:z3.Int('R'+str(f)) for f in fs}
    s=z3.Solver();s.set(timeout=1000*seconds)
    for f in fs:s.add(R[f]>=0,R[f]<=N)
    for f,g in combinations(fs,2):s.add(z3.Or(R[f]==N,R[g]==N,R[f]!=R[g]))
    H={}
    for q in [1,2,3]:
      for h in combinations(range(n),q):
        hset=set(h);rr=[R[f] for f in fs if hset<=set(f)]
        hh=z3.Int('H'+str(h));H[h]=hh
        s.add(hh>=0,hh<=N,z3.Or([hh==r for r in rr]))
        s.add([hh<=r for r in rr])
        if q==1:s.add(hh<N)
    s.add(R[(0,1,2,3)]==0,R[(0,1,2,4)]==1,R[(0,1,3,5)]==2)
    for v in range(4,n-1):s.add(H[(v,)]<H[(v+1,)])
    s.add(z3.Or([R[f]==N for f in fs]))
    for f in fs:
        rs=list(combinations(f,3))
        # Exact shelling of the selected facets.
        s.add(z3.Implies(R[f]<N,z3.Or(R[f]==0,*[H[r]<R[f] for r in rs])))
        for q in [1,2]:
          for h in combinations(f,q):
            covers=[H[r]<R[f] for r in rs if set(h)<=set(r)]
            s.add(z3.Implies(z3.And(R[f]<N,H[h]<R[f]),z3.Or(covers)))
        # If missing, at least one existing vertex/edge must be uncovered by boundary triangles.
        bad=[]
        for q in [1,2]:
          for h in combinations(f,q):
            cov=[H[r]<N for r in rs if set(h)<=set(r)]
            bad.append(z3.And(H[h]<N,z3.Not(z3.Or(cov))))
        s.add(z3.Or(R[f]<N,*bad))
    p=z3.Int('Pfacets');s.add(p==z3.Sum([z3.If(R[f]<N,1,0) for f in fs]))
    for f in fs:s.add(z3.Implies(R[f]<N,R[f]<p))
    def count(hs):return z3.Sum([z3.If(H[h]<N,1,0) for h in hs])
    ee=count(list(combinations(range(n),2)))
    tt=count(list(combinations(range(n),3)))
    h2=z3.Int('h2');h3=z3.Int('h3');h4=z3.Int('h4')
    s.add(h2==ee-3*n+6,h3==tt-2*ee+3*n-4,h4==p-tt+ee-n+1)
    s.add(h2>=0,h3>=0,h4>=0,h2<=comb(n-3,2))
    def mac(m,d):
        left=m;top=m+d;ans=0
        for j in range(d,0,-1):
            k=j-1
            while k+1<top and comb(k+1,j)<=left:k+=1
            if k>=j:
                left-=comb(k,j);ans+=comb(k+1,j+1)
            top=k
        assert left==0
        return ans
    maxh2=comb(n-3,2);maxh3=mac(maxh2,2)
    for m in range(maxh2+1):s.add(z3.Implies(h2==m,h3<=mac(m,2)))
    for m in range(maxh3+1):s.add(z3.Implies(h3==m,h4<=mac(m,3)))
    oldridge={f:z3.Sum([z3.If(H[r]<R[f],1,0) for r in combinations(f,3)]) for f in fs}
    for i,hh in [(1,n-4),(2,h2),(3,h3),(4,h4)]:
        s.add(hh==z3.Sum([z3.If(z3.And(R[f]<N,oldridge[f]==i),1,0) for f in fs]))
    for v in range(n):
        ev=count([e for e in combinations(range(n),2) if v in e])
        tv=count([t for t in combinations(range(n),3) if v in t])
        cv=z3.Sum([z3.If(R[f]<N,1,0) for f in fs if v in f])
        a=tv-2*ev+3;b=cv-tv+ev-1
        s.add(a>=0,b>=0)
        for m in range(3,n):s.add(z3.Implies(ev==m,a<=comb(m-2,2)))
        for m in range(maxh2+1):s.add(z3.Implies(a==m,b<=mac(m,2)))
    for e in combinations(range(n),2):
        te=count([t for t in combinations(range(n),3) if set(e)<=set(t)])
        ce=z3.Sum([z3.If(R[f]<N,1,0) for f in fs if set(e)<=set(f)])
        s.add(z3.Implies(H[e]<N,ce>=te-1))
    tm=time.time();ans=s.check();print('GENERAL n',n,ans,'seconds',time.time()-tm,flush=True)
    if ans==z3.sat:
        m=s.model();fac=sorted([f for f in fs if m.eval(R[f]).as_long()<N],key=lambda f:m.eval(R[f]).as_long())
        print(fac,flush=True)
        json.dump(fac,open('workspace/agent3_third0135trap'+str(n)+'.json','w'))
        # Independently check shelling and inadmissibility of EVERY missing facet.
        faces=set();selected=set()
        for f in fac:
            ff=set(f);old=[g for g in faces if set(g)<=ff]
            ridges=[g for g in old if len(g)==3]
            if selected:assert ridges and all(any(set(g)<=set(r) for r in ridges) for g in old)
            selected.add(f)
            faces.update(g for q in range(5) for g in combinations(f,q))
        for f in set(fs)-selected:
            old=[g for g in faces if set(g)<=set(f)];rr=[g for g in old if len(g)==3]
            assert not rr or any(not any(set(g)<=set(r) for r in rr) for g in old)
        print('INDEPENDENTLY VERIFIED shelling and all blockedmissingfacets',flush=True)
    return ans

if __name__=="__main__":
 search(9,600)
