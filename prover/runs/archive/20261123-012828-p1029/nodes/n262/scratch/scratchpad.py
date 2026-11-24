import sympy as s
S=s.diag(s.Rational(1,5),s.Rational(4,5))
B=s.eye(2)-S
t=s.Rational(3,10)
Plo=s.diag(1,0); Phi=s.diag(0,1)
tr=lambda X:s.trace(X)/2
print('S=',S,'tail B=',B,'t=',t)
print('low-corner tail minus claimed t-bound:',Plo*B*Plo-t*Plo)
print('high-cut compression loss=',tr(B)-tr(Phi*B*Phi),'>t:',tr(B)-tr(Phi*B*Phi)>t)
print('corner dimensions:',tr(Plo),tr(Phi))
print('normalized corner quasitraces of compressed B:',tr(Plo*B*Plo)/tr(Plo),tr(Phi*B*Phi)/tr(Phi))
print('correct high-corner bound (1-t)Phi - Phi B Phi:',(1-t)*Phi-Phi*B*Phi)
print('All examples use the ordinary trace: the issue precedes any quasitrace nonlinearity.')
