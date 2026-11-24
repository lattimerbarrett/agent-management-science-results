import pickle,sympy as S,time
from itertools import product
from pathlib import Path
D=pickle.load(open('workspace/agent3_ch232_general.pkl','rb'));vs=D['vars']
eq=[S.Poly(f,*vs).clear_denoms()[1] for f in D['equations']]
target=S.Poly(vs[0]*(vs[0]+vs[3]),*vs)

def mons(n,d):
    if n==1:
        for a in range(d+1): yield (a,)
    else:
        for a in range(d+1):
            for rest in mons(n-1,d-a): yield (a,)+rest

def mac(deg,p=32003,track=False):
    basis={};rows=[]
    terms=[f.terms() for f in eq]
    for i,f in enumerate(eq):
      for mm in mons(5,deg-f.total_degree()):rows.append((i,mm))
    print('degree',deg,'rows',len(rows),flush=True)
    def subtract(a,b,fac):
        for m,c in b.items():
            val=(a.get(m,0)-fac*c)%p
            if val:a[m]=val
            elif m in a:del a[m]
    for idx,(i,mm) in enumerate(rows):
        row={tuple(a+b for a,b in zip(m,mm)):int(c)%p for m,c in terms[i]}
        rep={idx:1} if track else {}
        while row:
            lead=max(row,key=lambda m:(sum(m),m))
            val=row[lead]
            if lead not in basis:
                inv=pow(val,-1,p)
                row={m:c*inv%p for m,c in row.items()}
                if track:rep={j:c*inv%p for j,c in rep.items()}
                basis[lead]=(row,rep);break
            old,oldrep=basis[lead]
            subtract(row,old,val)
            if track:subtract(rep,oldrep,val)
    row={m:int(c)%p for m,c in target.terms()};rep={}
    while row:
        lead=max(row,key=lambda m:(sum(m),m))
        if lead not in basis:break
        val=row[lead];old,oldrep=basis[lead]
        subtract(row,old,val)
        if track:subtract(rep,oldrep,-val)
    print('rank',len(basis),'target remainder terms',len(row),flush=True)
    return row,rep,rows

if __name__=='__main__':
  Path('workspace/agent3_macaulay232.py').write_text(Path(__file__).read_text())
  p=2**61-1
  t=time.time();rem,rep,rows=mac(10,p=p,track=True)
  print('time',time.time()-t,'representation entries',len(rep),flush=True)
  pickle.dump((p,rem,rep,rows),open('workspace/agent3_mac232_rep.pkl','wb'))
  import math
  def reconstruct(a,p):
    bound=math.isqrt(p//2);r0,r1=p,a;t0,t1=0,1
    while abs(r1)>bound:
      q=r0//r1;r0,r1=r1,r0-q*r1;t0,t1=t1,t0-q*t1
    if t1==0 or abs(t1)>bound or math.gcd(r1,t1)!=1:return None
    rr=S.Rational(r1,t1)
    if (int(rr.p)-a*int(rr.q))%p:return None
    return rr
  rr={i:reconstruct(c,p) for i,c in rep.items()}
  print('reconstruction failures',sum(v is None for v in rr.values()),flush=True)
  if all(v is not None for v in rr.values()):
    out={}
    for idx,c in rr.items():
      i,mm=rows[idx]
      for mon,co in eq[i].terms():
        key=tuple(a+b for a,b in zip(mm,mon));out[key]=out.get(key,0)+c*co
    for mon,co in target.terms():out[mon]=out.get(mon,0)-co
    out={m:S.cancel(c) for m,c in out.items() if c!=0}
    print('exact remainder terms',len(out),flush=True)
    if not out:
      pickle.dump((rr,rows),open('workspace/agent3_mac232_exact.pkl','wb'))
      print('EXACT CERTIFICATE VERIFIED',flush=True)
