"""Extract explicit free-group identities among SL3 relators from HAP3cells.
Every emitted identity is checked by literal free-word reduction.
"""
import json
from functools import lru_cache
from agent1_degree3 import red,inv

D=json.load(open('workspace/agent1_HAP_SL3Z_presentation_3cells_simple.json'))
E=[tuple(x for r in g for x in r) for g in D['matrix_elts']]
def mm(a,b):return tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3)) for i in range(3) for j in range(3))
def endpoints(e,m):
 b=D['boundaries']['1'][e-1]
 n=next(E[i-1] for s,i in b if s<0);p=next(E[i-1] for s,i in b if s>0)
 return mm(m,n),mm(m,p)

def baseface(f):
 edges=[]
 for e,i in D['boundaries']['2'][f]:
  m=E[i-1];u,v=endpoints(abs(e),m)
  if e<0:u,v=v,u
  edges.append((u,v,e,(abs(e),m),1 if e>0 else -1))
 r=D['relators'][f]
 def dfs(out,unused):
  if not unused:return out if out[-1][1]==out[0][0] else None
  label=r[len(out)]
  for j in unused:
   ee=edges[j]
   if ee[0]==out[-1][1] and ee[2]==label:
    z=dfs(out+[ee],unused-{j})
    if z:return z
  return None
 for j,ee in enumerate(edges):
  if ee[2]==r[0]:
   z=dfs([ee],set(range(len(edges)))-{j})
   if z:return z
 raise ValueError(('no attaching polygon',f,r))

def cancel(poly):
 out=[]
 for ee in poly:
  if out and out[-1][3]==ee[3] and out[-1][4]==-ee[4]:out.pop()
  else:out.append(ee)
 # Do not cyclicallycancel acrossbasepoint; linearcancellationenough.
 return out

def labels(poly):return tuple(e[2] for e in poly)
def translate(poly,g,sgn):
 out=[]
 for u,v,e,(idx,m),s in poly:out.append((mm(g,u),mm(g,v),e,(idx,mm(g,m)),s))
 if sgn<0:out=[(v,u,-e,ID,-s) for u,v,e,ID,s in out[::-1]]
 return out

def termsword(terms):
 out=()
 for q,f,s in terms:
  r=tuple(D['relators'][f]);r=r if s>0 else inv(r)
  out=red(out+q+r+inv(q))
 return out

def main():
 faces=[baseface(f) for f in range(len(D['relators']))]
 allident=[]
 for cell,b3 in enumerate(D['boundaries']['3']):
  pol=[]
  for f,i in b3:
   sign=1 if f>0 else -1
   pol.append((translate(faces[abs(f)-1],E[i-1],sign),[((),abs(f)-1,sign)]))
  while len(pol)>1:
   found=None
   for ia in range(len(pol)):
    for ib in range(ia+1,len(pol)):
     A,ta=pol[ia];B,tb=pol[ib]
     for a,ea in enumerate(A):
      for b,eb in enumerate(B):
       if ea[3]==eb[3] and ea[4]==-eb[4]:found=(ia,ib,a,b);break
      if found:break
     if found:break
    if found:break
   if found is None:break
   ia,ib,a,b=found;A,ta=pol[ia];B,tb=pol[ib]
   S=labels(A[:a+1]);Q=labels(B[:b]);conj=red(S+inv(Q))
   Brot=B[b:]+B[:b];new=cancel(A[:a]+Brot[1:]+A[a+1:])
   assert red(conj+labels(B)+inv(conj)+labels(A))==red(labels(new))
   terms=[(red(conj+q),f,s) for q,f,s in tb]+ta
   assert termsword(terms)==red(labels(new))
   for i in sorted((ia,ib),reverse=True):pol.pop(i)
   pol.append((new,terms))
  if len(pol)==1 and not red(labels(pol[0][0])):
   terms=pol[0][1];assert not termsword(terms)
   allident.append({'cell':cell+1,'terms':terms})
   print('VERIFIED FREE IDENTITY cell',cell+1,'terms',len(terms),flush=True)
  else:print('cell',cell+1,'not reduced toidentity; remainingpolygons',len(pol),'lengths',[len(p) for p,t in pol],flush=True)
 json.dump(allident,open('workspace/agent1_HAP_SL3Z_free_identities.json','w'))
 return allident
if __name__=='__main__':main()
