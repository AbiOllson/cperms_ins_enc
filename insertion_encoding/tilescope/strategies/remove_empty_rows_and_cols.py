"""This module contains the strategy for removing all the
empty rows and columns from a tiling and the strategy
for removing extra requirements when enumerating
restricted growth functions of matchings."""

from typing import Dict, Iterator, Optional, Tuple
from comb_spec_searcher import DisjointUnionStrategy
from comb_spec_searcher.exception import StrategyDoesNotApply

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm

Cell = Tuple[int, int]


class RemoveEmptyRowsAndColumnsStrategy(
    DisjointUnionStrategy[Tiling, GriddedCayleyPerm]
):
    """Strategy for removing empty rows and columns from a tiling."""

    def __init__(
        self,
        ignore_parent: bool = True,
        possibly_empty: bool = False,
    ):
        super().__init__(ignore_parent=ignore_parent, possibly_empty=possibly_empty)

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        rows_and_cols = comb_class.find_empty_rows_and_columns()
        if len(rows_and_cols[0]) == 0 and len(rows_and_cols[1]) == 0:
            raise StrategyDoesNotApply("No empty rows or columns")
        print("\nRemove empty rows and columns from tiling")
        print(comb_class)
        print(comb_class.remove_empty_rows_and_columns())
        return (comb_class.remove_empty_rows_and_columns(),)

    def extra_parameters(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[Dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))

    def formal_step(self):
        return "Remove empty rows and columns"

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
            f"{self.__class__.__name__}("
            f"ignore_parent={self.ignore_parent}, "
            f"possibly_empty={self.possibly_empty})"
        )

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "RemoveEmptyRowsAndColumnsStrategy":
        return cls(**d)


class MatchingsRemoveExtraReqsStrategy(
    DisjointUnionStrategy[Tiling, GriddedCayleyPerm]
):
    """Strategy for removing extra requirements from requirement lists in a tiling
    for enumerating restricted growth functions of matchings."""

    def __init__(
        self,
        ignore_parent: bool = True,
        possibly_empty: bool = False,
    ):
        super().__init__(ignore_parent=ignore_parent, possibly_empty=possibly_empty)

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        new_requirements: list[tuple[GriddedCayleyPerm, ...]] = []
        for req_list in comb_class.requirements:
            if len(req_list) == 1:
                new_requirements.append(req_list)
                continue
            new_req_list = tuple(req for req in req_list if len(req.positions) == 1)
            new_requirements.append(new_req_list)
        if new_requirements == comb_class.requirements:
            raise StrategyDoesNotApply("No extra requirements to remove")
        return (
            Tiling(comb_class.obstructions, new_requirements, comb_class.dimensions),
        )

    def extra_parameters(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[Dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))

    def formal_step(self):
        return "Remove extra requirements from requirement lists."

    def backward_map(
        self,
        comb_class: Tiling,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
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
            f"{self.__class__.__name__}("
            f"ignore_parent={self.ignore_parent}, "
            f"possibly_empty={self.possibly_empty})"
        )

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "MatchingsRemoveExtraReqsStrategy":
        return cls(**d)
