import itertools,json
checks=0
for n in range(1,5):
    U=set(range(n))
    for f in itertools.product(range(n),repeat=n):
        for mask in range(1<<n):
            KB={i for i in U if mask>>i&1}
            KA={i for i in U if f[i] in KB}
            assert U-KA=={i for i in U if f[i] in U-KB}
            checks+=1
print(json.dumps({'checks':checks}))
