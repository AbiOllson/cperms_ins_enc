from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from comb_spec_searcher import (
    StrategyPack,
    AtomStrategy,
)
from insertion_encoding.tilescope.strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
)
from insertion_encoding.tilescope.generic_searcher import GenericSearcher
from .rgf_tracked_tiling import TrackedTiling
from .pointplacement import TrackedRowPlacementFactoryRGF
from .factoring import TrackedFactorStrategyRGF

Cell = tuple[int, int]


class RGFTrackedSearcher(GenericSearcher):
    """A searcher for the horizontal insertion encoding for
    enumerating restricted growth functions."""

    def regular_check(self):
        return True

    def type_of_encoding(self):
        return "RGF fusion"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                TrackedFactorStrategyRGF(),
                # HorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[TrackedRowPlacementFactoryRGF()]],
            ver_strats=[AtomStrategy()],
            name="RGF Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    def start_class(self):
        til = Tiling(
            [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in self.basis],
            [],
            (1, 1),
        )
        return TrackedTiling(til)
