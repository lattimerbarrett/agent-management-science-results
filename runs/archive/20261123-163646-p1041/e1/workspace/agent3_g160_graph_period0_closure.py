import itertools,time,json,numpy as np,random
n=11;N=1<<n;ALL=(1<<N)-1
X=[sum(1<<x for x in range(N) if x>>i&1) for i in range(n)];LOW=[ALL^x for x in X]
def mob(a):
 for i in range(n):a^=(a&LOW[i])<<(1<<i)
 return a
def span(bs,shift=0):
 s=[shift]
 for v in bs:s += [x^v for x in s]
 return s
bases=[[1<<i for i in range(6)],[1<<i for i in [0,1,2,3,6,7]],[1<<i for i in [4,5,6,7,9,10]]];shifts=[0,0,1<<8]
g=0
for B,s in zip(bases,shifts):
 for x in span(B,s):g^=1<<x
assert g.bit_count()==160;ga=mob(g);print('gdegree',max(x.bit_count() for x in range(N) if ga>>x&1))
basis=[ALL]+X+[X[i]&X[j] for i in range(n) for j in range(i)];HIGH=sum(1<<x for x in range(N) if x.bit_count()>6)
piv={};kern=[]
for i,q in enumerate(basis):
 v=mob(q&g)&HIGH;u=1<<i
 while v:
  b=v.bit_length()-1
  if b not in piv:piv[b]=(v,u);break
  vv,uu=piv[b];v^=vv;u^=uu
 if not v:kern.append(u)
def btruth(u):
 q=0
 while u:
  l=u&-u;q^=basis[l.bit_length()-1];u^=l
 return q
K=[btruth(u) for u in kern];print('kernelQdim',len(K),'quadraticextras',len(K)-12)
def restriction_signature(q):
 v=0;z=0
 for B,s in zip(bases,shifts):
  for a,b in itertools.combinations(B,2):
   bit=((q>>s)^(q>>(s^a))^(q>>(s^b))^(q>>(s^a^b)))&1
   v|=bit<<z;z+=1
 return v
sig=[restriction_signature(q) for q in K];print('nonaffinebasis',sum(bool(v) for v in sig), 'sigbits',[v.bit_count() for v in sig])
json.dump({'g_truth_hex':hex(g),'bases':bases,'shifts':shifts,'quadratic_kernel_truth':[hex(q) for q in K],'nonlinear_restriction_sigs':sig},open('workspace/agent3_g160_graph_period0_kernel.json','w'))
def red(v,p):
 while v:
  b=v.bit_length()-1
  if b not in p:break
  v^=p[b]
 return v
p={}
for q in basis[:12]:
 v=red(q&g,p)
 if v:p[v.bit_length()-1]=v
extras=[]
for q in K:
 v=red(q&g,p)
 if v:p[v.bit_length()-1]=v;extras.append(q)
print('graphQmodaffine_dim',len(extras),flush=True)
n13=13;N13=8192;mons=[sum(1<<i for i in I) for d in range(6) for I in itertools.combinations(range(13),d)];pts=np.arange(N13,dtype=np.uint16);ev=np.empty((N13,len(mons)),dtype=np.uint8)
for j,m in enumerate(mons):ev[:,j]=((pts&m)==m)
cols=[int.from_bytes(row.tobytes(),'little') for row in np.packbits(ev,axis=1,bitorder='little')];del ev
M3=(1<<378)-1;Gpts=[x for x in range(N) if g>>x&1];ALL13=(1<<N13)-1
results=[]
for z in range(1<<len(extras)):
 Q=0
 for i,q in enumerate(extras):
  if z>>i&1:Q^=q
 h=0
 for x in Gpts:
  y=x+(((Q>>x)&1)<<11);h|=(1<<y)|(1<<(y+4096))
 assert h.bit_count()==320;S=[x for x in range(N13) if h>>x&1];p3={}
 for x in S:
  v=red(cols[x]&M3,p3)
  if v:p3[v.bit_length()-1]=v
 E=[x for x in range(N13) if not(h>>x&1) and not red(cols[x]&M3,p3)]
 print('Qclass',z,'cubicrank',len(p3),'closureextra',len(E),flush=True)
 pp={}
 for x in S:
  v=cols[x];u=1<<x
  while v:
   b=v.bit_length()-1
   if b not in pp:pp[b]=(v,u);break
   vv,uu=pp[b];v^=vv;u^=uu
 kb=[]
 for x in E:
  v=cols[x];u=1<<x
  while v:
   b=v.bit_length()-1
   if b not in pp:pp[b]=(v,u);break
   vv,uu=pp[b];v^=vv;u^=uu
  if not v:kb.append(u)
 rec={'class':z,'cubicrank':len(p3),'closureextras':len(E),'kernel_dim':len(kb)};results.append(rec)
 if len(kb)>24:print('LARGE KERNEL',len(kb),flush=True);continue
 C=0;dist={};outside=ALL13^h
 for zz in range(1<<len(kb)):
  if zz:C^=kb[(zz&-zz).bit_length()-1]
  w=(C&outside).bit_count();dist[w]=dist.get(w,0)+1
  if w in (1,3,5,7):
   F=C|((C^h)<<8192);assert F.bit_count()==320+2*w
   aa=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for bit in range(14):
    st=1<<bit;bl=aa.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   assert max(int(x).bit_count() for x in np.flatnonzero(aa))<=7
   print('FOUND!',F.bit_count(),flush=True);json.dump({'truth_hex':hex(F),'weight':F.bit_count()},open('workspace/agent3_graph_hit_'+str(F.bit_count())+'.json','w'))
 rec['outside_kernel_weight_dist']=dist;print('kernel_dim',len(kb),'dist',dist,flush=True)
json.dump(results,open('workspace/agent3_g160_graph_period0_closure_results.json','w'))
import shutil;shutil.copyfile(__file__,'workspace/agent3_g160_graph_period0_closure.py')
