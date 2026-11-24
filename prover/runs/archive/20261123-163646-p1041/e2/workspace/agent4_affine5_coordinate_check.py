import itertools,time
from pathlib import Path
A=127;B=A<<7;ALL=(1<<14)-1;targets={322,326,330,334}
def subbases(M):
 s=M
 while True:
  yield s
  if not s:break
  s=(s-1)&M
def intersection(fs):
 free=ALL;fixed=0;base=0
 for M,b in fs:
  fm=ALL^M
  if (base^b)&fixed&fm:return None
  base|=b;fixed|=fm;free&=M
 return free,base
def seeds():
 for k in range(1,7):
  C=((1<<k)-1)|(((1<<(7-k))-1)<<7);D=ALL^C
  da=[i for i in range(7) if D>>i&1];db=[i for i in range(7,14) if D>>i&1]
  for ia in range(len(da)+1):
   for ib in range(len(db)+1):
    c=sum(1<<i for i in da[:ia]+db[:ib]);fs=[(A,0),(B,0),(C,c)]
    terms=[];w3=0
    for z in range(1,4):
     for ids in itertools.combinations(range(3),z):
      out=intersection([fs[i] for i in ids])
      if out:
       M,b=out;coef=(-2)**(z-1);terms.append((M,b,coef));w3+=coef*(1<<M.bit_count())
    if w3<=334:
     assert w3 in {254,314,318}
     yield C,D,c,terms,w3

def hit(terms,H,h):
 return sum(coef*(1<<(H&M).bit_count()) for M,b,coef in terms if not ((h^b)&(ALL^(H|M))))

st=time.time();ct0=ctfree=0;seeds_list=list(seeds())
Es=[sum(1<<i for i in ids) for ids in itertools.combinations(range(14),7)]
for C,D,c,terms,w3 in seeds_list:
 # Fifth seven-flat is H6 x F2, crossing both slices.
 for kd in [5,6]:
  kc=6-kd
  for Hd in itertools.combinations([i for i in range(14) if D>>i&1],kd):
   for Hc in itertools.combinations([i for i in range(14) if C>>i&1],kc):
    H=sum(1<<i for i in Hd+Hc);constD=D&~H
    for d in subbases(C):
     for hd in subbases(constD):
      h=(d&~H)|hd
      w=w3+256-2*(hit(terms,H,h)+(1<<kd));ctfree+=1
      assert w not in targets
 # Fifth seven-flat is entirely in slice0; slice1 contributes128.
 for E in Es:
  upper=sum(1<<(E&M).bit_count() for M,b,coef in terms if coef==1)
  if 2*upper<w3+128-206:continue
  for e in subbases(ALL^E):
   w=w3+128-2*hit(terms,E,e);ct0+=1
   assert w not in {194,198,202,206}
 # Fifth seven-flat in slice1 cannot help: >=254+128=382.
 assert w3>=254
print('Checked',len(seeds_list),'canonical triple seeds;',ctfree,'crossing cases;',ct0,'slice0 cases; seconds',time.time()-st)
