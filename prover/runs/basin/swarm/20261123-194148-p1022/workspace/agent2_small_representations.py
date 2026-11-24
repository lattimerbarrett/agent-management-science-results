from fractions import Fraction
from itertools import product
import json

def gl_dimension(a):
    n=len(a)+1
    lam=[sum(a[i:]) for i in range(n-1)]+[0]
    ans=Fraction(1)
    for i in range(n):
        for j in range(i+1,n):
            ans*=Fraction(lam[i]-lam[j]+j-i,j-i)
    assert ans.denominator==1
    return int(ans)

results={}
for n in (2,3,4):
    bound=2*n-1
    reps=[]
    for a in product(range(bound),repeat=n-1):
        d=gl_dimension(a)
        if d<=bound:
            reps.append((a,d))
    expected={2:{((0,),1),((1,),2),((2,),3)},3:{((0,0),1),((1,0),3),((0,1),3)},4:{((0,0,0),1),((1,0,0),4),((0,0,1),4),((0,1,0),6)}}[n]
    assert set(reps)==expected
    results[n]=reps
# Coordinate rank bounds certify this search exhaustive: dim highest-weight irrep
# >= a_i+1 for each Dynkin coordinate a_i (its simple-root sl2 string).
print(json.dumps(results,indent=2))
with open('workspace/agent2_small_representations.json','w') as f:json.dump(results,f,indent=2)
