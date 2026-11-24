import pathlib
s=pathlib.Path('workspace/agent3_W3_256_Q382_310_constructor.py').read_text()
# only modify shared affine-flat generation to dimensions2/3, targetcounts and nested search manually later.
a=s.index('for piv in itertools.combinations(range(7),3):');b=s.index("print('goodhalves'")
gen=s[a:b]
gen=gen.replace('for piv in itertools.combinations(range(7),3):','for rr in (2,3):\n for piv in itertools.combinations(range(7),rr):')
# indent old body after firstline extra one space
ls=gen.splitlines(); gen='\n'.join(ls[:2]+[' '+l for l in ls[2:]])+'\n'
gen=gen.replace('c not in (4,5)','c not in (4,6)').replace('F[h,(h&o).bit_count()%2,c]','F[h,(h&o).bit_count()%2,rr,c]')
head=s[:a];tail='''
print('generated',sum(len(a) for a in F.values()),flush=True)
found=None
for h in range(1,128):
 for ep in range(2):
  for B1,o1,p1 in F[h,ep,3,6]:
   for B3,o3,p3 in F[h,1-ep,2,4]:
    for B2,o2,p2 in F[h,1-ep,3,4]:
     if rank(B2+B1)!=6 or rank(B2+B3)!=5 or p2&p3:continue
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
 E={b+(t<<7) for b in S for t in range(16)}
 B1,o1=found['outer'];B2,o2=found['center'];B3,o3=found['inner']
 for w in range(1,128):
  if (w&found['normal']).bit_count()%2 or rank(B2+B3+[w])!=6:continue
  # center outside coords11..14; inner extra outside11 plus w
  A1=pts(B1+[1<<j for j in range(7,11)],o1)
  A2=pts(B2+[1<<j for j in range(11,15)],o2)
  A3=pts(B3+[1<<j for j in range(7,11)]+[(1<<11)^w],o3)
  T=A1^A2^A3;out=E^T
  print('ACTUALweights',len(E),len(T),len(E&T),len(out),'pairints',len(A1&A2),len(A2&A3),len(A1&A3),flush=True)
  if len(out)==310:
   found['support']=sorted(out);found['extra']=w;found['component_supports']={'E':sorted(E),'A1':sorted(A1),'A2':sorted(A2),'A3':sorted(A3)}
   pathlib.Path('workspace/agent3_ACTUAL310_candidate.json').write_text(json.dumps(found,indent=2));break
pathlib.Path('workspace/agent3_W3_256_Q382_310_constructor2.py').write_text(pathlib.Path('scratchpad.py').read_text())
'''
s=head+gen+tail
pathlib.Path('workspace/agent3_W3_256_Q382_310_constructor2.py').write_text(s)
exec(compile(s,'construct2','exec'))
