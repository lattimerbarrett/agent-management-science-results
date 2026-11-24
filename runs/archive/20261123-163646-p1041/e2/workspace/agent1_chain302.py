import json,sys,itertools,pathlib,time,collections
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def basis(S,vs):
 B={};K=[]
 for i,p in enumerate(S):
  v=vs[p];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in B:B[k]=(v,c);break
   v^=B[k][0];c^=B[k][1]
  if not v:K.append(c)
 return B,K

def red(v,B):
 c=0;r=0
 while v:
  k=v.bit_length()-1
  if k not in B:r^=1<<k;v^=1<<k;continue
  v^=B[k][0];c^=B[k][1]
 return r,c

def ins(B,v):
 while v:
  k=v.bit_length()-1
  if k in B:v^=B[k]
  else:B[k]=v;return v
 return 0

def extras(S,m,K=None):
 if K is None:B,K=basis(S,veronese(m,5))
 B={}
 for j in range(-1,m):ins(B,sum(1<<i for i,p in enumerate(S) if j==-1 or p>>j&1))
 ex=[]
 for u in K:
  r=ins(B,u)
  if r:ex.append(r)
 L=[0]
 for u in ex:L +=[z^u for z in L]
 return L

def lift(S,m,P,B=None):
 vs=veronese(m,5)
 if B is None:B,K=basis(S,vs)
 z=0
 for p in P:z^=vs[p]
 r,c=red(z,B);assert not r
 H=P+[p for i,p in enumerate(S) if c>>i&1]
 return sorted(set(H)^set(p|(1<<m) for p in H)^set(p|(1<<m) for p in S))

D=json.load(open('workspace/agent4_T288_quadgraph_P16.json'));t0=time.time();seen12=set();hist=collections.Counter();ct4=0;ct2=0;hits=[];save=[]
for res in D['results']:
 for seed in res['seeds']:
  if seed['K5']!=14:continue
  S0=seed['support']
  for u in extras(S0,11)[1:]:
   S=[p|(((u>>i)&1)<<11) for i,p in enumerate(S0)];key=tuple(S)
   if key in seen12:continue
   seen12.add(key);X,r=closure(set(S),veronese(12,3));hist[len(X)]+=1
   if len(X)<4:continue
   B,K=basis(S,veronese(12,5));assert len(K)==13
   pp=[p for p,c in X];R=[red(veronese(12,5)[p],B) for p in pp];pairs={};P4=[];seen4=set()
   for i,j in itertools.combinations(range(len(pp)),2):
    v=R[i][0]^R[j][0]
    for k,l in pairs.get(v,[]):
     if len({i,j,k,l})<4:continue
     Q=tuple(sorted([pp[a] for a in [i,j,k,l]]))
     if Q not in seen4:seen4.add(Q);P4.append(Q)
    pairs.setdefault(v,[]).append((i,j))
   print('T28812',len(seen12),'cl3',len(X),'P4',len(P4),flush=True)
   for Q in P4:
    T=lift(S,12,list(Q),B);assert len(T)==296;ct4+=1;Y,r=closure(set(T),veronese(13,4))
    if len(Y)<2:continue
    B13,K13=basis(T,veronese(13,5));P13=[p for p,c in Y];RR=[red(veronese(13,5)[p],B13)[0] for p in P13]
    for i,j in itertools.combinations(range(len(P13)),2):
     if RR[i]!=RR[j]:continue
     G0=lift(T,13,[P13[i],P13[j]],B13);assert len(G0)==300;ct2+=1
     for label in extras(T,13,K13):
      G=set(G0)
      for ii,p in enumerate(T):
       if label>>ii&1:G.symmetric_difference_update([p,p|8192])
      G=sorted(G);C,r=closure(set(G),veronese(14,5));ans={'T288':S,'P4':Q,'T296':T,'P2':[P13[i],P13[j]],'support300':G,'K5_300':300-r,'cl5extra':len(C)};hits.append(ans)
      print('T300!',len(C),ans['K5_300'],time.time()-t0,flush=True)
      if C:ans['closure_witness']=[C[0][0],C[0][1]]
      json.dump(hits,open('workspace/agent1_chain302_hits.json','w'))
      if C:raise SystemExit('FOUND302')
print('DONE','S28812',len(seen12),'cl3hist',dict(hist),'P4lifts',ct4,'P2lifts',ct2,'time',time.time()-t0)
json.dump({'S28812':len(seen12),'cl3hist':dict(hist),'P4lifts':ct4,'P2lifts':ct2,'hits':hits},open('workspace/agent1_chain302_results.json','w'));pathlib.Path('workspace/agent1_chain302.py').write_text(pathlib.Path(__file__).read_text())
