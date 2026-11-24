import sys,itertools,json
sys.path.insert(0,'workspace')
from agent2_compute import make_A
from sage.all import matrix,QQ,vector
cells,ds=make_A(4)
B={k:matrix(QQ,len(cells[k-1]),len(cells[k]),ds[k]) for k in range(1,5)}
K=B[3].right_kernel().basis(); I=B[4].column_space()
z=next(v for v in K if v not in I)
M=B[4].augment(matrix(QQ,len(z),1,list(z)))
actions={}
for p in itertools.permutations(range(4)):
 out=[0]*len(z); ids={f:i for i,f in enumerate(cells[3])}
 for j,f in enumerate(cells[3]):
  ff=tuple((p[x],r) for x,r in f);inv=sum(ff[i][0]>ff[j][0] for i in range(3) for j in range(i+1,3));ff=tuple(sorted(ff));out[ids[ff]]+=(-1)**inv*z[j]
 c=M.solve_right(vector(QQ,out))[-1]
 parity=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
 actions[str(p)]=int(c)
 assert c==parity
print('A4 H2 carries sign representation of S4, checked all 24 permutations')
print('cycle',[(cells[3][i],int(v)) for i,v in enumerate(z) if v])
open('workspace/agent1_A4_action.json','w').write(json.dumps(actions,indent=2))
open('workspace/agent1_A4_action.py','w').write(open(__file__).read())