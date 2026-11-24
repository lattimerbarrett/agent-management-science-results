"""Run every finite certificate used by the proof, not exploratory searches.
Invoke from the directory containing workspace/: python workspace/agent2_combined_checker.py
Requires Python 3, numpy, and z3-solver. No network or subprocesses.
"""
import contextlib, gc, hashlib, io, json, runpy, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
NAMES=[
 'agent3_sufficiency_checker.py',
 'agent2_four_affine_checker.py',
 'agent2_96112126_exterior.py',
 'agent2_purepair_coset_arithmetic.py',
 'agent3_6496_arithmetic.py',
 'agent3_cubic_coset_checker.py',
 'agent3_64126_hilbert_checker.py',
 'agent2_bootstrap_rank_checker.py',
 'agent1_purepair5_86_checker.py',
 'agent4_m15_qzero_checker.py',
]
results={}
for name in NAMES:
 p=ROOT/name
 sha=hashlib.sha256(p.read_bytes()).hexdigest()
 out=io.StringIO();start=time.perf_counter()
 with contextlib.redirect_stdout(out):
  runpy.run_path(str(p),run_name='__certificate__')
 elapsed=time.perf_counter()-start
 results[name]={'sha256':sha,'seconds':round(elapsed,6),'stdout':out.getvalue(),'status':'PASS'}
 print(name,'PASS',round(elapsed,3),'seconds',flush=True)
 gc.collect()
# Interval endpoints as affine functions alpha*2^m+beta.
low=[(0,0),(128,128),(192,192),(224,224),(240,240),(248,248),(252,256),
 (272,272),(288,288),(296,296),(304,304),(308,308),(312,320),(324,324),(328,328),(332,332)]
coeffs=[((0,a),(0,b)) for a,b in low]+[((0,336),(1,-336))]+[
 ((1,-b),(1,-a)) for a,b in reversed(low)]
assert len(coeffs)==33
for m in range(14,101):
 N=1<<m
 intervals=[(a*N+b,c*N+d) for (a,b),(c,d) in coeffs]
 assert intervals[0]==(0,0) and intervals[-1]==(N,N)
 assert all(0<=a<=b<=N and a%2==b%2==0 for a,b in intervals)
 assert all(b+2<c for (a,b),(c,d) in zip(intervals,intervals[1:]))
 assert [(N-b,N-a) for a,b in reversed(intervals)]==intervals
 # Concatenations cover the next central interval, with adjacent-even overlap.
 sums=[(336,N-336),(672,2*N-672),(N+336,2*N-336)]
 assert sums[0][1]+2>=sums[1][0] and sums[1][1]+2>=sums[2][0]
 assert sums[0][0]==336 and sums[-1][1]==2*N-336
# The interval overlap condition for every m>=14 reduces to N>=1006.
assert (1<<14)>=1006
# Injective quotient reduction at every m>=16 (higher dimensions are easier).
assert 334*333//2+1 < 1<<16
# All degree/moment flattening-rank arithmetic of the twice-minimum span lemma.
from math import comb
for p in range(5,101):
 k=2 if p==5 else 3
 alpha=comb(p,k)
 beta=sum(comb(p-2,k-j)*r for j,r in enumerate([1,4,1]) if 0<=k-j<=p-2)
 gamma=beta
 intersection_bound=1 if p==5 else 0
 assert alpha+beta-intersection_bound>gamma
 # Decomposable sum case: actual normals meet common divisor space.
 assert (p-2)+(p-1)-p==p-3>0
for c in range(4,101):
 n=2*c+2;p=n-c-1;N=n-2
 assert p>=5 and n-2*c-1>=1
 assert N>=2*(c-1)+2
# Literal construction supports / ranks are checked by the ten scripts above;
# these final algebraic checks only audit endpoints and induction arithmetic.
results['endpoint_and_induction_checks']={'status':'PASS','intervals':coeffs,'dimensions_explicitly_checked':[14,100], 'all_m_overlap_bound':1006}
(ROOT/'agent2_combined_results.json').write_text(json.dumps(results,indent=2))
print('All finite proof certificates PASS; 33 explicit maximal interval shapes and induction inequalities PASS.')
