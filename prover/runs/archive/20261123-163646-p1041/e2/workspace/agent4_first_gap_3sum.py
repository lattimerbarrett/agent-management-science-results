"""Exact three-collision obstruction for the first possible post-2d gap.
For c=5 or7, T is the canonical (c-1)-even point set of size2^(c+1)-4.
We test ALL distinct outside triples whose degree(c-2) evaluation syndrome
could vanish modulo the span of T. No approximate or random computation.
"""
import itertools,sys,json,time,numpy as np
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese

def check(c):
 st=time.time();m=2*c-1;V=veronese(m,c-2)
 T=sorted(set(range(1<<c))^{x<<(c-1) for x in range(1<<c)})
 assert len(T)==(1<<(c+1))-4
 B={}
 for i,x in enumerate(T):
  v=V[x];co=1<<i
  while v:
   j=v.bit_length()-1
   if j in B:v^=B[j][0];co^=B[j][1]
   else:B[j]=(v,co);break
 pivots=sorted(B.items(),reverse=True);TS=set(T)
 outside=[p for p in range(1<<m) if p not in TS]
 sy=[];combs=[];by={}
 for i,p in enumerate(outside):
  v=V[p];co=0
  for j,(row,cc) in pivots:
   if v>>j&1:v^=row;co^=cc
  sy.append(v);combs.append(co);by[v]=i
 checks=0
 for i,a in enumerate(outside):
  si=sy[i]
  for j in range(i+1,len(outside)):
   checks+=1;k=by.get(si^sy[j],-1)
   if k<=j:continue
   b,d=outside[j],outside[k];co=combs[i]^combs[j]^combs[k]
   H={a,b,d}|{x for q,x in enumerate(T) if co>>q&1}
   assert __import__('functools').reduce(int.__xor__,[V[x] for x in H])==0
   f=np.zeros(1<<(m+1),dtype=np.uint8)
   for x in H:f[x]=1
   for x in H^TS:f[x+(1<<m)]=1
   assert int(f.sum())==(1<<(c+1))+2
   support=np.nonzero(f)[0].tolist()
   for bit in range(m+1):f=f.reshape(-1,2,1<<bit);f[:,1,:]^=f[:,0,:];f=f.reshape(-1)
   degree=max(int(q).bit_count() for q in np.nonzero(f)[0]);assert degree<=c
   result={'c':c,'collision_triple':[a,b,d],'support':support,'weight':len(support),'degree':degree}
   Path('workspace/agent4_firstgap_found.json').write_text(json.dumps(result));print('FOUND',result,flush=True);return result
  if c>=7 and i%2000==0:print('progress',i,'/',len(outside),'pairs',checks,'seconds',time.time()-st,flush=True)
 assert checks==len(outside)*(len(outside)-1)//2
 result={'c':c,'m':m,'T_size':len(T),'basisrank':len(B),'outside':len(outside),'unique_syndromes':len(by),'pairschecked':checks,'no_relation':True,'zero_syndromes':[outside[j] for j,v in enumerate(sy) if v==0],'seconds':time.time()-st}
 print('CHECKED',result,flush=True)
 Path('workspace/agent4_firstgap_%d_result.json'%c).write_text(json.dumps(result));return result

if __name__=='__main__':
 results=[check(5),check(7)]
 assert all(r.get('no_relation') for r in results)
