
import sympy as S
from functools import lru_cache
from itertools import product
x,y,T=S.symbols('x y T')
s=x+y;t=x*y
bases={1:[s],2:[s*s,t],3:[s**3,s*t],4:[s*s*t,t*t],5:[s*t*t],6:[t**3]}
@lru_cache(None)
def redmon(a,b):
    if a>=5:return {}
    if b<4:return {(a,b):1}
    out={}
    for i in range(1,5):
        for m,c in redmon(a+i,b-i).items():out[m]=out.get(m,0)-c
    return {m:c for m,c in out.items() if c}
def reduce(f):
    out={}
    for (a,b),c in S.Poly(S.expand(f),x,y).terms():
        for m,v in redmon(a,b).items():out[m]=out.get(m,0)+v*c
    return {m:S.expand(c) for m,c in out.items() if c!=0}
def comps(n):
    if n==0:yield ()
    for i in range(1,n+1):
        for c in comps(n-i):yield(i,)+c

def system(comp):
    variables=[]; fs=[]
    for i,m in enumerate(comp):
        f=(T+i*x)**m
        for j in range(1,min(m,6)+1):
            vv=S.symbols('c%d_%d_0:%d'%(i,j,len(bases[j])))
            variables.extend(vv)
            f+=sum(v*b for v,b in zip(vv,bases[j]))*(T+i*x)**(m-j)
        fs.append(f)
    pol=S.Poly(S.prod(fs).expand(),T)
    eqs=[]; cnums={}
    for (power,),coef in pol.terms():
        degree=sum(comp)-power
        rr=reduce(coef)
        if degree<=4:cnums[degree]=rr.pop((degree,0),0)
        eqs.extend(rr.values())
    eqs=list(dict.fromkeys(S.expand(e) for e in eqs if e!=0))
    return variables,eqs,cnums
if __name__=='__main__':
    import pickle,time,json,multiprocessing as mp
    def worker(comp,q):
        try:
            vs,es,cn=system(comp)
            g=S.groebner(es,*vs)
            q.put({'comp':comp,'variables':len(vs),'equations':len(es),'basis':[str(f) for f in g.polys],'unit':g.contains(S.Integer(1))})
        except Exception as e:q.put({'comp':comp,'error':repr(e)})
    results=[]
    for n in range(2,8):
        for comp in comps(n):
            if len(comp)<3 or comp>comp[::-1]:continue
            q=mp.Queue();p=mp.Process(target=worker,args=(comp,q));p.start();p.join(15)
            if p.is_alive():p.terminate();p.join();r={'comp':comp,'timeout':True}
            else:
                try:r=q.get(timeout=1)
                except:r={'comp':comp,'error':'empty queue'}
            results.append(r)
            print(r,flush=True)
            open('workspace/agent1_incidence_results.json','w').write(json.dumps(results,indent=2))
