"""Rigorous interval-exclusion infrastructure (not an exact-two example).
Uses Sage MPFI directed-rounded real intervals.  A successful run certifies
that all fixed points belong to designated neighbourhoods; uniqueness inside
those neighbourhoods requires a separate local argument.
"""
from sage.all import RealIntervalField, QQ
from itertools import product
R=RealIntervalField(80)

def stereographic(box, signs):
    out=[]
    for i,sgn in enumerate(signs):
        u,v=box[2*i:2*i+2]
        d=1+u*u+v*v
        out.extend((2*u/d,2*v/d,sgn*(1-u*u-v*v)/d))
    return tuple(out)

def exclude_fixed(F, centres, radius, max_boxes=1000000, max_depth=80):
    """Return complete=True only if every chart box has been certified.
    F receives six interval coordinates and returns six interval coordinates.
    centres are six-coordinate exact points; radius uses ambient R6 distance.
    Four product charts, with coordinates in [-1,1]^4, cover S2 x S2.
    """
    radius2=R(radius)**2
    centres=[tuple(R(c) for c in p) for p in centres]
    stack=[(sgn,tuple((QQ(-1),QQ(1)) for _ in range(4)),0)
           for sgn in product((-1,1), repeat=2)]
    tested=excluded=local=0
    unresolved=[]
    while stack and tested<max_boxes:
        signs,ends,depth=stack.pop()
        B=tuple(R(a,b) for a,b in ends)
        x=stereographic(B,signs)
        tested+=1
        if any(sum((t-c)**2 for t,c in zip(x,p)).upper()<radius2.lower()
               for p in centres):
            local+=1
            continue
        y=F(x)
        residual=[a-b for a,b in zip(y,x)]
        if any(0 not in a for a in residual):
            excluded+=1
            continue
        if depth==max_depth:
            unresolved.append((signs,ends))
            continue
        j=max(range(4), key=lambda j: ends[j][1]-ends[j][0])
        a,b=ends[j];mid=(a+b)/2
        for pair in ((a,mid),(mid,b)):
            new=list(ends);new[j]=pair
            stack.append((signs,tuple(new),depth+1))
    return dict(complete=not stack and not unresolved,tested=tested,
                excluded=excluded,local=local,remaining=len(stack)+len(unresolved))

def self_test():
    # Actual four-fixed-point Hamiltonian map: rotations pi/2 and pi/3.
    cs1=R.pi().cos() # unused, ensures interval pi available
    a=R.pi()/2;b=R.pi()/3
    ca,sa,cb,sb=a.cos(),a.sin(),b.cos(),b.sin()
    def F(x):
        X,Y,Z,U,V,W=x
        return ca*X-sa*Y,sa*X+ca*Y,Z,cb*U-sb*V,sb*U+cb*V,W
    centres=[(0,0,e,0,0,f) for e,f in product((-1,1), repeat=2)]
    result=exclude_fixed(F,centres,QQ(1)/2,max_boxes=100000)
    assert result['complete'],result
    print('Product-rotation exclusion certified:',result)
if __name__=='__main__': self_test()
