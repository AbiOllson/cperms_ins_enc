from cayley_permutations import CayleyPermutation
from insertion_encoding.rgf_clouds import RGFTrackedSearcher, RGFRCSepSearcher
from cayley_permutations import CanonicalAv
from comb_spec_searcher import CombinatorialSpecification, StrategyPack, AtomStrategy
from comb_spec_searcher.exception import ExceededMaxtimeError
import json

type_of_bases = ["3s", "3s_4x2", "3s_4x1", "4s_updated"]

# bases_running = [
#     (CayleyPermutation((0, 0, 0)), CayleyPermutation((0, 1, 0, 1))),
#     "Av(0102)",
#     "Av(0012)",
#     "Av(0101)",
#     "Av(0011)",
# ]

took_too_long = []
tot_found = 0

for basis_type in type_of_bases:
    with open(f"all_non_inenc_basis_classes_{basis_type}.txt", "r") as f:
        bases = sorted(eval(f.read()))[40:]

    print(len(bases))
    for basis in bases:
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
                spec = RGFRCSepSearcher(basis).auto_search(max_expansion_time=60 * 60)
                json_spec = json.dumps(spec.to_jsonable())
                with open(f"non fusion specs/{CanonicalAv(basis)}.json", "w") as f:
                    f.write(json_spec)
                tot_found += 1
            except ExceededMaxtimeError:
                pass
            if not found:
                try:
                    spec = RGFTrackedSearcher(basis).auto_search(
                        max_expansion_time=60 * 60
                    )
                    json_spec = json.dumps(spec.to_jsonable())
                    with open(f"fusion specs/{CanonicalAv(basis)}.json", "w") as f:
                        f.write(json_spec)
                    tot_found += 1
                except ExceededMaxtimeError:
                    print(f"Exceeded time for basis {basis}")
                    took_too_long.append(basis)

print(f"Total bases that took too long: {len(took_too_long)}")
print(took_too_long)
print(f"Total bases found: {tot_found}")

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
