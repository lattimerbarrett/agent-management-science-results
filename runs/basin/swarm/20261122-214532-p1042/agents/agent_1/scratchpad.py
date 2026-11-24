import itertools as it
import math, heapq
from collections import Counter
from functools import reduce

C = (1,3,9,24,54)
def sizes(m):
    return [math.comb(m,u)*sum(math.comb(m-u,a)*C[a]
             for a in range(5-u)) for u in range(5)]

def complex_data(m):
    cells=[[] for _ in range(5)]
    for s in range(5):
      for J in it.combinations(range(m),s):
       for colors in it.product(range(4),repeat=s):
        if any(colors.count(c)>2 for c in (1,2,3)): continue
        masks=tuple(sum(1<<j for j,c in zip(J,colors) if c==r)
                    for r in range(4))
        cells[masks[0].bit_count()].append(masks)
    ix=[{c:i for i,c in enumerate(cs)} for cs in cells]
    out={}; inc={}
    for k in range(4):
      for col,(U,*A) in enumerate(cells[k]):
       S=U|A[0]|A[1]|A[2]
       for j in range(m):
        bit=1<<j
        if U&bit: continue
        if S.bit_count()==4 and not ((A[0]|A[1]|A[2])&bit):continue
        dest=(U|bit,)+tuple(x&~bit for x in A)
        row=ix[k+1][dest]
        sign=(-1)**(j-(U&(bit-1)).bit_count())
        a=(k,col); b=(k+1,row)
        out.setdefault(a,{})[b]=sign
        inc.setdefault(b,{})[a]=sign
    assert list(map(len,cells))==sizes(m)
    # Verify the boundary squares to zero, integrally.
    for a,da in out.items():
      dd={}
      for b,v in da.items():
       for c,w in out.get(b,{}).items():dd[c]=dd.get(c,0)+v*w
      assert all(v==0 for v in dd.values())
    # Verify that the degree-zero matrix is exactly the 0/1 matrix in the answer.
    for col,(_, *A) in enumerate(cells[0]):
      for (k,row),v in out.get((0,col),{}).items():
       U,*B=cells[1][row];j=U.bit_length()-1
       assert v==(-1)**j
       assert A==B or (all((x&~(1<<j))==y for x,y in zip(A,B))
                               and sum(x.bit_count() for x in A)==1+sum(x.bit_count() for x in B))
    return cells,out,inc

def unit_reduce(cells,out,inc):
    alive=set((k,j) for k,cs in enumerate(cells) for j in range(len(cs)))
    heap=[];counter=0; cancelled0=0
    def push(a):
      nonlocal counter
      for b,v in out.get(a,{}).items():
       if abs(v)==1:
        counter+=1
        heapq.heappush(heap,((len(out[a])-1)*(len(inc[b])-1),counter,a,b))
    for a in out:push(a)
    while heap:
      cost,_,a,b=heapq.heappop(heap)
      v=out.get(a,{}).get(b,0)
      if abs(v)!=1:continue
      now=(len(out[a])-1)*(len(inc[b])-1)
      if now>cost:
       push(a);continue
      acol=dict(out[a]);brow=dict(inc[b]);changed=set()
      # Integral unit-pivot Schur complement: this is an exact chain contraction.
      for x,w in brow.items():
       if x==a:continue
       for y,z in acol.items():
        if y==b:continue
        old=out[x].get(y,0);new=old-w*v*z
        if new:
         out[x][y]=new;inc.setdefault(y,{})[x]=new
        elif old:
         del out[x][y];del inc[y][x]
        changed.add(x)
      if a[0]==0:cancelled0+=1
      for p in (a,b):
       for y in list(out.get(p,{})):
        del inc[y][p];changed.update(inc[y])
       for x in list(inc.get(p,{})):
        del out[x][p];changed.add(x)
       out.pop(p,None);inc.pop(p,None);alive.remove(p)
      for x in changed:push(x)
    return alive,out,cancelled0

def invariants(m):
    cells,out,inc=complex_data(m)
    alive,out,c0=unit_reduce(cells,out,inc)
    aa=sorted(a for a in alive if a[0]==0)
    bb=sorted(b for b in alive if b[0]==1)
    rows=[[out.get(a,{}).get(b,0) for a in aa] for b in bb]
    nonzero=[(i,j,x) for i,row in enumerate(rows) for j,x in enumerate(row) if x]
    if not nonzero: rank=0;tors=[]
    else:
      i,j,p=nonzero[0]
      # An exact, inexpensive rank-one certificate, when applicable.
      if all(p*rows[k][l]==rows[k][j]*rows[i][l]
             for k in range(len(bb)) for l in range(len(aa))):
       rank=1
       g=reduce(math.gcd,(abs(x) for _,_,x in nonzero))
       tors=[g] if g>1 else []
      else:
       from sympy import Matrix, ZZ
       from sympy.matrices.normalforms import smith_normal_form
       T=smith_normal_form(Matrix(rows),domain=ZZ)
       d=[abs(int(T[i,i])) for i in range(min(T.shape)) if T[i,i]]
       rank=len(d);tors=[x for x in d if x>1]
    b=sizes(m);r=c0+rank
    E=(m**4+14*m**3-m*m+34*m+24)//24
    s=b[1]-b[2]+b[3]-b[4]-r
    assert b[0]-r==s+E and s>=0
    # In these test cases the reduced complex has just degrees 0 and 1.
    if m<=9:
      assert all(k<=1 for k,j in alive)
      assert len(aa)-rank==s+E and len(bb)-rank==s
    return s,s+E,tors

def other_checks(m):
    # Color enumeration used in the five chain-group dimensions.
    assert tuple(sum(all(w.count(c)<=2 for c in range(3))
             for w in it.product(range(3),repeat=a)) for a in range(5))==C
    # Check the single-coordinate exchanges that prove the shelling.
    for f in it.product(range(4),repeat=m):
      # The other shelling: bounded first three rows, unbounded row 4.
      if all(f.count(c)<=2 for c in range(3)):
       assert f.count(3)>0
       for j in range(m):
        if f[j]!=3:
         g=f[:j]+(3,)+f[j+1:]
         assert all(g.count(c)<=2 for c in range(3))
         assert g.count(3)==f.count(3)+1
      if f.count(3)>m-5:continue
      for j in range(m):
       for c in range(f[j]):
        g=f[:j]+(c,)+f[j+1:]
        assert g.count(3)<=m-5
    # Check the specified unit preimages for every basis vector of Q^1.
    for r in (1,2,3):
      s=1+r%3
      for T in it.combinations(range(m),3):
       for j in set(range(m))-set(T):
        A={x:r for x in T};A[j]=s
        bad_boundaries=[]
        for x in A:
          B={y:c for y,c in A.items() if y!=x}
          if any(list(B.values()).count(c)>=3 for c in (1,2,3)):
           bad_boundaries.append((x,B))
        assert bad_boundaries==[(j,{x:r for x in T})]

if __name__=='__main__':
    import sympy as sp
    x=sp.symbols('x')
    binom=lambda n,k:sp.prod(n-i for i in range(k))/sp.factorial(k)
    bs=[binom(x,u)*sum(binom(x-u,a)*C[a] for a in range(5-u)) for u in range(5)]
    assert sp.expand(sum((-1)**u*bs[u] for u in range(5))-(x**4+14*x**3-x*x+34*x+24)/24)==0
    for m,expected in [(7,(0,309,[2])),(8,(14,493,[2])),(9,(42,751,[2]))]:
      other_checks(m)
      ans=invariants(m)
      assert ans==expected
      print(m,ans,flush=True)
