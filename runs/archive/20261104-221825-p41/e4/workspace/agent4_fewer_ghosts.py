"""Unconditional completion using d-1 ghosts, from any k-decomposition."""
from agent3_checker import verify
from agent3_tree_capacity_completion import conditional_completion

def completion_with_d_minus_one_ghosts(fs,k,c):
 fs=tuple(sorted(fs));r=fs[0].bit_count();assert r>=1
 verify(fs,k,c)
 U=0
 for F in fs:U|=F
 a=max(0,r-2)
 A=sum(1<<i for i in range(U.bit_length(),U.bit_length()+a))
 out=conditional_completion(fs,k,c,U|A)
 return A,out
