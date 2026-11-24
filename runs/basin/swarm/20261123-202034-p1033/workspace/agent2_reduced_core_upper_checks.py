from pathlib import Path
import itertools as it,json,time
start=time.time();n=8;m=2;T=n*m;c=T-n+1;r=n-2*m;ell=m*(2*m-1);D=r+ell;k=c+D;s=k-T
E=list(it.combinations(range(n),2));ix={e:j for j,e in enumerate(E)};b=0;count=0;minimum=100
for q in range(n):
 for seq in it.combinations(range(len(E)),q):
  A=set(seq);deg=[0]*n
  for j in seq:
   x,y=E[j];deg[x]+=1;deg[y]+=1
  required=0
  for a in range(n):
   if a==b:
    if deg[a]<2*m:required+=m-1
   elif deg[a]<2*m and ix[tuple(sorted((a,b)))] not in A:required+=m
  assert q+required>=n-1
  minimum=min(minimum,q+required);count+=1
assert 2*c>T and k>=T
result={'n':n,'m':m,'T':T,'core_size':c,'r':r,'ell':ell,'D':D,'k':k,'rank_excess':s,'all_actual_sets_size_at_most_n_minus_1':count,'minimum_actual_plus_required_partial_cores':minimum,'seconds':time.time()-start}
Path('workspace/agent2_reduced_core_upper_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_reduced_core_upper_checks.json').write_text(json.dumps(result,indent=2));print(result)
