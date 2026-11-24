from fractions import Fraction as Q
from itertools import product, permutations
modes=((0,0),(1,0),(-1,0),(0,1),(0,-1),(1,3),(-1,-3))
perms=list(permutations(range(4)))
def det4(A):
    total=Q(0)
    for p in perms:
        inversions=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        value=Q((-1)**inversions)
        for i in range(4): value*=A[i][p[i]]
        total+=value
    return total
nonzero=[]
c=Q(0)
closed=0
for steps in product(modes,repeat=5):
    if tuple(map(sum,zip(*steps))) != (0,0): continue
    closed+=1
    qs=[]; x=y=0
    for dx,dy in steps[:4]:
        x+=dx; y+=dy
        qs.append((x,y))
    if any(x==0 for x,y in qs): continue
    W=[[Q(i*x*x,4*(i*x*x+y*y)) for i in range(1,5)] for x,y in qs]
    determinant=det4(W)
    if determinant:
        weight=Q(1)
        for step in steps: weight*=Q(1,2) if step==(0,0) else Q(1,12)
        nonzero.append((steps,determinant))
        c+=2*weight*determinant
print('Closed paths:',closed)
print('Nonzero paths:',nonzero)
print('Total coefficient:',c)
assert len(nonzero)==4 and c==Q(1,531372441600)
