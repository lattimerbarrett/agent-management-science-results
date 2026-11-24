import pickle,json,os
from collections import Counter
from sage.all import ZZ
root='experiments/e1'
p=root+'/agent4_johnson_full_degree6.pickle'
with open(p,'rb') as f: d=pickle.load(f)
B=d['basis']
print('degree-six Johnson-image lattice matrix:',B.nrows(),'by',B.ncols())
print('stored Smith invariants:',Counter(map(int,d['smith'])))
print('independently recomputed Smith invariants:',Counter(map(int,B.elementary_divisors())))
print('Thus saturation/image is Z/3, and ambient/image is Z^130 + Z/3.')
print('This is a cokernel calculation, not a kernel calculation.')
p=root+'/agent3_W_detector_functional.json'
a=json.load(open(p));print('functional JSON keys:',list(a) if isinstance(a,dict) else type(a))
