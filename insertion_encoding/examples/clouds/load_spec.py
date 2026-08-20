from cayley_permutations import CayleyPermutation, CanonicalAv
from insertion_encoding.rgf_clouds import RGFTrackedSearcher
import json
from comb_spec_searcher import CombinatorialSpecification

basis = "Av(0011,0101,0102)"
n = 10

# with open(f"1cv specs rc sep wrong counts\{CanonicalAv(basis)}.json", "r") as f:
#     spec = CombinatorialSpecification.from_dict(json.load(f))
spec = RGFTrackedSearcher(basis).auto_search(max_expansion_time=6000)

spec.show()
# spec.get_genf()

spec_counts = [spec.count_objects_of_size(i) for i in range(n)]
print("spec counts")
print(spec_counts)
class_counts = CanonicalAv(basis).counter(n - 1)
print("actual counts")
print(class_counts)

# assert (
#     spec_counts == class_counts
# ), f"Counts do not match for basis {CanonicalAv(basis)}"
