import numpy as np

def char_diagonal(values,p):
    a=np.asarray(values,dtype=float)
    ratios=np.max((a[:,None,:]/a[None,:,:])**(1/p),axis=2)
    return np.mean(np.mean(ratios**(p/(p-1)),axis=1)**(p-1))
for p in [1.5,3.0]:
    w=np.array([1.,4.,25.])
    scalar=w.mean()*np.mean(w**(-1/(p-1)))**(p-1)
    scalar_matrix=char_diagonal(np.column_stack([w,w]),p)
    diagonal=char_diagonal(np.column_stack([w,np.ones(3)]),p)
    constant=char_diagonal(np.tile([0.01,100.],(3,1)),p)
    print(dict(p=p,scalar_Ap=scalar,scalar_matrix_Ap=scalar_matrix,diagonal_Ap=diagonal,constant_matrix_Ap=constant))
