from insertion_encoding.rgf_clouds import RGFTrackedSearcher

basis = "000"


spec = RGFTrackedSearcher(basis).auto_search(max_expansion_time=600)

# Print the specification
spec.show()

# Print the generating function
spec.get_genf()

# Print the counts up to size n
n = 10
print([spec.count_objects_of_size(i) for i in range(n)])
