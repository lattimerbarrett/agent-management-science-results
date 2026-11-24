import itertools,json,sympy as s
X=[{0},{1,2},{3,4,5}];V=set(range(6))
H=[{0,b,c} for b in X[1] for c in X[2]]+[X[1]|{c} for c in X[2]]+[X[2]]
assert len(H)==10 and all(len(F)==3 for F in H)
assert all(F&G for F in H for G in H)
assert all(any(not set(C)&F for F in H) for C in itertools.combinations(V,2))
y,z=s.symbols('y z');h2=y*(y-1);h3=z*(z-1)*(z-3);P=(2*y-1)*(3*z-4)**2
res=[s.cancel(P/(s.diff(h2,y)*s.diff(h3,z))).subs({y:b,z:c}) for b in [0,1] for c in [0,1,3]]
assert res==[s.Rational(16,3),-s.Rational(1,2),s.Rational(25,6)]*2
assert sum(res)==18 # coefficient y^1 z^2 in P is18, standard grid coefficient formula
# Show a special positive coefficient choice DOES achieve residue positivity here.
Ppositive=(2*y-1)*(z-s.Rational(1,2))*(z-2)
respositive=[s.cancel(Ppositive/(s.diff(h2,y)*s.diff(h3,z))).subs({y:b,z:c}) for b in [0,1] for c in [0,1,3]]
assert all(v>0 for v in respositive)
# Each desired linear factor z-a is positive combination of z,z-1,z-3.
# z-.5=(.6*z+.35*(z-1)+.05*(z-3)); z-2=(.1*z+.35*(z-1)+.55*(z-3)).
assert s.expand(s.Rational(6,10)*z+s.Rational(35,100)*(z-1)+s.Rational(5,100)*(z-3))==z-s.Rational(1,2)
assert s.expand(s.Rational(1,10)*z+s.Rational(35,100)*(z-1)+s.Rational(55,100)*(z-3))==z-2
out=dict(t=3,k=3,cores=[sorted(x) for x in X],H=[sorted(F) for F in H],cover2_absent=True,separator=str(P),residues=[str(v) for v in res],positive_choice_residues=[str(v) for v in respositive],same_sign_automatic=False)
json.dump(out,open('workspace/agent4_residue_sign_counterexample.json','w'));open('workspace/agent4_residue_sign_counterexample.py','w').write(open(__file__).read());print(out)
