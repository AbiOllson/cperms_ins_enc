"""For finding the total number of bases, number of symmetry classes,
and how many symmetry classes are insertion encodable or not."""

from cayley_permutations import CayleyPermutation, CanonicalAv, Av
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


"""Taking into account symmetries"""

all_bases = set()
initial_basis = set()
ins_enc_bases = set()
non_ins_enc_bases = set()
non_ins_enc_bases_lex_min = ""
all_bases_in_classes = set()

rgfs_to_size_4 = CanonicalAv([]).generate_cperms_dict(4)
size_3_rgfs = rgfs_to_size_4[3]
print("Size 3 rgfs:", len(size_3_rgfs))
size_4_rgfs = rgfs_to_size_4[4]
print("Size 4 rgfs:", len(size_4_rgfs))

# for rgf in size_4_rgfs:
#     print(rgf)
#     if not rgf.is_rgf():
#         print("Not an rgf!")


for n in range(1, 20):
    for basis in combinations(size_4_rgfs, n):
        basis = lex_min(minimise(set(basis)))
        basis_syms = sym_of_basis(basis)
        basis_syms = frozenset(set(basis_syms))
        if basis_syms in all_bases:
            continue
        if any(
            regular_horizontal_insertion_encoding(b)
            or regular_vertical_insertion_encoding(b)
            for b in basis_syms
        ):
            ins_enc_bases.add(basis_syms)
        else:
            non_ins_enc_bases.add(basis_syms)
            non_ins_enc_bases_lex_min = (
                non_ins_enc_bases_lex_min + str(Av(basis)) + "\n"
            )
        all_bases.add(basis_syms)
        initial_basis.add(basis)
        for b in basis_syms:
            all_bases_in_classes.add(frozenset(set(b)))

print("Total bases found 4s:", len(all_bases))
print("Insertion encodable bases found:", len(ins_enc_bases))
print("Non-insertion encodable bases found:", len(non_ins_enc_bases))
print("Non-insertion encodable bases lex min found:", len(non_ins_enc_bases_lex_min))
print("All bases in classes found:", len(all_bases_in_classes))


with open(f"all_non_inenc_basis_classes_4s_updated.txt", "w") as f:
    f.write(non_ins_enc_bases_lex_min)

# with_size_4s = set()
# initial_basis_with_4s = set()
# new_ins_enc_bases = set()
# new_non_ins_enc_bases = set()
# new_non_ins_enc_bases_lex_min = set()
# new_all_bases_in_classes = set()

# for basis in initial_basis:
#     for cperm in size_4_rgfs:
#         new_basis = lex_min(minimise(set(list(basis) + [cperm])))
#         basis_syms = sym_of_basis(new_basis)
#         basis_syms = frozenset(set(basis_syms))
#         if basis_syms in all_bases or basis_syms in with_size_4s:
#             continue
#         if any(
#             regular_horizontal_insertion_encoding(b)
#             or regular_vertical_insertion_encoding(b)
#             for b in basis_syms
#         ):
#             new_ins_enc_bases.add(basis_syms)
#         else:
#             new_non_ins_enc_bases.add(basis_syms)
#             new_non_ins_enc_bases_lex_min.add(new_basis)
#         with_size_4s.add(basis_syms)
#         initial_basis_with_4s.add(new_basis)
#         for b in basis_syms:
#             new_all_bases_in_classes.add(frozenset(set(b)))


# print("\nTotal bases found 3s_4x1:", len(with_size_4s))
# print("Insertion encodable bases found:", len(new_ins_enc_bases))
# print("Non-insertion encodable bases found:", len(new_non_ins_enc_bases))
# print(
#     "Non-insertion encodable bases lex min found:", len(new_non_ins_enc_bases_lex_min)
# )
# print("All bases in classes found:", len(new_all_bases_in_classes))


# with open(f"all_non_inenc_basis_classes_3s_4x1.txt", "w") as f:
#     f.write(repr(new_non_ins_enc_bases_lex_min))
