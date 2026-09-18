from cayley_permutations import CayleyPermutation
from insertion_encoding.rgf_clouds import RGFTrackedSearcher, RGFRCSepSearcher
from cayley_permutations import CanonicalAv
from comb_spec_searcher import CombinatorialSpecification, StrategyPack, AtomStrategy
from comb_spec_searcher.exception import ExceededMaxtimeError
import json

type_of_bases = ["3s", "3s_4x2", "3s_4x1", "4s_updated"]


took_too_long = []
tot_found = 0
enumerated = []

# for basis_type in type_of_bases:
#     with open(f"all_non_inenc_basis_classes_{basis_type}.txt", "r") as f:
#         bases = sorted(eval(f.read()))[40:]


with open("bases_4s.txt", "r") as f:
    bases = eval(f.read())

num_bases = len(bases)
basis_on = 1
for basis in bases:
    print(f"Basis {basis_on} of {num_bases}: {basis}")
    basis_on += 1
    # if basis in took_too_long_before:
    #     print(f"Skipping basis {basis} because it took too long last time")
    #     took_too_long.append(basis)
    #     continue
    found = False
    try:
        with open(f"non fusion specs/{CanonicalAv(basis)}.json", "r") as f:
            spec = CombinatorialSpecification.from_dict(json.load(f))
        found = True
        tot_found += 1
    except FileNotFoundError:
        pass
    try:
        with open(f"fusion specs/{CanonicalAv(basis)}.json", "r") as f:
            spec = CombinatorialSpecification.from_dict(json.load(f))
        found = True
        tot_found += 1
    except FileNotFoundError:
        pass
    if not found:
        try:
            spec = RGFRCSepSearcher(basis).auto_search(max_expansion_time=60 * 60 * 3)
            json_spec = json.dumps(spec.to_jsonable())
            with open(f"non fusion specs/{CanonicalAv(basis)}.json", "w") as f:
                f.write(json_spec)
            tot_found += 1
            enumerated.append(CanonicalAv(basis).as_one_based())
        except ExceededMaxtimeError:
            pass
        if not found:
            try:
                spec = RGFTrackedSearcher(basis).auto_search(
                    max_expansion_time=60 * 60 * 3
                )
                json_spec = json.dumps(spec.to_jsonable())
                with open(f"fusion specs/{CanonicalAv(basis)}.json", "w") as f:
                    f.write(json_spec)
                enumerated.append(CanonicalAv(basis).as_one_based())
                tot_found += 1
            except ExceededMaxtimeError:
                print(f"Exceeded time for basis {basis}")
                took_too_long.append(CanonicalAv(basis).as_one_based())
                with open(f"took_too_long.txt", "w") as f:
                    f.write(str(took_too_long))

print(f"Total bases that took too long: {len(took_too_long)}")
print(took_too_long)
print(f"Total bases found: {tot_found}")
print(f"Total bases enumerated: {len(enumerated)}")
print(enumerated)

# for basis in bases:
#     basis = CanonicalAv(basis).basis
#     try:
#         spec = RGFRCSepSearcher(basis).auto_search(max_expansion_time=60 * 60)
#         json_spec = json.dumps(spec.to_jsonable())
#         with open(f"non fusion specs/{CanonicalAv(basis)}.json", "w") as f:
#             f.write(json_spec)
#         break
#     except ExceededMaxtimeError:
#         try:
#             spec = RGFTrackedSearcher(basis).auto_search(max_expansion_time=60 * 60)
#             json_spec = json.dumps(spec.to_jsonable())
#             with open(f"fusion specs/{CanonicalAv(basis)}.json", "w") as f:
#                 f.write(json_spec)
#         except ExceededMaxtimeError:
#             print(f"Exceeded time for basis {basis}")
#             took_too_long.append(basis)

# print(f"Total bases that took too long: {len(took_too_long)}")
# print(took_too_long)
