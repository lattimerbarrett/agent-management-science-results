"""Exhaustively check downward closure of Kalimullin pairs on <=2 bits."""
from itertools import product
from pathlib import Path
import json

def ops(n):
    tables=[]
    for t in product((0,1),repeat=1<<n):
        if all(not t[a] or t[b] for a in range(1<<n) for b in range(1<<n) if a&b==a):
            tables.append(tuple(i for i,v in enumerate(t) if v))
    return list(product(tables,repeat=n))

def image(op,P):
    return sum(1<<x for x,row in enumerate(op) if any(F&P==F for F in row))

def rect(P,Q,n):
    return sum(1<<(x*n+y) for x in range(n) for y in range(n) if P>>x&1 and Q>>y&1)

def main():
    result={}
    for n in (1,2):
        full=(1<<n)-1
        operators=ops(n)
        rectangles={(P,Q):rect(P,Q,n) for P in range(1<<n) for Q in range(1<<n)}
        def kp(P,Q,W):
            return rectangles[P,Q]&W==rectangles[P,Q] and not rectangles[full^P,full^Q]&W
        checks=0
        for W in range(1<<(n*n)):
            pairs=[(P,Q) for P in range(1<<n) for Q in range(1<<n) if kp(P,Q,W)]
            for left in operators:
                for right in operators:
                    newW=sum(1<<(x*n+y) for x in range(n) for y in range(n)
                             if any(rectangles[F,G]&W==rectangles[F,G]
                                    for F in left[x] for G in right[y]))
                    for P,Q in pairs:
                        assert kp(image(left,P),image(right,Q),newW)
                        checks+=1
        cancellation_checks=0
        for P in range(1<<n):
            for gamma in operators:
                if image(gamma,P)!=(full^P): continue
                for Q in range(1<<n):
                    for W in range(1<<(n*n)):
                        if not kp(P,Q,W): continue
                        rows=[sum(1<<x for x in range(n) if W>>(x*n+q)&1) for q in range(n)]
                        # In the infinite proof strictness follows because P is not c.e.
                        if any(rows[q]==P for q in range(n) if Q>>q&1): continue
                        enumerated=sum(1<<q for q,R in enumerate(rows) if R&image(gamma,R))
                        assert enumerated==Q
                        cancellation_checks+=1
        result[n]={'operators':len(operators),'downward_K_pair_checks':checks,
                   'total_cancellation_algebra_checks':cancellation_checks}
    print(json.dumps(result,indent=2))
    Path('workspace/agent4_kpair_checks.json').write_text(json.dumps(result,indent=2))

if __name__=='__main__': main()

