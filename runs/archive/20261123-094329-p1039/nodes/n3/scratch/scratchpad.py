import sympy as s
# rho=(|z1|^2-1)^2+sum_{j>=2}|zj|^2-2.
# At q=(0,1,0,...), rho=0; its complex tangent has v2=0.
for n in range(2,6):
    ambient=s.diag(-2,*([1]*(n-1)))
    tangent=s.diag(-2,*([1]*(n-2)))
    print('n =', n, '; K-oriented tangent Levi =', list(tangent.diagonal()), '; complement-oriented =', list((-tangent).diagonal()))
