from sage.all import *
import time,pickle,os
start=time.time()
for n in range(6,11):
 key=f'int4_{n}.pkl'
 if os.path.exists(key):gs=pickle.load(open(key,'rb'))
 else:
  gs=[G.graph6_string() for G in graphs(n,degree_sequence=[2,2]+[4]*(n-2))]
  pickle.dump(gs,open(key,'wb'))
 best=(-1,None,None)
 for st in gs:
  G=Graph(st)
  if not G.is_connected():continue
  u,v=[i for i in G if G.degree(i)==2]
  ns=[i for i in G if i!=v]
  Q=G.kirchhoff_matrix(vertices=ns+[v])[:-1,:-1]
  rhs=vector(QQ,[int(i==u) for i in ns]);sol=Q.solve_right(rhs)
  r=sol[ns.index(u)]
  if r>best[0]:best=(r,st,(u,v))
 print(n,'count',len(gs),'best',best,'time',time.time()-start,flush=True)
 if best[1]:print('edges',Graph(best[1]).edges(labels=False),flush=True)
