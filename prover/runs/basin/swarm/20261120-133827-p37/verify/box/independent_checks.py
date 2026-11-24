from math import comb

def chains(n):
    cs=[[0]]
    for i in range(n):
        z=1<<i
        nc=[]
        for c in cs:
            nc.append(c+[c[-1]|z])
            if len(c)>1: nc.append([x|z for x in c[:-1]])
        cs=nc
    return cs

for n in range(13):
    cs=chains(n)
    loc={x:len(c) for c in cs for x in c}
    assert len(loc)==1<<n
    assert sum(map(len,cs))==1<<n
    assert len(cs)==comb(n,n//2)
    for c in cs:
        assert c[0].bit_count()+c[-1].bit_count()==n
        for a,b in zip(c,c[1:]):
            assert a & b==a and b.bit_count()==a.bit_count()+1
        for a,b in zip(c,c[2:]):
            diff=b^a
            mid=[a|(1<<i) for i in range(n) if diff>>i&1]
            assert any(loc[x]<len(c) for x in mid)
print('Independent verification: special symmetric chain property holds through n=12.')

# Independent exact count of cutting-group sets via subset enumeration,
# cross-checking the binomial-sum implementation and entropy component graphs.
import sys
sys.path.insert(0,'agents/agent_1')
import scratchpad as team
for n in range(8,17):
    gg=team.groups(n)
    groups=[]; k=0
    for g in gg:
        groups.append(((1<<g)-1)<<k); k+=g
    full=(1<<n)-1
    T=[s for s in range(1<<n) if s.bit_count()==n//2 and all(s&g and (full^s)&g for g in groups)]
    expected=sum(bool(s&1) for s in T) if n%2 else len(T)//2
    assert team.bit_count_construction(n)==expected
    if n in (9,11,13):
        L=[s for s in T if s&1]
        R=[s for s in T if not s&1]
        degrees=[sum(not(s&t) for t in R if s!=t) for s in R]
        assert max(degrees)<=1
        e=sum(degrees)//2; z=degrees.count(0)
        args=(5,13709,7219) if n==9 else (10,9219,4689)
        _,shape=team.odd_log_lower(n,*args)
        assert shape==(len(L),e,z)
print('Independent subset enumeration agrees on cutting counts for 8<=d<=16 and entropy graph decompositions for d=9,11,13.')
