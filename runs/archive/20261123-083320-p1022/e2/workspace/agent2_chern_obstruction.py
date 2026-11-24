"""Independent Chern-class obstruction for the explicit P5 example.
Conditional only on the standard elementary classification of homogeneous
rank<10 bundles on P5 into lines and at most one tangent/cotangent block.
"""
from fractions import Fraction
from itertools import product

def c2_from(c1,power_sum_two):
    ans=Fraction(c1*c1-power_sum_two,2)
    assert ans.denominator==1
    return int(ans)

def main():
    # Q has rank5, c1=1,c2=1, hence sum root squares=-1.
    q_rank,q_c1,q_p2=5,1,-1
    # For roots x_i+x_j, p2=(r-2)p2(Q)+c1(Q)^2.
    f_c1=(q_rank-1)*q_c1
    f_p2=(q_rank-2)*q_p2+q_c1*q_c1
    assert (f_c1,c2_from(f_c1,f_p2))==(4,9)
    target=sorted([1]*4+[0]*5)
    candidates=[]
    # All line factors have degree 0 or 1. A rank5 Q(t) or Q*(t)
    # block can match target only at t=0 or t=1, respectively.
    for kind in ('lines','Q','Qdual'):
        for t in range(-2,4):
            if kind=='lines':
                if t!=0: continue
                block=[]
                block_c1=block_p2=0
            elif kind=='Q':
                block=[t+1]+[t]*4
                block_c1=q_c1+5*t
                block_p2=q_p2+2*t*q_c1+5*t*t
            else:
                block=[t-1]+[t]*4
                block_c1=-q_c1+5*t
                block_p2=q_p2-2*t*q_c1+5*t*t
            for degrees in product((0,1),repeat=9-len(block)):
                if sorted(block+list(degrees))!=target:continue
                c1=block_c1+sum(degrees)
                p2=block_p2+sum(d*d for d in degrees)
                candidates.append((kind,t,c2_from(c1,p2)))
    results=set(candidates)
    assert results=={('lines',0,6),('Q',0,7),('Qdual',1,7)}
    assert all(c2!=9 for _,_,c2 in results)
    print('E has c1=4,c2=9; all matching homogeneous candidates:',sorted(results))
if __name__=='__main__': main()
