from insertion_encoding.rgf_clouds import RGFTrackedSearcher
from cayley_permutations import CanonicalAv, CayleyPermutation
import json

# with open("bases.txt", "r") as f:
#     bases = eval(f.read())
bases = [
    (CayleyPermutation((0, 0, 0, 0)), CayleyPermutation((0, 1, 1, 2))),
    (CayleyPermutation((0, 1, 0, 2)), CayleyPermutation((0, 1, 1, 1))),
    (CayleyPermutation((0, 0, 1, 1)), CayleyPermutation((0, 1, 1, 1))),
    (CayleyPermutation((0, 1, 0, 0)), CayleyPermutation((0, 1, 1, 1))),
    (CayleyPermutation((0, 0, 1, 0)), CayleyPermutation((0, 1, 1, 1))),
    (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 1, 1, 1))),
    (CayleyPermutation((0, 1, 1, 1)), CayleyPermutation((0, 0, 0, 0))),
    (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 1, 1, 0))),
    (CayleyPermutation((0, 0, 1, 0)), CayleyPermutation((0, 0, 1, 2))),
    (CayleyPermutation((0, 1, 0, 0)), CayleyPermutation((0, 0, 1, 1))),
    (CayleyPermutation((0, 0, 1, 0)), CayleyPermutation((0, 0, 1, 1))),
    (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 0, 1, 1))),
    (CayleyPermutation((0, 0, 1, 1)), CayleyPermutation((0, 0, 0, 0))),
    (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 1, 0, 0))),
    (CayleyPermutation((0, 1, 0, 0)), CayleyPermutation((0, 0, 0, 0))),
    (CayleyPermutation((0, 0, 1, 0)), CayleyPermutation((0, 0, 0, 0))),
    (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 0, 0, 0))),
]

bases = {
    "1122,1222",
    "1121,1123",
    "1211,1122",
    "1121,1122",
    "1112,1122",
    "1122,1111",
    "1112,1211",
}
n = 10

correct_counts = set()
incorrect_counts = set()
took_too_long = set()

for basis in bases:
    # basis = basis[3:-1]
    try:
        spec = RGFTrackedSearcher(basis).auto_search(max_expansion_time=6000)
    except Exception as e:
        print(f"Basis {CanonicalAv(basis)} took too long or failed with error: {e}")
        took_too_long.add(basis)
        continue

    with open(f"1cv_to_enumerate\{CanonicalAv(basis)}.json", "w") as f:
        f.write(json.dumps(spec.to_jsonable()))

    spec_counts = [spec.count_objects_of_size(i) for i in range(n)]
    print(spec_counts)
    class_counts = CanonicalAv(basis).counter(n - 1)
    print(class_counts)
    if spec_counts != class_counts:
        incorrect_counts.add(basis)
        print(f"Counts do not match for basis {CanonicalAv(basis)}")
    else:
        correct_counts.add(basis)
    print(
        len(correct_counts),
        " correct counts\n",
        len(incorrect_counts),
        " incorrect counts",
    )
    print(len(took_too_long), " took too long")

print("correct counts")
print(correct_counts)
print("wrong counts")
print(incorrect_counts)
print("took too long")
print(took_too_long)
