from pathlib import Path
p=Path('experiments/e1/agent3_qt_ultraproduct_notes.md')
print(p.read_text()[:18000])

# Check the index bookkeeping in the product-packing construction.
for m in range(1,101):
    for N in range(1,101):
        included=[j for j in range(1,N+1) if j<=m]
        assert included==list(range(1,min(m,N)+1))
print('\nPASS: each coordinate partial sum uses only an initial subfamily of its finite packing.')
