from pathlib import Path
import json
n=18;d=1;den=9
adj=[0]*n
for k in range(0,n,3):
 for i in range(k,k+3):
  adj[i]=sum(1<<j for j in range(k,k+3) if i!=j)
E=[0]*(1<<n);best=-1;opts=[]
for S in range(1<<n):
 if S:
  b=S&-S;i=b.bit_length()-1;R=S^b;E[S]=E[R]+(adj[i]&R).bit_count()
 p=S.bit_count();value=den*E[S]+p*(n-p)
 assert E[S]<=d*p
 if value>best:best=value;opts=[S]
 elif value==best:opts.append(S)
sizes=sorted(set(s.bit_count() for s in opts));pairs=0;nonnested=0
for S in opts:
 for T in opts:
  if S.bit_count()<=T.bit_count():continue
  J=S.bit_count()-T.bit_count();assert J<=d*den+1;pairs+=1
  if S&T!=T:nonnested+=1
out=dict(graph='6 disjoint triangles, cyclic orientationoutdegree1',n=n,d=d,M='1/9',all_profiles=1<<n,opt_objective=f'{best}/{den}',opt_sizes=sizes,opt_profiles=len(opts),different_size_ordered_pairs=pairs,nonnested_opt_pairs=nonnested,jump_bound=d*den+1)
print(json.dumps(out,indent=2))
Path('workspace/agent1_aligned_phase_jump_check.json').write_text(json.dumps(out,indent=2))
Path('workspace/agent1_aligned_phase_jump_check.py').write_text(Path('scratchpad.py').read_text())
Path('workspace/agent1_aligned_phase_jump_lemma.txt').write_text('''ALIGNED PURE-PROFILE COMMON-DUMMY JUMP LEMMA
AtfixedM>0 letx,ybeGLOBALoptimaofthecommon-dummyobjectivewithPUREreal/dummyclassstates.
LetS,Tbetherealclasssets,p=|S|>q=|T|,J=p-q. AssumeONLYthattherealprobabilitydistributions
ofeveryCOMMONrealclassi inSintersectTareIDENTICALbetweenx,y. SetsS,TneedNOTbenested.
SetA=SminusT. Fori inA, letw_i bewithin-classactualQfromitsxdistribution.
Removingwholeclassifromxlosescrossdeg_x(i)+w_i andchangesdummytermb yM(2p-t-1),
sooptimalitygivescrossdeg_x(i)+w_i>=M(2p-t-1).
Addingithesamexdistributionatygainscrossdeg_y(i)+w_i andchangesdummytermbyM(t-2q-1),
sooptimalitygivescrossdeg_y(i)+w_i<=M(2q-t+1).
Subtract: crossdeg_x(i)-crossdeg_y(i)>=2M(J-1).
Commonclasscontributionscancelbyalignment. NegativeTminusSpartcanbedropped, hence
crossdeg_x(i)-crossdeg_y(i)<=deg_to_Aminus_i(i).
SummingA, RHS=2Qcross(A)<=2d|A|byoutcoloredtargetbudgetd.
Thus J<=d/M+1. ThisrequiresNOcoordinatewisenestingofS,T.
ItDOESrequirealignmentofcommon-classactualdistributions; noalignmenttheoremhasbeenproved.
CHECK: ALL2^18pureprofilesforsixdisjointtrianglesoutdegree1,M=1/9.
Objectiveopt20, optimalrealcounts12and15,21optimalprofiles.
ALL90different-sizeoptimalpairschecked, INCLUDING60NONNESTEDpairs; jump3<=10.
''')
