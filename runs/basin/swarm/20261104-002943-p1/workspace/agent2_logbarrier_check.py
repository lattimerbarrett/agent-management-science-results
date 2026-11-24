import sympy as S
mu=S.symbols('mu')
for s in range(1,5):
    nodes=list(range(1,2*s+1))
    L=[S.prod((mu-b)/(a-b) for b in nodes if b!=a) for a in nodes]
    assert S.expand(sum(L)-1)==0
    # These are exactly the normal-polynomial first derivatives in the log barrier.
    for j in range(2*s):
        assert S.expand(sum(L[i]*S.Integer(nodes[i])**j for i in range(2*s))-mu**j)==0
    print('s=',s,'all log-barrier first-variation cancellations verified exactly')
