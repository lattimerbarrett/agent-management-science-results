import z3,networkx as nx,itertools,time,json
n=14;cut=7
E={(u,v):z3.Bool(f'e{u}_{v}') for u in range(n) for v in range(u+1,n)}
def ez(u,v):return E[tuple(sorted((u,v)))]
def onepart_required(kind,prefix,s):
 q=8 if kind=='matching' else 9
 rr=[z3.Int(prefix+str(i)) for i in range(n)]
 for r in rr:s.add(r>=0,r<=q+1)
 def allowed(a,b):
  cross=z3.Or(z3.And(a==q+1,b!=q+1),z3.And(b==q+1,a!=q+1))
  d=2 if kind=='matching' else 3
  inside=z3.Or(*[z3.And(a==u,b==v) for u in range(q) for v in range(q) if u!=v and u//d==v//d])
  return z3.Or(cross,inside)
 for (u,v),e in E.items():
  s.add(z3.Or(rr[u]!=rr[v],rr[u]>=q));s.add(z3.Implies(e,allowed(rr[u],rr[v])))
 return rr

def signed_allow(a,b):
 aa=z3.Or(a<9,a==18);ab=z3.Or(b<9,b==18)
 cross=z3.Xor(aa,ab)
 holes=z3.And(a<18,b<18,a%3==1,b%3==1,a%9/3==b%9/3)
 inside=z3.And(a<18,b<18,a/9==b/9,a/3==b/3,z3.Or(a-b==1,b-a==1))
 return z3.Or(z3.And(cross,z3.Not(holes)),inside)
def signed_embedding(H):
 q=z3.Solver();q.set(timeout=15000);rr=[z3.Int('r'+str(i)) for i in range(n)]
 for r in rr:q.add(r>=0,r<20)
 for u,v in itertools.combinations(range(n),2):q.add(z3.Or(rr[u]!=rr[v],rr[u]>=18))
 for u,v in H.edges():q.add(signed_allow(rr[u],rr[v]))
 st=q.check()
 if st==z3.unknown:raise RuntimeError('oracle timeout')
 return None if st==z3.unsat else [q.model().eval(r).as_long() for r in rr]
def pyallowed(a,b):
 aa=(a<9 or a==18);ab=(b<9 or b==18)
 if aa!=ab:return not(a<18 and b<18 and a%3==b%3==1 and (a%9)//3==(b%9)//3)
 return a<18 and b<18 and a//9==b//9 and a//3==b//3 and abs(a-b)==1
s=z3.Solver();s.set(timeout=120000)
L=list(range(1,cut));R=list(range(cut,n))
for side in [L,R]:
 for u,v in itertools.combinations(side,2):s.add(z3.Not(ez(u,v)))
 for u,v in zip(side,side[1:]):
  s.add(z3.Implies(ez(0,v),ez(0,u)))
  if u!=side[0]:s.add(z3.Implies(ez(0,u)==ez(0,v),z3.Sum([z3.If(ez(u,w),1,0) for w in (R if side==L else L)])>=z3.Sum([z3.If(ez(v,w),1,0) for w in (R if side==L else L)])))
s.add(ez(0,1),ez(0,cut),ez(1,cut));s.add(z3.AtMost(*[ez(0,v) for v in L],3))
mvars=onepart_required('matching','m',s);tvars=onepart_required('triangles','t',s)
open('workspace/agent4_signed_cegar.py','w').write(open(__file__).read())
start=time.time()
for it in range(2000):
 st=s.check()
 if st!=z3.sat:print('SYNTHESIS',st,'iteration',it);break
 model=s.model();H=nx.Graph();H.add_nodes_from(range(n))
 mr=[model.eval(v).as_long() for v in mvars];tr=[model.eval(v).as_long() for v in tvars]
 def pyone(a,b,q,d):return (a==q+1)!=(b==q+1) or (a<q and b<q and a!=b and a//d==b//d)
 for u,v in E:
  if u and v and ((u<cut)==(v<cut)):continue
  if not(pyone(mr[u],mr[v],8,2) and pyone(tr[u],tr[v],9,3)):continue
  if u==0 and v<cut and not z3.is_true(model.eval(ez(u,v),model_completion=True)):continue
  H.add_edge(u,v)
 for v in L:
  if sum(H.has_edge(0,w) for w in L)>=3:break
  if pyone(mr[0],mr[v],8,2) and pyone(tr[0],tr[v],9,3):H.add_edge(0,v)
 wit=signed_embedding(H)
 if wit is None:
  print('FOUND',list(H.edges()));open('workspace/agent4_signed_cegar_found.json','w').write(json.dumps(list(H.edges())));break
 s.add(z3.Or(*[e for (u,v),e in E.items() if not pyallowed(wit[u],wit[v])]))
 if it%20==0:print(it,len(H.edges()),round(time.time()-start,2),flush=True)
else:print('iteration limit')
print('elapsed',time.time()-start)
