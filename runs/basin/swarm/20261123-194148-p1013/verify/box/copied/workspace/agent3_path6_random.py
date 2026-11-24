import networkx as nx,z3,random,sys,json,time
from pathlib import Path
sys.path.insert(0,'workspace');from agent3_packing_host import packing_embedding
rng=random.Random(355);start=time.time();counts=[0,0,0]
for it in range(20000):
 q=rng.randint(2,5);na=3+3*q;n=na+rng.randint(6,15);ac=list(range(na));cols=[rng.randrange(2)for _ in range(n)];cols[1]=0;cols[2]=1
 # C4red vertex set, 0 and1 formadjacentrededge,2BLUE
 special=[0,1,na,3,4,na+1];red=set(special)|{u for u in range(3,n)if rng.random()<.63};rest=list(red-set(special));rng.shuffle(rest);order=special+rest;pos={u:(j//6,j%6)for j,u in enumerate(order)}
 cols[na]=1;cols[3]=0;cols[4]=1;cols[na+1]=0
 def ok3(u,v):
  return (u<na)!=(v<na) or (u<na and v<na and u//3==v//3)
 def ok4(u,v):
  if (u in red)!=(v in red):return True
  if u not in red:return False
  x,a=pos[u];y,b=pos[v];return x==y and (a-b)%6 in [1,5]
 H=nx.Graph();H.add_nodes_from(range(n));H.add_edges_from((u,v)for u in range(n)for v in range(u+1,n)if (u==0 or cols[u]!=cols[v])and ok3(u,v)and ok4(u,v));assert H.has_edge(0,1)and H.has_edge(0,2)and H.has_edge(1,2)
 counts[0]+=1
 if packing_embedding(H,nx.path_graph(5)) is not None:continue
 counts[1]+=1
 c5=packing_embedding(H,nx.cycle_graph(5));claw=packing_embedding(H,nx.star_graph(3));p6=packing_embedding(H,nx.path_graph(6))
 data={'n':n,'edges':list(H.edges()),'C3A':ac,'C4A':sorted(red),'bipcolors':cols,'claw':claw,'C5':c5,'P6':p6}
 if it%1000==0:print('P5FREE',it,'n',n,'C5',c5 is not None,'P6',p6 is not None,flush=True)
 c4=packing_embedding(H,nx.cycle_graph(4))
 if c4 is not None and c5 is not None and p6 is not None:
  data['C4']=c4;Path('workspace/agent3_PATH5_BASE.json').write_text(json.dumps(data,default=list));break
print('counts',counts,'sec',time.time()-start)

