import random,math,time,pickle
random.seed(123)

def pts(bs,shift):
 p=[shift]
 for b in bs:p +=[x^b for x in p]
 return p

def mask(bs,shift):return sum(1<<x for x in pts(bs,shift))
def basis(ix):return [1<<i for i in ix]
def rank(bs):
 d={}
 for a in bs:
  while a:
   k=a.bit_length()-1
   if k in d:a^=d[k]
   else:d[k]=a;break
 return len(d)
base=[(basis([0,1,2,3,4,5,6]),0),(basis([0,1,2,3,7,8,9]),0),(basis([4,5,6,10,11,12,13]),0)]
targets={322,326,330,334};found={};counts={};start=time.time()
for restart in range(12):
 fs=[(bs[:],s,mask(bs,s)) for bs,s in base]
 for _ in range(1+restart%3):
  bs=basis(random.sample(range(14),7));s=random.randrange(16384);b=mask(bs,s)
  fs.extend([(bs[:],s,b),(bs[:],s,b)])
 word=0
 for _,_,f in fs:word^=f
 w=word.bit_count();assert w==338
 target=sorted(targets)[restart%4]
 for it in range(200000):
  j=random.randrange(len(fs));bs,s,b=fs[j]
  b2=bs[:];s2=s
  if random.random()<.85:
   i=random.randrange(7);b2[i]^=random.randrange(1,16384)
   if rank(b2)<7:continue
  else:s2^=random.randrange(1,16384)
  m2=mask(b2,s2);new=word^b^m2;ww=new.bit_count()
  T=random.choice([1.,2.,4.,8.]) if restart%2 else 2.
  delta=abs(ww-target)-abs(w-target)
  if delta<=0 or random.random()<math.exp(-delta/T):
   word=new;w=ww;fs[j]=(b2,s2,m2)
   counts[w]=counts.get(w,0)+1
   if w in targets:
    found[w]=[(a,b) for a,b,_ in fs]
    pickle.dump(found,open('anneal_found.pkl','wb'));print('FOUND',w,found[w],flush=True)
    targets.remove(w)
    if not targets:break
 if not targets:break
 print('restart',restart,'w',w,'elapsed',round(time.time()-start,2),flush=True)
print('found',found)
print('low reached',sorted(w for w in counts if w<338))
