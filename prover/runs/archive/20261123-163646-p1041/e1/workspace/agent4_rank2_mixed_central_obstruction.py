import itertools,collections
A=[16,24,28,32,36,40];C=[8,12]+list(range(14,41,2))
P=[]
for a,c in itertools.product(A,C):
 for i in range(1,min(a,c)+1,2):
  if a+c-i>41 or a+c-2*i not in C:continue
  # min16 f flat and small12 hquad: oddcap<=3; h8 restrictdegree3 => oddcap<=7; f24quad on6 => oddcap h8<=3.
  if a==16 and c==8 and i!=1:continue
  if a==16 and c==12 and i>3:continue
  if a==24 and c==8 and i>3:continue
  # sameTOP4 symbol: h andh+f cannotweights8/12/14different becauseleadingannihilatorranks4/2/1.
  cp=a+c-2*i
  if {c,cp}=={12,14}:continue # quartic leading-form annihilator dimensions 2 vs 1
  ip=a-i
  if a==16 and cp==8 and ip!=1:continue
  if a==16 and cp==12 and ip>3:continue
  if a==24 and cp==8 and ip>3:continue
  P.append((a,c,i,cp))
for t in [322,326,330,334]:
 hits=[]
 for p,q in itertools.product(P,P):
  a,c,i,_=p;d,b,j,_=q
  if a*b+c*d-2*i*j==t:hits.append((p,q))
 print(t,'hits',len(hits),hits[:40]);assert not hits
open('workspace/agent4_rank2_mixed_central_obstruction.py','w').write(open(__file__).read())
