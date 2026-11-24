import itertools,collections,json,pathlib
n=6;S=[]
for a in range(16):
 x=[a>>i&1 for i in range(4)];q=[x[0]*x[1],x[0]*x[2]^x[1]*x[3]];S.append(a+sum(v<<(4+j) for j,v in enumerate(q)))
SS=set(S);F=collections.defaultdict(list)
def rank(bs):
 D={}
 for b in bs:
  while b:
   j=b.bit_length()-1
   if j in D:b^=D[j]
   else:D[j]=b;break
 return len(D)
for rr in (2,3):
 for piv in itertools.combinations(range(n),rr):
  non=[j for j in range(n) if j not in piv];free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
  for z in range(1<<len(free)):
   B=[1<<p for p in piv]
   for k,(i,j) in enumerate(free):
    if z>>k&1:B[i]^=1<<j
   H=[0]
   for b in B:H += [x^b for x in H]
   ns=[h for h in range(1,1<<n) if all((h&b).bit_count()%2==0 for b in B)]
   offs=[0]
   for j in non:offs += [x^(1<<j) for x in offs]
   for o in offs:
    pts={x^o for x in H};c=len(SS&pts)
    if (rr,c) not in ((2,4),(3,6)):continue
    for h in ns:F[h,(h&o).bit_count()%2,rr,c].append((B,o,pts))
print('generated',sum(len(a) for a in F.values()),flush=True)
found=None
for h in range(1,1<<n):
 for ep in range(2):
  for B1,o1,p1 in F[h,ep,3,6]:
   for B3,o3,p3 in F[h,1-ep,2,4]:
    for B2,o2,p2 in F[h,1-ep,2,4]:
     if rank(B2+B1)!=5 or rank(B2+B3)!=4 or p2&p3:continue
     found={'normal':h,'outer_side':ep,'core':S,'outer':(B1,o1),'center':(B2,o2),'inner':(B3,o3)};break
    if found:break
   if found:break
  if found:break
 if found:break
print('FOUND',found,flush=True)
if found:
 def pts(B,o):
  p=[o]
  for b in B:p += [x^b for x in p]
  return set(p)
 E={b+(t<<n) for b in S for t in range(16)}
 B1,o1=found['outer'];B2,o2=found['center'];B3,o3=found['inner']
 for w in range(1,1<<n):
  if (w&found['normal']).bit_count()%2 or rank(B2+B3+[w])!=5:continue
  A1=pts(B1+[1<<j for j in range(n,n+4)],o1)
  A2=pts(B2+[1<<j for j in range(n+4,15)],o2)
  A3=pts(B3+[1<<j for j in range(n,n+4)]+[(1<<(n+4))^w],o3)
  T=A1^A2^A3;out=E^T
  print('ACTUALweights',len(E),len(T),len(E&T),len(out),'pairints',len(A1&A2),len(A2&A3),len(A1&A3),flush=True)
  if len(out)==310:
   found['support']=sorted(out);found['extra']=w;found['component_supports']={'E':sorted(E),'A1':sorted(A1),'A2':sorted(A2),'A3':sorted(A3)}
   pathlib.Path('workspace/agent3_ACTUAL310_candidate.json').write_text(json.dumps(found,indent=2));break
pathlib.Path('workspace/agent3_W2_256_Q382_310_constructor.py').write_text(pathlib.Path('scratchpad.py').read_text())
