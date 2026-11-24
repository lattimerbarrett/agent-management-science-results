from itertools import combinations
import json
# x_i=0,1,2; v=3; q12=4,q13=5,q23=6.
x=[0,1,2]; v=3; q={(0,1):4,(0,2):5,(1,2):6}
classes=[]
for i in range(3):
 j,k=[a for a in range(3) if a!=i]
 classes.append([{i,v,q[tuple(sorted((j,k)))]},{i,q[tuple(sorted((i,j)))],q[tuple(sorted((i,k)))]}])
def tau(H):
 for s in range(8):
  for C in combinations(range(7),s):
   if all(set(C)&E for E in H):return s
H=sum(classes,[])
assert all(len(E)==3 for E in H)
assert all(E&F for E,F in combinations(H,2))
assert tau(H)==3
assert all(set.intersection(*Fi)=={i} for i,Fi in enumerate(classes))
H0=[E for E in H if v not in E]
assert tau(H0)==2
bad=[]
for size in range(1,4):
 for I in combinations(range(3),size):
  K=[E for i in I for E in classes[i] if v not in E]
  if tau(K)<len(I):bad.append(list(I))
minimal=[I for I in bad if not any(set(J)<set(I) for J in bad)]
assert minimal==[[0,1],[0,2],[1,2]]
assert all(tau([E for j in range(3) if j!=i for E in classes[j] if v not in E])==1 for i in range(3))
result=dict(classes=[[sorted(E) for E in Fi] for Fi in classes],tau=3,tau_avoid_v=2,minimal_bad_coalitions=minimal,pruning_cost=2)
print(json.dumps(result,indent=2))
Path=__import__('pathlib').Path
Path('workspace/agent3_fano_pruning_checks.json').write_text(json.dumps(result,indent=2))
