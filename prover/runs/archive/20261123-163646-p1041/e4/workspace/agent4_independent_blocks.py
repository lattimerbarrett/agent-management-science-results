from itertools import product
from math import comb,prod

def data(ns,target=310):
    cells=list(product(*(range(n+1) for n in ns)));index={v:i for i,v in enumerate(cells)};rows=[]
    for ij in cells:
        if sum(ij)<=7:continue
        mask=0
        for u in product(*(range(i+1) for i in ij)):
            if all(u0&i==u0 for u0,i in zip(u,ij)):mask^=1<<index[u]
        rows.append(mask)
    weights=[prod(comb(n,i) for n,i in zip(ns,ij)) for ij in cells]
    rows +=[1<<i for i,w in enumerate(weights) if w>target]
    piv={}
    for row in rows:
        while row:
            i=row.bit_length()-1
            if i in piv:row^=piv[i]
            else:piv[i]=row;break
    basis=[]
    for j in range(len(cells)):
        if j in piv:continue
        mask=1<<j
        for i in sorted(piv):
            if (mask&piv[i]).bit_count()%2:mask^=1<<i
        assert all((mask&row).bit_count()%2==0 for row in rows)
        basis.append(mask)
    return weights,cells,basis
if __name__=='__main__':
    for ns in [(4,5,5),(3,5,6),(4,4,6)]:
        weights,cells,basis=data(ns);print(ns,len(weights),len(basis))
