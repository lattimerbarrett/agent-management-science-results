import sys
sys.path.insert(0,'workspace')
from agent3_certificates import numerical_blocks
for m in (1,2,3,4,5):
    assert all(d<0 for d in numerical_blocks(m,600,dps=200))
print('All negative signs independently stable at 200 decimal digits.')
