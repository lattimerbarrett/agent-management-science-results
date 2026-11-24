"""Fast field-membership tests for current VERIFIED rank3 source relation lattice.
Source generators: C12,C13,C21,C23,C31,C32,M1;23,M2;13,M3;12.
M is LEFT multiplication xi -> [xj,xk]xi. Word products R-to-L composition.
Each returned nonzero residue certifies an additional source relation is new
IF supplied word has independently been checked an actual automorphism identity.
This is NOT an IA presentation or a classification theorem.
"""
import pickle,sys
sys.path.insert(0,'workspace')
from agent2_cubic_source import magnus3

def insert(B,v,p):
    v={k:int(c)%p for k,c in v.items() if c%p}
    while v:
        k=min(v);c=v[k]
        if k in B:
            for j,d in B[k].items():
                a=(v.get(j,0)-c*d)%p
                if a:v[j]=a
                else:v.pop(j,None)
        else:
            a=pow(c,-1,p);B[k]={j:a*d%p for j,d in v.items()};return True
    return False

def reduce(B,v,p):
    v={k:int(c)%p for k,c in v.items() if c%p}
    # Keep nonpivot terms; cannot stop at the first such term.
    for k,w in sorted(B.items()):
        c=v.get(k,0)
        if c:
            for j,d in w.items():
                a=(v.get(j,0)-c*d)%p
                if a:v[j]=a
                else:v.pop(j,None)
    return v

def vector(word):
    p=magnus3(tuple(word),9);v={}
    assert not any(len(u)==1 for u in p),'identity word must have zero exponent sums'
    for u,c in p.items():
        if len(u)==2:v[9*u[0]+u[1]]=c
        if len(u)==3:v[81+81*u[0]+9*u[1]+u[2]]=c
    return v

def load():return pickle.load(open('workspace/agent2_source_defect_bases.pkl','rb'))
def defect(word,bases=None):
    if bases is None:bases=load()
    v=vector(word)
    return {p:reduce(B,v,p) for p,B in bases.items()}
