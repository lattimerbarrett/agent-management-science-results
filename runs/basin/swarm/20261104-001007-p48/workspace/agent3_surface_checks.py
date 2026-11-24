from pathlib import Path
# Cohomology of O(d) on P1.
def h0(d): return max(d+1,0)
def h1(d): return max(-d-1,0)
# E0|f* = O(-5) + O(1): sections move compact surfaces in Tot(O_P(E0|f)(1)).
assert h0(-5)+h0(1)==2
assert h1(-5)+h1(1)==4
print('Moving-surface section space dimension:',h0(-5)+h0(1))
print('Vertical normal H1 dimension:',h1(-5)+h1(1))
# Every ample rank2 bundle restricted to P1 splits O(a)+O(b), a,b>=1.
for a in range(1,4):
 b=4-a
 assert h0(-a)+h0(-b)==0
print('For ample degree-4 restrictions, no graph sections: verified all positive splittings (1,3),(2,2),(3,1).')
