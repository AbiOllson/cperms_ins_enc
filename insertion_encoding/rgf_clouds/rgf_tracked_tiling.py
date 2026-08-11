from functools import cached_property
from typing import Iterable, Optional, Iterator, Dict
from itertools import product
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap

Cell = tuple[int, int]
Clouds = tuple[tuple[int, ...], ...]


class TrackedTiling(Tiling):
    """A Tiling with clouds which keep track of areas of the tiling.
    One type of cloud tracks the number of values in the cells and the other
    tracks the number of indices in the cells."""

    # pylint:disable=too-many-public-methods

    def __init__(
        self,
        tiling: Tiling,
        indices_clouds: Iterable[Iterable[int]] = (),
        value_clouds: Iterable[Iterable[int]] = (),
        simplify: bool = False,
        intersect_clouds_with_active: bool = True,
        rows_had_vals: set[int] = set(),
    ) -> None:
        # pylint:disable=too-many-arguments
        # pylint:disable=too-many-positional-arguments
        self.rows_had_vals = rows_had_vals
        self.tiling = tiling
        super().__init__(
            tiling.obstructions, tiling.requirements, tiling.dimensions, simplify
        )
        self.value_clouds = tuple(
            sorted(set(tuple(sorted(set(c))) for c in value_clouds))
        )
        self.indices_clouds = tuple(
            sorted(set(tuple(sorted(set(c))) for c in indices_clouds))
        )
        if intersect_clouds_with_active:
            active_cols, active_rows = self.active_col_rows
            self.value_clouds = tuple(
                sorted(
                    set(
                        c
                        for c in [
                            tuple(
                                sorted(set(row for row in cloud if row in active_rows))
                            )
                            for cloud in value_clouds
                        ]
                        if c
                    )
                )
            )
            self.indices_clouds = tuple(
                sorted(
                    set(
                        c
                        for c in [
                            tuple(
                                sorted(set(col for col in cloud if col in active_cols))
                            )
                            for cloud in indices_clouds
                        ]
                        if c
                    )
                )
            )

    def remove_clouds(self) -> "TrackedTiling":
        """Remove all clouds from the tracked tiling."""
        return TrackedTiling(self.tiling)

    def remove_idx_cloud(self, idx_cloud: tuple[int, ...]) -> "TrackedTiling":
        """Remove an index cloud from the tracked tiling."""
        new_idx_clouds = tuple(
            cloud for cloud in self.indices_clouds if cloud != idx_cloud
        )
        return TrackedTiling(
            self.tiling,
            indices_clouds=new_idx_clouds,
            value_clouds=self.value_clouds,
        )

    def remove_val_cloud(self, val_cloud: tuple[int, ...]) -> "TrackedTiling":
        """Remove a value cloud from the tracked tiling."""
        new_val_clouds = tuple(
            cloud for cloud in self.value_clouds if cloud != val_cloud
        )
        return TrackedTiling(
            self.tiling,
            indices_clouds=self.indices_clouds,
            value_clouds=new_val_clouds,
        )

    def add_clouds(
        self,
        value_clouds: Optional[Clouds] = None,
        indices_clouds: Optional[Clouds] = None,
    ) -> "TrackedTiling":
        """Add clouds to the tracked tiling."""
        new_value_clouds = (
            tuple(sorted(set(self.value_clouds + value_clouds)))
            if value_clouds is not None
            else self.value_clouds
        )
        new_indices_clouds = (
            tuple(sorted(set(self.indices_clouds + indices_clouds)))
            if indices_clouds is not None
            else self.indices_clouds
        )
        return TrackedTiling(
            self.tiling,
            indices_clouds=new_indices_clouds,
            value_clouds=new_value_clouds,
        )

    @cached_property
    def active_col_rows(self) -> tuple[set[int], set[int]]:
        """Returns the columns and rows in the tiling that have active cells."""
        active_rows = set()
        active_cols = set()
        for cell in self.active_cells:
            active_cols.add(cell[0])
            active_rows.add(cell[1])
        return active_cols, active_rows

    @classmethod
    def map_clouds(
        cls,
        indices_clouds: Clouds,
        value_clouds: Clouds,
        tiling_map: RowColMap,
    ) -> tuple[Clouds, Clouds]:
        """For a given row-col map of self.tiling to a new tiling,
        updates the clouds to match the new tiling.

        Can add this to the new tiling, check that intersects active cells."""
        new_value_clouds = tuple(
            sorted(
                c
                for c in [
                    tuple(sorted(tiling_map.preimages_of_rows(cloud)))
                    for cloud in value_clouds
                ]
                if c
            )
        )
        new_indices_clouds = tuple(
            sorted(
                c
                for c in [
                    tuple(sorted(tiling_map.preimages_of_cols(cloud)))
                    for cloud in indices_clouds
                ]
                if c
            )
        )
        return (
            new_indices_clouds,
            new_value_clouds,
        )

    def delete_rows_and_columns(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> "TrackedTiling":
        """Return a new tiling with the given rows and columns removed
        and updated clouds."""
        new_til, rc_map = self.tiling_and_rc_map_after_deleting_rows_and_columns(
            cols, rows
        )
        row_map, col_map = rc_map.row_map, rc_map.col_map
        new_value_clouds = tuple(
            sorted(
                tuple(sorted(row_map[row] for row in cloud if row not in rows))
                for cloud in self.value_clouds
            )
        )
        new_indices_clouds = tuple(
            sorted(
                tuple(sorted(col_map[col] for col in cloud if col not in cols))
                for cloud in self.indices_clouds
            )
        )
        return TrackedTiling(
            new_til,
            value_clouds=new_value_clouds,
            indices_clouds=new_indices_clouds,
        )

    def remove_empty_rows_and_columns(self) -> "TrackedTiling":
        """Deletes any rows and columns in the gridding that are empty"""
        empty_cols, empty_rows = self.find_empty_rows_and_columns()
        return self.delete_rows_and_columns(empty_cols, empty_rows)

    def fuse(self, fuse_rows: bool, index: int) -> "TrackedTiling":
        """If fuse_rows, tries to fuse rows, otherwise, tries to fuse cols.
        Creates a cloud at index 'index' of rows if fuse_rows else columns."""
        new_cloud = (index,)
        if fuse_rows is False:
            underlying = self.tiling.delete_rows_and_columns(cols=[index], rows=[])
            new_indices_clouds = tuple(
                tuple(x if x <= index else x - 1 for x in cloud)
                for cloud in self.indices_clouds
            ) + (new_cloud,)
            return TrackedTiling(
                underlying,
                indices_clouds=new_indices_clouds,
                value_clouds=self.value_clouds,
            )
        fuse_idx = index if index in self.point_rows else index + 1
        underlying = self.tiling.delete_rows_and_columns(cols=[], rows=[fuse_idx])
        value_clouds = tuple(
            tuple(x if x <= index else x - 1 for x in cloud)
            for cloud in self.value_clouds
        ) + (new_cloud,)
        return TrackedTiling(
            underlying,
            indices_clouds=self.indices_clouds,
            value_clouds=value_clouds,
        )

    def is_fusable(self, fuse_rows: bool, index: int) -> bool:
        """If fuse rows, checks if the rows at index and index+1 are fuseable,
        otherwise does the same for cols at index and index+1.

        can't fuse rows/cols if a cloud maps onto only part of the rows/cols to be fused,
        must map to all or none of it."""
        if fuse_rows:
            test_tiling = self.delete_rows_and_columns(cols=[], rows=[index])
        else:
            test_tiling = self.delete_rows_and_columns(cols=[index], rows=[])
        new_test_tiling = test_tiling.split_row_or_col(fuse_rows, index)
        return new_test_tiling == self

    def add_obstructions(self, gcps: Iterable[GriddedCayleyPerm]) -> "TrackedTiling":
        """
        Returns a new tiling with the given gridded Cayley permutations added as obstructions.
        """
        return TrackedTiling(
            Tiling(self.obstructions + tuple(gcps), self.requirements, self.dimensions),
            indices_clouds=self.indices_clouds,
            value_clouds=self.value_clouds,
            intersect_clouds_with_active=True,
        )

    def add_requirements(
        self, requirements: Iterable[Iterable[GriddedCayleyPerm]]
    ) -> "TrackedTiling":
        """
        Returns a new tiling with the given requirements added.
        """
        return TrackedTiling(
            Tiling(
                self.obstructions,
                self.requirements + tuple(requirements),
                self.dimensions,
            ),
            indices_clouds=self.indices_clouds,
            value_clouds=self.value_clouds,
        )

    def add_requirement_list(
        self, requirement_list: Iterable[GriddedCayleyPerm]
    ) -> "TrackedTiling":
        """
        Returns a new tiling with the given requirement list added.
        """
        return self.add_requirements([requirement_list])

    # CSS methods
    @property
    def extra_parameters(self) -> tuple[str, ...]:
        """Indices are first, then values."""
        index_cloud_params = [f"i_{i}" for i in range(len(self.indices_clouds))]
        value_cloud_params = [f"v_{i}" for i in range(len(self.value_clouds))]
        return tuple(index_cloud_params + value_cloud_params)

    def find_parameter(self, cloud: tuple[int, ...], row: bool) -> str:
        """Finds the name of the parameter for the cloud."""
        try:
            index = (
                self.value_clouds.index(cloud)
                if row
                else self.indices_clouds.index(cloud)
            )
        except ValueError as exc:
            raise ValueError("Cloud not found in tracked tiling.") from exc
        return f"v_{index}" if row else f"i_{index}"

    def get_minimum_value(self, parameter: str) -> int:
        return min(
            self.get_value(gcp, parameter) for gcp in self.minimal_gridded_cperms()
        )

    def get_value(self, gcp: GriddedCayleyPerm, parameter: str) -> int:
        """Returns the value of the parameter on the given gridded Cayley permutation."""
        x, y = parameter.split("_")
        if x == "v":
            cloud = self.value_clouds[int(y)]
            return len(
                set(
                    gcp.pattern[i]
                    for i, cell in enumerate(gcp.positions)
                    if cell[1] in cloud
                )
            )
        if x == "i":
            cloud = self.indices_clouds[int(y)]
            return sum(1 for cell in gcp.positions if cell[0] in cloud)
        raise ValueError(f"Not a valid parameter: {parameter}")

    def get_cloud(self, parameter: str) -> tuple[int, ...]:
        """Returns the cloud corresponding to the parameter."""
        x, y = parameter.split("_")
        if x == "v":
            return self.value_clouds[int(y)]
        if x == "i":
            return self.indices_clouds[int(y)]
        raise ValueError(f"Not a valid parameter: {parameter}")

    def get_parameters(self, obj: GriddedCayleyPerm) -> tuple[int, ...]:
        return tuple(self.get_value(obj, param) for param in self.extra_parameters)

    def possible_parameters(self, n: int) -> Iterator[Dict[str, int]]:
        parameters = [
            self.find_parameter(cloud, False) for cloud in self.indices_clouds
        ] + [self.find_parameter(cloud, True) for cloud in self.value_clouds]
        for values in product(*[range(n + 1) for _ in parameters]):
            yield dict(zip(parameters, values))

    def __eq__(self, other):
        if isinstance(other, TrackedTiling):
            return (
                self.tiling == other.tiling
                and self.indices_clouds == other.indices_clouds
                and self.value_clouds == other.value_clouds
            )
        return NotImplemented

    def __hash__(self):
        return hash((hash(self.tiling), self.indices_clouds, self.value_clouds))

    def to_jsonable(self) -> dict:
        res = {
            "indices_clouds": [list(cloud) for cloud in self.indices_clouds],
            "value_clouds": [list(cloud) for cloud in self.value_clouds],
        }
        res.update(super().to_jsonable())
        return res

    @classmethod
    def from_dict(cls, d: dict) -> "Tiling":
        return TrackedTiling(
            Tiling.from_dict(d),
            indices_clouds=d["indices_clouds"],
            value_clouds=d["value_clouds"],
        )

    def __str__(self) -> str:
        return (
            f"Tiling: \n{self.tiling}\n"
            f"Indices clouds: {self.indices_clouds}\n"
            f"Value clouds: {self.value_clouds},"
        )

    def __repr__(self) -> str:
        return (
            f"TrackedTiling(tiling={repr(self.tiling)}, "
            f"indices_clouds={repr(self.indices_clouds)}, "
            f"value_clouds={repr(self.value_clouds)})"
        )
