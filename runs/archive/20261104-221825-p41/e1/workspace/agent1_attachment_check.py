import itertools, json
from pathlib import Path

def check(n,d):
    fs=[sum(1<<i for i in c) for c in itertools.combinations(range(n), d+1)]
    m=len(fs); count=1<<m
    def appendable(mask,j):
        if mask==0: return True
        F=fs[j]
        ints=[F&fs[h] for h in range(m) if mask>>h&1]
        ridges=[I for I in ints if I.bit_count()==d]
        return all(any(I&~R==0 for R in ridges) for I in ints)
    shell=bytearray(count); shell[0]=1
    for mask in range(1,count):
        for j in range(m):
            if mask>>j&1:
                prev=mask^(1<<j)
                if shell[prev] and appendable(prev,j):
                    shell[mask]=1; break
    checks=0
    for mask in range(1,count):
        if not shell[mask]: continue
        for j in range(m):
            if mask>>j&1:
                prev=mask^(1<<j)
                if prev:
                    assert appendable(prev,j), (n,d,mask,j)
                    checks+=1
    return dict(n=n,d=d,facets=m,complexes=count-1,shellable=sum(shell)-1,one_facet_checks=checks)
results=[check(5,2), check(6,3)]
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent1_attachment_checks.json').write_text(json.dumps(results,indent=2))
Path('workspace/agent1_attachment_check.py').write_text(Path(__file__).read_text())
print(json.dumps(results,indent=2))
