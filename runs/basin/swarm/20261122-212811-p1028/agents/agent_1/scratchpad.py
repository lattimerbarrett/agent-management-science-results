import itertools, time, pickle
from sage.all import Graph

def regular_reps(n,d):
    rem=[d]*n
    adj=[0]*n
    for j in range(1,d+1):
        adj[0]|=1<<j; adj[j]|=1;rem[j]-=1
    rem[0]=0
    reps={};count=0; start=time.time()
    def rec(i):
        nonlocal count
        while i<n and rem[i]==0:i+=1
        if i==n:
            count+=1
            edges=[(v,w) for v in range(n) for w in range(v+1,n) if adj[v]>>w&1]
            g=Graph([list(range(n)),edges],format='vertices_and_edges')
            key=g.canonical_label().graph6_string()
            if key not in reps: reps[key]=edges
            return
        choices=[j for j in range(i+1,n) if rem[j]>0]
        r=rem[i]
        if len(choices)<r:return
        rem[i]=0
        for ns in itertools.combinations(choices,r):
            for j in ns:rem[j]-=1;adj[i]|=1<<j;adj[j]|=1<<i
            positive=sum(x>0 for x in rem[i+1:])
            if all(x<positive for x in rem[i+1:] if x):rec(i+1)
            for j in ns:rem[j]+=1;adj[i]^=1<<j;adj[j]^=1<<i
        rem[i]=r
    rec(1)
    print('degree',d,'leaves',count,'classes',len(reps),'seconds',round(time.time()-start,2),flush=True)
    return list(reps.values())

def arithmetic_data(n,a):
    from sage.all import matrix, ZZ, QQ
    L=matrix(ZZ,n,n)
    k=0
    for i in range(n):
        for j in range(i+1,n):
            b=(a//(2**k))-2*(a//(2**(k+1))); k+=1
            L[i,i]+=b;L[j,j]+=b;L[i,j]-=b;L[j,i]-=b
    ids=[i for i in range(n) if i!=1]
    T=L.matrix_from_rows_and_columns(ids,ids).det()
    F=L[2:,2:].det()
    c=1-(1//(T+1))
    r=1
    for i in range(1,n):r*=1//(1+(L[i,i]-L[0,0])**2)
    score=QQ(n*L[0,0]*c*r*F)/(T+1-c)
    return L,T,F,c,r,score

def hit(L,target,start):
    from sage.all import QQ, vector
    ids=[i for i in range(L.nrows()) if i!=target]
    A=L.matrix_from_rows_and_columns(ids,ids).change_ring(QQ)
    h=A.solve_right(vector(QQ,[L[i,i] for i in ids]))
    return h[ids.index(start)]

def small_checks():
    from sage.all import factorial
    for n in range(2,6):
        scores=[]
        for a in range(1<<(n*(n-1)//2)):
            L,T,F,c,r,s=arithmetic_data(n,a)
            assert 0<=T<=(n-1)**(n-1) and F>=0
            assert c==int(T>0)
            assert r==int(len(set(L.diagonal()))==1)
            if c:
                commute=hit(L,1,0)+hit(L,0,1)
                assert commute==sum(L.diagonal())*F/T
                if r:assert commute==s
            if not(c and r):assert s==0
            assert (factorial((n-1)**(n-1))*s).denominator()==1
            scores.append(s)
        top=max(scores)
        if n<=3:
            Q=factorial((n-1)**(n-1));B=(1<<(n*(n-1)//2))+1
            Z=sum(B**int(Q*s) for s in scores)
            k=0
            while Z>=B:Z//=B;k+=1
            assert k/Q==top
        print('all-mask check',n,'masks',len(scores),'value',top,flush=True)

if __name__=='__main__':
    small_checks()
    reps={}
    import os
    if os.path.exists('regular10.pkl'):
        with open('regular10.pkl','rb') as f:reps=pickle.load(f)
    else:
        for d in range(5):reps[d]=regular_reps(10,d)
        with open('regular10.pkl','wb') as f:pickle.dump(reps,f)
    from sage.all import matrix, QQ
    for d in range(10):
        best=QQ(0);connected=0
        for edges in reps[min(d,9-d)]:
            G=Graph([list(range(10)),edges],format='vertices_and_edges')
            if d>=5:G=G.complement()
            if not G.is_connected():continue
            connected+=1
            L=G.laplacian_matrix().change_ring(QQ)
            A=L[:9,:9].inverse()
            rr=max((A[u,u] if v==9 else A[u,u]+A[v,v]-2*A[u,v]) for u in range(9) for v in range(u+1,10))
            val=10*d*rr
            if val>best:best=val
        print('maximum',d,connected,best,flush=True)
