import networkx as nx,z3,itertools,time,json,random
from pathlib import Path
Path('workspace/agent3_signed_cegar.py').write_text(Path(__file__).read_text())

def signed_map(H):
 n=len(H);ad=[sum(1<<w for w in H[u])for u in H];full=(1<<n)-1
 # sample promisingpartitions? exhaustivefallback
 for A in range(1<<(n-1)):
  comps=[];ok=True
  for M in [A,full^A]:
   unseen=M;C=[]
   while unseen:
    todo=unseen&-unseen;c=0
    while todo:
     bit=todo&-todo;todo^=bit;u=bit.bit_length()-1;c|=bit;unseen&=~bit;todo|=ad[u]&M&~c
    k=c.bit_count()
    if k==1:continue
    if k>3:ok=False;break
    vs=[u for u in H if c>>u&1];ds=[(ad[u]&c).bit_count()for u in vs]
    if sum(ds)>4:ok=False;break
    centers=vs if k==2 else [vs[ds.index(2)]];C.append((vs,centers))
    if len(C)>3:ok=False;break
   if not ok:break
   comps.append(C)
  if not ok:continue
  ca,cb=comps
  for la in itertools.permutations(range(3),len(ca)):
   for lb in itertools.permutations(range(3),len(cb)):
    for roots in itertools.product(*[C[1]for C in ca+cb]):
     ra=roots[:len(ca)];rb=roots[len(ca):]
     if any(H.has_edge(ra[i],rb[j])for i in range(len(ca))for j in range(len(cb))if la[i]==lb[j]):continue
     mp=[18 if A>>u&1 else 19 for u in H]
     for side,(cc,ll,rr)in enumerate([(ca,la,ra),(cb,lb,rb)]):
      for i,(vs,centers)in enumerate(cc):
       r=rr[i];mp[r]=9*side+3*ll[i]
       for j,u in enumerate(x for x in vs if x!=r):mp[u]=9*side+3*ll[i]+1+j
     return mp
 return None

def adjacent(a,b):
 pa=0 if a<9 or a==18 else 1;pb=0 if b<9 or b==18 else 1
 if pa!=pb:
  return not(a<18 and b<18 and a%3==b%3==0 and (a%9)//3==(b%9)//3)
 if a>=18 or b>=18:return False
 return a//3==b//3 and (a%3==0)!=(b%3==0)

Bsize=12;n=9+Bsize;col={1:0,2:1,3:0,4:1,5:1,6:1,7:0,8:0}
for j,y in enumerate(range(9,n)):col[y]=j%2
fixed=[(0,1),(0,2),(1,2),(3,4),(3,5),(6,7),(6,8)]+[(0,y)for y in [9,11,10,12,14,16]]
pool=[(x,y)for x in range(1,9)for y in range(9,n)if col[x]!=col[y]]
e={p:z3.Bool('e'+str(i))for i,p in enumerate(pool)};R=[z3.Bool('r'+str(i))for i in range(n)];edges=[(u,v,z3.BoolVal(True))for u,v in fixed]+[(u,v,e[u,v])for u,v in pool]
s=z3.Solver()
for u,v,b in edges:s.add(z3.Implies(b,z3.Or(R[u],R[v])))
for u,v in pool:s.add(z3.Implies(z3.Xor(R[u],R[v]),e[u,v]))
mono=[z3.And(b,R[u],R[v])for u,v,b in edges]
s.add(z3.PbEq([(a,1)for a in mono],4))
for u in range(n):s.add(z3.PbLe([(z3.And(b,R[x],R[y]),1)for x,y,b in edges if u in(x,y)],1))
start=time.time()
for it in range(10000):
 if s.check()==z3.unsat:print('UNSAT',n,it,time.time()-start);break
 m=s.model();E=fixed+[p for p in pool if z3.is_true(m.eval(e[p]))];H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from(E)
 mp=signed_map(H)
 if mp is None:
  data={'n':n,'edges':E,'matchingwitness':[u for u in range(n)if z3.is_true(m.eval(R[u]))]};print('COUNTER',it,data,flush=True);json.dump(data,open('workspace/agent3_signed_cegar_counter.json','w'));break
 missing=[e[p]for p in pool if not adjacent(mp[p[0]],mp[p[1]])]
 assert all(not z3.is_true(m.eval(x))for x in missing)
 s.add(z3.Or(missing))
 if it%10==0:print('it',it,'sec',time.time()-start,'block',len(missing),flush=True)
print('time',time.time()-start)