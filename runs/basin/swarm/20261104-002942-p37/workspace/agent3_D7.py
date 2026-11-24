"""Exact D(7) certificate via Boolean-lattice ideals and crown maps.
No stored Dedekind numbers are inputs.
"""
import itertools, numpy as np, time

def ideals_B4():
    down=[sum(1<<y for y in range(16) if y&x==y) for x in range(16)]
    return [mask for mask in range(1<<16) if all(not(mask>>x&1) or mask&down[x]==down[x] for x in range(16))]

def compute_D7():
    L=ideals_B4(); assert len(L)==168
    answer=0; intervals=0; cubes=0
    for T in L:
        Q=[x for x in L if x&T==x]
        union=np.bitwise_or(np.array(Q,dtype=np.uint64)[:,None],np.array(Q,dtype=np.uint64)[None,:])
        C=np.zeros((len(Q),len(Q)),dtype=np.int64)
        for z in Q:C+=(union & np.uint64(z))==union
        for B in Q:
            inds=[i for i,x in enumerate(Q) if x&B==B]
            M=C[np.ix_(inds,inds)]
            # sum M_xy M_yz M_zx = trace(M^3); entries are nonnegative
            answer+=int(np.sum((M@M)*M.T))
            intervals+=1;cubes+=len(inds)**3
    return answer,intervals,cubes

if __name__=='__main__':
    t=time.time(); result=compute_D7()
    assert result[0]==2414682040998
    print('computed D7, interval count, cubic work units:',result)
    print('seconds:',time.time()-t)
