"""A searcher for the horizontal insertion encoding."""

from functools import cached_property
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm
from check_regular_ins_enc import (
    regular_horizontal_insertion_encoding,
)
from comb_spec_searcher import (
    CombinatorialSpecificationSearcher,
    StrategyPack,
    AtomStrategy,
)
from comb_spec_searcher.rule_db import RuleDBForest
from .strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    FactorStrategy,
    RGFFactorStrategy,
    HorizontalInsertionEncodingPlacementFactory,
    HorizontalInsertionEncodingRequirementInsertionFactory,
    RGFHorizontalInsertionEncodingPlacementFactory,
    MatchingRequirementInsertionFactory,
    MatchingsRemoveExtraReqsStrategy,
)
from ..check_regular import (
    rgf_regular_horizontal_insertion_encoding,
)
from .generic_searcher import GenericTilingsSearcher


class HorizontalSearcher(GenericTilingsSearcher):
    """A searcher for the horizontal insertion encoding."""

    def regular_check(self):
        return regular_horizontal_insertion_encoding(self.basis)

    def type_of_encoding(self) -> str:
        return "horizontal"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                FactorStrategy(),
                HorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[HorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )


class RGFHorizontalSearcher(HorizontalSearcher):
    """A searcher for the horizontal insertion encoding for
    enumerating restricted growth functions."""

    def regular_check(self):
        return rgf_regular_horizontal_insertion_encoding(self.basis)

    def type_of_encoding(self) -> str:
        return "RGF horizontal"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                RGFFactorStrategy(),
                HorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[RGFHorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="RGF Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )


class MatchingHorizontalSearcher(RGFHorizontalSearcher):
    """A searcher for the horizontal insertion encoding for
    enumerating restricted growth functions."""

    def type_of_encoding(self) -> str:
        return "RGFs of matchings horizontal"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                RGFFactorStrategy(),
                MatchingRequirementInsertionFactory(),
            ],
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                MatchingsRemoveExtraReqsStrategy(),
            ],
            expansion_strats=[[RGFHorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="RGFs of Matchings Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    def start_class(self):
        return (
            super()
            .start_class()
            .add_obstruction(
                GriddedCayleyPerm(
                    CayleyPermutation([0, 0, 0]), [(0, 0), (0, 0), (0, 0)]
                )
            )
        )

    @cached_property
    def comb_spec_searcher(self) -> CombinatorialSpecificationSearcher:
        """Returns the CombinatorialSpecificationSearcher object for this searcher."""
        print(self.pack(), self.pack().name)
        return CombinatorialSpecificationSearcher(
            self.start_class(), self.pack(), debug=self.debug, ruledb=RuleDBForest()
        )
