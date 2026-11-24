import sympy as s
# Exact graph pullback: (y,t) -> (y,t+h(y)); verify kinetic inverse and boundary density.
p,q,A,B,C=s.symbols('p q A B C', real=True)
J=s.Matrix([[1,0,0],[0,1,0],[p,q,1]])
G=J.T*J
print('inverse pullback metric:');print(s.simplify(G.inv()))
# In 2 tangential dimensions the same tensor formula applies in all dimensions.
S=1+p*p+q*q
b=A+B-(p*p*A+2*p*q*C+q*q*B)/S
print('H dS =',s.factor(b))
print('Exact energy graph terms: -int h_a v_a v_n + (1/2)int |Dh|^2 v_n^2 + c int [Delta h - h_a h_b h_ab/(1+|Dh|^2)] v^2.')
# physical cutoff V=eta U: retain every graph term, including derivatives of eta
u,ua,un,eta,ea,en,fa=s.symbols('U U_a U_n eta eta_a eta_n f_a')
lin=-fa*(eta*ua+u*ea)*(eta*un+u*en)
print('Linear bulk cutoff contribution beyond eta^2 core:',s.expand(lin+fa*eta**2*ua*un))
print('Quadratic bulk cutoff integrand:',s.expand(s.Rational(1,2)*fa**2*(eta*un+u*en)**2))
print('At second order after eliminating correction, coefficient is B_cut - 1/2<S_cut,A_cut^{-1}S_cut>, not the source pairing alone.')
