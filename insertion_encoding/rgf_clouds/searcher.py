from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from comb_spec_searcher import (
    StrategyPack,
    AtomStrategy,
)
from insertion_encoding.tilescope.generic_searcher import GenericSearcher
from .rgf_tracked_tiling import TrackedTiling
from .pointplacement import TrackedRowPlacementFactoryRGF
from .factoring import TrackedFactorStrategyRGF
from clouds.strategies import (
    TrackedFusionFactory,
    TrackedFusionPointRowFactory,
    TrackedRemoveEmptyRowsAndColumnsStrategy,
)

from insertion_encoding.rgf_clouds.tracked_searcher import TrackedSearcher
from insertion_encoding.rgf_clouds.rc_sep import (
    RGFTrackedLessThanOrEqualRowColSeparationFactory,
    RGFTrackedLessThanRowColSeparationStrategy,
)
from functools import cached_property

Cell = tuple[int, int]


class RGFRCSepSearcher(GenericSearcher):
    """A searcher with rc sep for
    enumerating restricted growth functions."""

    def regular_check(self):
        return True

    def type_of_encoding(self):
        return "RGF rc sep"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                TrackedFactorStrategyRGF(),
                RGFTrackedLessThanOrEqualRowColSeparationFactory(),
            ],
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                RGFTrackedLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[[TrackedRowPlacementFactoryRGF()]],
            ver_strats=[AtomStrategy()],
            name="RGF RC Sep Insertion Encoding",
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

    @cached_property
    def comb_spec_searcher(self) -> TrackedSearcher:
        """Returns the CombinatorialSpecificationSearcher object for this searcher."""
        print(self.pack(), self.pack().name)
        return TrackedSearcher(
            self.start_class(), self.pack(), debug=self.debug, max_cvs=1
        )

    def auto_search(self, max_expansion_time=600) -> TrackedSearcher:
        """Search for a specification."""
        return self.comb_spec_searcher.auto_search(
            max_expansion_time=max_expansion_time
        )


class RGFTrackedSearcher(RGFRCSepSearcher):
    """A searcher with rc sep and fusion for
    enumerating restricted growth functions."""

    def type_of_encoding(self):
        return "RGF fusion"

    def pack(self):
        return StrategyPack(
            initial_strats=[
                TrackedFactorStrategyRGF(),
                RGFTrackedLessThanOrEqualRowColSeparationFactory(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                RGFTrackedLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[[TrackedRowPlacementFactoryRGF()]],
            ver_strats=[AtomStrategy()],
            name="RGF Fusion Insertion Encoding",
            symmetries=[],
            iterative=False,
        )
