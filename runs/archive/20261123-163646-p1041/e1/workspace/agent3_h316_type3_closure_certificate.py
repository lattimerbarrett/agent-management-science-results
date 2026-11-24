import os,json,itertools,time,numpy as np,random
start=time.time();n=13;N=1<<n
mons=[sum(1<<i for i in I) for d in range(6) for I in itertools.combinations(range(n),d)]
points=np.arange(N,dtype=np.uint16);ev=np.empty((N,len(mons)),dtype=np.uint8)
for j,mask in enumerate(mons):ev[:,j]=((points&mask)==mask)
p=np.packbits(ev,axis=1,bitorder='little');cols=[int.from_bytes(row.tobytes(),'little') for row in p];del ev,p
print('moments',len(mons),'built',time.time()-start,flush=True)
def reduce(v,piv):
 while v:
  b=v.bit_length()-1
  if b not in piv:break
  v^=piv[b]
 return v
def quotient(S):
 piv={}
 for x in S:
  v=reduce(cols[x],piv)
  if v:piv[v.bit_length()-1]=v
 # Standard reduction must continue below missing top pivot: eliminate all pivots high-to-low.
 order=sorted(piv,reverse=True)
 out=[]
 for x in range(N):
  if x in S:continue
  v=cols[x]
  for b in order:
   if v>>b&1:v^=piv[b]
  out.append((x,v))
 return piv,out
def span(bs):
 s=[0]
 for v in bs:s += [x^v for x in s]
 return s
bs=[[1<<i for i in range(7)],[1<<i for i in [0,1,2,3,4,7,8]],[1<<i for i in [5,7,8,9,10,11,12]]]
h=0
for i,B in enumerate(bs):
 for x in span(B):h^=1<<(x^((1<<6) if i==2 else 0))
S={x for x in range(N) if h>>x&1};assert len(S)==316
piv,out=quotient(S);print('rankinside',len(piv),'outside',len(out),'nonzero',sum(bool(v) for x,v in out),'distinct',len({v for x,v in out}),'time',time.time()-start,flush=True)
mask=(1<<64)-1
def fp(v):
 for sh in (2048,1024,512,256,128,64):v^=v>>sh
 return v&mask
F=[fp(v) for x,v in out];lookup={}
for j,f in enumerate(F):lookup.setdefault(f,[]).append(j)
hits=[];sus=0
for i,fi in enumerate(F):
 for j in range(i+1,len(F)):
  ks=lookup.get(fi^F[j])
  if ks:
   for k in ks:
    if k<=j:continue
    sus+=1
    if out[i][1]^out[j][1]^out[k][1]==0:hits.append([out[i][0],out[j][0],out[k][0]]);print('HIT',hits[-1],flush=True)
print('DONE',len(hits),'fingerprintmatches',sus,'time',time.time()-start,flush=True)
json.dump({'rankinside':len(piv),'outside':len(out),'triple_hits':hits,'suspects':sus},open('workspace/agent3_h316_type3_outside3_result.json','w'))
mask3=(1<<sum(__import__('math').comb(13,d) for d in range(4)))-1;piv3={}
for x in S:
 v=reduce(cols[x]&mask3,piv3)
 if v:piv3[v.bit_length()-1]=v
E=[x for x,v in out if not reduce(cols[x]&mask3,piv3)];print('closure3rank',len(piv3),'outsideE',len(E),flush=True)
pp={}
for x in S:
 v=cols[x];g=1<<x
 while v:
  b=v.bit_length()-1
  if b not in pp:pp[b]=(v,g);break
  vv,gg=pp[b];v^=vv;g^=gg
kern=[]
for x in E:
 v=cols[x];g=1<<x
 while v:
  b=v.bit_length()-1
  if b not in pp:pp[b]=(v,g);break
  vv,gg=pp[b];v^=vv;g^=gg
 if not v:kern.append(g)
print('kernelE',len(kern),flush=True)
if len(kern)<=25:
 dist={};g=0;ALL=(1<<N)-1;outside=ALL^h
 for z in range(1<<len(kern)):
  if z:g^=kern[(z&-z).bit_length()-1]
  w=(g&outside).bit_count();dist[w]=dist.get(w,0)+1
  if w in (3,5,7,9):
   F=g|((g^h)<<N);print('FOUNDcandidate',316+2*w,F.bit_count(),flush=True)
   arr=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for bit in range(14):
    st=1<<bit;bl=arr.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   assert max(int(x).bit_count() for x in np.flatnonzero(arr))<=7
   json.dump({'truth_hex':hex(F),'weight':F.bit_count()},open('workspace/agent3_h316_type3_hit_'+str(F.bit_count())+'.json','w'))
 print('kernelweightdist',dist,flush=True)
classes={};order3=sorted(piv3,reverse=True)
for x,vv in out:
 v=cols[x]&mask3
 for b in order3:
  if v>>b&1:v^=piv3[b]
 classes.setdefault(v,[]).append(x)
from collections import Counter
print('nonzerocubicquotientclasssizes',Counter(len(xs) for v,xs in classes.items() if v),'max',max(len(xs) for v,xs in classes.items() if v),flush=True)
json.dump({'closure3outside':E,'cubicclasssizehist':dict(Counter(len(xs) for v,xs in classes.items() if v))},open('workspace/agent3_h316_type3_closure_result.json','w'))
import shutil
shutil.copyfile(__file__,'workspace/agent3_h316_type3_closure_certificate.py')

