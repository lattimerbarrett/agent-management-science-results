"""Exact quadratic-ramification calculations for the P2 fibre obstruction."""
import sympy as s

def check():
 x,y,z=s.symbols('x y z')
 A,B,C,D,E,F=s.symbols('A B C D E F')
 g=s.Matrix([A*x+B*y,C*x+D*y,E*x+F*y])
 normal=s.Matrix([y*y,-2*x*y,x*x])
 condition=s.Poly((normal.dot(g)),x,y)
 sol=s.solve(condition.coeffs(),(A,B,E,F),dict=True)
 assert sol==[{A:2*D,B:0,E:0,F:2*C}]
 a,b,c,d,e,f=s.symbols('a b c d e f')
 quadrics=s.Matrix([x*x+z*(a*x+b*y)+c*z*z,
                     y*y+z*(d*x+e*y)+f*z*z,z*z])
 jac=s.factor(quadrics.jacobian((x,y,z)).det())
 assert s.expand(jac-2*z*((2*x+a*z)*(2*y+e*z)-b*d*z*z))==0
 assert s.expand((jac/(2*z)).subs(z,0))==4*x*y
 print({'conic_tangent_constraints':sol,'pencil_jacobian':jac})

if __name__=='__main__':check()
