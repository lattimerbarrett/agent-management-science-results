import z3,itertools,time,json
K=4;E=16;M=31;D=16
r=[z3.Int('r%d'%S) for S in range(32)]
s=z3.Solver();s.add(r[0]==0,r[E]==1)
for S in range(1,32):s.add(r[S]>=0,r[S]<=16)
for i in range(4):s.add(r[1<<i]==8,r[(1<<i)|E]==9)
for A in range(32):
 for B in range(A,32):
  if A&B==A:s.add(r[A]<=r[B])
  s.add(r[A]+r[B]>=r[A|B]+r[A&B])
for T in range(32):
 for A in range(1,32):
  if T&A:continue
  for B in range(1,32):
   if (T|A)&B:continue
   for C in range(1,32):
    if (T|A|B)&C:continue
    for DD in range(1,32):
     if (T|A|B|C)&DD:continue
     s.add(r[A|B|T]+r[A|C|T]+r[A|DD|T]+r[B|C|T]+r[B|DD|T]>=r[A|T]+r[B|T]+r[C|DD|T]+r[A|B|C|T]+r[A|B|DD|T])
def it(S):return 16-r[S]
for ids in itertools.permutations(range(4)):
 a,b,c,d=[1<<j for j in ids]
 base=it(a|b)+it(a|c)+it(b|c)-it(a|b|c)
 for x,y in [(a,b),(a,c),(b,c)]:
  # 15=rank(Ua+Ub+Uc+Ud) <=28-base-(ixd+iyd-ixyd).
  s.add(base+it(x|d)+it(y|d)-it(x|y|d)<=16)
for i,j in itertools.combinations(range(4),2):
 P=(1<<i)|(1<<j);s.add(z3.Implies(r[P|E]==r[P]+1,r[P|E]>=11))
def pw(d):return sum(z3.If(d==j,1<<j,0) for j in range(8))
w=512
for k in range(2,5):
 for ids in itertools.combinations(range(4),k):
  S=sum(1<<j for j in ids);card=z3.If(r[S|E]==r[S]+1,pw(16-r[S|E]),0);w+=(-2)**(k-1)*card
for ids in itertools.combinations(range(4),3):
 U=sum(1<<j for j in ids)
 paircards=[]
 for a,b in itertools.combinations(ids,2):
  P=(1<<a)|(1<<b);paircards.append(z3.If(r[P|E]==r[P]+1,pw(16-r[P|E]),0))
 tc=z3.If(r[U|E]==r[U]+1,pw(16-r[U|E]),0)
 s.add(384-2*sum(paircards)+4*tc>=256)
for target in [322,326,330,334]:
 s.push();s.add(w==target);s.set(timeout=10000);st=time.time();ans=s.check();print(target,ans,time.time()-st,flush=True)
 if ans==z3.sat:
  md=s.model();out={S:md[r[S]].as_long() for S in range(32)};print(out,flush=True)
  from pathlib import Path
  Path('workspace/agent4_co6_rankcone_%d.json'%target).write_text(json.dumps(out))
 s.pop()
