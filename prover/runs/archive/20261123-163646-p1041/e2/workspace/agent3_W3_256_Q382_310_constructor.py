import itertools,collections,json,pathlib,time
S=[]
for a in range(16):
 x=[a>>i&1 for i in range(4)];q=[x[0]*x[1],x[0]*x[2],x[0]*x[3]^x[1]*x[2]]
 S.append(a+sum(v<<(4+j) for j,v in enumerate(q)))
SS=set(S);F=collections.defaultdict(list)
def rank(bs):
 D={}
 for b in bs:
  while b:
   j=b.bit_length()-1
   if j in D:b^=D[j]
   else:D[j]=b;break
 return len(D)
for piv in itertools.combinations(range(7),3):
 non=[j for j in range(7) if j not in piv];free=[(i,j) for i,p in enumerate(piv) for j in non if j>p]
 for z in range(1<<len(free)):
  B=[1<<p for p in piv]
  for k,(i,j) in enumerate(free):
   if z>>k&1:B[i]^=1<<j
  H=[0]
  for b in B:H += [x^b for x in H]
  ns=[h for h in range(1,128) if all((h&b).bit_count()%2==0 for b in B)]
  offs=[0]
  for j in non:offs += [x^(1<<j) for x in offs]
  for o in offs:
   pts={x^o for x in H};c=len(SS&pts)
   if c not in (4,5):continue
   for h in ns:F[h,(h&o).bit_count()%2,c].append((B,o,pts))
print('goodhalves',[(h,len(F[h,0,5]),len(F[h,1,5])) for h in range(1,128) if F[h,0,5] and F[h,1,5]],flush=True)
found=None
for h in range(1,128):
 for ep in range(2):
  for B1,o1,p1 in F[h,ep,5]:
   for B3,o3,p3 in F[h,1-ep,5]:
    for B2,o2,p2 in F[h,1-ep,4]:
     if rank(B2+B1)!=6 or rank(B2+B3)!=6:continue
     inter=p2&p3;assert len(inter)==1
     if inter&SS:continue
     found={'normal':h,'outer_side':ep,'core':S,'outer':(B1,o1),'center':(B2,o2),'inner':(B3,o3),'interpoint':next(iter(inter))};break
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
 E={b+(t<<7) for b in S for t in range(16)}
 A1=pts(found['outer'][0]+[1<<j for j in range(7,11)],found['outer'][1])
 A3=pts(found['inner'][0]+[1<<j for j in range(7,11)],found['inner'][1])
 A2=pts(found['center'][0]+[1<<j for j in range(11,15)],found['center'][1])
 T=A1^A2^A3;out=E^T
 print('ACTUALweights',len(E),len(T),len(E&T),len(out),'pairints',len(A1&A2),len(A2&A3),len(A1&A3),flush=True)
 found['support']=sorted(out);found['component_supports']={'E':sorted(E),'A1':sorted(A1),'A2':sorted(A2),'A3':sorted(A3)}
 pathlib.Path('workspace/agent3_ACTUAL310_candidate.json').write_text(json.dumps(found,indent=2))
pathlib.Path('workspace/agent3_W3_256_Q382_310_constructor.py').write_text(pathlib.Path('scratchpad.py').read_text())
