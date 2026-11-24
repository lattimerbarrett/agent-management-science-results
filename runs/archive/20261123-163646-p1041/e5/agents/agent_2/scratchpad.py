import z3,math,itertools,time,pickle
sizes=[5,5,4];points=list(itertools.product(*(range(n+1) for n in sizes)));f={p:z3.Bool('f_'+'_'.join(map(str,p))) for p in points}
s=z3.Solver();s.set(timeout=60000)
for p in points:
 if sum(p)<=7:continue
 terms=[f[q] for q in points if all(a&b==a for a,b in zip(q,p))]
 v=terms[0]
 for t in terms[1:]:v=z3.Xor(v,t)
 s.add(z3.Not(v))
s.add(z3.Sum([z3.If(v,math.prod(math.comb(n,a) for n,a in zip(sizes,p)),0) for p,v in f.items()])==310)
print('begin',flush=True);start=time.time();ret=s.check();print(ret,time.time()-start)
if ret==z3.sat:
 md=s.model();supp=[p for p,v in f.items() if z3.is_true(md[v])];print(supp);pickle.dump((sizes,supp),open('workspace/agent2_310_symmetric.pkl','wb'))