def verify():
 d,M=128,28
 for w in range(280,313,2):
  assert (w-d)/2>M
  assert w>d+2*M
  assert 5*w>8*d+12*M
 triple_weights={256,272,288,296,304,308,312,314,316}
 for w in (322,326,330,334):
  allowed=[]
  for P in range(9,40,2):
   g=w-2*P
   if g>=256 and g in triple_weights and (g-128)<=4*P:allowed.append(g)
  assert allowed==[256],(w,allowed)
  assert (2*w+128)//3<272
 print('PASS projected-pair three/four-flat arithmetic and conditional Case1')
if __name__=='__main__':verify()
