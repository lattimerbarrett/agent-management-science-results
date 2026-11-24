from itertools import product
possible=[]
for t,a,b,c,d,u,v in product(range(8),repeat=7):
    if a+b>7 or c+d>7 or u+v>t:continue
    if u>min(a,c) or v>min(b,d):continue
    if a+c-u>7 or b+d-v>7:continue
    if max(a-u,c-u,b-v,d-v)>7-t:continue
    if a+b==7 and c+d==7 and u+v!=t:continue
    I=2**a+2**b+2**c+2**d-2**(u+1)-2**(v+1)
    w=510-2**(t+1)-2*I
    if w==310:possible.append((t,a,b,c,d,u,v))
assert not possible
print('No XOR4 linear7-flat weight310, via necessarydimensionconstraints')
open('workspace/agent2_no_four_linear.py','w').write(open('scratchpad.py').read())