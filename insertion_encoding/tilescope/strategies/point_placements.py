"""Places a point requirement in a tiling in extreme directions.
0 = rightmost
1 = topmost, taking the rightmost if there are multiple
2 = topmost, taking the leftmost if there are multiple
3 = leftmost
4 = bottommost, taking the leftmost if there are multiple
5 = bottommost, taking the rightmost if there are multiple"""

from typing import Dict, Iterable, Iterator, Optional, Tuple
from comb_spec_searcher import DisjointUnionStrategy, StrategyFactory

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.point_placements import (
    PointPlacement,
    DIRECTIONS,
    DIR_LEFT,
    DIR_LEFT_BOT,
)
from cayley_permutations import CayleyPermutation

Cell = Tuple[int, int]


class RGFVPointPlacement(PointPlacement):
    """Point placement for restricted growth functions
    vertical insertion encoding."""

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


class RGFHPointPlacement(RGFVPointPlacement):
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


class RequirementPlacementStrategy(DisjointUnionStrategy[Tiling, GriddedCayleyPerm]):
    """Strategy for placing requirements in a tiling."""

    DIRECTIONS = DIRECTIONS

    def __init__(
        self,
        gcps: Iterable[GriddedCayleyPerm],
        indices: Iterable[int],
        direction: int,
        ignore_parent: bool = False,
    ):
        self.gcps = tuple(gcps)
        self.indices = tuple(indices)
        self.direction = direction
        assert direction in self.DIRECTIONS
        super().__init__(ignore_parent=ignore_parent)

    def algorithm(self, tiling: Tiling) -> PointPlacement:
        """The point placement algorithm."""
        return PointPlacement(tiling)

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        return (comb_class.add_obstructions(self.gcps),) + self.algorithm(
            comb_class
        ).point_placement(self.gcps, self.indices, self.direction)

    def extra_parameters(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[Dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))

    def formal_step(self):
        return (
            f"Placed the point of the requirement {self.gcps}"
            + f" at indices {self.indices} in direction {self.direction}"
        )

    def backward_map(
        self,
        comb_class: Tiling,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        # pylint: disable=duplicate-code
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: Tiling,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Tuple[Optional[GriddedCayleyPerm], ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"RequirementPlacementStrategy(gcps={self.gcps}, "
            f"indices={self.indices}, direction={self.direction}, "
            f"ignore_parent={self.ignore_parent})"
        )

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        d.pop("possibly_empty")
        d["gcps"] = tuple(gp.to_jsonable() for gp in self.gcps)
        d["indices"] = self.indices
        d["direction"] = self.direction
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "RequirementPlacementStrategy":
        gcps = tuple(GriddedCayleyPerm.from_dict(gcp) for gcp in d.pop("gcps"))
        return cls(gcps=gcps, **d)


class RGFVRequirementPlacementStrategy(RequirementPlacementStrategy):
    """Strategy for placing requirements in a tiling for restricted growth functions
    vertical insertion encoding."""

    def algorithm(self, tiling: Tiling) -> PointPlacement:
        return RGFVPointPlacement(tiling)

    def formal_step(self):
        return "Point placement in RGF"


class RGFHRequirementPlacementStrategy(RequirementPlacementStrategy):
    """Strategy for placing requirements in a tiling for restricted growth functions
    horizontal insertion encoding."""

    def algorithm(self, tiling: Tiling) -> PointPlacement:
        return RGFHPointPlacement(tiling)

    def formal_step(self):
        return "Point placement in RGF"


class VerticalInsertionEncodingPlacementFactory(StrategyFactory[Tiling]):
    """Factory for creating RequirementPlacementStrategy to place points
    for the vertical insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        direction = DIR_LEFT_BOT
        yield RequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "VerticalInsertionEncodingPlacementFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Place next point of insertion encoding"


class RGFVerticalInsertionEncodingPlacementFactory(StrategyFactory[Tiling]):
    """Factory for creating RequirementPlacementStrategy to place points
    for the vertical insertion encoding for enumerating restricted growth functions."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[RGFVRequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        direction = DIR_LEFT_BOT
        yield RGFVRequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "RGFVerticalInsertionEncodingPlacementFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Place next point in RGF"


class HorizontalInsertionEncodingPlacementFactory(StrategyFactory[Tiling]):
    """Factory for creating RequirementPlacementStrategy to place points
    for the horizontal insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        direction = DIR_LEFT
        yield RequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "HorizontalInsertionEncodingPlacementFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Place next point of insertion encoding"


class RGFHorizontalInsertionEncodingPlacementFactory(
    HorizontalInsertionEncodingPlacementFactory
):
    """Factory for creating RequirementPlacementStrategy to place points
    for the horizontal insertion encoding for enumerating restricted growth functions.
    """

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[RGFHRequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        direction = DIR_LEFT
        yield RGFHRequirementPlacementStrategy(gcps, indices, direction)
