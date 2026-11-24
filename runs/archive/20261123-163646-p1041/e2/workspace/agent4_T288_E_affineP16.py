import sys,json,time
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure
s=Path('workspace/agent1_boundary272_relatives.py').read_text();exec(s[:s.index('raw=json.load')])
raw=json.loads(Path('workspace/agent4_boundary256_orbits.json').read_text());results=[];st=time.time()
for ob in raw:
 if not ob['solvable']:continue
 S=sorted({(p&63)|((p>>3)&64) for p in ob['support']});SS=set(S);cl,_=closure(SS,veronese(7,2));extra={p for p,c in cl};assert len(extra)==16
 S256=sorted(p|(r<<7) for p in S for r in range(8));v10=veronese(10,5);B256=basis([v10[p] for p in S256]);v11=veronese(11,5)
 rr={'type':ob['type'],'counts':{}};khist={}
 for d in range(1,5):
  vs=veronese(7,d+1);B=basis([vs[p] for p in S]);total=valid=outside=0
  for Q in flats(7,d):
   total+=1
   if SS.intersection(Q):continue
   z=0
   for p in Q:z^=vs[p]
   if red(z,B)[0]:continue
   valid+=1
   if not set(Q)<=extra:
    outside+=1;P=[p|(r<<7) for p in Q for r in range(1<<(4-d))];assert len(P)==16
    zz=0
    for p in P:zz^=v10[p]
    rem,co=red(zz,B256);assert rem==0
    H=P+[p for j,p in enumerate(S256) if co>>j&1]
    F=sorted(set(H)^set(p|1024 for p in H)^set(p|1024 for p in S256));assert len(F)==288
    kk=288-len(basis([v11[p] for p in F]));af=len(basis([(p^F[0]) for p in F]));assert af<=11
    assert af<=10 or kk==12
    khist[af,kk]=khist.get((af,kk),0)+1
  rr['outside_K5_affinerank_hist']={str(k):v for k,v in khist.items()}
  rr['counts'][d]={'total':total,'valid':valid,'not_contained_cl2':outside}
  print(ob['type'],d,rr['counts'][d],'seconds',time.time()-st,flush=True)
 results.append(rr)
Path('workspace/agent4_T288_E_affineP16.json').write_text(json.dumps({'results':results,'seconds':time.time()-st}))
