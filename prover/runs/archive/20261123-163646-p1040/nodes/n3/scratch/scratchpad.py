# Filtered-group countermodels: G = UT_{d+1}(F_3), 1 <= d <= 6.
# Its lower central series C has |C_r| = 3^((d+1-r)(d+2-r)/2)
# for r <= d and C_r=1 otherwise. Its last term C_d has order 3.
# Define A_r=C_r for r<=d, A_r=C_d for d<r<=7, A_r=1 for r>=8.
# The delayed term is central, so this is a strongly central filtration.
def clog(d, r):
    return (d+1-r)*(d+2-r)//2 if r <= d else 0

def alog(d, r):
    return clog(d, r) if r <= d else (1 if r <= 7 else 0)

for d in range(1,7):
    # Since all terms are nested C-series terms, log-order of an
    # intersection is the smaller log-order.
    kernels = [r for r in range(1,8)
               if min(clog(d,r), alog(d,r+1)) > clog(d,r+1)]
    cokernel7 = alog(d,7) - max(clog(d,7), alog(d,8))
    print(f'class {d}: nonzero kernel degrees {kernels}; degree-7 cokernel order {3**cokernel7}')
