import itertools,json,os

def partitions(n,k):
 def rec(a,m):
  if len(a)==n:
   if m==k-1:yield a
   return
  for j in range(min(m+1,k-1)+1):yield from rec(a+[j],max(m,j))
 for a in rec([0],0):yield tuple(sum(1<<i for i,c in enumerate(a) if c==j) for j in range(k))

def tree_example(d=8,depth=4):
 full=(1<<d)-1
 pairs=[s for s in range(1<<d) if s.bit_count()==d//2 and s<(full^s)]
 colors=list(partitions(d,3)); paths=[]; leafcolors=[]
 def rec(i,V,path,dep):
  if dep==depth or i==len(pairs):
   paths.append(path);leafcolors.append(colors[V[0]]);return len(paths)-1
  s=pairs[i];t=full^s
  a=[j for j in V if all(s&b for b in colors[j])]
  b=[j for j in V if all(t&bb for bb in colors[j])]
  if not a or not b:return rec(i+1,V,path,dep)
  return (s,rec(i+1,a,path+[s],dep+1),rec(i+1,b,path+[t],dep+1))
 T=rec(0,list(range(len(colors))),[],0)
 def order(T,r):
  if isinstance(T,int):return [T]
  s,a,b=T
  return order(b,r)+order(a,r) if s>>r&1 else order(a,r)+order(b,r)
 orders=[order(T,r) for r in range(d)]
 ranks=[{x:i for i,x in enumerate(L)} for L in orders]
 c=[[next(j for j,b in enumerate(C) if b>>r&1) for r in range(d)] for C in leafcolors]
 N=len(paths)
 assert all(all(a&b for a in H for b in H) for H in paths)
 assert all(any(ranks[r][i]>ranks[r][j] and ranks[r][i]>ranks[r][k] for r in range(d)) for i,j,k in itertools.permutations(range(N),3))
 assert all(any(ranks[r][i]>ranks[r][j] and c[i][r]==h for r in range(d)) for i,j in itertools.permutations(range(N),2) for h in range(3))
 return ranks,c

def standard_example(t):
 X=list(range(2*t));R={(x,x) for x in X}|{(i,t+j) for i in range(t) for j in range(t) if i!=j}
 L=[]
 for i in range(t):
  oth=[j for j in range(t) if j!=i]
  L.append(oth+[i+t,i]+[j+t for j in oth])
 f=[{x:i for i,x in enumerate(O)} for O in L]
 assert all(((x,y) in R)==all(r[x]<=r[y] for r in f) for x in X for y in X)
 return X,R,f

def check_embedding(t,ranks,c):
 N=len(c);d=len(ranks);X,R,f=standard_example(t);B=len(X)+1
 Q=[a for k in [1,2] for a in itertools.combinations(range(N),k)]
 PX=list(itertools.product(X,Q));embedding={}
 for p,A in PX:
  coords=[]
  for r in range(d):
   v=max(A,key=lambda i:ranks[r][i])
   coords.append(B*ranks[r][v]+f[c[v][r]][p])
  coords += [ff[p] for ff in f[3:]]
  embedding[p,A]=coords
 for x in PX:
  ex=embedding[x]
  for y in PX:
   true=(x[0],y[0]) in R and set(x[1])<=set(y[1])
   assert true==all(a<=b for a,b in zip(ex,embedding[y])),(x,y,ex,embedding[y])
 return {'P_dimension':t,'Q_vertices':N,'product_elements':len(PX),'coordinates':d+t-3,'ordered_pairs_checked':len(PX)**2}

if __name__=='__main__':
 ranks,c=tree_example()
 results=[check_embedding(t,ranks,c) for t in [3,4]]
 os.makedirs('workspace',exist_ok=True)
 open('workspace/agent3_embedding_checks.py','w').write(open(__file__).read())
 json.dump(results,open('workspace/agent3_embedding_checks.json','w'),indent=2)
 print(json.dumps(results,indent=2))
