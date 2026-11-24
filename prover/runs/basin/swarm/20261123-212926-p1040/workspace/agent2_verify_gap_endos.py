import sys,json
sys.path.insert(0,'workspace')
from agent2_source_relations import generators,extend,cat,inv
from agent2_cubic_source import compose
D=json.load(open('workspace/agent4_gap_ia3_data.json'));G=generators(3);gi={g:i+1 for i,g in enumerate(G)};unit=((1,),(2,),(3,));conv={}
for k,g in enumerate(D['names'],1):
    typ,*a=g;a=[x-1 for x in a]
    if typ=='C':conv[k]=(gi[(typ,*a)],)
    else:
        i,j,l=a;b=gi['C',i,j];c=gi['C',i,l];m=gi['M',i,j,l];conv[k]=(-c,-b,c,b,m)
def evaluate(w):
    A=unit
    for x in w:A=extend(A,G[abs(x)-1],1 if x>0 else -1)
    return A
def convert(w):return cat(*(conv[x] if x>0 else inv(conv[-x]) for x in w[::-1]))
base=[evaluate(conv[k]) for k in range(1,10)]
for e in D['endomorphisms']:
    name=e['name']
    if name=='I1':S=((-1,),(2,),(3,));Si=S
    elif name.startswith('M12'):
        sa,sb=map(int,name[4:-1].split(','));alpha=1 if sa==0 else -1;beta=1 if sb==0 else -1
        # (xb^beta * xa^alpha)^alpha
        w=(beta*2,alpha*1);w=w if alpha==1 else inv(w)
        S=(w,(2,),(3,))
        wi=((-beta*2,1) if alpha==1 else (1,beta*2));Si=(wi,(2,),(3,))
        assert compose(S,Si)==unit
    else:continue
    flags=[True,True];bad=[]
    for k,A in enumerate(base):
        B=evaluate(convert(e['images'][k]))
        f=B==compose(compose(S,A),Si);g=B==compose(compose(Si,A),S)
        flags[0]&=f;flags[1]&=g
        if not(f or g):bad.append(k+1)
    print(name,'consistent conjugation directions',flags,'bad gens',bad,flush=True)
