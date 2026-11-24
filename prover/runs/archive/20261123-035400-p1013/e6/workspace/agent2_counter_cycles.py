"""Exact proposed-counterphase cycle comparison.
Uses the independently brute-verified join formula in agent1_cycles.py.
Default q=8 takes roughly 25 seconds and computes actual integer counts.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from agent1_cycles import path_polynomial,power,mul,cycles_join_r3
from fractions import Fraction

def add(*ps):
    out=[0]*max(map(len,ps))
    for p in ps:
        for i,a in enumerate(p):out[i]+=a
    return out

def path_q(n):
    A=[1];B=[0];C=[0]
    for _ in range(n):
        S=add(A,B,C)
        A,B,C=S,[0]+S,add([2*x for x in B],C)
    return add(A,B,C)

def compare(q=8):
    for n in range(1,8):
        assert path_q(n)==path_polynomial(n,[(i,i+1) for i in range(n-1)])
    star=path_polynomial(11,[(0,i) for i in range(1,11)])
    m=11*q;iso=power([1,1],m)
    A=cycles_join_r3(mul(power(star,q-2),path_q(22)),iso,iso,(m,m,m))
    B=cycles_join_r3(power(path_q(11),q),iso,iso,(m,m,m))
    assert B>A
    return dict(n=3*m,edge_difference=1,cycle_ratio=Fraction(B,A),
                A_cycles=A,B_cycles=B)

if __name__=='__main__':
    result=compare()
    print('n=',result['n'],'edge difference=',result['edge_difference'])
    print('exact c(B)>c(A):',result['B_cycles']>result['A_cycles'])
    print('cycle ratio:',float(result['cycle_ratio']))
