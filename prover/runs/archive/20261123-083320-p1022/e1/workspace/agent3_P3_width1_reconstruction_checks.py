import sympy as s, json, os
x,y,t,c2,c3=s.symbols('x y t c2 c3')
a=2
f=lambda z: a*z+(a*a-2*c2)*z*z/2+(a**3-3*a*c2+3*c3)*z**3/6
num=s.cancel((f(t*x)-f(t*y))/(t*(x-y)))
den=sum(t**(k-1)*sum(x**j*y**(k-1-j) for j in range(k))/s.factorial(k) for k in range(1,4))
ch=s.series(num/den,t,0,3).removeO().expand()
c1v=s.expand(ch.coeff(t,1)); ch2=s.expand(ch.coeff(t,2));c2v=s.expand(c1v*c1v/2-ch2)
assert s.expand(c1v-(1-c2)*(x+y))==0
expected={(1,0):0,(2,0):x*x+x*y+y*y,(2,2):0}
for vals,v in expected.items(): assert s.expand(c2v.subs({c2:vals[0],c3:vals[1]})-v)==0
A,H,K=s.symbols('A H K')
flag=-A*H*K-A*A*K*K
sol0=s.solve([s.expand(flag).coeff(H,1).coeff(K,1),s.expand(flag).coeff(K,2)],A)
sol1=s.solve([s.expand(flag-(H*K-K*K)).coeff(H,1).coeff(K,1),s.expand(flag-(H*K-K*K)).coeff(K,2)],A)
assert sol0==[(0,)] or sol0=={A:0}
assert sol1==[(-1,)] or sol1=={A:-1}
out={'c1V':str(c1v),'c2V':str(c2v),'expected':{str(k):str(v) for k,v in expected.items()},'flag_split_solution':str(sol0),'flag_spinor_solution':str(sol1)}
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent3_P3_width1_reconstruction_checks.json','w') as out_f: json.dump(out,out_f)
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_P3_width1_reconstruction_checks.py'):
 source=open(__file__).read()
 with open('workspace/agent3_P3_width1_reconstruction_checks.py','w') as out_f: out_f.write(source)
print(json.dumps(out,indent=2))
