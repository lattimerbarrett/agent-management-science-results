import itertools,time,json,pickle

def mul(a,b):
 return sum(((((a>>(2*i))&1)*((b>>j)&1))^(((a>>(2*i+1))&1)*((b>>(j+2))&1)))<<(2*i+j) for i in range(2) for j in range(2))
M=[[mul(a,b) for b in range(16)] for a in range(16)]
GL=[a for a in range(1,16) if (a&1)*((a>>3)&1)^((a>>1)&1)*((a>>2)&1)];inv={a:next(b for b in GL if M[a][b]==9) for a in GL}
spaces=sorted(set(tuple(sorted((a,b,a^b))) for a in range(1,16) for b in range(a+1,16)))
affines=sorted(set(tuple(sorted({c,c^sp[0],c^sp[1],c^sp[2]})) for sp in spaces for c in range(16)));ai={a:i for i,a in enumerate(affines)}
perms=[(tuple(M[M[inv[l]][a]][inv[r]]-1 for a in range(1,16)),l,r) for l in GL for r in GL]
left={(a,l):ai[tuple(sorted(M[l][x] for x in af))] for a,af in enumerate(affines) for l in GL}
right={(a,r):ai[tuple(sorted(M[x][r] for x in af))] for a,af in enumerate(affines) for r in GL}
trans=[[(i-1,M[i][a]-1) for i in range(1,16) for a in aff if M[i][a]] for aff in affines]
functionals=[tuple(i-1 for i in range(1,16) if (i&c).bit_count()%2) for c in range(1,16)]
traceforms=[tuple(i-1 for i in range(1,16) if ((M[g][i]&1)^((M[g][i]>>3)&1))) for g in GL]
def canon(v):
 best=None;lr=None
 for p,l,r in perms:
  vv=tuple(v[j] for j in p)
  if best is None or vv<best:best=vv;lr=(l,r)
 return best,lr
D={};start=time.time()
for a,af in enumerate(affines):
 v=[int(i in af) for i in range(1,16)];v,(l,r)=canon(v);D[v]=(right[left[a,l],r],)
checkpoint=pickle.load(open('workspace/agent4_trace_dp_checkpoint.pkl','rb'));D=checkpoint['D'];firststep=checkpoint['step']+1
print('resuming',firststep,'states',len(D),flush=True)
for step in range(firststep,8):
 DD={};cut=334//(1<<(7-step));transitions=0
 for v,path in D.items():
  for a,tr in enumerate(trans):
   out=[0]*15
   for i,j in tr:out[j]+=v[i]
   vals=[sum(out[j] for j in js) for js in functionals];pos=[x for x in vals if x]
   if not pos or min(pos)>cut:continue
   vv,(l,r)=canon(out)
   if vv not in DD:
    pp=list(path)+[a];pp[0]=left[pp[0],l];pp[-1]=right[pp[-1],r];DD[vv]=tuple(pp)
  transitions+=1
  if transitions%100000==0:print('step',step,'processed',transitions,'next',len(DD),'elapsed',time.time()-start,flush=True)
 D=DD;print('STEPDONE',step,'states',len(D),'time',time.time()-start,flush=True)
 pickle.dump({'D':D,'step':step,'affines':affines},open('workspace/agent4_trace_dp_checkpoint.pkl','wb'))
 if step==7:
  found={}
  for v,path in D.items():
   for g,js in zip(GL,traceforms):
    w=sum(v[j] for j in js)
    if w in [310,322,326,330,334]:found[w]={'path':path,'g':g}
  print('FOUND',found,flush=True);json.dump({'affines':affines,'found':found},open('workspace/agent4_trace_allaffine.json','w'))
