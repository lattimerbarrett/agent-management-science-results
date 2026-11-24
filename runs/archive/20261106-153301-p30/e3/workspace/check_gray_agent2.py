import math,itertools,json,os

def v2(n):
    assert n>0
    return (n & -n).bit_length()-1

def gray_counts(m):
    # A mass interval must traverse a Hamiltonian path in the square:
    # its flip sequence is ABA or BAB. Concatenation determines all signs.
    counts={}
    for word in itertools.product((0,1),repeat=2*m):
        a=sum(2 if t==0 else 1 for t in word)
        b=6*m-a
        counts[(a,b)]=counts.get((a,b),0)+1
    return counts

def main():
    results=[]
    for s in range(3,16):
        m=2**(s-1)-1;j=2*m;d=3*m
        c=math.comb(2*m,m);a=math.comb(2*m,m-1)
        cat=c//(m+1)
        assert c%(m+1)==0
        assert c-a==cat
        assert v2(c)==s-1
        assert v2(c//2)==s-2
        assert cat%2==a%2==1
        results.append(dict(s=s,m=m,j=j,d=d,v2_raw=v2(c),v2_D8_orbits=v2(c//2),catalan_odd=True,asymmetric_odd=True))
    for m in (1,2,3,4,5,6,7):
        counts=gray_counts(m)
        assert counts[(3*m,3*m)]==math.comb(2*m,m)
        assert counts[(3*m-1,3*m+1)]==math.comb(2*m,m+1)
        assert counts[(3*m+1,3*m-1)]==math.comb(2*m,m-1)
        # No path ABC with just two labels can visit every square vertex;
        # enumerating proves ABA and BAB are the only three-edge paths.
    good=[]
    for flips in itertools.product((0,1),repeat=3):
        x=(0,0);states=[x]
        for f in flips:
            x=tuple(x[i]^(i==f) for i in (0,1));states.append(x)
        if len(set(states))==4:good.append(flips)
    assert good==[(0,1,0),(1,0,1)]
    print(json.dumps(results,indent=2))
    print('Verified Hamiltonian flip paths:',good)
    print('All checks passed; these are parity diagnostics, NOT an upper-bound proof.')

if __name__=='__main__':
    import shutil
    os.makedirs('workspace',exist_ok=True)
    shutil.copyfile(__file__,'workspace/check_gray_agent2.py')
    main()
