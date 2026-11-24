import sympy as s
th,ph=s.symbols('theta phi',real=True)
f=s.sin(th)+s.sin(ph)-s.sin(th+ph)
print('Meridian derivatives:',[s.diff(f,t) for t in (th,ph)])
for t in [0,2*s.pi/3,4*s.pi/3]:
 print('theta=phi=',t,'gradient=',[s.simplify(s.diff(f,q).subs({th:t,ph:t})) for q in (th,ph)],'value=',s.simplify(f.subs({th:t,ph:t})))
c=s.symbols('c')
print('cos theta equation:',s.factor(c-(2*c*c-1)))
x1,x2,x3,y1,y2,y3=s.symbols('x1 x2 x3 y1 y2 y3',real=True)
F=x1*(1-y3)+y1*(1-x3)
print('Ambient gradients:',[s.diff(F,q) for q in [x1,x2,x3]],[s.diff(F,q) for q in [y1,y2,y3]])
print('At origin theta=phi=0 cubic:',s.series(f.subs({th:s.Symbol('a')*th,ph:s.Symbol('a')*ph}),s.Symbol('a'),0,4))
