from itertools import product

# Every positive Boolean predicate on subsets of a three-element universe
# is the finite analogue of one output coordinate of an enumeration operator.
n = 3
subsets = range(1 << n)
monotone = []
for truth_table in range(1 << (1 << n)):
    if all(not ((truth_table >> a) & 1) or ((truth_table >> b) & 1)
           for a in subsets for b in subsets if a & b == a):
        monotone.append(truth_table)
assert len(monotone) == 20
supports = {
    t: tuple(a for a in subsets
             if (t >> a) & 1
             and not any(b != a and b & a == b and (t >> b) & 1
                         for b in subsets))
    for t in monotone
}
for t in monotone:
    for a in subsets:
        assert ((t >> a) & 1) == any(f & a == f for f in supports[t])

# Universal diagonal/cylinder: projections uniformly recover the input;
# their complementary coordinates recover the complement from the skip.
projection_indices = []
for x in range(n):
    projection = sum(((a >> x) & 1) << a for a in subsets)
    projection_indices.append(monotone.index(projection))
for a in subsets:
    k = sum(((t >> a) & 1) << e for e, t in enumerate(monotone))
    skip = ((1 << len(monotone)) - 1) ^ k
    decoded_a = sum(((k >> e) & 1) << x
                    for x, e in enumerate(projection_indices))
    decoded_complement = sum(((skip >> e) & 1) << x
                             for x, e in enumerate(projection_indices))
    assert decoded_a == a
    assert decoded_complement == ((1 << n) - 1) ^ a

# Exhaustively check the finite positive-conjunction quantifier transformation
# used to show that applying an enumeration operator preserves Sigma_2.
# A(x) = exists u forall v R(x,u,v), with u,v in {0,1}.
checks = 0
for bits in range(1 << (n * 2 * 2)):
    def R(x, u, v):
        return bool((bits >> (4*x + 2*u + v)) & 1)
    a = sum(any(all(R(x, u, v) for v in range(2))
                for u in range(2)) << x for x in range(n))
    for t in monotone:
        lhs = bool((t >> a) & 1)
        rhs = False
        for f in supports[t]:
            xs = [x for x in range(n) if (f >> x) & 1]
            for us in product(range(2), repeat=len(xs)):
                if all(all(R(x, u, v) for x, u, v in zip(xs, us, vs))
                       for vs in product(range(2), repeat=len(xs))):
                    rhs = True
        assert lhs == rhs
        checks += 1

# Dummy quantifier padding, checked for both labels and every truth table
# through three genuine alternating blocks over a two-element domain.
def quantified(table, labels, prefix=()):
    if not labels:
        index = 0
        for bit in prefix:
            index = 2 * index + bit
        return bool((table >> index) & 1)
    values = [quantified(table, labels[1:], prefix + (bit,))
              for bit in range(2)]
    return any(values) if labels[0] == 'E' else all(values)

padding_checks = 0
for m in range(1, 4):
    for first in ('E', 'A'):
        labels = tuple(first if i % 2 == 0 else ('A' if first == 'E' else 'E')
                       for i in range(m))
        for table in range(1 << (1 << m)):
            original = quantified(table, labels)
            # Front dummy block changes the initial label.
            front_table = table | (table << (1 << m))
            front_label = 'A' if first == 'E' else 'E'
            assert quantified(front_table, (front_label,) + labels) == original
            # End dummy block preserves the initial label.
            end_table = sum(((table >> i) & 1) << (2*i + dummy)
                            for i in range(1 << m) for dummy in range(2))
            last_label = 'A' if labels[-1] == 'E' else 'E'
            assert quantified(end_table, labels + (last_label,)) == original
            padding_checks += 1

print('Monotone predicates checked:', len(monotone))
print('Universal-cylinder/skip inputs checked:', 1 << n)
print('Sigma_2 closure finite identities checked:', checks)
print('Quantifier-padding truth tables checked:', padding_checks)
