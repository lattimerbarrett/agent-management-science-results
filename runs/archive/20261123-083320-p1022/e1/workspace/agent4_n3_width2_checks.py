import sympy as s, json, pathlib
h,H,t=s.symbols('h H t')
G=s.groebner([h**4,H**3-2*h*H**2+2*h**2*H],H,h)
def reduce_expr(expr):
    # split coefficient variables from the incidence ring variables
    pp=s.Poly(s.expand(expr),H,h)
    out=0
    for (i,j), coeff in pp.terms():
        out+=coeff*G.reduce(H**i*h**j)[1]
    return s.expand(out)

def equations(mult):
    vs=[]; factors=[]
    for i,m in enumerate(mult):
        a=len(mult)-1-i
        b=s.Symbol('b'+str(i));vs.append(b)
        if m==1:
            factor=1+(a*h+b*H)*t
        elif m in (2,3):
            u,v=s.symbols('u'+str(i)+' v'+str(i));vs.extend([u,v])
            c2=u*H**2+v*(h*H-h**2)
            factor=1+(m*a*h+b*H)*t+(s.binomial(m,2)*a*a*h*h+(m-1)*a*h*b*H+c2)*t*t
            if m==3:
                w=s.Symbol('w'+str(i));vs.append(w)
                factor+=(a**3*h**3+a*a*h*h*b*H+a*h*c2+w*H*(h*H-h*h))*t**3
        else: raise NotImplementedError
        factors.append(factor)
    total=s.Poly(s.prod(factors),t)
    eq=[]
    for degree in range(1,sum(mult)+1):
        p=s.Poly(reduce_expr(total.nth(degree)),H,h)
        for (i,j), coeff in p.terms():
            if i!=0: eq.append(coeff)
    eq=list(dict.fromkeys(s.factor(x) for x in eq if x!=0))
    return vs,eq,total
result={}
for mult in [(2,1,2)]:
    vs,eq,total=equations(mult)
    print('MULT',mult,'variables',vs,'eq',eq,flush=True)
    if mult in [(1,2,2),(2,1,2)]:
        sub=s.solve(eq[:3], [vs[4],vs[5],vs[6]],dict=True)[0]
        eq=[s.factor(e.subs(sub)) for e in eq[3:]]
        vs=vs[:4]
        print('REDUCED',sub,eq,flush=True)
    gb=s.groebner(eq,*vs,order='grevlex',method='f5b')
    print('GROEBNER',list(gb),flush=True)
    if gb.is_zero_dimensional:
        gb=gb.fglm(order='lex');print('LEX',list(gb),flush=True)
    result[str(mult)]={'variables':list(map(str,vs)),'equations':list(map(str,eq)),'groebner':list(map(str,gb))}
pathlib.Path('workspace/agent4_n3_width2_checks.py').write_text(pathlib.Path(__file__).read_text())
pathlib.Path('workspace/agent4_n3_width2_checks.json').write_text(json.dumps(result,indent=2))
print('Stored exact Groebner conditions.')
