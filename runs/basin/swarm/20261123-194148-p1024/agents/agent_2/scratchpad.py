import sys,random
sys.path.insert(0,'workspace')
from agent4_laurent_matrix import matrix, rankexact
random.seed(2026)
count=0
for g in range(2,7):
    r=(g+2)//3
    vectors=[]
    for s in range(1,r+1):
        vectors.append([random.randint(-3,3) for _ in range(s-1)]+[random.choice([-3,-2,-1,1,2,3])]+[0]*(r-s))
    for b in vectors:
        hs=[]
        for kind in ['O','S','L']:
            rows,cols=matrix(g,b,kind)
            hs.append(rows-rankexact(cols))
        s=max(i for i,c in enumerate(b) if c)+1
        T=s*(g+r+1-2*s)
        expected=[g*g+1-T,6*g*g-7*g+3-2*T+s,5*g*g-7*g+3-T]
        assert hs==expected,(g,b,hs,expected)
        print(g,b,hs,'Delta',hs[0]-hs[1]+hs[2])
        count+=1
print('Independent exact matrix cross-checks passed:',count)
