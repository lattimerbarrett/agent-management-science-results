import sys,itertools,json,time,pathlib
sys.path.insert(0,'workspace')
from agent3_check import *
from agent4_fastcert import fastcert
from agent1_filling import check_certificate
G=tuple(sorted(json.load(open('workspace/agent2_gluecounter.json'))['G']));n=7
cg=k_certificate(G,1);assert cg is not None and k_certificate(G,0) is None

def joincert(A,ca,B,cb):
 if ca[0]=='simplex' and cb[0]=='simplex':return ('simplex',A[0]|B[0])
 if ca[0]=='simplex':return joincert(B,cb,A,ca)
 _,s,dc,lc=ca
 D=tuple(f for f in A if f&s!=s);L=tuple(sorted(f^s for f in A if f&s==s))
 return ('shed',s,joincert(D,dc,B,cb),joincert(L,lc,B,cb))
def shiftcert(c,n):
 if c[0]=='simplex':return ('simplex',c[1]<<n)
 return ('shed',c[1]<<n,shiftcert(c[2],n),shiftcert(c[3],n))
D=tuple(sorted(f|(g<<n) for f in G for g in G));H=tuple(sorted({f^(1<<v) for f in D for v in range(14) if f>>v&1}))
c=joincert(G,cg,tuple(f<<n for f in G),shiftcert(cg,n))
assert check_certificate(D,1,c)
assert fastcert(H,0) is None
print('Verified: G1decomp/nonVD; G*G explicit1certificate valid; skeleton nonVD exactsearch',fastcert.cache_info())
json.dump({'G':G,'D':D,'H':H,'D_certificate':c},open('workspace/agent2_nonVD_proper_skeleton.json','w'))
pathlib.Path('workspace/agent2_nonVD_proper_skeleton.py').write_text(pathlib.Path(__file__).read_text())
