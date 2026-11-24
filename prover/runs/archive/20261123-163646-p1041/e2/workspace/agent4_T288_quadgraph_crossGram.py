import sys,json,time
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
R=json.loads(Path('workspace/agent4_T288_quadgraph_P16.json').read_text());v4=veronese(11,4);v5=veronese(11,5)
def kernel(S,V):
 B={};K=[]
 for i,p in enumerate(S):
  v=V[p];c=1<<i
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j][0];c^=B[j][1]
   else:B[j]=(v,c);break
  if not v:K.append(c)
 return K
stats={};bad=[]
for rr in R['results']:
 for r in rr['seeds']:
  S=r['support'];K4=kernel(S,v4);K5=kernel(S,v5);n=sum((u&v).bit_count()%2 for u in K4 for v in K5)
  stats[len(K4),len(K5),n]=stats.get((len(K4),len(K5),n),0)+1
  if n:bad.append(r)
print('K4/K5 Gram stats',stats,'bad',len(bad));assert not bad
Path('workspace/agent4_T288_quadgraph_crossGram.json').write_text(json.dumps({str(k):v for k,v in stats.items()}))
