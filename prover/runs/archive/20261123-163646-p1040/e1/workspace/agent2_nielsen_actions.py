"""Exact free-group checks of Magnus-generator expressions for Aut conjugation."""
import sys,json
from pathlib import Path
from degree2_certificate import compose,inv,red
from degree1_certificate import generators

def magnus(n):
 ident=tuple((i+1,) for i in range(n));gs=[];gis=[];names=[]
 for name,i,w in generators(n):
  g=list(ident);g[i]=w;gs.append(tuple(g));names.append(name)
  if name[0]=='K':
   j=name[2];wi=(-j-1,i+1,j+1)
  else:
   j,k=name[2:];wi=(i+1,k+1,j+1,-k-1,-j-1)
  gi=list(ident);gi[i]=wi;gis.append(tuple(gi))
  assert compose(g,gi)==ident and compose(gi,g)==ident
 return ident,gs,gis,names

def expressions(n=3,radius=4):
 ident,gs,gis,names=magnus(n);m=len(gs)
 letters=[(i+1,g,gis[i]) for i,g in enumerate(gs)]+[(-i-1,gis[i],g) for i,g in enumerate(gs)]
 table={ident:((),ident)};frontier=[ident]
 for depth in range(1,radius+1):
  new=[]
  for f in frontier:
   w,fi=table[f]
   for x,g,gi in letters:
    if w and w[-1]==-x:continue
    h=compose(f,g)
    if h in table:continue
    table[h]=(w+(x,),compose(gi,fi));new.append(h)
  frontier=new;print('radius',depth,'size',len(table),flush=True)
 # Standard elementary transvection, swap, inversion, cycle.
 acts=[]
 t=list(ident);ti=list(ident);t[0]=(1,2);ti[0]=(1,-2)
 acts.append(('T',tuple(t),tuple(ti)))
 t=list(ident);t[0],t[1]=t[1],t[0];acts.append(('P',tuple(t),tuple(t)))
 t=list(ident);t[0]=(-1,);acts.append(('I',tuple(t),tuple(t)))
 cyc=tuple(((i+1)%n+1,) for i in range(n));cyci=tuple(((i-1)%n+1,) for i in range(n))
 acts.append(('C',cyc,cyci))
 result={}
 def evaluate(w):
  f=ident
  for x in w:f=compose(f,gs[x-1] if x>0 else gis[-x-1])
  return f
 for name,t,ti in acts:
  assert compose(t,ti)==ident and compose(ti,t)==ident
  words=[]
  for k,g in enumerate(gs):
   target=compose(t,compose(g,ti));answer=None
   if target in table:answer=table[target][0]
   else:
    for b,(bw,bi) in table.items():
     a=compose(target,bi)
     if a in table:
      answer=red(table[a][0]+bw);break
   if answer is None:raise ValueError(('not found',name,k))
   assert evaluate(answer)==target
   words.append(answer)
   print('action',name,'generator',k+1,'word',answer,flush=True)
  result[name]={'auto':t,'inverse':ti,'words':words}
 data={'n':n,'generators':gs,'inverses':gis,'names':names,'actions':result}
 Path('workspace/agent2_nielsen_actions_n%d.json'%n).write_text(json.dumps(data))
 print('All conjugation words checked exactly',flush=True)
 return data
if __name__=='__main__':expressions(int(sys.argv[1]) if len(sys.argv)>1 else 3)
