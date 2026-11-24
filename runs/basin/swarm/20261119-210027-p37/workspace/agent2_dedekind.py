"""Compute Dedekind numbers D6,D7 exactly in about ten seconds."""
import os,pickle

def certify_d6_d7(cache=None):
    if cache and os.path.exists(cache):
        ideals,up,down=pickle.load(open(cache,'rb'))
    else:
        ideals=[0,1] # ideals of B0
        for n in range(1,6):
            shift=1<<(n-1)
            ideals=[a|(b<<shift) for a in ideals for b in ideals if b&a==b]
        assert len(ideals)==7581
        up=[sum(1<<j for j,b in enumerate(ideals) if a&b==a) for a in ideals]
        down=[sum(1<<j for j,b in enumerate(ideals) if a&b==b) for a in ideals]
        if cache:pickle.dump((ideals,up,down),open(cache,'wb'))
    D6=sum(x.bit_count() for x in up)
    D7=0
    for i,mask in enumerate(up):
        while mask:
            low=mask&-mask;j=low.bit_length()-1;mask-=low
            D7+=(up[i]&down[j]).bit_count()**2
    assert (D6,D7)==(7828354,2414682040998)
    return D6,D7

if __name__=='__main__':print(certify_d6_d7())
