from insertion_encoding.rgf_clouds import RGFTrackedSearcher
from cayley_permutations import CanonicalAv

basis = "0001,0101,0010,0111,0100,0000,0011"


spec = RGFTrackedSearcher(basis).auto_search(max_expansion_time=600)

# with open("clouds_spec.json", "w") as f:
#     f.write(spec.to_jsonable())

# Print the specification
# spec.show()

# Print the generating function
# spec.get_genf()

# Print the counts up to size n
n = 10
print([spec.count_objects_of_size(i) for i in range(n)])
print(CanonicalAv(basis).counter(n - 1))

# for gcp in spec.get_objects(5)[()]:
#     print(gcp.pattern)

for rgf in CanonicalAv(basis).generate_cperms(5):
    print(rgf)
