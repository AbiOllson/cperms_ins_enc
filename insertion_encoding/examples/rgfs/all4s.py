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

rgfs_to_size_4 = CanonicalAv([]).generate_cperms_dict(4)
size_4_rgfs = rgfs_to_size_4[4]
print("Size 4 rgfs:", len(size_4_rgfs))

all_bases = set()
ins_enc_basis = set()
non_ins_enc_basis = set()
# to_compute = ""

for n in range(20):
    for basis in combinations(size_4_rgfs, n):
        basis = frozenset(basis)
        if basis in all_bases:
            continue
        all_bases.add(basis)
        if regular_horizontal_insertion_encoding(
            basis
        ) or regular_vertical_insertion_encoding(basis):
            ins_enc_basis.add(basis)
        else:
            non_ins_enc_basis.add(basis)
            # to_compute += str(Av(sorted(basis))) + "\n"
            # for rgf in basis:
            #     if not rgf.is_rgf():
            #         raise ValueError(f"{rgf} is not an RGF")
    print("with", n, "size 4 patterns")
    print(f"ins enc bases found {len(ins_enc_basis)}")
    print(f"non ins enc bases found {len(non_ins_enc_basis)}")
    print("total bases found", len(all_bases))

to_compute = ""
for basis in sorted(non_ins_enc_basis, key=lambda x: (len(x), x)):
    to_compute += str(Av(sorted(basis))) + "\n"

with open(f"all_non_inenc_basis_classes_4s_updated.txt", "w") as f:
    f.write(to_compute)
