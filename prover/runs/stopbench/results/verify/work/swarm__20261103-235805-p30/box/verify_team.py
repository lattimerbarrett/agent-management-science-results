import sys, time
sys.path.insert(0, '/workspace')
# use relative shared folder as documented
sys.path.insert(0, 'workspace')
import agent1_full_certificate as a1
import agent2_upper_certificate as a2
import agent4_gaussian_certificate as a4
for s in range(3,15):
    print('upper',s,a2.upper_certificate(s),flush=True)
for s in (3,4,5):
    print('integrated',a1.check(s),flush=True)
    print('lower',a4.certificate(s),flush=True)
