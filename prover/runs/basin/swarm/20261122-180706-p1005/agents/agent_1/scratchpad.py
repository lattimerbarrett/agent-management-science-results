import os,pickle,itertools,time,collections,math
from sage.all import GF

def make(q):
    fn=f'data{q}.pkl'
    # Regenerate all field and geometry data; do not trust cached data.
    p=3 if q==9 else q
    K=GF(q*q,'z'); els=[K.zero(),K.one()]+[x for x in K if x not in (0,1)]; n=q*q
    ix={a:i for i,a in enumerate(els)}
    add=[[ix[a+b] for b in els] for a in els]
    mul=[[ix[a*b] for b in els] for a in els]
    sub=[[ix[a-b] for b in els] for a in els]
    inv=[0]+[ix[1/a] for a in els[1:]]
    fq=[i for i,a in enumerate(els) if a**q==a]
    # circle generation from triples until all found via orbit affine circles
    circles=set()
    for a in els:
        for r in els:
            if not r or r**q!=r: continue
            circles.add(tuple(i for i,z in enumerate(els) if (z-a)**(q+1)==r))
    for a in range(n):
        for b in range(1,n):
            circles.add(tuple(sorted([n]+[add[a][mul[b][s]] for s in fq])))
    circles=sorted(circles)
    assert len(circles)==q*(q*q+1)
    triples=set()
    for C in circles:
        assert len(C)==q+1
        for tri in itertools.combinations(C,3):
            assert tri not in triples
            triples.add(tri)
    assert len(triples)==math.comb(n+1,3)
    masks=[sum(1<<i for i in C) for C in circles]
    through=[sum(1<<j for j,C in enumerate(circles) if i in C) for i in range(n+1)]
    gen=K.multiplicative_generator(); lg={ix[gen**i]:i%(q+1) for i in range(n-1)}
    shifts=[]
    for C in circles:
        if n in C:
            a,c=C[:2]; u=(1,a); v=(0,sub[c][a])
        else:
            a,b,c=C[:3]; lam=mul[sub[c][a]][inv[sub[b][c]]]
            u=(1,a);v=(lam,mul[lam][b])
        ds={}
        for s in fq+[n]:
            if s==n: x,y=v
            else: x=add[u[0]][mul[s][v[0]]];y=add[u[1]][mul[s][v[1]]]
            k=mul[y][inv[x]] if x else n
            ds[k]=lg[x if x else y]
        assert sorted(ds)==list(C)
        shifts.append(ds)
    D=(q,circles,masks,through,shifts,(add,mul,sub,inv,fq))
    pickle.dump(D,open(fn,'wb'));return D

