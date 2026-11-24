import numpy as np, json, os
from scipy.optimize import differential_evolution

def adj(A): return np.array([[A[1,1],-A[0,1]],[-A[1,0],A[0,0]]])
def detone_interval_max(Wi,Wj,A,L,li,lj):
    # Exact candidate enumeration for sup det((A+uWi+vWj)/(L+u+v)).
    c=float(np.trace(adj(Wi)@Wj)); d=float(np.trace(adj(A)@Wi)); e=float(np.trace(adj(A)@Wj)); f=float(np.linalg.det(A))
    candidates=[]
    def add(u,v):
        if -1e-10<=u<=li+1e-10 and -1e-10<=v<=lj+1e-10 and L+u+v>1e-14:
            u=min(max(u,0),li); v=min(max(v,0),lj)
            val=(u*u+v*v+c*u*v+d*u+e*v+f)/(L+u+v)**2
            candidates.append((val,u,v))
    for u in [0.,li]:
        for v in [0.,lj]: add(u,v)
        B=c*u+e; C=u*u+d*u+f; E=L+u
        den=2*E-B
        if abs(den)>1e-14: add(u,(2*C-B*E)/den)
    for v in [0.,lj]:
        B=c*v+d; C=v*v+e*v+f; E=L+v
        den=2*E-B
        if abs(den)>1e-14: add((2*C-B*E)/den,v)
    if abs(2-c)>1e-12:
        k=(e-d)/(2-c)
        aa=2+c; bb=d+e-(2+c)*k; cc=k*k-e*k+f; E=L-k
        den=2*aa*E-2*bb
        if abs(den)>1e-12:
            u=(4*cc-bb*E)/den; add(u,u-k)
    if L==0:
        add(min(li,lj)/2,min(li,lj)/2)
    return max(candidates)

def sup_det_mean(leaves):
    n=len(leaves); result=(1.,None)
    for i in range(n):
        A=np.zeros((2,2)); L=0.
        for j in range(i+1,n):
            val,u,v=detone_interval_max(leaves[i][0],leaves[j][0],A,L,leaves[i][1],leaves[j][1])
            if val>result[0]: result=(val,(i,j,u,v))
            A+=leaves[j][1]*leaves[j][0]; L+=leaves[j][1]
    return result

rng=np.random.default_rng(913)
checks=[]
for trial in range(8):
    n=6
    lengths=rng.uniform(.05,1,n); lengths/=sum(lengths)
    leaves=[]
    for l in lengths:
        theta=rng.uniform(-np.pi,np.pi); a=rng.uniform(-3,3)
        R=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        W=R@np.diag([np.exp(a),np.exp(-a)])@R.T
        leaves.append((W,l))
    result=sup_det_mean(leaves)
    edges=np.r_[0,np.cumsum(lengths)]
    def objective(st):
        s,t=sorted(st)
        if t-s<1e-10:return -1.
        M=sum(max(0,min(t,edges[j+1])-max(s,edges[j]))*W for j,(W,l) in enumerate(leaves))/(t-s)
        return -np.linalg.det(M)
    opt=differential_evolution(objective,[(0,1),(0,1)],tol=1e-10,popsize=20,seed=trial)
    err=abs(result[0]+opt.fun)
    assert err<1e-6,(trial,result,-opt.fun)
    checks.append({'trial':trial,'candidate_sup':result[0],'global_optimizer':-opt.fun,'absolute_error':err})
print(json.dumps(checks,indent=2))
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_interval_checks.py','w') as f:f.write(open('scratchpad.py').read())
with open('workspace/agent3_interval_checks.json','w') as f:json.dump(checks,f,indent=2)
