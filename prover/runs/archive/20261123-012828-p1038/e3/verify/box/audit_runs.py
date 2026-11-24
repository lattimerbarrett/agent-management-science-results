import sys, runpy, time
sys.path.insert(0,'/workspace')
sys.path.insert(0,'workspace')
# Paths relative to sandbox own folder are provided by accessible workspace.
import agent3_certificates as c
import agent2_endpoint_checks as e
import agent4_direct_check as d
print('EXACT')
c.exact_certificates()
print('NUMERICAL LARGE K')
for m in range(1,6):
 vals=c.numerical_blocks(m,600,100)
 assert all(v<0 for v in vals)
print('ORIGINAL-FACTOR / CANONICAL / ENDPOINT CHECKS')
import mpmath as mp
mp.mp.dps=80
for m in range(1,9):
 err,_=e.check(m,mp.mpf(1))
 _,det=e.check(m,mp.mpf('1e-12'))
 print(m,mp.nstr(err,5),mp.nstr(det,18))
 assert abs(det-1)<mp.mpf('1e-6')
print('DIRECT FULL MATRIX')
d.direct_check()
