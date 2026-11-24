import networkx as nx,itertools,json,time

def perfects(vs):
 if not vs:yield [];return
 x=vs[0]
 for j in range(1,len(vs)):
  y=vs[j]
  for rest in perfects(vs[1:j]+vs[j+1:]):yield [(x,y)]+rest

def matchings(G):
 E=list(G.edges())
 def rec(i,used,es):
  if i==len(E):yield es;return
  u,v=E[i]
  yield from rec(i+1,used,es)
  if not((1<<u|1<<v)&used):yield from rec(i+1,used|1<<u|1<<v,es+[(u,v)])
 yield from rec(0,0,[])

def states(R):
 n=len(R);out={};L=n-1
 for M in matchings(R):
  Q=R.copy();Q.remove_edges_from(M);path=[];cyc=[];bad=False;star=False
  for c in nx.connected_components(Q):
   T=Q.subgraph(c);ds=sorted(dict(T.degree()).values(),reverse=True);e=T.number_of_edges()
   if ds[0]<=2:
    if len(c)==e:cyc.append(e)
    else:path.append(e)
   elif len(c)==4 and ds==[3,1,1,1]:star=True
   else:bad=True;break
  if bad:continue
  if not star and not cyc:out['path']=M
  for ell in range(3,L):
   if all(p<=ell for p in path) and all(c==ell for c in cyc) and (not star or ell==3):out[str(ell)]=M
 return out
start=time.time()
for n in [8,10,12]:
 count=0;best=0;hist={}
 found=None
 for ports in itertools.combinations(range(n),2):
  vs=[v for v in range(n)if v not in ports]
  for chords in perfects(vs):
   if any((u-v)%n in [1,n-1] for u,v in chords):continue
   R=nx.cycle_graph(n);R.add_edges_from(chords);count+=1
   st=states(R);score=len(st)
   if score>best:best=score;print('n',n,'best',score,'count',count,'chords',chords,'states',sorted(st),flush=True)
   if 'path'in st and all(str(ell)in st for ell in range(3,n-1)):
    found=dict(n=n,ports=ports,chords=chords,states=st,edges=list(R.edges()));print('FOUND',found,flush=True);break
  if found:break
 print('n',n,'total',count,'best',best,'elapsed',time.time()-start,flush=True)
 if found:
  open('workspace/agent4_linegraph_path_found.json','w').write(json.dumps(found,indent=2));break
 if n==10:break
open('workspace/agent4_linegraph_path_search.py','w').write(open(__file__).read())
