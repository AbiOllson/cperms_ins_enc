from cayley_permutations import CayleyPermutation
from insertion_encoding.rgf_clouds import RGFTrackedSearcher
from cayley_permutations import CanonicalAv
from comb_spec_searcher import StrategyPack, AtomStrategy
from comb_spec_searcher.exception import ExceededMaxtimeError
import json

type_of_bases = "3s"
# type_of_bases = "3s_4x2"
# type_of_bases = "3s_4x1"
# type_of_bases = "4s_updated"

with open(f"all_non_inenc_basis_classes_{type_of_bases}.txt", "r") as f:
    bases = eval(f.read())

print(len(bases))

took_too_long = []
for basis in bases:
    try:
        spec = RGFTrackedSearcher(basis).auto_search(max_expansion_time=600)
        json_spec = json.dumps(spec.to_jsonable())
        with open(f"non fusion specs/{CanonicalAv(basis)}.json", "w") as f:
            f.write(json_spec)
    except ExceededMaxtimeError:
        print(f"Exceeded time for basis {basis}")
        took_too_long.append(basis)
        continue

print(f"Total bases that took too long: {len(took_too_long)}")
print(took_too_long)
