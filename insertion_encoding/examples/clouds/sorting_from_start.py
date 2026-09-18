from cayley_permutations import CayleyPermutation, CanonicalAv
from comb_spec_searcher import CombinatorialSpecification
import json

not_found = [
    "Av(000,0101)",
    "Av(0001,0010,0101)",
    "Av(0001,0010,0101,0000)",
    "Av(0001,0010,0101,0111)",
    "Av(0001,0010,0101,0111,0000)",
    "Av(0001,0100,0101)",
    "Av(0001,0100,0101,0000)",
    "Av(0001,0100,0101,0010)",
    "Av(0001,0100,0101,0111)",
    "Av(0001,0101)",
    "Av(0001,0101,0000)",
    "Av(0001,0101,0010,0100,0000)",
    "Av(0001,0101,0010,0111,0100)",
    "Av(0001,0101,0010,0111,0100,0000)",
    "Av(0001,0101,0111)",
    "Av(0001,0101,0111,0000)",
    "Av(0001,0101,0111,0100,0000)",
    "Av(0001,0101,0111,0100,0000,0011)",
    "Av(0001,0101,0111,0100,0011)",
    "Av(0001,0110,0000)",
    "Av(0001,0110,0111)",
    "Av(0001,0110,0111,0000)",
    "Av(0001,0111,0000)",
    "Av(0001,0111,0100,0000,0011)",
    "Av(0001,0111,0100,0000,0112)",
    "Av(0010,0101)",
    "Av(0010,0101,0000)",
    "Av(0010,0101,0111)",
    "Av(0010,0101,0111,0000)",
    "Av(0011)",
    "Av(0011,0012)",
    "Av(0011,0102)",
    "Av(0011,0102,0012)",
    "Av(0012)",
    "Av(0012,0101,0111)",
    "Av(0100,0101)",
    "Av(0100,0101,0000)",
    "Av(0100,0101,0010)",
    "Av(0100,0101,0010,0000)",
    "Av(0100,0101,0010,0111)",
    "Av(0100,0101,0111)",
    "Av(0100,0101,0111,0000)",
    "Av(0101)",
    "Av(0101,0000)",
    "Av(0101,0010,0111,0100,0000)",
    "Av(0101,0011)",
    "Av(0101,0011,0012)",
    "Av(0101,0012)",
    "Av(0101,0111)",
    "Av(0101,0111,0000)",
    "Av(0102)",
    "Av(0102,0012)",
]


took_too_long = {
    "Av(0100,0101,0111)",
    "Av(0101,0111,0000)",
    "Av(0012,0101,0111)",
    "Av(0001,0010,0101,0000)",
    "Av(0100,0101,0010,0111)",
    "Av(0011,0102)",
    "Av(0100,0101,0000)",
    "Av(0101,0111)",
    "Av(0001,0100,0101,0010)",
    "Av(0100,0101,0111,0000)",
    "Av(0001,0100,0101,0000)",
    "Av(0102,0012)",
    "Av(0100,0101)",
    "Av(0011,0102,0012)",
    "Av(0001,0100,0101,0111)",
    "Av(0010,0101,0111)",
    "Av(0101)",
    "Av(0001,0010,0101,0111)",
    "Av(0010,0101,0111,0000)",
    "Av(0001,0100,0101)",
    "Av(0010,0101,0000)",
    "Av(0001,0101)",
    "Av(0001,0101,0111,0100,0000)",
    "Av(0011)",
    "Av(0001,0101,0010,0111,0100,0000)",
    "Av(0001,0101,0010,0111,0100)",
    "Av(0001,0010,0101,0111,0000)",
    "Av(0102)",
    "Av(0100,0101,0010,0000)",
    "Av(0010,0101)",
    "Av(0101,0010,0111,0100,0000)",
    "Av(0001,0101,0010,0100,0000)",
    "Av(0101,0000)",
    "Av(0001,0010,0101)",
    "Av(0101,0012)",
    "Av(0001,0101,0000)",
    "Av(0001,0101,0111,0000)",
    "Av(0100,0101,0010)",
    "Av(0001,0101,0111)",
}


found_spec = []
found_spec_and_found_before = []
no_spec_too_long_before = []
no_spec_found_before = []

for basis in not_found:
    f = False
    f = True
    # try:
    #     with open(f"specs/{basis}.json", "r") as f:
    #         spec = CombinatorialSpecification.from_dict(json.load(f))
    #     f = True
    # except FileNotFoundError:
    #     pass

    # try:
    #     with open(f"specs/{basis[3:-1]}.json", "r") as f:
    #         spec = CombinatorialSpecification.from_dict(json.load(f))
    #     f = True
    # except FileNotFoundError:
    #     pass

    if f:
        found_spec.append(basis)
        if basis not in took_too_long:
            found_spec_and_found_before.append(basis)
    else:
        if basis in took_too_long:
            no_spec_too_long_before.append(basis)
        else:
            no_spec_found_before.append(basis)


print("Bases with spec before:", len(found_spec))
print(found_spec)
print("Bases with spec and found before:", len(found_spec_and_found_before))
print(found_spec_and_found_before)
print("Bases with no spec:", len(no_spec_found_before))
print(no_spec_found_before)
print("Bases with no spec and took too long:", len(no_spec_too_long_before))
print(no_spec_too_long_before)
