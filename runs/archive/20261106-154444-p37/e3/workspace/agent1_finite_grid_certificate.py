"""Exact rational certificate for finite MacMahon upper bounds (no floating point)."""
from math import comb
from fractions import Fraction
import json, time
S=1<<40

def ln_bounds(x, terms=24):
    z=(x-1)/(x+1); p=z; total=Fraction(0)
    for r in range(terms):
        total += 2*p/(2*r+1); p*=z*z
    return total,total+2*p/((2*terms+1)*(1-z*z))
L2,U2=ln_bounds(Fraction(2))
def log2_bounds(j):
    q=j.bit_length()-1
    l,u=ln_bounds(Fraction(j,1<<q))
    low=Fraction(q)+l/U2; high=Fraction(q)+u/L2
    return (low.numerator*S//low.denominator,
            (high.numerator*S+high.denominator-1)//high.denominator)

def hyper_bounds(n):
    lo=[0]*(n+1);hi=[0]*(n+1);fl=fu=0
    for j in range(1,n+1):
        lo[j]=lo[j-1]+fl;hi[j]=hi[j-1]+fu
        l,u=log2_bounds(j);fl+=l;fu+=u
    return lo,hi

def chains(n):
    a=[0]*(n+2)
    for r in range(n//2+1):a[n-2*r+1]=comb(n,r)-(comb(n,r-1) if r else 0)
    return a

def pack(a,bits):
    v=0
    for x in reversed(a):v=(v<<bits)|x
    return v

def unpack(v,bits,size):
    mask=(1<<bits)-1;out=[]
    for _ in range(size):out.append(v&mask);v>>=bits
    assert v==0
    return out

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def grid_upper(m,lo,hi):
    a=m//3;b=(m-a)//2;c=m-a-b
    aa,bb,cc=map(chains,(a,b,c)); sa,sb,sc=map(sum,(aa,bb,cc))
    bits=m+2;pa,pb,pc=(pack(v,bits) for v in (aa,bb,cc))
    ab=unpack(pa*pb,bits,len(aa)+len(bb)-1)
    ac=unpack(pa*pc,bits,len(aa)+len(cc)-1)
    bc=unpack(pb*pc,bits,len(bb)+len(cc)-1)
    abc=unpack(pa*pb*pc,bits,len(aa)+len(bb)+len(cc)-2)
    upper=dot(abc,hi)+dot(aa,hi)*sb*sc+dot(bb,hi)*sa*sc+dot(cc,hi)*sa*sb
    upper-=dot(ab,lo)*sc+dot(ac,lo)*sb+dot(bc,lo)*sa
    return upper

def freebits(d):
    sizes=[d//3,(d+1)//3,(d+2)//3];r=d//2
    if d%2==0:
        # choose r elements, strictly between zero and full in every color
        ways=sum(comb(sizes[0],i)*comb(sizes[1],j)*comb(sizes[2],r-i-j)
                 for i in range(1,sizes[0]) for j in range(1,sizes[1])
                 if 1<=r-i-j<sizes[2])
        assert ways%2==0
        return ways//2
    # r-subsets containing a distinguished point in first color class
    return sum(comb(sizes[0]-1,i-1)*comb(sizes[1],j)*comb(sizes[2],r-i-j)
               for i in range(1,sizes[0]) for j in range(1,sizes[1])
               if 1<=r-i-j<sizes[2])

def main():
    start=time.time();lo,hi=hyper_bounds(1002)
    ds=[12]+list(range(14,1002)); margins=[]
    for d in ds:
        a=freebits(d);u=grid_upper(d-2,lo,hi)
        assert u<a*S,(d,u,a*S)
        margins.append((d,a*S-u))
    result={'checked_d':[12,14,1001],'number_checked':len(ds),
            'all_exact_inequalities_pass':True,'fixedpoint_scale':S,
            'minimum_integer_margin':min(v for d,v in margins),
            'seconds':time.time()-start}
    print(result)
    with open('workspace/agent1_finite_grid_result.json','w') as f:json.dump(result,f,indent=2)
if __name__=='__main__':main()
