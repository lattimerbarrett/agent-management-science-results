import itertools, json, os

def transitive_relations(n):
    pairs=list(itertools.combinations(range(n),2))
    for mask in range(1<<len(pairs)):
        R={(i,i) for i in range(n)}|{p for j,p in enumerate(pairs) if mask>>j&1}
        if all((i,k) in R for i,j in R for jj,k in R if j==jj):
            yield R

def critical_pairs(X, le):
    D={x:{z for z in X if z!=x and le(z,x)} for x in X}
    U={x:{z for z in X if z!=x and le(x,z)} for x in X}
    return {(x,y) for x in X for y in X if not le(x,y) and not le(y,x) and D[x]<=D[y] and U[y]<=U[x]}

def check_critical_characterization(n,m):
    Q=[frozenset(x) for k in [1,2] for x in itertools.combinations(range(m),k)]
    count=0
    for R in transitive_relations(n):
        X=list(range(n));le=lambda x,y:(x,y) in R
        cp={(p,q) for p in X for q in X if not le(p,q) and all(not le(z,p) or z==p or le(z,q) for z in X) and all(not le(q,z) or z==q or le(p,z) for z in X)}
        mins={x for x in X if not any(y!=x and le(y,x) for y in X)}
        maxs={x for x in X if not any(y!=x and le(x,y) for y in X)}
        PX=list(itertools.product(X,Q))
        true=critical_pairs(PX,lambda x,y: le(x[0],y[0]) and x[1]<=y[1])
        pred={((p,A),(q,B)) for p in X for q in X for A in Q for B in Q if len(A)==1 and len(B)==2 and ((A<=B and (p,q) in cp) or (not A<=B and p in mins and q in maxs))}
        assert true==pred,(n,m,R,true^pred)
        count+=1
    return count

def s3_certificate():
    X=list(range(6));R={(i,i) for i in X}|{(i,3+j) for i in range(3) for j in range(3) if i!=j}
    orders=[]
    for i in range(3):
        others=[j for j in range(3) if j!=i]
        orders.append(others+[i+3,i]+[j+3 for j in others])
    ranks=[{x:i for i,x in enumerate(L)} for L in orders]
    assert all(((x,y) in R)==all(r[x]<=r[y] for r in ranks) for x in X for y in X)
    # No linear extension can reverse two diagonal incomparable pairs.
    exts=[p for p in itertools.permutations(X) if all(p.index(x)<=p.index(y) for x,y in R)]
    assert all(sum(L.index(i+3)<L.index(i) for i in range(3))<=1 for L in exts)
    return {'realizer':orders,'number_linear_extensions':len(exts)}

if __name__=='__main__':
    results={'S3':s3_certificate(),'critical_pair_checks':{}}
    for n in range(1,5):
        for m in [3,4]:
            results['critical_pair_checks'][str((n,m))]=check_critical_characterization(n,m)
    os.makedirs('workspace',exist_ok=True)
    with open('workspace/agent3_product_checks.py','w') as f: f.write(open(__file__).read())
    with open('workspace/agent3_checks.json','w') as f: json.dump(results,f,indent=2)
    print(json.dumps(results,indent=2))
