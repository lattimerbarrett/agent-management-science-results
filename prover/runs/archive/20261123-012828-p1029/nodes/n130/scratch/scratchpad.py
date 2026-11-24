import os
for team in ['e1','e2','e3']:
    root=os.path.join('experiments',team)
    print(root, 'exists:',os.path.isdir(root))
    if os.path.isdir(root):
        for base,dirs,files in os.walk(root):
            for f in files:
                if any(k in f for k in ['completion_audit','reduction_notes','partial_proof','spectral_norm_detector']):
                    print(os.path.join(base,f))
print('\nContinuity audit: if a = sup a_n, set b_n=a-a_n, c_n=1-b_n.')
print('Then b_n decreases to 0; c_n increases to 1.')
print('For fixed increments eta, monotonicity gives tau(b_n)>=eta.')
print('Since b_n commutes with 1, tau(c_n)=1-tau(b_n)<=1-eta.')
print('Thus tau fails normality along the increasing sequence c_n with supremum 1.')
