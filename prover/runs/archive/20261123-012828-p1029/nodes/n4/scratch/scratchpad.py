# Audit of implications used in the previous answers.
claims = {
    'AW*-factor => quasitracial metric complete': False,
    'faithful normalized trace => increments telescope': True,
    'metric Cauchy + closed embedded bounded ball => limit belongs to M': True,
    'completion alone => limit belongs to M': False,
}
for claim, valid in claims.items():
    print(('VALID' if valid else 'INVALID') + ': ' + claim)
print('For a trace, N constant increments give N*eta = tau(a_N)-tau(a_0) <= 1.')
