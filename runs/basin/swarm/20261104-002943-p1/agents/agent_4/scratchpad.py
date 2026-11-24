from sage.all import ComplexBallField,RealBallField
C=ComplexBallField(80)
print(hasattr(C,'integral'))
print(C.integral.__doc__[:6000] if hasattr(C,'integral') else '')