def hemi(D,sol):
    q,C,M,T,ds,_=D;m=q+1
    # parity union find for variables (circle,index)
    g=[[] for _ in range(len(sol)*m)]
    for i,a in enumerate(sol):
        for j in range(i):
            b=sol[j]
            for p in set(C[a])&set(C[b]):
                d=(ds[a][p]-ds[b][p])%m
                for x in range(m):
                    y=(x+d)%m
                    u=i*m+x;v=j*m+y
                    g[u].append(v);g[v].append(u)
    col={}
    for v in range(len(g)):
        if v in col:continue
        col[v]=0; st=[v]
        while st:
            x=st.pop()
            for y in g[x]:
                if y in col:
                    if col[y]==col[x]:return False
                else:col[y]=1-col[x];st.append(y)
    assert all(sum(col[i*m+j] for j in range(m))==m//2 for i in range(len(sol)))
    return True

def affine_group(D):
    q,C,M,T,ds,tables=D;add,mul,sub,inv,fq=tables;n=q*q
    p=3 if q==9 else q; e=4 if q==9 else 2
    lookup={tuple(c):i for i,c in enumerate(C)}
    def power(x,k):
        y=1
        while k:
            if k&1:y=mul[y][x]
            x=mul[x][x];k//=2
        return y
    G=[]
    for j in range(e):
        fr=[power(x,p**j) for x in range(n)]
        for a in fq[1:]:
            for b in fq:
                P=[add[mul[a][fr[x]]][b] for x in range(n)]+[n]
                perm=[lookup[tuple(sorted(P[x] for x in c))] for c in C]
                G.append((P,perm))
    return G

def enum(D,tmax,root=None,frontier=False,jobs=None):
    q,C,M,T,ds,_=D; B=len(C);allc=(1<<B)-1
    root=C.index(tuple(sorted(D[-1][-1]+[q*q]))) if root is None else root
    G=affine_group(D)
    nodes=collections.Counter();out=[];start=time.time()
    maskid={m:i for i,m in enumerate(M)}
    def rec(sol,U,O,A,G):
        k=len(sol);nodes[k]+=1
        if frontier and k==3:
            out.append((sol,U,O,A,G));return
        if not O:
            out.append(tuple(sorted(sol)));return
        r=tmax-k
        if r<=0:return
        if any((M[a]&O).bit_count()>2*r for a in sol):return
        if r==1:
            a=maskid.get(O)
            if a is not None and A>>a&1:out.append(tuple(sorted(sol+[a])))
            return
        # discard any future block unable to close with the remaining r-1 blocks
        lower=q+1-2*(r-1)
        if lower>=4:
            aa=A;A=0
            while aa:
                v=aa&-aa;aa-=v;a=v.bit_length()-1
                if (M[a]&O).bit_count()>=lower:A|=v
        # candidates meeting most constrained open point
        best=None;bc=B+1
        bits=O
        while bits:
            v=bits&-bits;bits-=v;p=v.bit_length()-1
            cs=A&T[p];c=cs.bit_count()
            if not c:return
            if c<bc:best=cs;bc=c;bp=p
        if k==1:bp=q*q;best=A&T[bp];bc=best.bit_count()
        if not bc:return
        if len(G)>1:G=[g for g in G if g[0][bp]==bp]
        sym=len(G)>1
        while best:
            v=best&-best;a=v.bit_length()-1;m=M[a]
            orbit=sum(1<<i for i in set(g[1][a] for g in G)) if sym else v
            best &= ~orbit
            nbase=A&~v
            # remaining sibling branches exclude the whole orbit
            A &= ~orbit
            nO=O^m
            if (m&nO).bit_count()>2*(r-1):continue
            sat=m&O
            nA=nbase
            while sat:
                w=sat&-sat;sat-=w;nA &= ~T[w.bit_length()-1]
            rec(sol+[a],U|m,nO,nA,[g for g in G if g[1][a]==a] if sym else G)
    if jobs is None:
        rec([root],M[root],M[root],allc^(1<<root),G)
    else:
        os.makedirs(f'jobs{q}',exist_ok=True)
        for job,args in jobs:
            fn=f'jobs{q}/{job}.pkl'
            if os.path.exists(fn):continue
            out.clear();rec(*args)
            pickle.dump(out,open(fn,'wb'))
            print('job',job,args[0],round(time.time()-start,1),'out',len(out),flush=True)
    print('nodes',nodes,'out',len(out),flush=True)
    return out

def root_group(D):
    q,C,M,T,ds,tables=D;add,mul,sub,inv,fq=tables;n=q*q
    lookup={tuple(c):i for i,c in enumerate(C)}
    aff=affine_group(D)
    G=[g[1] for g in aff]
    for c in fq:
        P=[inv[sub[x][c]] if x!=c else n for x in range(n)]+[0]
        ip=[lookup[tuple(sorted(P[x] for x in cl))] for cl in C]
        G += [[g[1][ip[a]] for a in range(len(C))] for g in aff]
    assert len(G)==q*(q*q-1)*(4 if q==9 else 2)
    return G

def classes(D,sols):
    q,C,M,T,ds,tables=D;add,mul,sub,inv,fq=tables;n=q*q
    G=root_group(D)
    def canon(s):return min(tuple(sorted(g[a] for a in s)) for g in G)
    rooted=set(canon(s) for s in sols)
    print('rooted classes',q,collections.Counter(map(len,rooted)),flush=True)
    lookup={tuple(c):i for i,c in enumerate(C)}; rebase={}
    def change(s,r):
        if r not in rebase:
            a,b,c=C[r][:3]
            f=mul[sub[c][a]][inv[sub[c][b]]]
            P=[mul[mul[sub[x][b]][inv[sub[x][a]]]][f] if x!=a else n for x in range(n)]+[f]
            rebase[r]=[lookup[tuple(sorted(P[x] for x in cl))] for cl in C]
        g=rebase[r]
        return tuple(sorted(g[a] for a in s))
    ans=[]
    while rooted:
        s=min(rooted)
        orb={canon(change(s,r)) for r in s}
        # every equivalent rooting need not occur in the symmetry-pruned search
        rooted.difference_update(orb)
        ans.append(min(orb))
    print('full classes',q,collections.Counter(map(len,ans)),flush=True)
    print('rooting-orbits',[(len(s),len({canon(change(s,r)) for r in s})) for s in ans],flush=True)
    return ans

if __name__=='__main__':
    import sys
    q=int(sys.argv[1]) if len(sys.argv)>1 else 11
    for q in [5,7,9,11]:
        print('field',q,GF(q*q,'z').modulus(),flush=True)
        D=make(q);st=time.time()
        if q in [5,7,9]:
            out=enum(D,q)
            pickle.dump(out,open(f'uniform{q}.pkl','wb'))
            print('uniform counts',q,collections.Counter(map(len,out)),flush=True)
        else:out=pickle.load(open(f'raw{q}.pkl','rb'))
        assert len(out)==len(set(out))
        for s in out:
            cnt=collections.Counter(p for a in s for p in D[1][a])
            assert set(cnt.values())=={2}
            seen={s[0]}
            while True:
                new={b for b in s if any(D[2][b]&D[2][a] for a in seen)}|seen
                if new==seen:break
                seen=new
            assert len(seen)==len(s)
        bad=[s for s in out if not hemi(D,s)]
        print(q,'raw',len(out),'bad',len(bad),flush=True)
        # raw5 and raw7 used a different root; no bad solutions exist there
        ans=classes(D,bad) if bad else []
        pickle.dump(ans,open(f'badclasses{q}.pkl','wb'))
        print('time',time.time()-st,flush=True)
