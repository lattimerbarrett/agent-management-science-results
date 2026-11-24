from pathlib import Path
import itertools as it, random, json, time
start=time.time(); rng=random.Random(295); results=[]
for n,m in [(4,1),(8,2)]:
 T=n*m;r=n-2*m;ell=m*(2*m-1);D=r+ell;k=T+D
 E=list(it.combinations(range(n),2)); ix={e:j for j,e in enumerate(E)}; stars=[set(j for j,e in enumerate(E) if a in e) for a in range(n)]
 base=[]
 for a in range(n):
  for P in it.combinations(stars[a],r):
   P=set(P); omitted=[b for b in range(n) if b!=a and ix[tuple(sorted((a,b)))] not in P]
   targets={b*m+c for b in omitted for c in range(m)}
   assert len(targets)==ell
   for c in range(m):base.append((a*m+c,P,targets))
 paircount=0
 for j,(i,P,L) in enumerate(base):
  for q,Q,M in base[j+1:]:
   assert i==q or P&Q or q in L or i in M
   paircount+=1
 def activate(A):
  deg=[sum(e in A for e in stars[a]) for a in range(n)]
  J={i for i in range(T) if deg[i//m]>=2*m}
  assert len(J)<=len(A)
  return J
 if n==4:
  for mask in range(1<<len(E)):
   A={j for j in range(len(E)) if mask>>j&1};J=activate(A)
   assert J=={i for i in range(T) if all(P&A for j,P,L in base if j==i)}
  # All members including independent target-core choices.
  cores=[set(range(len(E)+i*T,len(E)+(i+1)*T)) for i in range(T)]
  final=[]
  for i,P,L in base:
   for choices in it.product(*(cores[j] for j in sorted(L))):
    F=cores[i]|P|set(choices); assert len(F)==k;final.append(F)
  for a,F in enumerate(final):
   for G in final[a+1:]:assert F&G
  U=range(len(E)+T*T); nc=0
  for q in range(T):
   for C in it.combinations(U,q):
    C=set(C);assert any(not F&C for F in final);nc+=1
  for choices in it.product(*cores):assert all(set(choices)&F for F in final)
  additional={'actual_sets':1<<len(E),'final_members':len(final),'all_small_covers_rejected':nc}
 else:
  # Check every graphical degree sequence (the activation count is degree-determined).
  def graphical(seq):
   a=sorted(seq,reverse=True)
   while a and a[0]:
    d=a.pop(0)
    if d>len(a):return False
    for j in range(d):
     a[j]-=1
     if a[j]<0:return False
    a.sort(reverse=True)
   return True
  ng=0
  for seq in it.combinations_with_replacement(range(n),n):
   if graphical(seq):
    assert m*sum(x>=2*m for x in seq)<=sum(seq)//2;ng+=1
  for q in range(20000):
   A={j for j in range(len(E)) if rng.randrange(2)};J=activate(A)
   assert J=={i for i in range(T) if all(P&A for j,P,L in base if j==i)}
  additional={'graphical_degree_sequences':ng,'random_actual_sets_exact_activation':20000}
 results.append(dict(n=n,m=m,T=T,r=r,ell=ell,D=D,k=k,base_petals=len(base),all_base_pairs=paircount,**additional))
 print(results[-1],flush=True)
Path('workspace/agent2_duplicate_center_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_duplicate_center_checks.json').write_text(json.dumps(results,indent=2));print('seconds',time.time()-start)
