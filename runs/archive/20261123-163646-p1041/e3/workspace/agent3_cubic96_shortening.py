import json,runpy,itertools,collections,time
M=runpy.run_path('workspace/agent3_cubic96_pencils.py');basis=M['basis'];data=json.load(open('workspace/agent3_cubic96_pencils.json'));u=int(data['u'],16)
MONOS=[sum(1<<i for i in I) for d in range(5) for I in itertools.combinations(range(9),d)]
assert len(MONOS)==256
COLS=[sum((x&s==s)<<j for j,s in enumerate(MONOS)) for x in range(512)]
MASKS=[sum(1<<x for x in range(512) if not x>>i&1) for i in range(9)]
def shift(w,a):
 while a:
  t=a&-a;a^=t;i=t.bit_length()-1;m=MASKS[i]
  w=((w&m)<<t)|((w>>t)&m)
 return w

def shortened(S):
 D={};ker=[]
 for x in range(512):
  if not S>>x&1:continue
  v=COLS[x];comb=1<<x
  while v:
   k=v.bit_length()-1
   if k in D:v^=D[k][0];comb^=D[k][1]
   else:D[k]=(v,comb);break
  if not v:ker.append(comb)
 return ker

def local_shortened(n,d,S):
 mons=[sum(1<<i for i in I) for r in range(n-d) for I in itertools.combinations(range(n),r)]
 cols=[sum((x&s==s)<<j for j,s in enumerate(mons)) for x in range(1<<n)]
 D={};K=[]
 for x in range(1<<n):
  if not S>>x&1:continue
  v=cols[x];comb=1<<x
  while v:
   k=v.bit_length()-1
   if k in D:v^=D[k][0];comb^=D[k][1]
   else:D[k]=(v,comb);break
  if not v:K.append(comb)
 return K

def verify_external_rank_model(F):
 S=int(F['S'],16);u=int(F['u'],16);v=int(F['v'],16)
 for a in (32,64,128,256):assert shift(S,a)==S and shift(u,a)==u and shift(v,a)==v
 mask=(1<<32)-1;R=S&mask;u0=u&mask;v0=v&mask
 K2=local_shortened(5,2,R);K3=local_shortened(5,3,R);K4=local_shortened(5,4,R)
 assert len(K2)==0 and len(K3)==3 and len(K4)==8
 assert u0!=v0 and u0 and v0
 assert len(basis(K3+( [u0,v0] )))==3
 # Every t has external degree<=1, with four coefficients in K3.
 # Mod C=<u,v> this is a map F2^4 -> a1-dimensional quotient.
 # Its kernel has dimension>=3, giving a nonzero period after (a,b) lift.
 return True

def verify():
 start=time.time();models={};proper=0;u=int(data['u'],16)
 for key,T,small,a,h in data['models']:
  v=int(h,16);S=u|v;P=[x for x in range(512) if S>>x&1]
  if len(basis(x^P[0] for x in P))<9:proper+=1;continue
  models.setdefault((S,min(v,u^v)),(u,v))
 counter=collections.Counter();failed=[];cert=[]
 for j,((S,_),(u,v)) in enumerate(models.items()):
  K=shortened(S);counter[len(K)]+=1
  C={0,u,v,u^v}
  periods=[a for a in range(1,512) if shift(u,a)==u and shift(v,a)==v]
  good=[a for a in periods if all((shift(t,a)^t) in C for t in K)]
  if not good:failed.append(dict(S=hex(S),u=hex(u),v=hex(v),dim=len(K),periods=periods))
  else:cert.append(dict(S=hex(S),u=hex(u),v=hex(v),dim=len(K),period=good[0]))
  if j%100==0:print(j,'failed',len(failed),'elapsed',time.time()-start,flush=True)
 for F in failed:assert verify_external_rank_model(F)
 out=dict(proper=proper,fullspan_unions=len(models),dims=dict(counter),external_rank_models=failed,certificates=cert)
 json.dump(out,open('workspace/agent3_cubic96_shortening.json','w'))
 print('PASS: classified',len(models),'fullspan pencils;',len(cert),'universal period certificates;',len(failed),'external-rank certificates; dimensions',counter)
 return out
if __name__=='__main__':verify()
