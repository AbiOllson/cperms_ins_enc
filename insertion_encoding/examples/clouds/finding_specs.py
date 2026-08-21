from insertion_encoding.rgf_clouds import RGFTrackedSearcher
from cayley_permutations import CanonicalAv, CayleyPermutation
import json
from comb_spec_searcher import CombinatorialSpecification
from comb_spec_searcher.exception import ExceededMaxtimeError

# with open("bases.txt", "r") as f:
#     bases = eval(f.read())
# bases = [
#     (CayleyPermutation((0, 0, 0, 0)), CayleyPermutation((0, 1, 1, 2))),
#     (CayleyPermutation((0, 1, 0, 2)), CayleyPermutation((0, 1, 1, 1))),
#     (CayleyPermutation((0, 0, 1, 1)), CayleyPermutation((0, 1, 1, 1))),
#     (CayleyPermutation((0, 1, 0, 0)), CayleyPermutation((0, 1, 1, 1))),
#     (CayleyPermutation((0, 0, 1, 0)), CayleyPermutation((0, 1, 1, 1))),
#     (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 1, 1, 1))),
#     (CayleyPermutation((0, 1, 1, 1)), CayleyPermutation((0, 0, 0, 0))),
#     (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 1, 1, 0))),
#     (CayleyPermutation((0, 0, 1, 0)), CayleyPermutation((0, 0, 1, 2))),
#     (CayleyPermutation((0, 1, 0, 0)), CayleyPermutation((0, 0, 1, 1))),
#     (CayleyPermutation((0, 0, 1, 0)), CayleyPermutation((0, 0, 1, 1))),
#     (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 0, 1, 1))),
#     (CayleyPermutation((0, 0, 1, 1)), CayleyPermutation((0, 0, 0, 0))),
#     (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 1, 0, 0))),
#     (CayleyPermutation((0, 1, 0, 0)), CayleyPermutation((0, 0, 0, 0))),
#     (CayleyPermutation((0, 0, 1, 0)), CayleyPermutation((0, 0, 0, 0))),
#     (CayleyPermutation((0, 0, 0, 1)), CayleyPermutation((0, 0, 0, 0))),
# ]

# bases = {
#     "1122,1222",
#     "1121,1123",
#     "1211,1122",
#     "1121,1122",
#     "1112,1122",
#     "1122,1111",
#     "1112,1211",
# }

bases = {
    "0101,0111,0112",
    "0011,0102",
    "0101,0102,0012,0112",
    "0111,0012,0102,0011,0112",
    "0101,0102,0012",
    "0100,0112",
    "0011,0102,0012",
    "0011,0101,0102",
    "0101,0112",
    "0011,0102,0111",
    "0101,0102,0111",
    "0011,0101,0102,0111",
    "0101,0102",
    "0102,0111,0112",
    "0012,0102,0111,0112",
    "0102,0012",
    "0100,0000,0112",
    "0100,0010,0000,0112",
    "0101,0102,0112",
    "0001,0100,0010,0112",
    "0011,0102,0111,0112",
    "0011,0102,0112",
    "0001,0100,0000,0112",
    "0100,0010,0112",
    "0102,0012,0112",
    "0001,0010,0111,0100,0000",
    "0011,0102,0012,0112",
    "0102",
    "0001,0010,0100,0000,0112",
    "0102,0112",
    "0101,0000",
    "0010,0101",
    "0101,0012",
    "0100,0101,0000",
    "0100,0101",
    "0001,0101,0111,0000",
    "0100,0101,0010,0111",
    "0001,0101,0111,0100,0000",
    "0001,0100,0101",
    "0101,0111",
    "0101,0111,0000",
    "0001,0100,0101,0010",
    "0001,0010,0101,0111,0000",
    "0012,0101,0111",
    "0001,0010,0101,0111",
    "0001,0100,0101,0000",
    "0100,0101,0010",
    "0001,0101,0000",
    "0011",
    "0001,0010,0101,0000",
    "0101,0010,0111,0100,0000",
    "0100,0101,0111,0000",
    "0100,0101,0010,0000",
    "0010,0101,0000",
    "0001,0101,0010,0111,0100",
    "0001,0101,0111",
    "0100,0101,0111",
    "0010,0101,0111",
    "0010,0101,0111,0000",
    "0101",
    "0001,0101",
    "0001,0100,0101,0111",
    "0001,0101,0010,0100,0000",
    "0001,0010,0101",
    "0001,0101,0010,0111,0100,0000",
}

bases = sorted(bases)
print(len(bases), " bases to check")
n = 10  # how far to check counts

correct_counts = set()
incorrect_counts = set()
took_too_long = set()
found_before = set()

for basis in bases:
    try:
        with open(f"1cv specs rc sep\{CanonicalAv(basis)}.json", "r") as f:
            spec = CombinatorialSpecification.from_dict(json.load(f))
        found_before.add(basis)
        continue
    except FileNotFoundError:

        try:
            spec = RGFTrackedSearcher(basis).auto_search(max_expansion_time=1200)
        except ExceededMaxtimeError:
            print(f"Basis {CanonicalAv(basis)} took too long")
            took_too_long.add(basis)
            continue

        spec_counts = [spec.count_objects_of_size(i) for i in range(n)]
        print(spec_counts)
        class_counts = CanonicalAv(basis).counter(n - 1)
        print(class_counts)
        if spec_counts != class_counts:
            incorrect_counts.add(basis)
            print(f"Counts do not match for basis {CanonicalAv(basis)}")
            with open(
                f"1cv specs rc sep wrong counts\{CanonicalAv(basis)}.json", "w"
            ) as f:
                f.write(json.dumps(spec.to_jsonable()))
        else:
            correct_counts.add(basis)
            with open(f"1cv specs rc sep\{CanonicalAv(basis)}.json", "w") as f:
                f.write(json.dumps(spec.to_jsonable()))
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
