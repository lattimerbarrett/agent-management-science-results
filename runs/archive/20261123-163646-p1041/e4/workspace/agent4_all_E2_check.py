"""All weight-two outside restrictions of RM(6,12), shortened near D304.
This is exact linear algebra, not a search restricted to affine flats.
"""
import json,itertools,collections

def classes(D):
    S=set(D['support'])
    mons=[sum(1<<j for j in js) for k in range(6) for js in itertools.combinations(range(12),k)]
    index={m:i for i,m in enumerate(mons)}
    cols=[]
    for x in range(4096):
        col=0;s=x
        while True:
            if s in index:col|=1<<index[s]
            if not s:break
            s=(s-1)&x
        cols.append(col)
    piv={}
    for x in S:
        c=cols[x]
        while c:
            i=c.bit_length()-1
            if i in piv:c^=piv[i]
            else:piv[i]=c;break
    order=sorted(piv,reverse=True);C=collections.defaultdict(list)
    for x,c in enumerate(cols):
        if x in S:continue
        for i in order:
            if c>>i&1:c^=piv[i]
        assert c # outside singleton would contradict orthogonality to constant+D
        C[c].append(x)
    return len(piv),[v for v in C.values() if len(v)>1]
if __name__=='__main__':
    data=json.load(open('workspace/agent4_fullD304.json'))
    for i,D in enumerate(data):
        rank,C=classes(D)
        expected=[[32,33],[64,65],[96,97],[128,129]] if i==0 else []
        assert C==expected,(i,C)
        print(D['venn'],'D-column rank',rank,'all outside-pair classes',C)
