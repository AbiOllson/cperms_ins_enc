from typing import Iterator
from collections import defaultdict
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm
from clouds.strategies import (
    TrackedRowPlacementFactory,
)
from clouds.strategies.point_placement import TrackedRequirementPlacementStrategy
from clouds.tracked_algos import (
    TrackedPointPlacement,
)
from insertion_encoding.tilescope.strategies.point_placements import (
    RGFVPointPlacement,
)
from .rgf_tracked_tiling import TrackedTiling

Cell = tuple[int, int]


class TrackedRGFVPointPlacement(RGFVPointPlacement):
    """Point placement for restricted growth functions
    vertical insertion encoding."""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        super().__init__(tracked_tiling)

    def cells_to_place_in(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
    ) -> set[Cell]:
        """Return the set of cells to place points in."""
        cells = set()
        for idx, gcp in zip(indices, requirement_list):
            cells.add(gcp.positions[idx])
        return cells

    def tracked_point_placement(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
    ) -> tuple[TrackedTiling | None, ...]:
        """Point placement for restricted growth functions.

        If vertical and only one row then just do a new max placement.
        If horizontal and only one row then will only be a 1x1 tiling anyway
        so also a new max placement.

        Else, for both do a new max in the leftmost active cell  in the
        top row and repeat vals in all other active cells in other rows.
        """
        if direction not in self.DIRECTIONS:
            raise ValueError(f"Direction {direction} is not a valid direction.")
        cells_in_rows = defaultdict(set)
        point_placements = {}
        order_for_cells = self.cells_to_place_in(requirement_list, indices)
        point_placements: dict[Cell, TrackedTiling | None] = {
            cell: None for cell in order_for_cells
        }
        for cell in order_for_cells:
            cells_in_rows[cell[1]].add(cell)
        for row in cells_in_rows:
            cells = sorted(cells_in_rows[row])
            if row in self.tracked_tiling.rows_had_vals:
                for cell in cells:
                    point_placements[cell] = self.tracked_point_placement_in_cell(
                        requirement_list, indices, direction, cell
                    )
            else:
                leftmost_cell = min(cells)
                point_placements[leftmost_cell] = self.new_max_point_placement(
                    requirement_list, indices, direction, leftmost_cell
                )
                for cell in cells:
                    if cell != leftmost_cell:

                        rgf_obs = set()
                        x, y = cell
                        _, m = self.tracked_tiling.dimensions
                        for i in range(0, x + 1):
                            for j in range(y + 1, m + 2):
                                rgf_obs.add(GriddedCayleyPerm([0], [(i, j)]))

                        point_placements[cell] = self.tracked_point_placement_in_cell(
                            requirement_list, indices, direction, cell
                        ).add_obstructions(rgf_obs)
        return tuple(point_placements.values())

    def new_max_point_placement(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
        cell: tuple[int, int],
    ) -> TrackedTiling:
        """Inserts a new max into an RGF"""
        tracked_tiling = self.tracked_point_placement_in_cell(
            requirement_list, indices, direction, cell
        )
        extra_forced_obs = [
            GriddedCayleyPerm(CayleyPermutation([0]), [(cell[0] + 2, cell[1])])
        ]
        for new_cell in tracked_tiling.cells_in_col(cell[0]):
            extra_forced_obs.append(
                GriddedCayleyPerm(CayleyPermutation([0]), [new_cell])
            )
        return tracked_tiling.add_obstructions(extra_forced_obs)

    def tracked_point_placement_in_cell(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
        cell: tuple[int, int],
    ) -> TrackedTiling:
        tiling = self.point_placement_in_cell(
            requirement_list, indices, direction, cell
        )

        map_for_cells = self.multiplex_map(cell)
        indices_clouds, value_clouds = TrackedTiling.map_clouds(
            indices_clouds=self.tracked_tiling.indices_clouds,
            value_clouds=self.tracked_tiling.value_clouds,
            tiling_map=map_for_cells,
        )
        row_map = map_for_cells.preimage_map()[1]
        rows_had_vals = set(
            row_map[row][0]
            for row in self.tracked_tiling.rows_had_vals
            if row != cell[1]
        )
        rows_had_vals.add(cell[1] + 1)
        return TrackedTiling(
            tiling, indices_clouds, value_clouds, rows_had_vals=rows_had_vals
        )


class TrackedRGFVRequirementPlacementStrategy(TrackedRequirementPlacementStrategy):
    """Strategy for placing requirements in a tiling for restricted growth functions
    vertical insertion encoding."""

    def algorithm(self, tiling: TrackedTiling) -> TrackedRGFVPointPlacement:
        return TrackedRGFVPointPlacement(tiling)

    def formal_step(self):
        return "Tracked point placement in RGF"


class TrackedVPointPlacementFactoryRGF(TrackedRowPlacementFactory):
    """A factory for placing the minimum leftmost points in tilings
    for rgfs with fusion."""

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRGFVRequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        yield TrackedRGFVRequirementPlacementStrategy(gcps, indices, 4)

    @classmethod
    def from_dict(cls, d: dict) -> "TrackedVPointPlacementFactoryRGF":
        return cls(**d)


# class TrackedVReqPlacementFactoryRGF(TrackedRowPlacementFactory):
#     """A factory for placing the minimum leftmost points in the rows of tilings
#     for rgfs with fusion."""

#     def __call__(
#         self, comb_class: TrackedTiling
#     ) -> Iterator[TrackedRGFVRequirementPlacementStrategy]:
#         cells = comb_class.active_cells
#         gcps = tuple(
#             GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
#         )
#         indices = tuple(0 for _ in gcps)
#         yield TrackedRGFVRequirementPlacementStrategy(gcps, indices, 3)

#     @classmethod
#     def from_dict(cls, d: dict) -> "TrackedVReqPlacementFactoryRGF":
#         return cls(**d)
