"""Strategies for row and column separation in tracked tilings."""

from typing import Iterator, Optional, Iterable
from gridded_cayley_permutations import GriddedCayleyPerm
from tilescope.strategies import (
    AbstractLessThanOrEqualRowColSeparationFactory,
)
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)
from cayley_permutations import CayleyPermutation
from clouds.strategies.row_col_sep import (
    TrackedLessThanRowColSeparationStrategy,
    TrackedLessThanOrEqualRowColSeparationStrategy,
)
from .rgf_tracked_tiling import TrackedTiling

Cell = tuple[int, int]


class RGFTrackedLessThanRowColSeparation(LessThanRowColSeparation):
    """Separates rows and columns with less than constraints and tracks clouds."""

    def __init__(
        self, tracked_tiling: TrackedTiling, row_order: Optional[list[set[Cell]]] = None
    ) -> None:
        self.tracked_tiling = tracked_tiling
        self.rows_had_vals = tracked_tiling.rows_had_vals
        super().__init__(tracked_tiling.tiling, row_order=row_order)

    def tracked_row_col_separation(self) -> Iterable[TrackedTiling]:
        """Yield the separated tilings with tracked clouds."""
        for separated_tiling in self.row_col_separation():
            indices_clouds, value_clouds = TrackedTiling.map_clouds(
                indices_clouds=self.tracked_tiling.indices_clouds,
                value_clouds=self.tracked_tiling.value_clouds,
                tiling_map=self.row_col_map,
            )
            yield TrackedTiling(
                separated_tiling,
                value_clouds=value_clouds,
                indices_clouds=indices_clouds,
                intersect_clouds_with_active=True,
                rows_had_vals=self.rows_had_vals,
            )

    def inequalities_sets(
        self,
    ) -> tuple[set[tuple[Cell, Cell]], set[tuple[Cell, Cell]], set[tuple[Cell, Cell]]]:
        """Finds the length 2 obstructions in different cells.
        If they are on the same column and are an increasing obstruction,
        they are added to less_than_col to separate columns.
        If they are on the same row and are an increasing obstruction,
        they are added to less_than_row to separate rows.
        If they are in the same row and a constant obstruction,
        they are added to not_equal to help with strictly less than later.
        """
        not_equal = set()
        less_than_row = set()
        less_than_col = set()
        for ob in self.tiling.obstructions:
            if len(ob) == 2:
                cell1, cell2 = ob.positions
                if cell1 == cell2:
                    continue
                if cell1[0] == cell2[0]:
                    if ob.pattern == CayleyPermutation([0, 1]):
                        less_than_col.add((cell2, cell1))
                    if ob.pattern == CayleyPermutation([1, 0]):
                        less_than_col.add((cell2, cell1))
                elif cell1[1] == cell2[1]:
                    if ob.pattern == CayleyPermutation([0, 1]):
                        if cell1[1] in self.rows_had_vals:
                            less_than_row.add((cell2, cell1))
                    if ob.pattern == CayleyPermutation([1, 0]):
                        if (cell2, cell1) in less_than_row:
                            less_than_row.remove((cell2, cell1))
                        else:
                            less_than_row.add((cell1, cell2))
                    if ob.pattern == CayleyPermutation([0, 0]):
                        not_equal.add((cell1, cell2))
                        not_equal.add((cell2, cell1))
        return less_than_col, less_than_row, not_equal


