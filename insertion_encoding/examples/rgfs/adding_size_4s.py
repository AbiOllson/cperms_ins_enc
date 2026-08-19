"""For finding the total number of bases, number of symmetry classes,
and how many symmetry classes are insertion encodable or not."""

from cayley_permutations import CayleyPermutation, CanonicalAv
from cayley_permutations.simplify_basis import minimise, lex_min
from typing import Iterable
from itertools import combinations, permutations
from insertion_encoding import (
    rgf_regular_horizontal_insertion_encoding as regular_horizontal_insertion_encoding,
)
from insertion_encoding import (
    rgf_regular_vertical_insertion_encoding as regular_vertical_insertion_encoding,
)


def complement(cperm: CayleyPermutation) -> CayleyPermutation:
    """returns the complement of the cperm"""
    n = len(cperm)
    m = max(cperm)
    return CayleyPermutation(tuple(m - cperm[i] for i in range(n)))


def symmetries(cperm: CayleyPermutation) -> frozenset[CayleyPermutation]:
    """returns the list of symmetries of the cperm"""
    return list(
        frozenset(
            [cperm, complement(cperm), cperm.reverse(), complement(cperm.reverse())]
        )
    )


def sym_of_basis(cperms: list[CayleyPermutation]) -> list[frozenset[CayleyPermutation]]:
    """returns the list of symmetries of the list of cperms"""
    return [frozenset(cperms)]
    b1 = []
    b2 = []
    b3 = []
    for cperm in cperms:
        b1.append(cperm.reverse())
        b2.append(complement(cperm))
        b3.append(complement(cperm.reverse()))
    return sorted(
        [frozenset(cperms), frozenset(b1), frozenset(b2), frozenset(b3)],
        key=lambda x: (len(x), x),
        # key=lambda x: sorted(list(x))[0],
    )


# with open(f"cayley tilings/3s_4x1/all_non_inenc_basis_classes.txt", "r") as f:
#     bases_3s_4x1 = eval(f.readline())
# bases_to_add_to = bases_3s_4x1.copy()

with open(f"all_non_inenc_basis_classes_3s_4x1.txt", "r") as f:
    bases_to_add_to = eval(f.readline())


def check_lengths_of_cperms(basis, n: int) -> bool:
    """If there are fewer than n cperms of length 4 in the basis, return False."""
    count = 0
    for cperm in basis:
        if len(cperm) == 4:
            count += 1
    return count >= n


rgfs_to_size_4 = CanonicalAv([]).generate_cperms_dict(4)
size_3_rgfs = rgfs_to_size_4[3]
print("Size 3 rgfs:", len(size_3_rgfs))
size_4_rgfs = rgfs_to_size_4[4]
print("Size 4 rgfs:", len(size_4_rgfs))

for n in range(16):  # n+1 = number of size 4 patterns
    insenc_bases_classes_this_iter = set()
    non_insenc_bases_classes_this_iter = set()
    bases_this_iter = set()  # non ins enc, just bases not classes
    if not bases_to_add_to:
        break
    for basis in bases_to_add_to:
        for cperm in size_4_rgfs:
            new_basis = lex_min(minimise(set(list(basis) + [cperm])))
            basis_syms = sym_of_basis(new_basis)
            basis_syms = frozenset(set(basis_syms))
            if not check_lengths_of_cperms(new_basis, n + 1):
                continue
            if (
                # basis_syms in all_bases_considered
                basis_syms in insenc_bases_classes_this_iter
                or basis_syms in non_insenc_bases_classes_this_iter
            ):
                continue
            if any(
                regular_horizontal_insertion_encoding(b)
                or regular_vertical_insertion_encoding(b)
                for b in basis_syms
            ):
                insenc_bases_classes_this_iter.add(basis_syms)
            else:
                non_insenc_bases_classes_this_iter.add(basis_syms)
                bases_this_iter.add(new_basis)
    print("with", n + 1, "size 4 patterns")
    print(f"ins enc bases found {len(insenc_bases_classes_this_iter)}")
    print(f"non ins enc bases found {len(non_insenc_bases_classes_this_iter)}")

    with open(f"all_non_inenc_basis_classes_3s_4x{n+1}.txt", "w") as f:
        f.write(repr(bases_this_iter))

    # all_bases_considered.update(non_insenc_bases_classes_this_iter)
    bases_to_add_to = bases_this_iter
