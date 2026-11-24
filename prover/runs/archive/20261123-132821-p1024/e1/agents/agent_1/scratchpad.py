import sys
sys.path.insert(0,'workspace')
from agent4_cech import compute
for alpha,d in [(0,0),(1,0),(0,-10),(1,-10)]:
    print(alpha,d,compute(6,[0,1],alpha,d))
