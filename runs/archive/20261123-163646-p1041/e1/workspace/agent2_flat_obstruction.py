from z3 import Int,IntVal,Solver,Sum,If,Or,unsat
from itertools import permutations,combinations
import time
TARGETS=[322,326,330,334]
def obstruction(n):
 """Necessary dimension identities for n linear dimension-seven flats in ambient14.
 For n=5 we can assume a shortest flat decomposition: all proper partial sums
 then have weight >=192, by the RM minimum/second minimum and the n<5 checks.
 """
 count=1<<n
 D={0:IntVal(14)}|{S:Int('d%d_%d'%(n,S)) for S in range(1,count)}
 solver=Solver()
 for S in range(1,count):solver.add(D[S]>=0,D[S]<=7)
 singles=[1<<i for i in range(n)]
 for S in singles:solver.add(D[S]==7)
 for A in range(count):
  for B in range(count):
   if A&B==A:solver.add(D[B]<=D[A])
   solver.add(D[A|B]+D[A&B]>=D[A]+D[B])
 for A,B,C,E in permutations(singles,4):
  solver.add(D[A|B]+D[A|C]+D[A|E]+D[B|C]+D[B|E] <= D[A]+D[B]+D[C|E]+D[A|B|C]+D[A|B|E])
 def exp(x):return Sum([If(x==j,1<<j,0) for j in range(8)])
 def wt(T):return Sum([(-2)**(S.bit_count()-1)*exp(D[S]) for S in range(1,count) if S&T==S])
 if n==5:
  for T in range(1,count-1):
   if T.bit_count()>=2:solver.add(wt(T)>=192)
  # Target2mod4 forces an odd number of point pair intersections.
  # Choose a point pair A,B; all other pairs have dimensions <=5.
  solver.add(D[3]==0)
  for A,B in combinations(singles,2):solver.add(D[A|B]<=5)
  # If all six endpoint intersections have dimension <=3, pair sum P<=145.
  # For five linear flats, wt>=656-2P>=366, impossible for TARGETS.
  # Thus choose C and interchange A,B to maximize endpoint intersection at AC.
  solver.add(D[5]>=4,D[5]>=D[9],D[9]>=D[17],D[5]>=D[6],D[5]>=D[10],D[5]>=D[18])
 solver.add(Or(*[wt(count-1)==t for t in TARGETS]))
 start=time.time();result=solver.check();print(n,result,'seconds',time.time()-start,flush=True)
 assert result==unsat
if __name__=='__main__':
 open('workspace/agent2_flat_obstruction.py','w').write(open(__file__).read())
 for n in range(1,6):obstruction(n)
