import json,itertools,pickle,time
# F8 GF(2)[t]/(t^3+t+1)
def mul(a,b):
 out=0
 while b:
  if b&1:out^=a
  b>>=1;a<<=1
  if a&8:a^=11
 return out
inv={a:next(b for b in range(1,8) if mul(a,b)==1) for a in range(1,8)}
def key6(x):
 a=x&7;b=x>>3
 if a:return 1+mul(b,inv[a])
 if b:return 9
 return 0
orbs={}
for x in range(16384):
 k=(key6(x&63),key6((x>>6)&63),x>>12)
 orbs.setdefault(k,[]).append(x)
keys=list(orbs);ix={k:i for i,k in enumerate(keys)}
vals=[0]*16384
for i,k in enumerate(keys):
 for x in orbs[k]:vals[x]=1<<i
for b in range(14):
 for x in range(16384):
  if x>>b&1:vals[x]^=vals[x^(1<<b)]
piv={}
for x,r in enumerate(vals):
 if x.bit_count()<=7:continue
 while r:
  p=r.bit_length()-1
  if p in piv:r^=piv[p]
  else:piv[p]=r;break
weights={i:len(orbs[k]) for i,k in enumerate(keys)}
L=[i for i,w in weights.items() if w==7];H=[i for i,w in weights.items() if w==49]
D={'L':L,'H':H,'rows':list(piv.values()),'weights':weights}
json.dump(D,open('workspace/agent4_f8_matrix.json','w'));pickle.dump((keys,orbs),open('workspace/agent4_f8_orbits.pkl','wb'))
print('dim',400-len(piv),'rank',len(piv),'L',len(L),'H',len(H),flush=True)
text=open('workspace/a1_cyclic_sparse_check.py').read().replace('a1_cyclic','agent4_f8')
open('workspace/agent4_f8_sparse_check.py','w').write(text)
exec(compile(text,'workspace/agent4_f8_sparse_check.py','exec'))
