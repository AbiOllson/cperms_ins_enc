# from insertion_encoding.rgf_clouds import RGFTrackedSearcher
from cayley_permutations import CanonicalAv
from insertion_encoding import RGFVerticalSearcher
import json

basis = "0001,0101,0010,0111,0100,0000,0011"
basis = "021, 000, 012"


spec = RGFVerticalSearcher(basis).auto_search(max_expansion_time=600)

with open(f"Av({basis}).json", "w") as f:
    f.write(json.dumps(spec.to_jsonable()))

# Print the specification
# spec.show()

# Print the generating function
# spec.get_genf()

# Print the counts up to size n
n = 10
print([spec.count_objects_of_size(i) for i in range(n)])
print(CanonicalAv(basis).counter(n - 1))
