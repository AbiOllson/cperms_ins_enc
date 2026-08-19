from clouds.tracked_algos import TrackedFactors
from clouds.strategies.factoring import TrackedFactorStrategy
from typing import Iterable

from .rgf_tracked_tiling import TrackedTiling

Cell = tuple[int, int]


class TrackedFactorsRGF(TrackedFactors):
    """Factors and tracks clouds"""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        self.tiling = tracked_tiling.tiling
        self.cells = list(sorted(self.tiling.active_cells))
        self.cells_dict = {cell: cell for cell in self.cells}

    def find_tracked_factors(self) -> Iterable[TrackedTiling]:
        """Return the factors of the tracked tiling."""
        factors = self.rgf_find_factors()
        # only one child where the row is positive needs a cloud for a point row
        for factor in factors:
            yield TrackedTiling(
                factor,
                value_clouds=self.new_value_clouds(factor.active_cells),
                indices_clouds=self.tracked_tiling.indices_clouds,
                intersect_clouds_with_active=True,
                rows_had_vals=self.tracked_tiling.rows_had_vals,
            )


class TrackedFactorStrategyRGF(
    TrackedFactorStrategy,
):
    """
    A strategy for finding factors in a tracked tiling.
    """

    def algorithm(self, comb_class: TrackedTiling) -> TrackedFactorsRGF:
        return TrackedFactorsRGF(comb_class)
