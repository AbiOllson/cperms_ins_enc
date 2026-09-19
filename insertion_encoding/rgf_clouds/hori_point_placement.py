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
from .pointplacement import TrackedRGFVPointPlacement
from .rgf_tracked_tiling import TrackedTiling

Cell = tuple[int, int]


class TrackedRGFHPointPlacement(TrackedRGFVPointPlacement):
    """Point placement for restricted growth functions
    horizontal insertion encoding."""

    def point_placement(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
    ) -> tuple[TrackedTiling, ...]:
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


class TrackedRGFHRequirementPlacementStrategy(TrackedRequirementPlacementStrategy):
    """Strategy for placing requirements in a tiling for restricted growth functions
    horizontal insertion encoding."""

    def algorithm(self, tiling: TrackedTiling) -> TrackedRGFHPointPlacement:
        return TrackedRGFHPointPlacement(tiling)

    def formal_step(self):
        return "Tracked point placement in RGF"


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
