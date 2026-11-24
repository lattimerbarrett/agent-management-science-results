import sympy as s
x,t,S,T=s.symbols('x t S T');P=(x+3)*(x+1)*(x-1)*(x-2)*(x-3);M=s.Matrix([[1,2-t,7-2*t],[2-t,7-2*t,9-7*t],[7-2*t,9-7*t,39-9*t]]);a=M*s.Matrix([T,-S,1]);K=-s.diff(a,t);kap=-20*P.subs(x,t)/(11*(t**3-7*t-5));k=s.Matrix([0,kap,2*kap]);A=-10*s.Matrix([1,2-t,7-2*t]);sol=s.simplify(s.Matrix.hstack(a,k,A).inv()*K);D=11*(t*t-S*t+T)/(4*P.subs(x,t));sub={T:S*S-7};assert s.factor(sol[0]+1/(S+t))==0;assert s.factor(sol[2].subs(sub))==0
pred=11*((S**3-7*S)*(t**3-7*t)+25)/(20*(S+t)**2*P.subs(x,t));assert s.factor(((D-sol[1])/(S+t)).subs(sub)-pred)==0
print('exact s3 moment identity verified; coefficient changes sign')
