from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from comb_spec_searcher import (
    StrategyPack,
    AtomStrategy,
)
from insertion_encoding.tilescope.generic_searcher import GenericTilingsSearcher
from .rgf_tracked_tiling import TrackedTiling

from .pointplacement import TrackedVPointPlacementFactoryRGF

from .hori_point_placement import TrackedHReqPlacementFactoryRGF

# from .pointplacement import TrackedVPointPlacementFactoryRGF
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


class RGFVRCSepSearcher(GenericTilingsSearcher):
    """A searcher with rc sep for
    enumerating restricted growth functions."""

    def regular_check(self):
        return True

    def type_of_encoding(self):
        return "RGF vertical rc sep"

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
            expansion_strats=[[TrackedVPointPlacementFactoryRGF()]],
            ver_strats=[AtomStrategy()],
            name="RGF RC Sep Vertical Insertion Encoding",
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


class RGFVTrackedSearcher(RGFVRCSepSearcher):
    """A searcher with rc sep and fusion for
    enumerating restricted growth functions."""

    def type_of_encoding(self):
        return "RGF vertical fusion"

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
            expansion_strats=[[TrackedVPointPlacementFactoryRGF()]],
            ver_strats=[AtomStrategy()],
            name="RGF Fusion Vertical Insertion Encoding",
            symmetries=[],
            iterative=False,
        )


class RGFRCSepHoriSearcher(RGFVRCSepSearcher):
    """A searcher with rc sep for
    enumerating restricted growth functions."""

    def regular_check(self):
        return True

    def type_of_encoding(self):
        return "RGF horizontal rc sep"

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
            expansion_strats=[[TrackedHReqPlacementFactoryRGF()]],
            ver_strats=[AtomStrategy()],
            name="RGF RC Sep Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )


class RGFHTrackedSearcher(RGFRCSepHoriSearcher):
    """A searcher with rc sep and fusion for
    enumerating restricted growth functions."""

    def type_of_encoding(self):
        return "RGF horizontal fusion"

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
            expansion_strats=[[TrackedHReqPlacementFactoryRGF()]],
            ver_strats=[AtomStrategy()],
            name="RGF Fusion Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )
