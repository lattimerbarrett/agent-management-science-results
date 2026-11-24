import sys
sys.path.insert(0,'workspace')
from agent4_certificate import *
from pathlib import Path
code='''import mpmath as mp
from agent4_certificate import rows

def direct_check(k=150,dps=100):
    mp.mp.dps=dps
    A,B,(x,y,u,v)=rows(1,k)
    n=2*k+2
    M=mp.matrix(n,n)
    for j in range(k):
        M[j,j]=1; M[j,j+1]=-(x+y); M[j,j+2]=x*y
        M[k+2+j,k+j]=u*v
        M[k+2+j,k+j+1]=-(u+v)
        M[k+2+j,k+j+2]=1
    for e in range(n):M[k,e]=A[e];M[k+1,e]=B[e]
    # Completely independent full coefficient-matrix determinant.
    full=mp.det(M)
    V=[]
    for t in [u,v]:
        w=[mp.mpf(0)]*n
        for e in range(k,n):w[e]=t**(e-k)
        for e in range(k-1,-1,-1):w[e]=(x+y)*w[e+1]-x*y*w[e+2]
        V.append(w)
    W=mp.matrix([[mp.fdot(P,w) for w in V] for P in [A,B]])
    reduced=mp.det(W)/(v-u)
    assert full<0 and reduced<0
    assert abs((full-reduced)/full)<mp.mpf('1e-60')
    print('m=1, k=',k,'full det=',mp.nstr(full,30))
    print('dual determinant / (v-u) agrees to >60 digits')
    return full,reduced

if __name__=='__main__':direct_check()
'''
Path('workspace/agent4_direct_check.py').write_text(code)
exec(compile(code,'workspace/agent4_direct_check.py','exec'))
