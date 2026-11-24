from pathlib import Path
p=Path('experiments')
print('exists',p.exists())
if p.exists():
 for x in p.iterdir():
  print(x, list(x.iterdir())[:8])
print('Lefschetz sum must be 4. The local germs Re(z^3+w^2) show that isolated indices 2 are locally possible; hence a global extremal-selector restriction is essential, not a bound on each local index.')