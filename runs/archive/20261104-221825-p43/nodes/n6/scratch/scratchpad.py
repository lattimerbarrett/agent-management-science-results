# Test the proposed joining arc for the properties usually needed to
# coalesce critical points along a gradient trajectory.
import sympy as s
t=s.symbols('t',real=True)
x=s.Matrix([s.sin(t),0,s.cos(t)])
y=s.Matrix([s.sin(t),0,-s.cos(t)])
e=s.Matrix([0,0,1])
grad=s.Matrix.vstack(e-x[2]*x,e-y[2]*y)
tangent=s.Matrix.vstack(x.diff(t),y.diff(t))
print('f along arc:',s.simplify(x[2]+y[2]))
print('df(tangent):',s.simplify(grad.dot(tangent)))
print('|grad f|^2:',s.simplify(grad.dot(grad)))
print('gradient dot arc tangent:',s.simplify(grad.dot(tangent)))
print('Thus the arc is in a level set and is nowhere a gradient trajectory in its interior.')