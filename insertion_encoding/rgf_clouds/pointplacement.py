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
from insertion_encoding.tilescope.strategies.point_placements import (
    RGFVPointPlacement,
    RGFHPointPlacement,
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


class TrackedRGFVPointPlacement(RGFVPointPlacement):
    """Point placement for restricted growth functions
    vertical insertion encoding."""

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

    def point_placement(
        self,
        requirement_list: Tuple[GriddedCayleyPerm, ...],
        indices: Tuple[int, ...],
        direction: int,
    ) -> Tuple[Tiling, ...]:
        """Point placement for restricted growth functions.

        If vertical and only one row then just do a new max placement.
        If horizontal and only one row then will only be a 1x1 tiling anyway
        so also a new max placement.

        Else, for both do a new max in the leftmost active cell  in the
        top row and repeat vals in all other active cells in other rows.
        """
        if direction not in self.DIRECTIONS:
            raise ValueError(f"Direction {direction} is not a valid direction.")
        top_row = self.tiling.dimensions[1] - 1
        if top_row == 0:
            return (
                self.new_max_point_placement(
                    requirement_list,
                    indices,
                    direction,
                    min(self.tiling.active_cells),
                ),
            )
        point_placements = []
        top_leftmost_cell = min(self.tiling.cells_in_row(top_row))
        point_placements.append(
            self.new_max_point_placement(
                requirement_list,
                indices,
                direction,
                top_leftmost_cell,
            )
        )
        for row in range(top_row):
            point_placements.extend(
                self.point_placement_in_cell(requirement_list, indices, direction, cell)
                for cell in sorted(self.tiling.cells_in_row(row))
            )
        return tuple(point_placements)

    def new_max_point_placement(
        self,
        requirement_list: Tuple[GriddedCayleyPerm, ...],
        indices: Tuple[int, ...],
        direction: int,
        cell: Tuple[int, int],
    ) -> Tiling:
        """Inserts a new max into an RGF"""
        tiling = self.point_placement_in_cell(
            requirement_list, indices, direction, cell
        )
        extra_forced_obs = [
            GriddedCayleyPerm(CayleyPermutation([0]), [(cell[0] + 2, cell[1])])
        ]
        for new_cell in tiling.cells_in_col(cell[0]):
            extra_forced_obs.append(
                GriddedCayleyPerm(CayleyPermutation([0]), [new_cell])
            )
        return tiling.add_obstructions(extra_forced_obs)


class TrackedRGFHPointPlacement(RGFVPointPlacement):
    """Point placement for restricted growth functions
    horizontal insertion encoding."""

    def point_placement(
        self,
        requirement_list: Tuple[GriddedCayleyPerm, ...],
        indices: Tuple[int, ...],
        direction: int,
    ) -> Tuple[Tiling, ...]:
        """Point placement for restricted growth functions.

        Every cell is treated as a new max (is leftmost in all of tiling)
        """
        if direction not in self.DIRECTIONS:
            raise ValueError(f"Direction {direction} is not a valid direction.")
        cells = []
        for idx, gcp in zip(indices, requirement_list):
            cells.append(gcp.positions[idx])
        cells = sorted(set(cells))
        return tuple(
            self.new_max_point_placement(requirement_list, indices, direction, cell)
            for cell in cells
        )


class TrackedRequirementPlacementStrategyRGF(
    TrackedRequirementPlacementStrategy,
):
    """
    A strategy for placing requirements with tracked clouds.
    """

    def algorithm(self, tiling):
        """Return the point placement algorithm to use for the strategy."""
        return TrackedPointPlacementRGF(tiling)


class TrackedRGFVRequirementPlacementStrategy(RequirementPlacementStrategy):
    """Strategy for placing requirements in a tiling for restricted growth functions
    vertical insertion encoding."""

    def algorithm(self, tiling: Tiling) -> PointPlacement:
        return TrackedRGFVPointPlacement(tiling)

    def formal_step(self):
        return "Point placement in RGF"


class TrackedRGFHRequirementPlacementStrategy(RequirementPlacementStrategy):
    """Strategy for placing requirements in a tiling for restricted growth functions
    horizontal insertion encoding."""

    def algorithm(self, tiling: Tiling) -> PointPlacement:
        return TrackedRGFHPointPlacement(tiling)

    def formal_step(self):
        return "Point placement in RGF"


class TrackedRowPlacementFactoryRGF(TrackedRowPlacementFactory):
    """A factory for placing the minimum leftmost points in the rows of tilings
    for rgfs with fusion."""

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRequirementPlacementStrategyRGF]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        yield TrackedRequirementPlacementStrategyRGF(gcps, indices, 4)

    @classmethod
    def from_dict(cls, d: dict) -> "TrackedRowPlacementFactoryRGF":
        return cls(**d)


class TrackedVReqPlacementFactoryRGF(TrackedRowPlacementFactory):
    """A factory for placing the minimum leftmost points in the rows of tilings
    for rgfs with fusion."""

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRGFVRequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        yield TrackedRGFVRequirementPlacementStrategy(gcps, indices, 3)

    @classmethod
    def from_dict(cls, d: dict) -> "TrackedVReqPlacementFactoryRGF":
        return cls(**d)


class TrackedHReqPlacementFactoryRGF(TrackedRowPlacementFactory):
    """A factory for placing the minimum leftmost points in the rows of tilings
    for rgfs with fusion."""

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRGFHRequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        yield TrackedRGFHRequirementPlacementStrategy(gcps, indices, 3)

    @classmethod
    def from_dict(cls, d: dict) -> "TrackedHReqPlacementFactoryRGF":
        return cls(**d)
