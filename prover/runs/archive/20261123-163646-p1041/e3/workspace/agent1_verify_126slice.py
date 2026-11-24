# Supplemental exact checks for the 126-point hyperplane-slice exclusion.
# Uses only standard Python. Structural proofs are in accompanying discussion.
import itertools
def wedge(form,vector):
 out=set()
 for mask in form:
  for i in range(12):
   if vector>>i&1 and not(mask>>i&1):
    j=mask|1<<i
    if j in out:out.remove(j)
    else:out.add(j)
 return out

def rank(rows):
 piv={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)



def hs(T,n=12,k=6):
 out=[]
 for j in range(k+1):
  cols={sum(1<<i for i in S):a for a,S in enumerate(itertools.combinations(range(n),k-j))}
  rows=[]
  for S in itertools.combinations(range(n),j):
   mask=sum(1<<i for i in S);r=0
   for t in T:
    if t&mask==mask:r^=1<<cols[t^mask]
   rows.append(r)
  out.append(rank(rows))
 return out

def q(T,n=12):
 return sum(1 for a,b in itertools.combinations(T,2) if a^b==(1<<n)-1 and a&b==0)%2

rows=[]
for a in range(7):
 for b in range(7-a):
  c=6-a-b
  vec=[1<<i for i in range(a)]+[1<<(6+i) for i in range(b)]
  vec +=[(1<<(a+i))^(1<<(6+b+i)) for i in range(c)]
  beta={0}
  for v in vec:beta=wedge(beta,v)
  gamma={0x3f,0xfc0}^beta
  h=hs(gamma);L=sum(h)
  rows.append((a,b,c,q(gamma),L))
q0=[x for x in rows if x[3]==0]
assert {x[4] for x in q0}=={64,124,154,168,174,176}
assert {(a,b,c) for a,b,c,par,L in q0 if L==124}=={(0,5,1),(5,0,1)}
assert {(a,b,c) for a,b,c,par,L in q0 if L==64}=={(0,6,0),(6,0,0)}
# Canonical second/third words' moment Hilbert vectors.
base96={0xf | (3<<4),0xf | (3<<6)}
# free4 wedge quadratic on4: masks have disjoint four common bits.
assert hs(base96)[1]==8
# 112: free2 wedge Hodge4-form of rank6 quadratic, or free3 wedge two3volumes.
base112a={3 | (0b1111<<2),3 | (0b110011<<2),3 | (0b111100<<2)}
base112b={7 | (7<<3),7 | (7<<6)}
assert hs(base112a)[1]==8
assert hs(base112b)[1]==9
# Arithmetic in fixed-top124 gap.
for W in [136,144]:
 assert (W-128)//2 in [4,8]
 assert (W-128)//2<16
 assert W//2 in [68,72]
 assert (W//2-32) not in [32] and 32<W//2-32<48
 assert (W//2)%4==0
# Numerical small-half possibilities in 126 slice.
known_below128={0,64,96,112,120,124,126}
for total in [196,200,204,208]:
 pairs=[]
 for a in known_below128:
  b=total-a
  if a and a<=b and a<=104:
   if a==64 and b in [132,140]:continue # KTA forbidden
   if a==96 and b in [100,104,108]:continue # KT forbidden
   pairs.append((a,b))
 expected={196:[],200:[(64,136)],204:[],208:[(64,144),(96,112)]}[total]
 assert pairs==expected,(total,pairs)
print('Checked 28 exterior orbits, q=0 apolar lengths, KTA96/112 moment ranks, and all 126-slice arithmetic.')
