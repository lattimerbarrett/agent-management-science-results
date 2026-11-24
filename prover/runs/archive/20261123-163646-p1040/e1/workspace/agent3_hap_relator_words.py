import sys,json,pickle,time
from pathlib import Path
sys.path.insert(0,'workspace')
from agent2_nielsen_actions import magnus
from degree2_certificate import compose,red

def build():
 ident,gs,gis,names=magnus(3)
 letters=[(i+1,g,gis[i]) for i,g in enumerate(gs)]+[(-i-1,gis[i],g) for i,g in enumerate(gs)]
 table={ident:((),ident)};frontier=[ident]
 for depth in range(1,5):
  new=[]
  for f in frontier:
   w,fi=table[f]
   for x,g,gi in letters:
    if w and w[-1]==-x:continue
    h=compose(f,g)
    if h not in table:table[h]=(w+(x,),compose(gi,fi));new.append(h)
  frontier=new;print('radius',depth,'size',len(table),flush=True)
 data=json.loads(Path('workspace/agent3_hap_aut_lifts.json').read_text());out=[]
 def evaluate(w):
  f=ident
  for x in w:f=compose(f,gs[x-1] if x>0 else gis[-x-1])
  return f
 for num,r in enumerate(data['relator_auts']):
  r=tuple(map(tuple,r));ans=table[r][0] if r in table else None
  if ans is None:
   for b,(bw,bi) in table.items():
    a=compose(r,bi)
    if a in table:ans=red(table[a][0]+bw);break
  if ans is not None:assert evaluate(ans)==r
  out.append(ans);print('relator',num+1,'Magnusword',ans,flush=True)
 data['magnus_relator_lifts']=out
 Path('workspace/agent3_hap_relator_words.json').write_text(json.dumps(data))
 return out
if __name__=='__main__':build()
