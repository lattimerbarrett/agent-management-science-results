from pathlib import Path
old=Path('workspace/agent4_shift_reservoir.py').read_text()
new=old.replace('nf=r+2*len(E); q=max(m,r,2)\n    scale=max(1,(nf+(1<<(q-2))-1)//(1<<(q-2)))\n    D=scale*(1<<(q-2)); n=nf+15*D','nf=r+2*len(E); q=max(1,(max(m,r)-1).bit_length())\n    D0=1<<(q-1); scale=(nf+D0-1)//D0\n    D=scale*D0; n=nf+15*D')
a='''    def attach(v,region,domain,left,right):
        B=regions[region][1];rep=scale*(1<<(q-domain))
        for S in range(1<<domain):
            if (S>>left)&1 and not (S>>right)&1:
                for j in range(rep):join(v,B.start+S*rep+j)'''
b='''    def attach(v,region,domain,left,right):
        # Palette colors are pairwise-independent affine GF(2) cuts.
        B=regions[region][1]
        for a in range(1<<q):
            for b in range(2):
                l=((a&left).bit_count()&1)^b
                h=((a&right).bit_count()&1)^b
                if l==1 and h==0:
                    S=2*a+b
                    for j in range(scale):join(v,B.start+S*scale+j)'''
assert a in new
new=new.replace(a,b)
new=new.replace("return dict(m=m,shift_vertices=r", "return dict(m=m,palette_size=1<<(q+1),shift_vertices=r")
new=new[:new.index("if __name__=='__main__':")]+'''def check_shift_chromatic(m):
    import z3
    V=list(combinations(range(m),2));index={v:i for i,v in enumerate(V)}
    E=[(index[i,j],index[j,k]) for i,j,k in combinations(range(m),3)]
    k=(m-1).bit_length()
    # Explicit upper coloring: index of most significant differing binary digit.
    color=[(i^j).bit_length()-1 for i,j in V]
    assert max(color)<k
    assert all(color[u]!=color[v] for u,v in E)
    # Exact solver proves no (k-1)-coloring for these concrete graphs.
    s=z3.Solver();x=[z3.Int('x%d'%i) for i in range(len(V))]
    s.add(*[z3.And(t>=0,t<k-1) for t in x])
    s.add(*[x[u]!=x[v] for u,v in E])
    assert s.check()==z3.unsat
    # Verify all outgoing color sets distinct (general lower-bound proof invariant).
    masks=[sum(1<<c for c in {color[index[i,j]] for j in range(i+1,m)}) for i in range(m)]
    assert len(set(masks))==m
    return k

if __name__=='__main__':
    results=[]
    for m in range(3,10):
        report=build_and_check(m)
        report['shift_chromatic_number']=check_shift_chromatic(m)
        results.append(report)
    print(json.dumps(results,indent=2))
'''
Path('workspace/agent4_shift_affine.py').write_text(new)
exec(compile(new,'workspace/agent4_shift_affine.py','exec'))
