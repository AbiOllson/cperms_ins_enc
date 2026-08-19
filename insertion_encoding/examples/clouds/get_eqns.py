from comb_spec_searcher import CombinatorialSpecification
from comb_spec_searcher.strategies import Rule
from clouds.strategies.add_cloud import AddCloudsStrategy
from clouds.strategies.fusion import (
    TrackedFusionStrategy,
    TrackedFusionPointRowStrategy,
)
from cayley_permutations import CanonicalAv
import json

bases = {
    "1122,1222",
    "1121,1123",
    "1211,1122",
    "1121,1122",
    "1112,1122",
    "1122,1111",
    "1112,1211",
}

not_found = []

count = 0
tot = len(bases)
for basis in bases:
    count += 1
    print(f"{count} out of {tot}: {CanonicalAv(basis)}")
    try:
        with open(f"1cv specs/{CanonicalAv(basis)}.json", "r") as f:
            spec_string = f.read().replace("false", "False").replace("true", "True")
            spec = CombinatorialSpecification.from_dict(eval(spec_string))
    except FileNotFoundError:
        print(f"Basis {CanonicalAv(basis)} does not have a specification file.")
        not_found.append(basis)
        continue
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
                AddCloudsStrategy(val_clouds=[[rule.strategy.index]], idx_clouds=[])
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

    new_spec = CombinatorialSpecification(spec.root, new_all_rules).expand_verified()

    with open(f"1cv specs expanded for eqns/{CanonicalAv(basis)}.json", "w") as f:
        f.write(json.dumps(spec.to_jsonable()))
    eqns = new_spec.get_maple_equations()
    with open(f"eqns/{CanonicalAv(basis)}.txt", "w") as f:
        f.write(eqns)
    print(eqns)

print(f"Not found: {len(not_found)}")
print(not_found)
