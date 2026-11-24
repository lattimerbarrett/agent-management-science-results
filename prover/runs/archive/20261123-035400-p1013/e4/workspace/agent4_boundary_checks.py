"""Independent finite checks of necessary boundary-template calculations.
Not a proof of the main boundary theorem.
"""
from itertools import product
import networkx as nx

def parts(n,r):
    return [n//r+(i<n%r) for i in range(r)]

def turan(n,r):
    s=parts(n,r)
    return (n*n-sum(x*x for x in s))//2

def check():
    count=0
    for r in range(2,11):
        for n in range(3*r,101):
            s=parts(n,r)
            G=nx.complete_multipartite_graph(*s)
            assert G.number_of_edges()==turan(n,r)
            a=s[0]
            # Star augmentation, P3 tiling, and matchings in two parts.
            for kind in ['star','p3','two_matchings']:
                H=G.copy()
                if kind=='star':
                    H.add_edges_from((0,j) for j in range(1,a)); extra=a-1
                elif kind=='p3':
                    for j in range(a//3): H.add_edges_from([(3*j,3*j+1),(3*j+1,3*j+2)])
                    extra=2*(a//3)
                else:
                    for offset,size in [(0,s[0]),(s[0],s[1])]:
                        H.add_edges_from((offset+2*j,offset+2*j+1) for j in range(size//2))
                    extra=s[0]//2+s[1]//2
                assert H.number_of_edges()==turan(n,r)+extra
                if kind=='star': assert abs(extra-n/r)<=2
                elif kind=='p3': assert abs(extra-2*n/(3*r))<=2
                else: assert abs(extra-n/r)<=2
                count+=1
    return count
if __name__=='__main__': print('Verified template edge counts:',check())
