"""Executable certificates for all exceptional low weights of RM(7,14).
Every support is an XOR of affine 7-flats; the checker independently computes
its full 16384-entry truth table and algebraic normal form.
"""
import numpy as np

N=1<<14

def flat(free, shift=0):
    free=tuple(free)
    assert len(free)==7 and len(set(free))==7
    assert all(0<=i<14 for i in free)
    ans=np.zeros(N,dtype=np.uint8)
    for bits in range(128):
        x=shift
        for j,c in enumerate(free):
            if bits>>j&1:x^=1<<c
        ans[x]=1
    assert int(ans.sum())==128
    return ans

def triple(regions):
    t,p,q,s,u,v,z=regions
    memberships=((0,1,2),(0,1),(0,2),(1,2),(0,),(1,),(2,))
    coords=[[],[],[]]
    j=0
    for count,mem in zip(regions,memberships):
        for i in mem:coords[i].extend(range(j,j+count))
        j+=count
    assert j<=14
    return flat(coords[0])^flat(coords[1])^flat(coords[2])

def seeds():
    A=flat(range(7))
    out={0:np.zeros(N,dtype=np.uint8),128:A}
    for dim in range(6):
        B=flat(list(range(dim))+list(range(7,14-dim)))
        out[256-2*(1<<dim)]=A^B
    out[256]=A^flat(range(7),1<<7)
    regs={272:(2,2,2,3,1,0,0),288:(2,1,2,3,2,1,0),
          296:(1,2,2,4,2,0,0),304:(1,1,2,4,3,1,0),
          308:(0,2,2,5,3,0,0)}
    out.update({w:triple(r) for w,r in regs.items()})
    return out

def degree(truth):
    a=truth.copy()
    for bit in range(14):
        step=1<<bit
        blocks=a.reshape(-1,step*2)
        blocks[:,step:]^=blocks[:,:step]
    return max((int(i).bit_count() for i in np.flatnonzero(a)),default=-1)

def main():
    expected={0,128,192,224,240,248,252,254,256,272,288,296,304,308}
    assert set(seeds())==expected
    for w,f in sorted(seeds().items()):
        assert int(f.sum())==w,(w,int(f.sum()))
        deg=degree(f)
        assert deg<=7,(w,deg)
        print(w,deg)
    # Numerical evaluation ONLY of the classical low-weight theorem's chains.
    # This verifies arithmetic, not the structural theorem itself.
    k=7
    chains={2**(k+1)-2**j for j in range(1,k+1)}
    chains|={2**(k+1)}
    chains|={5*2**(k-1)-2**j for j in range(1,k-1)}
    chains|={5*2**(k-1)-3*2**j for j in range(1,k-2)}
    assert {0}|{w for w in chains if w<312}==expected
    print('Low-weight chain arithmetic and all exceptional constructions verified.')

if __name__=='__main__':main()
