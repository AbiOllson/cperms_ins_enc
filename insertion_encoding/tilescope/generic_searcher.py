"""A generic searcher class for insertion encodings."""

import abc
from functools import cached_property
from comb_spec_searcher import (
    CombinatorialSpecificationSearcher,
    CombinatorialSpecification,
    StrategyPack,
)
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import string_to_basis


class GenericSearcher(abc.ABC):
    """A generic searcher class for insertion encodings."""

    def __init__(self, basis: str, debug=False):
        self.debug = debug
        if isinstance(basis, str):
            self.basis = string_to_basis(basis)
        else:
            self.basis = basis
        if not self.regular_check():
            raise ValueError(
                f"The class Av{tuple(self.basis)} can not be enumerated with "
                f"{self.type_of_encoding()} insertion encoding"
            )

    @abc.abstractmethod
    def type_of_encoding(self) -> str:
        """Returns the type of encoding."""

    @abc.abstractmethod
    def start_class(self):
        """Returns the starting class - a tiling or configuration avoiding a basis."""

    def regular_check(self) -> bool:
        """Checks if the class can be enumerated with the given insertion encoding."""
        return True

    @abc.abstractmethod
    def pack(self) -> "StrategyPack":
        """Returns the strategy pack."""


class GenericTilingsSearcher(GenericSearcher):
    """A generic searcher for methods which use tilings."""

    def start_class(self):
        return Tiling(
            [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in self.basis],
            [],
            (1, 1),
        )

    def auto_search(self, max_expansion_time=600) -> CombinatorialSpecification:
        """Search for a specification."""
        return self.comb_spec_searcher.auto_search(
            max_expansion_time=max_expansion_time
        )

    @cached_property
    def comb_spec_searcher(self) -> CombinatorialSpecificationSearcher:
        """Returns the CombinatorialSpecificationSearcher object for this searcher."""
        print(self.pack(), self.pack().name)
        return CombinatorialSpecificationSearcher(
            self.start_class(), self.pack(), debug=self.debug
        )
