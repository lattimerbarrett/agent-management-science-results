import pickle,sympy as S
D=pickle.load(open('workspace/agent2_s3_m5_Kflow.pkl','rb'))
t,z,mu=D['t'],D['z'],D['mu'];P=D['P'];Q=D['Q'];C=D['C'];poly=D['D'];w=D['w'];T=D['T'];flow=D['flow'];force=D['force']
nodes=[-3,-2,1,2,3]
assert S.simplify(sum(w)-1)==0
for j in range(3):assert S.factor(sum(wi*P.subs(z,x)*x**j for wi,x in zip(w,nodes)))==0
assert S.factor(T.det())!=0
k0,k1=S.symbols('k0 k1');Pt=P.subs(z,t);Qt=Q.subs(z,t);Dt=poly.subs(z,t);Kt=k0+k1*t;v=2*Dt*Kt/C
assert S.factor(flow[0]+t*flow[1]+k1*v+Kt*S.diff(Pt*Qt,t)*v/(2*Pt*Qt))==0
assert S.factor(flow[2]+C*(Pt+Qt)*v*v/(4*Dt))==0
minus_relation=(P*Q+C).subs(z,mu)
force_error=S.together(force[2]-4*(P.subs(z,mu)**2+C))
assert S.rem(S.fraction(force_error)[0],minus_relation,mu)==0
print('Exact s3/m5 cycle, physical chart, noflip clock, fuel, and minus-force identities verified.')
