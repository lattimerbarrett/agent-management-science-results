import z3,itertools,time,json
Hedges=[(0,3),(0,4),(0,6),(0,7),(1,3),(1,5),(1,7),(2,5),(2,7),(3,7),(4,7),(6,7)]
M=1000

def f(n):return max(a*(n-a)+(2*a)//3 for a in range(n+1))

def search(k,seconds=120):
 start=time.time(); out=z3.Solver(); inn=z3.Solver(); inn.set(timeout=10000)
 vv={}
 def V(key):
  if key not in vv:vv[key]=z3.Bool('e_'+str(key))
  return vv[key]
 for side in range(2):
  for a,b in itertools.combinations(range(3),2):V(('b',side,a,b))
 for c in range(k):
  for role in range(6):V(('a',c,role))
 for c,d in itertools.combinations(range(k),2):V(('c',c,d))
 weight=z3.Sum([z3.If(v,1 if key[0]=='c' else M,0) for key,v in vv.items()])
 target=f(6*M+k)+1-9*M*M
 out.add(weight>=target)
 copies=4; size=3*copies; N=2*size+k
 X=[z3.Int('x'+str(i)) for i in range(8)]
 inn.add(z3.Distinct(X),*[z3.And(x>=0,x<N) for x in X])
 def edge(x,y):
  terms=[z3.And(x<size,y>=size,y<2*size),z3.And(y<size,x>=size,x<2*size)]
  for side in range(2):
   lo=side*size;hi=lo+size
   for a,b in itertools.combinations(range(3),2):
    terms.append(z3.And(x>=lo,x<hi,y>=lo,y<hi,(x-lo)/3==(y-lo)/3,z3.Or(z3.And((x-lo)%3==a,(y-lo)%3==b),z3.And((x-lo)%3==b,(y-lo)%3==a)),V(('b',side,a,b))))
  for c in range(k):
   for role in range(6):
    side=role//3;r=role%3;lo=side*size;hi=lo+size
    terms.append(z3.And(x==2*size+c,y>=lo,y<hi,(y-lo)%3==r,V(('a',c,role))))
    terms.append(z3.And(y==2*size+c,x>=lo,x<hi,(x-lo)%3==r,V(('a',c,role))))
  for c,d in itertools.combinations(range(k),2):
   terms.append(z3.And(z3.Or(z3.And(x==2*size+c,y==2*size+d),z3.And(y==2*size+c,x==2*size+d)),V(('c',c,d))))
  return z3.Or(terms)
 for u,v in Hedges:inn.add(edge(X[u],X[v]))
 def edgekey(u,v):
  if u>=2*size and v>=2*size:
   c,d=sorted((u-2*size,v-2*size));return ('c',c,d)
  if max(u,v)>=2*size:
   if u<v:u,v=v,u
   return ('a',u-2*size,(v//size)*3+(v%3))
  if u//size!=v//size:return None
  a,b=sorted((u%3,v%3));assert u//3==v//3 and a!=b
  return ('b',u//size,a,b)
 iterations=0
 while time.time()-start<seconds:
  status=out.check()
  if status!=z3.sat:
   print('k',k,'outer',status,'iterations',iterations,'time',round(time.time()-start,2),flush=True);return None
  model=out.model();assignment={key:z3.is_true(model.eval(var,model_completion=True)) for key,var in vv.items()}
  ans=inn.check(*[var if assignment[key] else z3.Not(var) for key,var in vv.items()])
  if ans==z3.unknown:
   print('k',k,'inner unknown',inn.reason_unknown(),flush=True);return None
  if ans==z3.unsat:
   print('FOUND k',k,'gain',model.eval(weight),'target',target,'iterations',iterations,flush=True)
   print([key for key,value in assignment.items() if value],flush=True)
   json.dump({'k':k,'present':[list(key) for key,value in assignment.items() if value]},open('h8_found.json','w'));return assignment
  im=inn.model();mapping=[im.eval(x).as_long() for x in X]
  keys={edgekey(mapping[u],mapping[v]) for u,v in Hedges};keys.discard(None)
  assert keys and all(assignment[key] for key in keys)
  out.add(z3.Or([z3.Not(vv[key]) for key in keys]))
  iterations+=1
  if iterations%100==0:print('k',k,'iteration',iterations,'time',round(time.time()-start,2),flush=True)
 print('k',k,'time limit','iterations',iterations,flush=True)
for k in [0,1,2,3,4,5,6]:
 if search(k,70) is not None:break
