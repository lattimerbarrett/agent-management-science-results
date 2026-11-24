from itertools import product
# Types C_i (core propercolor i), A_i and B_i reservoir sides.
types=list(product('CAB',range(3)))
def allowed(x,y):
    a,i=x;b,j=y
    if a==b=='C':return i!=j
    if i!=j:return False
    return {a,b} in ({'A','B'},{'C','B'})
for ell in (3,5):
    total=0; core=0; shortcut=0
    for seq in product(types,repeat=ell):
        if not all(allowed(seq[i],seq[(i+1)%ell]) for i in range(ell)):continue
        total+=1
        if all(a=='C' for a,i in seq):
            core+=1
            continue
        # Every non-core possible odd short cycle must be a length-2
        # reservoir shortcut plus a 3-edge core path. Its endpoints
        # share B_i and so contradict palette independence in odd cube.
        assert ell==5
        bb=[i for i,x in enumerate(seq) if x[0]=='B']
        assert len(bb)==1
        j=bb[0]
        assert all(seq[(j+k)%ell][0]=='C' for k in range(1,5))
        assert seq[(j+1)%ell][1]==seq[(j+4)%ell][1]==seq[j][1]
        shortcut+=1
    print('length',ell,'allowed type cycles',total,'all-core',core,'forbidden palette-shortcut',shortcut)
print('All type assignments exhausted: 9^3 + 9^5 =',9**3+9**5)
open('workspace/agent3_cycle_type_audit.py','w').write(open('scratchpad.py').read())
