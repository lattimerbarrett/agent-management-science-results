import itertools,random,pickle,time,json
random.seed(666)
cols=pickle.load(open('workspace/a1_punctured157.pkl','rb'))['cols'];NT=4096
A=sum(1<<i for i in range(6));B=sum(1<<i for i in [0,1,2,3,6,7]);P=sum(1<<i for i in [4,5,8,9,10,11]);ps=[x&~P==0 for x in range(NT)];qs=[(x&~A==0)^(x&~B==0) for x in range(NT)];U=[x for x in range(NT) if ps[x] or qs[x]]
ALL=(1<<128)-1;X=[]
for i in range(7):X.append(sum(1<<j for j in range(128) if j>>i&1))
low=[ALL^x for x in X];qwords=[ALL]+X+[X[i]&X[j] for i in range(7) for j in range(i)];qb={}
for v in qwords:
 while v:
  p=v.bit_length()-1
  if p not in qb:qb[p]=v;break
  v^=qb[p]
qp=sorted(qb,reverse=True)
def decode(h):
 q=0
 for i in range(7):
  vi=h^(h>>(1<<i))
  for j in range(i):
   v=(vi^(vi>>(1<<j)))&low[i]&low[j]
   if v.bit_count()>16:q^=X[i]&X[j]
 h^=q
 for i in range(7):
  if ((h^(h>>(1<<i)))&low[i]).bit_count()>32:q^=X[i]
 h0=h
 for i in range(7):
  if ((h0^(h0>>(1<<i)))&low[i]).bit_count()>32:h^=X[i]
 if h.bit_count()>64:q^=ALL;h^=ALL
 return q,h

def image_on_D(U,D):
 """Image of RM(7,12) shortened to U union D, on affine 7-flat D.
 D[j] must be affine-linear in j's 7 binary coordinates.
 Returns complement representatives modulo RM(2,7), not full basis.
 """
 DD=set(D);bas={}
 for x in U:
  if x in DD:continue
  v=cols[x]
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,0);break
   v^=bas[p][0]
 extras=[];eb={}
 for j,x in enumerate(D):
  v=cols[x];img=1<<j
  while v:
   p=v.bit_length()-1
   if p not in bas:bas[p]=(v,img);break
   a,b=bas[p];v^=a;img^=b
  if v:continue
  for p in qp:
   if img>>p&1:img^=qb[p]
  while img:
   p=img.bit_length()-1
   if p not in eb:eb[p]=img;extras.append(img);break
   img^=eb[p]
 return extras

def small_coset_words(N,extras,maxweight=15):
 """Exact all words of weight <=maxweight in N+image, maxweight<=15.
 Yields (residual_word, image_word), e=N+image_word.
 """
 assert maxweight<=15
 h=N;previous=0
 for s in range(1<<len(extras)):
  gray=s^(s>>1)
  if s:h^=extras[(gray^previous).bit_length()-1]
  previous=gray;q,e=decode(h)
  if e.bit_count()<=maxweight:yield e,e^N
