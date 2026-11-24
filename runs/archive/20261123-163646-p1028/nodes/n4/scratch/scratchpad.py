import networkx as nx
import numpy as np
import sympy as sp
import random, math, pickle, os, time
random.seed(4921)

def score(A,d):
    n=len(A)
    Q=np.linalg.inv(d*np.eye(n)-A+np.ones((n,n))/n)
    if np.max(np.abs(Q))>1e6:return -1e100
    R=np.diag(Q)[:,None]+np.diag(Q)[None,:]-2*Q
    return n*d*np.max(R)

def exact(A):
    n=len(A);d=int(sum(A[0]));L=d*sp.eye(n)-sp.Matrix(A.tolist())
    Q=(L+sp.ones(n,n)/n).inv()
    val,u,v=max((n*d*(Q[i,i]+Q[j,j]-2*Q[i,j]),i,j) for i in range(n) for j in range(i))
    return val,u,v

def search(n,d,restarts=8,steps=4500):
    best=-1;bestA=None
    for rep in range(restarts):
        G=nx.random_regular_graph(d,n,seed=random.randrange(2**30))
        if not nx.is_connected(G):continue
        A=nx.to_numpy_array(G,nodelist=range(n),dtype=int)
        edges=list(G.edges());cur=score(A,d)
        for k in range(steps):
            i,j=random.sample(range(len(edges)),2)
            a,b=edges[i];c,e=edges[j]
            if random.randrange(2):c,e=e,c
            if len({a,b,c,e})!=4 or A[a,c] or A[b,e]:continue
            A[a,b]=A[b,a]=A[c,e]=A[e,c]=0
            A[a,c]=A[c,a]=A[b,e]=A[e,b]=1
            try:
                val=score(A,d)
                if val>1e6 or val<0:val=-1e100
            except np.linalg.LinAlgError:val=-1e100
            temp=n*(0.25*(1-k/steps)**2+0.001)
            if val>cur or random.random()<math.exp(min(0,(val-cur)/temp)):
                edges[i]=(a,c);edges[j]=(b,e);cur=val
                if cur>best+1e-7:
                    best=cur;bestA=A.copy()
            else:
                A[a,c]=A[c,a]=A[b,e]=A[e,b]=0
                A[a,b]=A[b,a]=A[c,e]=A[e,c]=1
    return best,bestA

if __name__=='__main__':
    results=pickle.load(open('search_results.pkl','rb')) if os.path.exists('search_results.pkl') else {}
    start=time.time()
    for n in [10,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]:
        ds=range(3,min(n,10)) if n%2==0 else range(4,min(n,11),2)
        for d in ds:
            best,A=search(n,d,restarts=15,steps=15000)
            if A is not None:
                val,u,v=exact(A)
                old=results.get((n,d))
                if old is None or val>old[0]:results[n,d]=(val,A,u,v)
                print(n,d,'exact',val,'decimal',float(val),'best saved',results[n,d][0],flush=True)
                pickle.dump(results,open('search_results.pkl','wb'))
    print('seconds',time.time()-start)
