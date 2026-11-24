import sympy as s, numpy as np, json, os
Q=s.symbols('Q', positive=True)
a=2-1/Q; b=s.sqrt(1-1/Q)
Mp=s.Matrix([[a,b],[b,1]]); Mm=s.Matrix([[a,-b],[-b,1]])
L=2*s.eye(2)-(Mp+Mm)/2
assert s.simplify(Mp.det()-1)==0
assert s.simplify(Mm.det()-1)==0
assert s.simplify(L.det()-1/Q)==0
assert s.simplify((Mp+Mm)/4+L/2-s.eye(2))==s.zeros(2)

def branch(W,Q,depth):
    d,U=np.linalg.eigh(W); G=U@np.diag(np.sqrt(d))
    a=2-1/Q; b=np.sqrt(1-1/Q)
    P=G@np.array([[a,b],[b,1.]])@G.T
    M=G@np.array([[a,-b],[-b,1.]])@G.T
    L=G@np.diag([1/Q,1.])@G.T
    if depth==0:
        # Terminal splitting retains average W and makes determinant 1.
        t=np.sqrt(1-1/Q)
        return [(G@np.array([[1.,t],[t,1.]])@G.T,.5),(G@np.array([[1.,-t],[-t,1.]])@G.T,.5)]
    return [(A,w/4) for A,w in branch(P,Q,depth-1)]+[(L,.25)]+[(A,w/4) for A,w in branch(M,Q,depth-1)]+[(L,.25)]

results=[]
for q in [2.,3.,5.,10.]:
    root=np.diag([q,1.])
    leaves=branch(root,q,5)
    avg=sum(w*A for A,w in leaves)
    invavg=sum(w*np.linalg.inv(A) for A,w in leaves)
    err=max(np.linalg.norm(avg-root), np.linalg.norm(invavg-np.diag([1.,q])))
    deterr=max(abs(np.linalg.det(A)-1) for A,w in leaves)
    assert err < 1e-8 and deterr<1e-8
    assert abs(np.trace(avg@invavg)/2-q)<1e-8
    results.append({'Q':q,'leaves':len(leaves),'mean_error':err,'det_error':deterr})
print(json.dumps(results,indent=2))
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_tree_checks.json','w') as f: json.dump(results,f,indent=2)
with open('workspace/agent3_tree_checks.py','w') as f: f.write(open('scratchpad.py').read())

from scipy.linalg import svdvals

def phi(t):
    return 0. if t==0 else t*np.log(abs(t))-t

def compression(leaves):
    lengths=np.array([w for A,w in leaves]); edges=np.r_[0,np.cumsum(lengths)]
    n=len(leaves); K=np.zeros((n,n)); Fs=[]; Bs=[]
    for A,w in leaves:
        d,U=np.linalg.eigh(A); Fs.append((U*np.sqrt(d))@U.T); Bs.append((U*(1/np.sqrt(d)))@U.T)
    T=np.zeros((2*n,2*n))
    for i in range(n):
        a,b=edges[i:i+2]
        for j in range(i):
            c,d=edges[j:j+2]
            z=(phi(b-c)-phi(a-c)-phi(b-d)+phi(a-d))/(np.pi*np.sqrt(lengths[i]*lengths[j]))
            T[2*i:2*i+2,2*j:2*j+2]=z*Fs[i]@Bs[j]
            T[2*j:2*j+2,2*i:2*i+2]=-z*Fs[j]@Bs[i]
    # Endpoint-interval characteristic and equal-mass adjacent pair tests.
    prefix=np.concatenate([np.zeros((1,2,2)),np.cumsum(np.array([w*A for A,w in leaves]),axis=0)])
    char=1.
    for i in range(n):
        for j in range(i+1,n+1):
            av=(prefix[j]-prefix[i])/(edges[j]-edges[i]); char=max(char,np.linalg.det(av))
        if i+1<n: char=max(char,np.linalg.det((leaves[i][0]+leaves[i+1][0])/2))
    return svdvals(T)[0],char
for q in [2.,4.,8.,16.,32.]:
    leaves=branch(np.diag([q,1.]),q,5)
    norm,ch=compression(leaves)
    print('compression Q, norm, tested full A2 lower:',q,norm,ch)

