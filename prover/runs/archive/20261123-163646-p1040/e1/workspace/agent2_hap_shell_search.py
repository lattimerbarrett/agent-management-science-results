"""Search alternate spherical face gluings; accepts only free identities."""
import json,random
from collections import defaultdict
from agent1_hap_spherical_identities import D,E,baseface,translate,cancel,labels,termsword,red,inv

faces=[baseface(f) for f in range(len(D['relators']))]
def cycred(p,t=None):
 k=0
 while 2*k<len(p) and p[k][3]==p[-k-1][3] and p[k][4]==-p[-k-1][4]:k+=1
 if not k:return (p,t) if t is not None else p
 v=inv(labels(p[:k]));p=p[k:len(p)-k]
 if t is None:return p
 return p,[(red(v+q),f,s) for q,f,s in t]

def solve(cell,seed=0):
 rng=random.Random(seed);pol=[]
 for f,i in D['boundaries']['3'][cell-1]:
  s=1 if f>0 else -1
  p,t=cycred(translate(faces[abs(f)-1],E[i-1],s),[((),abs(f)-1,s)])
  pol.append((p,t))
 rng.shuffle(pol)
 while len(pol)>1:
  lookup=defaultdict(list)
  for ia,(A,ta) in enumerate(pol):
   for a,ea in enumerate(A):lookup[ea[3],ea[4]].append((ia,a))
  best=None;score=-1;ties=0
  for (ID,sgn),occs in lookup.items():
   if sgn<0:continue
   for ia,a in occs:
    for ib,b in lookup.get((ID,-sgn),[]):
     if ia==ib:continue
     A,ta=pol[ia];B,tb=pol[ib];Br=B[b:]+B[:b]
     nn=cycred(cancel(A[:a]+Br[1:]+A[a+1:]))
     sc=len(A)+len(B)-len(nn)
     if sc>score:best=(ia,ib,a,b);score=sc;ties=1
     elif sc==score:
      ties+=1
      if rng.randrange(ties)==0:best=(ia,ib,a,b)
  if best is None:return None,[len(p) for p,t in pol]
  ia,ib,a,b=best;A,ta=pol[ia];B,tb=pol[ib]
  conj=red(labels(A[:a+1])+inv(labels(B[:b])))
  Br=B[b:]+B[:b];new=cancel(A[:a]+Br[1:]+A[a+1:])
  terms=[(red(conj+q),f,s) for q,f,s in tb]+ta
  new,terms=cycred(new,terms)
  for z in sorted((ia,ib),reverse=True):pol.pop(z)
  pol.append((new,terms))
 if not red(labels(pol[0][0])):
  assert not termsword(pol[0][1]);return pol[0][1],[]
 return None,[len(pol[0][0])]

def run(cells=range(8,13),tries=30):
 try:out=json.load(open('workspace/agent2_HAP_extra_free_identities.json'))
 except FileNotFoundError:out=[]
 known={x['cell'] for x in out}
 for c in cells:
  if c in known:continue
  for seed in range(tries):
   ans,lens=solve(c,seed)
   if ans is not None:
    print('VERIFIED cell',c,'seed',seed,'terms',len(ans),flush=True);out.append({'cell':c,'terms':ans});break
   print('cell',c,'try',seed,'remaining',lens,flush=True)
  json.dump(out,open('workspace/agent2_HAP_extra_free_identities.json','w'))
 return out
if __name__=='__main__':run()
