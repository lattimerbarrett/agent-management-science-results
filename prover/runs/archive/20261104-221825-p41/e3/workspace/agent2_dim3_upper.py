import sys,itertools,random,pathlib
sys.path.insert(0,'workspace')
from agent3_check import *
from agent1_filling import lift_filling_certificate,check_certificate

def prefix_order(F,k,c):
 if c[0]=='simplex':return [(F[0],c)]
 _,s,dc,lc=c;faces=all_faces(F)
 D=maximal(f for f in faces if f&s!=s)
 L=maximal(f^s for f in F if f&s==s)
 return prefix_order(D,k,dc)+[(s|h,('shed',s,dc,hc)) for h,hc in prefix_order(L,k,lc)]

def boundary_extend(F,f,k,c):
 '''Lift k-certificate after adding a facet with all proper faces already old.'''
 if c[0]=='simplex':
  assert F[0].bit_count()==1 and f.bit_count()==1
  return ('shed',f,c,('simplex',0))
 _,s,dc,lc=c;faces=all_faces(F)
 if f&s!=s:
  D=maximal(g for g in faces if g&s!=s)
  return ('shed',s,boundary_extend(D,f,k,dc),lc)
 L=maximal(g^s for g in F if g&s==s)
 return ('shed',s,dc,boundary_extend(L,f^s,k,lc))

def complete_ridges_dim3(F,k):
 '''Certified same-vertex completion of triangle skeleton of k-decomposable pure tetra complex.'''
 F=tuple(sorted(F));G=tuple(sorted({f^(1<<v) for f in F for v in range(f.bit_length()) if f>>v&1}))
 c=k_certificate(G,k);assert c is not None
 start=F[0];C=start;visited={start};todo=set(F)-visited;out=[]
 while todo:
  f=next(f for f in todo if any((f&g).bit_count()==3 for g in visited))
  todo.remove(f);visited.add(f)
  new=f&~C
  assert new.bit_count()<=1
  if not new:continue
  v=new;S=f&C;w=S&-S
  for ubit in [1<<u for u in range(C.bit_length()) if C>>u&1]:
   edge=v|ubit
   if edge not in all_faces(G):
    h=edge|w;assert h.bit_count()==3
    c=('shed',edge,c,('simplex',w));G=tuple(sorted(G+(h,)))
    assert check_certificate(G,k,c)
    out.append((h,c))
  C|=v
  for tri in itertools.combinations([u for u in range(C.bit_length()) if C>>u&1],3):
   h=sum(1<<u for u in tri)
   if h in G:continue
   assert all((h^(1<<u)) in all_faces(G) for u in tri)
   c=boundary_extend(G,h,k,c);G=tuple(sorted(G+(h,)))
   assert check_certificate(G,k,c)
   out.append((h,c))
 return out

def complete_dim3(F,k):
 F=tuple(sorted(F));n=max(f.bit_length() for f in F);a=1<<n
 cert=k_certificate(F,k);assert cert is not None
 G=tuple(sorted({f^(1<<v) for f in F for v in range(n) if f>>v&1}))
 gc=k_certificate(G,k);cur=F;out=[]
 for h,hc in prefix_order(G,k,gc):
  g=a|h;cur=tuple(sorted(cur+(g,)));c=('shed',a,cert,hc)
  assert check_certificate(cur,k,c);out.append(g)
 for h,hc in complete_ridges_dim3(F,k):
  G=tuple(sorted(G+(h,)));cur=tuple(sorted(cur+(a|h,)))
  c=lift_filling_certificate(G,F,a,k,hc)
  assert check_certificate(cur,k,c);out.append(a|h)
 gc=k_certificate(G,0);assert gc is not None
 fills=set(F)
 for tet in itertools.combinations(range(n),4):
  h=sum(1<<v for v in tet)
  if h in fills:continue
  fills.add(h);cur=tuple(sorted(cur+(h,)));c=lift_filling_certificate(G,tuple(sorted(fills)),a,0,gc)
  assert check_certificate(cur,0,c);out.append(h)
 assert len(cur)==len(list(itertools.combinations(range(n+1),4)))
 return out

if __name__=='__main__':
 random.seed(1265);checked=steps=0
 for n in [5,6,7,8]:
  fs=[sum(1<<v for v in s) for s in itertools.combinations(range(n),4)]
  for trial in range(30):
   F=[random.choice(fs)];left=set(fs)-set(F)
   for j in range(random.randint(1,min(20,len(fs)-1))):
    pos=[f for f in left if appendable(F,f)]
    if not pos:break
    h=random.choice(pos);F.append(h);left.remove(h)
   # Vertex set exactly an initial interval by relabeling, and shellable =3decomp.
   used=sorted({v for f in F for v in range(n) if f>>v&1});ren={v:i for i,v in enumerate(used)}
   F=tuple(sorted(sum(1<<ren[v] for v in used if f>>v&1) for f in F))
   k=1 if k_certificate(F,1) is not None else 3
   steps+=len(complete_dim3(F,k));checked+=1
 print('Complete dimension3 construction:',checked,'random shellable inputs;',steps,'additions checked by explicit recursive certificates')
 pathlib.Path('workspace/agent2_dim3_upper.py').write_text(pathlib.Path(__file__).read_text())
