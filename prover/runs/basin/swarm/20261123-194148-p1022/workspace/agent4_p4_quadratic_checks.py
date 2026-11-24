"""Finite symbolic checks for the P3-direction-map quadratic obstruction."""
import sympy as s

def check():
 h=s.symbols('h')
 tangent_quadric=s.series((1+2*h)**5/(1+4*h),h,0,4).removeO().expand()
 horizontal=(1+2*h)**3
 assert tangent_quadric.coeff(h,2)==16
 assert horizontal.expand().coeff(h,2)==12
 assert s.expand(horizontal).coeff(h,1)==6
 assert s.expand((1+2*h)**4).coeff(h,1)==8
 a,b,c,d,e,f,z,w=s.symbols('a b c d e f z w')
 q=a*z*z+b*z*w+c*w*w
 r=d*z*z+e*z*w+f*w*w
 J=s.expand(s.diff(q,z)*s.diff(r,w)-s.diff(q,w)*s.diff(r,z))
 assert J==s.expand(2*(a*e-b*d)*z*z+4*(a*f-c*d)*z*w+2*(b*f-c*e)*w*w)
 # The three coefficients are the three 2x2 minors of [[a,b,c],[d,e,f]],
 # up to nonzero constants: J identically zero iff q,r proportional.
 print({'horizontal_c2':12,'quadric_tangent_c2':16,
        'linear_span_c1':8,'horizontal_c1':6,'binary_Jacobian':J})
if __name__=='__main__':check()
