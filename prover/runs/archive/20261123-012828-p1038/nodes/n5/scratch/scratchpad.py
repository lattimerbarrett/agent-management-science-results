import sympy as s
h,x,y,d,T=s.symbols('h x y d T',real=True)
w=x+s.I*y
D=d+h
relation=d**2-h**2-x**2-y**2
# The stereographic coordinate of a direction (h,x,y)/d is w/(d-h).
# The given forward factor, evaluated at that coordinate:
forward_numerator=s.expand(D*(d-h)-s.conjugate(w)*w)
print('forward evaluation numerator:',s.factor(forward_numerator))
print('minus norm relation:',s.simplify(forward_numerator-relation))
# The backward direction has stereographic coordinate -w/(d+h).
print('backward factor at backward coordinate:',s.simplify(-w/D+w/D))
# A unit spinor (alpha,beta)=(D,conjugate(w))/sqrt(2*d*D).
# Hopf map H(alpha,beta)=(|alpha|^2-|beta|^2,2*alpha*conjugate(beta)).
H_height=(D**2-x**2-y**2)/(2*d*D)
print('Hopf height difference numerator:',s.factor(s.together(H_height-h/d)))
print('Hopf complex component:',s.simplify(2*D*w/(2*d*D)))
print('spinor norm minus one:',s.factor((D**2+x**2+y**2)/(2*d*D)-1))
# Homogeneous root forms for spinor (D,bar(w)) and its antipode (-w,D).
print('forward root form:',s.expand(s.conjugate(w)*T-D))
print('backward root form:',s.expand(D*T+w))
print('forward form + D*f_ij:',s.simplify(s.conjugate(w)*T-D+D*(1-s.conjugate(w)/D*T)))
print('backward form - D*f_ji:',s.simplify(D*T+w-D*(T+w/D)))
