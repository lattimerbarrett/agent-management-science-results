import itertools as it, pickle
from collections import defaultdict

def add(out,key,v):
 if not v:return
 out[key]=out.get(key,0)+v
 if not out[key]:del out[key]
def lin(fun,x):
 out={}
 for c,a in x.items():
  for t,b in fun(c).items():add(out,t,a*b)
 return out
class Model:
 def __init__(self,m):self.m=m;self.k=m-5
 def pivot(self,s):return next(j for j in range(self.m) if j not in dict(s))
 def vert(self,c):
  s,t=c;return {(s,t[:j]+t[j+1:]):(-1)**(len(s)+j) for j in range(len(t))}
 def delta(self,c):
  s,t=c;return {(s[:j]+s[j+1:],t):(-1)**j for j in range(len(s))}
 def d(self,c):
  out=self.vert(c)
  for z,a in self.delta(c).items():add(out,z,a)
  return out
 def h(self,c):
  s,t=c;p=self.pivot(s)
  if p in t or len(t)>=self.k:return {}
  return {(s,tuple(sorted(t+(p,)))):(-1)**(len(s)+sum(j<p for j in t))}
 def p(self,c):
  s,t=c;p=self.pivot(s)
  return {c:1} if len(t)==self.k and p not in t else {}
 def i(self,c):
  s,t=c;p=self.pivot(s);u=tuple(sorted(t+(p,)));ip=u.index(p)
  return {(s,u[:j]+u[j+1:]):(-1)**(j+ip) for j in range(len(u))}
 def dc(self,c):return lin(self.p,lin(self.delta,self.i(c)))
 def P(self,c):
  out={};x={c:1}
  while x:
   for z,a in lin(self.p,x).items():add(out,z,a)
   x={z:-a for z,a in lin(self.delta,lin(self.h,x)).items()}
  return out
 def H(self,c):
  out={};x={c:1}
  while x:
   for z,a in lin(self.h,x).items():add(out,z,a)
   x={z:-a for z,a in lin(self.delta,lin(self.h,x)).items()}
  return out
 def cells(self):
  for q in range(7):
   for S in it.combinations(range(self.m),q):
    U=tuple(j for j in range(self.m) if j not in S)
    for colors in it.product(range(3),repeat=q):
     if any(colors.count(a)>2 for a in range(3)):continue
     s=tuple(zip(S,colors))
     for r in range(min(self.k,len(U))+1):
      for t in it.combinations(U,r):yield s,t
 def critical(self):
  return [c for c in self.cells() if self.p(c)]

if __name__=='__main__':
 M=Model(7);crit=M.critical();print('critical',len(crit),flush=True)
 for c in crit:
  assert lin(M.d,M.i(c))==lin(M.i,M.dc(c)),('I chain',c)
  assert lin(M.P,M.i(c))=={c:1},('PI',c)
  assert not lin(M.dc,M.dc(c)),('dc2',c)
 print('I is a chain map, PI=1, dc^2=0 on every reduced basis element',flush=True)
 n=0
 for c in M.cells():
  assert lin(M.P,M.d(c))==lin(M.dc,M.P(c)),('P chain',c)
  lhs=lin(M.d,M.H(c))
  for z,a in lin(M.H,M.d(c)).items():add(lhs,z,a)
  rhs={c:1}
  for z,a in lin(M.i,M.P(c)).items():add(rhs,z,-a)
  assert lhs==rhs,('homotopy',c,lhs,rhs)
  n+=1
 print('P is a chain map and dH+Hd=1-IP on all',n,'original basis elements',flush=True)
 dims,old=pickle.load(open('mats7.pkl','rb'))
 cells=[[c for c in crit if len(c[0])==q] for q in range(5)]
 ids=[{c:j for j,c in enumerate(cs)} for cs in cells]
 for q in range(1,5):
  new=[{ids[q-1][z]:a for z,a in M.dc(c).items()} for c in cells[q]]
  print('degree',q,'old matches:',new==old[q-1],flush=True)
 pickle.dump((list(map(len,cells)),[[{ids[q-1][z]:a for z,a in M.dc(c).items()} for c in cells[q]] for q in range(1,5)]),open('verified7.pkl','wb'))
