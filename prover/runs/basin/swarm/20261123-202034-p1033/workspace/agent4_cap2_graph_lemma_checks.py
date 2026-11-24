import itertools,json,time
st=time.time();result=[]
for n in range(3,7):
 E=list(itertools.combinations(range(n),2));N=len(E);vm=[sum(1<<v for v in e) for e in E]
 disj=[sum(1<<j for j,m in enumerate(vm) if not m&vm[i]) for i in range(N)]
 avoid2=[sum(1<<j for j,m in enumerate(vm) if not m&sum(1<<v for v in C)) for C in itertools.combinations(range(n),2)]
 tau3=0;exceptions=[]
 for G in range(1<<N):
  if not all(G&a for a in avoid2):continue
  tau3+=1;left=G;comps=[]
  while left:
   b=left&-left;front=b;seen=0
   while front:
    x=front&-front;front-=x;i=x.bit_length()-1
    if seen&x:continue
    seen|=x;front|=(disj[i]&G&~seen)
   comps.append(seen);left&=~seen
  if len(comps)>1:
   edges=[e for i,e in enumerate(E) if G>>i&1];V=set().union(*map(set,edges))
   assert len(V)==4 and len(edges)==6 and len(comps)==3 and all(c.bit_count()==2 for c in comps)
   exceptions.append([list(e) for e in edges])
 assert len(exceptions)==len(list(itertools.combinations(range(n),4)))
 result.append(dict(n=n,graphs_total=1<<N,graphs_tau_at_least3=tau3,disconnected_KG=len(exceptions),all_disconnected_are_K4=True))
# Rigidity of cap1 on three colors, with arbitrary actual singleton represented by one external point.
rigid=[]
for out in itertools.product(range(3),repeat=3):
 if any(out[i]==i for i in range(3)):continue
 if not all(out[i]==j or out[j]==i for i,j in itertools.combinations(range(3),2)):continue
 allowed=[]
 for i in range(3):
  candidates=[(frozenset(),frozenset()),(frozenset({0}),frozenset())]+[(frozenset(),frozenset({j})) for j in range(3) if j!=i]
  ok=[]
  for P,T in candidates:
   if all((j in T or i==out[j]) for j in range(3) if j!=i):ok.append((sorted(P),sorted(T)))
  assert ok==[([], [out[i]])];allowed.append(ok)
 rigid.append(dict(out=out,compatible_patterns=allowed))
assert len(rigid)==2
out=dict(graph_classification=result,cap1_cycle_rigidity=rigid,seconds=time.time()-st)
json.dump(out,open('workspace/agent4_cap2_graph_lemma_checks.json','w'));open('workspace/agent4_cap2_graph_lemma_checks.py','w').write(open(__file__).read());print(json.dumps(out))
