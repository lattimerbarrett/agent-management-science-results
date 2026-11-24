import sympy as s
q=s.symbols('q')
# basis: 1,a,b,p with a^2=b^2=q and p=ab
A=s.Matrix([[0,q,0,0],[1,0,0,0],[0,0,0,q],[0,0,1,0]])
B=s.Matrix([[0,0,q,0],[0,0,0,q],[1,0,0,0],[0,1,0,0]])
print('a^2=q:',A*A==q*s.eye(4))
print('b^2=q:',B*B==q*s.eye(4))
print('ab=ba:',A*B==B*A)
print('spectral consequences with T=4*pi:')
print('c(1)>c(a)>c(1)-T; c(1)>c(b)>c(1)-T')
print('c(a),c(b)>c(p)>c(a)-T,c(b)-T')
print('If there were only two action residues, these inequalities alone allow c(a)=c(b), c(p)=c(1)-T.')
print('Therefore scalar spectral inequalities alone do not prove the lower bound; the full degenerate Arnold-Floer theorem is required.')