class RGFTrackedLessThanOrEqualRowColSeparation(
    LessThanOrEqualRowColSeparation,
):
    """Separates rows and columns with less than or equal constraints and tracks clouds."""

    def __init__(
        self, tracked_tiling: TrackedTiling, row_order: Optional[list[set[Cell]]] = None
    ) -> None:
        self.tracked_tiling = tracked_tiling
        self.rows_had_vals = tracked_tiling.rows_had_vals

        super().__init__(tracked_tiling.tiling, row_order=row_order)

    def tracked_row_col_separation(
        self,
    ) -> Iterable[TrackedTiling]:
        """Yield the separated tilings with tracked clouds."""
        for separated_tiling in self.row_col_separation():
            indices_clouds, value_clouds = TrackedTiling.map_clouds(
                indices_clouds=self.tracked_tiling.indices_clouds,
                value_clouds=self.tracked_tiling.value_clouds,
                tiling_map=self.row_col_map,
            )
            yield TrackedTiling(
                separated_tiling,
                value_clouds=value_clouds,
                indices_clouds=indices_clouds,
                intersect_clouds_with_active=True,
                rows_had_vals=self.rows_had_vals,
            )

    def inequalities_sets(
        self,
    ) -> tuple[set[tuple[Cell, Cell]], set[tuple[Cell, Cell]], set[tuple[Cell, Cell]]]:
        """Finds the length 2 obstructions in different cells.
        If they are on the same column and are an increasing obstruction,
        they are added to less_than_col to separate columns.
        If they are on the same row and are an increasing obstruction,
        they are added to less_than_row to separate rows.
        If they are in the same row and a constant obstruction,
        they are added to not_equal to help with strictly less than later.
        """
        not_equal = set()
        less_than_row = set()
        less_than_col = set()
        for ob in self.tiling.obstructions:
            if len(ob) == 2:
                cell1, cell2 = ob.positions
                if cell1 == cell2:
                    continue
                if cell1[0] == cell2[0]:
                    if ob.pattern == CayleyPermutation([0, 1]):
                        less_than_col.add((cell2, cell1))
                    if ob.pattern == CayleyPermutation([1, 0]):
                        less_than_col.add((cell2, cell1))
                elif cell1[1] == cell2[1]:
                    if ob.pattern == CayleyPermutation([0, 1]):
                        if cell1[1] in self.rows_had_vals:
                            less_than_row.add((cell2, cell1))
                    if ob.pattern == CayleyPermutation([1, 0]):
                        if (cell2, cell1) in less_than_row or GriddedCayleyPerm(
                            CayleyPermutation([0, 1]), (cell2, cell1)
                        ) in self.tracked_tiling.tiling.obstructions:
                            less_than_row.remove((cell2, cell1))
                        else:
                            if (
                                GriddedCayleyPerm(
                                    CayleyPermutation([0, 1]), (cell1, cell2)
                                )
                                not in self.tracked_tiling.tiling.obstructions
                            ):
                                less_than_row.add((cell1, cell2))
                    if ob.pattern == CayleyPermutation([0, 0]):
                        not_equal.add((cell1, cell2))
                        not_equal.add((cell2, cell1))
        return less_than_col, less_than_row, not_equal


class RGFTrackedLessThanRowColSeparationStrategy(
    TrackedLessThanRowColSeparationStrategy,
):
    """A strategy for separating rows and columns with less than constraints."""

    def algorithm(self, comb_class):
        """Return the algorithm for row and column separation."""
        return RGFTrackedLessThanRowColSeparation(comb_class)


class RGFTrackedLessThanOrEqualRowColSeparationStrategy(
    TrackedLessThanOrEqualRowColSeparationStrategy,
):
    # pylint: disable=too-many-ancestors
    """A strategy for separating rows and columns with less than or equal constraints."""

    def algorithm(self, comb_class):
        return RGFTrackedLessThanOrEqualRowColSeparation(comb_class, self.row_order)


class RGFTrackedLessThanOrEqualRowColSeparationFactory(
    AbstractLessThanOrEqualRowColSeparationFactory
):
    """A factory for creating strategies for separating rows and columns
    with less than or equal constraints."""

    def algorithm(
        self, comb_class: TrackedTiling
    ) -> RGFTrackedLessThanOrEqualRowColSeparation:
        """Return the algorithm for row and column separation."""
        return RGFTrackedLessThanOrEqualRowColSeparation(comb_class)

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[RGFTrackedLessThanOrEqualRowColSeparationStrategy]:
        """Finds max expansion and if any row separates more than 2 cells then
        it merges them together so that each row splits into at most 2 rows
        (plus a point row between them) and yields all possible ways of doing this."""

        for row_order in self.row_separations(comb_class):
            yield RGFTrackedLessThanOrEqualRowColSeparationStrategy(
                row_order=row_order,
            )
