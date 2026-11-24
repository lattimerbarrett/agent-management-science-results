import sys
sys.path.insert(0,'workspace')
import agent2_k7_integral_certificate as c
faces,active,D=c.main()
assert len(active[5])==1 and len(active[6])==310
