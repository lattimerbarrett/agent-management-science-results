import pickle,itertools,time,json,random
D=pickle.load(open('workspace/agent2_C35.pkl','rb'));C=D['C'];R=D['R'];N=35;ALL=(1<<310)-1
# coefficientinversion
E={}
for i,c in enumerate(C):
 co=1<<i
 while c:
  p=c.bit_length()-1
  if p in E:c^=E[p][0];co^=E[p][1]
  else:E[p]=(c,co);break

def co(t):
 out=0
 while t:
  p=t.bit_length()-1;t^=E[p][0];out^=E[p][1]
 return out
RC=[co(r) for r in R]
def ev(v):
 out=0
 while v:
  b=v&-v;v^=b;out^=C[b.bit_length()-1]
 return out
cache={}
def row(q):
 if q not in cache:cache[q]=sum(((q&c).bit_count()%2)<<i for i,c in enumerate(C))
 return cache[q]
def insert(B,v):
 while v:
  p=v.bit_length()-1
  if p in B:v^=B[p]
  else:B[p]=v;return

def null(rows,n=N):
 B={}
 for v in rows:insert(B,v)
 ans=[]
 for i in range(n):
  if i in B:continue
  v=1<<i
  for p,r in sorted(B.items()):
   if (v&r).bit_count()%2:v^=1<<p
  ans.append(v)
 return ans

def rank(rows,cap=100):
 B={}
 for v in rows:
  insert(B,v)
  if len(B)>cap:return len(B)
 return len(B)
G=RC[2:];GT=R[2:];span=[0];products=[ALL]
for t in GT:span +=[x^t for x in span];products +=[x&t for x in products]
base=[row(q) for q in products];surv=[];hist={};start=time.time()
for code in range(1,1024):
 v=code<<25;vt=ev(v)
 if any(not 64<=(x^vt).bit_count()<=246 for x in span):continue
 W=null(base+[row(q&vt) for q in products]);d=len(W);cap=2*(d-14);TT=[ev(w) for w in W]
 maxrank=0;matrices=[]
 for value in range(16):
  F=ALL
  for j,t in enumerate(GT+[vt]):F &= t if value>>j&1 else ~t
  mat=[sum(((a&b&F).bit_count()%2)<<j for j,b in enumerate(TT)) for a in TT]
  rr=rank(mat,cap);maxrank=max(maxrank,rr)
  if rr>cap:break
  matrices.append(mat)
 hist[d,maxrank]=hist.get((d,maxrank),0)+1
 if maxrank<=cap:
  surv.append((v,d,matrices,W))
  if len(surv)<20:print('SURV',code,d,maxrank,flush=True)
print('hist',hist,'surv',len(surv),'secs',time.time()-start,flush=True)
pickle.dump({'RC':RC,'G':G,'base':base,'survivors':surv},open('workspace/agent3_C35_fourths.pkl','wb'))
