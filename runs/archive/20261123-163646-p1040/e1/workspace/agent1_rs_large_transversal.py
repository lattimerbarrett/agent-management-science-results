"""Finite exact Reidemeister-Schreier chunks; no completeness claim."""
import json,pickle
from pathlib import Path
from degree2_certificate import compose,inv,red
from agent2_nielsen_actions import magnus

def mat(f):return tuple(sum((1 if x==i+1 else -1 if x==-i-1 else 0) for x in f[j]) for i in range(3) for j in range(3))
def mm(a,b):return tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3)) for i in range(3) for j in range(3))

def run(radius=4,mitm=3,start_radius=2,verbose=False):
 ar=json.load(open('workspace/agent3_AutF3_presentation.json'))
 A=[tuple(map(tuple,f)) for f in ar['aut_images']];AI=[tuple(map(tuple,f)) for f in ar['inverse_images']]
 ident,gs,gis,names=magnus(3);mi=mat(ident)
 letters=[(i+1,g,AI[i],mat(g)) for i,g in enumerate(A)]+[(-i-1,AI[i],g,mat(AI[i])) for i,g in enumerate(A)]
 # Short GL transversal, with exact Aut lifts and inverse lifts.
 trans={mi:((),ident,ident)};front=[mi]
 for depth in range(1,radius+1):
  new=[]
  for M in front:
   w,f,fi=trans[M]
   for x,g,gi,Mg in letters:
    Q=mm(M,Mg)
    if Q in trans:continue
    trans[Q]=(w+(x,),compose(f,g),compose(gi,fi));new.append(Q)
  front=new;print('GLball',depth,len(trans),flush=True)
 # Magnus radius4 table.
 ll=[(i+1,g,gis[i]) for i,g in enumerate(gs)]+[(-i-1,gis[i],g) for i,g in enumerate(gs)]
 tab={ident:((),ident)};front=[ident];short=[]
 for depth in range(1,5):
  new=[]
  for f in front:
   w,fi=tab[f]
   for x,g,gi in ll:
    if w and w[-1]==-x:continue
    h=compose(f,g)
    if h in tab:continue
    tab[h]=(w+(x,),compose(gi,fi));new.append(h)
  front=new
  if depth<=mitm:short+=new
 print('IA radius4',len(tab),'complements',len(short),flush=True)
 cp=Path('workspace/agent1_rs_edgecache.pkl')
 cache=pickle.loads(cp.read_bytes()) if cp.exists() else {}
 fail=set();relations=[]
 starts=[M for M,(w,f,fi) in trans.items() if len(w)<=start_radius]
 def express(f):
  if f in cache:return cache[f]
  if f in fail:return None
  if f in tab:cache[f]=tab[f][0];return cache[f]
  for b in short:
   bw,bi=tab[b];a=compose(f,bi)
   if a in tab:
    cache[f]=red(tab[a][0]+bw);return cache[f]
  fail.add(f);return None
 def ev(w):
  f=ident
  for x in w:f=compose(f,gs[x-1] if x>0 else gis[-x-1])
  return f
 def al(x):return A[x-1] if x>0 else AI[-x-1]
 def ali(x):return AI[x-1] if x>0 else A[-x-1]
 # Build missing transversal vertices consistently from actual loop prefixes.
 loops=[tuple(reversed(r)) for r in ar['relators']]
 paths=[(start,ri,r) for start in starts for ri,r in enumerate(loops)]
 for start,ri,r in paths:
  w,f,fi=trans[start];M=start
  for x in r:
   M=mm(M,mat(al(x)));f=compose(f,al(x));fi=compose(ali(x),fi);w=w+(x,)
   if M not in trans:trans[M]=(w,f,fi)
  assert f==trans[start][1] and M==start
 for loopnum,(start,ri,r) in enumerate(paths):
  M=start;out=();okay=True
  for pos,x in enumerate(r):
   Q=mm(M,mat(al(x)));f=compose(trans[M][1],compose(al(x),trans[Q][2]))
   assert mat(f)==mi
   w=express(f)
   if w is None:
    
    if verbose:print('loop',loopnum,'edge',pos,'FAIL autlength',sum(map(len,f)),flush=True)
    okay=False;break
   out=red(out+w);M=Q
  if okay:
   assert ev(out)==ident
   if out:
    relations.append(out)
    
    if verbose:print('loop',loopnum,'SUCCESS IAwordlength',len(out),flush=True)
 Path('workspace/agent1_rs_relator_words.json').write_text(json.dumps(relations))
 cp.write_bytes(pickle.dumps(cache))
 print('Saved',len(relations),'exact RS identities; cache',len(cache),'fails',len(fail),flush=True)
 return relations
if __name__=='__main__':run()
