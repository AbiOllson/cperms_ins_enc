from comb_spec_searcher import CombinatorialSpecification
from comb_spec_searcher.strategies import Rule
from clouds.strategies.add_cloud import AddCloudsStrategy
from clouds.strategies.fusion import (
    TrackedFusionStrategy,
    TrackedFusionPointRowStrategy,
)
from cayley_permutations import CanonicalAv
import json
from cayley_permutations import CayleyPermutation
from insertion_encoding.rgf_clouds import RGFTrackedSearcher, RGFRCSepSearcher
from cayley_permutations import CanonicalAv
from comb_spec_searcher import CombinatorialSpecification, StrategyPack, AtomStrategy
from comb_spec_searcher.exception import ExceededMaxtimeError
import json
from collections import defaultdict

type_of_bases = ["3s", "3s_4x2", "3s_4x1", "4s_updated"]
gfs_dict_count = 0

# bases_running = [
#     (CayleyPermutation((0, 0, 0)), CayleyPermutation((0, 1, 0, 1))),
#     "Av(0102)",
#     "Av(0012)",
#     "Av(0101)",
#     "Av(0011)",
# ]

took_too_long = []
tot_found = 0

not_found = []

non_fusion = []
fusion = []
both = []

gfs_dict = defaultdict(list)

for basis_type in type_of_bases:
    with open(f"all_non_inenc_basis_classes_{basis_type}.txt", "r") as f:
        bases = sorted(eval(f.read()))

    print(len(bases))
    for basis in bases:
        found = False
        try:
            with open(f"non fusion specs/{CanonicalAv(basis)}.json", "r") as f:
                spec = CombinatorialSpecification.from_dict(json.load(f))
            found = True
            tot_found += 1
            non_fusion.append(basis)
            gf = spec.get_genf()
            gfs_dict[gf] += CanonicalAv(basis).basis
        except FileNotFoundError:
            pass
        try:
            with open(f"fusion specs/{CanonicalAv(basis)}.json", "r") as f:
                spec = CombinatorialSpecification.from_dict(json.load(f))
            if found:
                both.append(basis)
            fusion.append(basis)
            found = True
            tot_found += 1

            all_rules = list(spec.rules_dict.values())
            new_all_rules = []
            for rule in all_rules:
                if rule.get_op_symbol() == "⚮":
                    cloud_to_add = (rule.strategy.index,)
                    if (
                        rule.strategy.fuse_rows
                        and cloud_to_add in rule.comb_class.value_clouds
                        or not rule.strategy.fuse_rows
                        and cloud_to_add in rule.comb_class.indices_clouds
                    ):
                        new_all_rules.append(rule)
                        continue
                    add_cloud_strat = (
                        AddCloudsStrategy(
                            val_clouds=[[rule.strategy.index]], idx_clouds=[]
                        )
                        if rule.strategy.fuse_rows
                        else AddCloudsStrategy(
                            val_clouds=[], idx_clouds=[[rule.strategy.index]]
                        )
                    )
                    add_cloud_children = add_cloud_strat(rule.comb_class).children
                    add_cloud_rule = Rule(
                        add_cloud_strat,
                        rule.comb_class,
                        children=add_cloud_children,
                    )
                    new_all_rules.append(add_cloud_rule)
                    if rule.formal_step[:5] == "Point":
                        new_all_rules.append(
                            Rule(
                                TrackedFusionPointRowStrategy(
                                    rule.strategy.fuse_rows, rule.strategy.index
                                ),
                                add_cloud_children[0],
                                children=TrackedFusionPointRowStrategy(
                                    rule.strategy.fuse_rows, rule.strategy.index
                                )(add_cloud_rule.comb_class).children,
                            )
                        )
                    elif rule.formal_step[:4] == "Fuse":
                        new_all_rules.append(
                            Rule(
                                TrackedFusionStrategy(
                                    rule.strategy.fuse_rows, rule.strategy.index
                                ),
                                add_cloud_children[0],
                                children=TrackedFusionStrategy(
                                    rule.strategy.fuse_rows, rule.strategy.index
                                )(add_cloud_rule.comb_class).children,
                            )
                        )
                    else:
                        print("OH NOO")
                else:
                    new_all_rules.append(rule)

            new_spec = CombinatorialSpecification(
                spec.root, new_all_rules
            ).expand_verified()

            with open(f"expanded spec/{CanonicalAv(basis)}.json", "w") as f:
                f.write(json.dumps(spec.to_jsonable()))
            eqns = new_spec.get_maple_equations()
            with open(f"eqns/{CanonicalAv(basis)}.txt", "w") as f:
                f.write(eqns)
            print(eqns)

        except FileNotFoundError:
            pass
        if not found:
            not_found.append(basis)

for gf, bases in gfs_dict.items():
    print(gf)
    for basis in bases:
        print(basis)

with open(f"gfs_dict_{gfs_dict_count}.json", "w") as f:
    f.write(repr(gfs_dict))


print(f"Not found: {len(not_found)}")
print(not_found)

print("non fusion:", len(non_fusion))
print(non_fusion)

print("fusion:", len(fusion))
print(fusion)

print("both:", len(both))
print(both)
