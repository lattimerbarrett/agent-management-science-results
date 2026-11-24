s=3
j=2**s-2
lower=(3*j+1)//2
upper=j+2**(j.bit_length()-1)
print(f's={s}, measures={j}')
print(f'Moment-curve lower bound: {lower}')
print(f'General two-hyperplane upper bound: {upper}')
print(f'Unresolved candidate dimensions: {list(range(lower,upper+1))}')
print('An exact formula for all s would in particular determine Delta(6,2).')
