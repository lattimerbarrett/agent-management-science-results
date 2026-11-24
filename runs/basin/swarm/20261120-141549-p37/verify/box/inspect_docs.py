try:
 from sage.all import Posets
 p=Posets.AntichainPoset(2)
 print(p.cartesian_product.__doc__)
 print(p.dimension.__doc__)
except Exception as e:print(type(e),e)
