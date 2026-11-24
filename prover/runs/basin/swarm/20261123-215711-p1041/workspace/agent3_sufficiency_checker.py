from collections import Counter
TABLE = [([127, 1927, 6203], 127), ([127, 8065, 926], 8423), ([127, 1927, 16256], 14729), ([127, 3971, 14212], 127), ([127, 911, 2032], 15505), ([127, 415, 15968], 4001), ([127, 415, 1955], 4004), ([127, 415, 15968], 15875), ([127, 415, 15968], 1927), ([127, 911, 7569], 8080), ([127, 415, 15968], 3683), ([127, 1927, 16256], 2297), ([127, 191, 1863], 127)]
# Each mask M denotes the coordinate 7-space {x:x&~M=0}.
def flat(M):
 assert M.bit_count()==7
 return {x for x in range(16384) if x & (16383 ^ M)==0}
covered=0
for masks,Q in TABLE:
 assert Q.bit_count()==7
 S=flat(masks[0])^flat(masks[1])^flat(masks[2])
 counts=Counter(x&Q for x in S)
 occupancies=list(counts.values())+[0]*(128-len(counts))
 assert len(occupancies)==128 and sum(occupancies)==len(S)
 # Choose independently either S or its complement in each Q-coset.
 base=sum(min(n,128-n) for n in occupancies)
 bits=1
 for n in occupancies:bits |= bits<<abs(128-2*n)
 covered |= bits<<base
missing=[w for w in range(336,8193,2) if not((covered>>w)&1)]
assert missing==[358,362],missing
print('13 explicit coset-switch families cover every even weight 336..8192 except 358,362')

WITNESSES = {0: ['empty', 6, 1, 1, 1, 0, 0, 0, 0], 128: ['empty', 5, 2, 1, 1, 0, 0, 0, 1], 192: ['empty', 5, 1, 1, 1, 1, 0, 0, 0], 224: ['empty', 4, 2, 2, 1, 0, 0, 1, 1], 240: ['empty', 2, 5, 1, 1, 0, 0, 0, 4], 248: ['empty', 1, 6, 1, 1, 0, 0, 0, 5], 252: ['empty', 0, 7, 1, 1, 0, 0, 0, 6], 254: ['common', 0, 6, 1, 0, 0, 0, 1, 6], 256: ['empty', 4, 2, 1, 1, 1, 0, 0, 1], 272: ['empty', 3, 3, 2, 1, 0, 0, 1, 2], 288: ['empty', 4, 1, 1, 1, 2, 0, 0, 0], 296: ['empty', 2, 4, 2, 1, 0, 0, 1, 3], 304: ['empty', 3, 2, 2, 1, 1, 0, 1, 1], 308: ['empty', 1, 5, 2, 1, 0, 0, 1, 4], 312: ['empty', 2, 3, 3, 1, 0, 0, 2, 2], 314: ['empty', 0, 6, 2, 1, 0, 0, 1, 5], 316: ['empty', 0, 6, 1, 1, 1, 0, 0, 5], 318: ['common', 0, 5, 1, 0, 1, 0, 1, 5], 320: ['empty', 3, 2, 1, 1, 2, 0, 0, 1], 324: ['common', 1, 3, 3, 0, 0, 0, 3, 3], 328: ['empty', 2, 3, 2, 1, 1, 0, 1, 2], 332: ['empty', 1, 4, 3, 1, 0, 0, 2, 3], 358: ['empty', 0, 4, 3, 1, 1, 0, 2, 3], 362: ['empty', 0, 4, 2, 1, 2, 0, 1, 3]}
def check_witness(w,params):
 typ,t,a,b,c,d,x,y,z=params
 A=[];B=[];C=[];ell=0;pos=0
 def block(n,which,pick=False):
  nonlocal pos,ell
  for j in range(n):
   v=1<<pos;pos+=1
   for L in which:L.append(v)
   if pick and j==0:ell|=v
 block(t,[A,B,C]);block(a,[A,B],True);block(b,[A,C],True);block(c,[B,C],True)
 for j in range(d):
  e=1<<pos;f=1<<(pos+1);pos+=2;A.append(e);B.append(f);C.append(e^f)
 block(x,[A]);block(y,[B]);block(z,[C])
 r=8 if typ=='empty' else 7
 assert len(A)==len(B)==len(C)==r and pos<=r+7
 def supp(basis):
  S={0}
  for v in basis:S|={v^q for q in S}
  if typ=='empty':S={q for q in S if (q&ell).bit_count()%2}
  assert len(S)==128
  return S
 S=supp(A)^supp(B)^supp(C)
 assert len(S)==w,(w,len(S),params)
for w,p in WITNESSES.items():
 check_witness(w,p)
 covered|=1<<w
assert all(covered>>w&1 for w in range(336,8193,2))
print('All proposed low weights and every even central weight constructed in RM(7,14).')
