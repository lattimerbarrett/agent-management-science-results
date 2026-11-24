from agent4_r2_counter import count,star,triangle
def brute(a,b,ta,tb):
 adj=[set() for _ in range(a+b)]
 for u in range(a):
  for v in range(a,a+b):adj[u].add(v);adj[v].add(u)
 for base,t in [(0,ta),(a,tb)]:
  if t[0]=='s':ed=[(base,base+j) for j in range(1,t[1]+1)]
  elif t[0]=='t':ed=[(base,base+1),(base+1,base+2),(base+2,base)]
  else:ed=[]
  for u,v in ed:adj[u].add(v);adj[v].add(u)
 ans=0
 for root in range(a+b):
  def dfs(path,used):
   nonlocal ans
   for v in adj[path[-1]]:
    if v==root:
     if len(path)>=3 and path[1]<path[-1]:ans+=1
    elif v>root and v not in used:dfs(path+[v],used|{v})
  dfs([root],{root})
 return ans
if __name__=='__main__':
 ct=0
 for a in range(1,7):
  for b in range(1,7):
   if a+b>9:continue
   for ta in [('n',0)]+[('s',d) for d in range(1,a)]+([('t',0)] if a>=3 else []):
    for tb in [('n',0)]+[('s',d) for d in range(1,b)]+([('t',0)] if b>=3 else []):
     def cp(t):return [] if t[0]=='n' else [star(t[1])] if t[0]=='s' else [triangle()]
     assert count(a,b,cp(ta),cp(tb))==brute(a,b,ta,tb),(a,b,ta,tb)
     ct+=1
 print('Independent brute DFS checks passed:',ct)
