from itertools import combinations
for t in range(2,6):
 V=set(range(2*t-1)); fs=list(map(frozenset,combinations(V,t)))
 parts=[[F for F in fs if min(F & set(range(t)))==i] for i in range(t)]
 assert all(parts) and sum(map(len,parts))==len(fs)
 assert all(F&G for F in fs for G in fs)
 for C in combinations(V,t-1):
  assert any(not (set(C)&F) for F in fs)
 assert all(set(range(t))&F for F in fs)
 print(t,len(fs),t*(t-1))
