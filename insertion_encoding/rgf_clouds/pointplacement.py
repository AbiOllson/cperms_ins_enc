from typing import Iterator
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm
from clouds.strategies import (
    TrackedRowPlacementFactory,
)
from clouds.strategies.point_placement import TrackedRequirementPlacementStrategy
from clouds.tracked_algos import (
    TrackedPointPlacement,
)
from .rgf_tracked_tiling import TrackedTiling

Cell = tuple[int, int]


class TrackedPointPlacementRGF(TrackedPointPlacement):
    """Point placement tracking clouds."""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        super().__init__(tracked_tiling)

    def tracked_point_placement(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
    ) -> tuple[TrackedTiling, ...]:
        """Yield the tilings with tracked clouds after point placement."""
        if direction not in self.DIRECTIONS:
            raise ValueError(f"Direction {direction} is not a valid direction.")
        cells = self.cells_to_place_in(requirement_list, indices)
        all_tracked_tilings = []
        for placed_cell in cells:
            placed_row = placed_cell[1]

            rgf_obs = set()
            if placed_row not in self.tracked_tiling.rows_had_vals:
                x, y = placed_cell
                _, m = self.tracked_tiling.dimensions
                for i in range(0, x + 1):
                    for j in range(y + 1, m + 2):
                        rgf_obs.add(GriddedCayleyPerm([0], [(i, j)]))
            tiling = self.point_placement_in_cell(
                requirement_list, indices, direction, placed_cell
            ).add_obstructions(rgf_obs)
            map_for_cells = self.multiplex_map(placed_cell)
            indices_clouds, value_clouds = TrackedTiling.map_clouds(
                indices_clouds=self.tracked_tiling.indices_clouds,
                value_clouds=self.tracked_tiling.value_clouds,
                tiling_map=map_for_cells,
            )
            row_map = map_for_cells.preimage_map()[1]
            rows_had_vals = set(
                row_map[row][0]
                for row in self.tracked_tiling.rows_had_vals
                if row != placed_row
            )
            rows_had_vals.add(placed_cell[1] + 1)
            all_tracked_tilings.append(
                TrackedTiling(
                    tiling,
                    indices_clouds=indices_clouds,
                    value_clouds=value_clouds,
                    intersect_clouds_with_active=True,
                    rows_had_vals=rows_had_vals,
                )
            )
        return tuple(all_tracked_tilings)


class TrackedRequirementPlacementStrategyRGF(
    TrackedRequirementPlacementStrategy,
):
    """
    A strategy for placing requirements with tracked clouds.
    """

    def algorithm(self, tiling):
        """Return the point placement algorithm to use for the strategy."""
        return TrackedPointPlacementRGF(tiling)


class TrackedRowPlacementFactoryRGF(TrackedRowPlacementFactory):
    """A factory for placing the minimum leftmost points in the rows of tilings
    for rgfs with fusion."""

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRequirementPlacementStrategyRGF]:
        for row in set(range(comb_class.dimensions[1])):
            all_gcps = []
            for col in range(comb_class.dimensions[0]):
                cell = (col, row)
                if cell in comb_class.active_cells:
                    gcps = GriddedCayleyPerm(CayleyPermutation([0]), (cell,))
                    all_gcps.append(gcps)
            indices = tuple(0 for _ in all_gcps)
            yield TrackedRequirementPlacementStrategyRGF(all_gcps, indices, 4)

    @classmethod
    def from_dict(cls, d: dict) -> "TrackedRowPlacementFactoryRGF":
        return cls(**d)
