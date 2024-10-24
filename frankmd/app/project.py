import os
from typing import Self

from frankmd.app.sheet import Sheet


class LibraryDir:
    """Reference to a directory within a library"""

    __slots__ = (
        "_path",  # Absolute path
        "_depth",  # Relative to library root dir
        "_subdirs",
        "_sheets",
    )

    def __init__(self, path: str, depth: int) -> None:
        self._path: str = path
        self._depth: int = depth
        self._subdirs: dict[str, Self] = {}
        self._sheets: dict[str, Sheet] = {}

    def __repr__(self) -> str:
        return self._path

    def __lt__(self, other: Self) -> bool:
        return os.path.basename(self._path) < os.path.basename(other._path)

    def get_depth(self) -> int:
        return self._depth

    def get_display_name(self) -> str:
        return os.path.basename(self._path)

    def get_path(self) -> str:
        return self._path

    # def get_sheets(self)

    def get_subdirs(self) -> list[Self]:
        """Returns subdirs sorted by name."""
        subdirs: list[Self] = []
        for item in self._subdirs.items():
            subdirs.append(item[1])
        return sorted(subdirs)

    def get_sheets(self) -> list[Sheet]:
        """Returns sheets sorted by path."""
        sheets: list[Sheet] = []
        for item in self._sheets.items():
            sheets.append(item[1])
        return sorted(sheets)

    def refresh(self) -> None:
        """Re-crawl the project directory"""

        for entry in os.scandir(self._path):
            if entry.is_symlink():
                continue
            if entry.name.startswith("."):
                continue

            if entry.is_dir():
                subdir = self._subdirs.get(entry.path)
                if subdir is None:
                    new_subdir = LibraryDir(entry.path, self._depth + 1)
                    self._add_subdir(new_subdir)
                    new_subdir.refresh()
                else:
                    subdir.refresh()

            elif entry.name.endswith(".md"):
                sheet = self._sheets.get(entry.path)
                if sheet is None:
                    new_sheet = Sheet(entry.path)
                    self._add_sheet(new_sheet)
                    # new_sheet.refresh()
                else:
                    pass  # sheet.refresh()

    def create_sheet(self) -> None:
        path = os.path.join(self._path, "New sheet.md")

        attempt_no = 1
        while os.path.exists(path):
            attempt_no += 1
            path = os.path.join(self._path, f"New sheet {attempt_no}.md")

        with open(path, "w", encoding="utf-8") as _:
            pass

        self._add_sheet(Sheet(path))

    def _add_subdir(self, subdir: Self) -> None:
        assert self._subdirs.get(subdir.get_path()) is None
        self._subdirs[subdir.get_path()] = subdir

    def _add_sheet(self, sheet: Sheet) -> None:
        assert self._sheets.get(sheet.get_path()) is None
        self._sheets[sheet.get_path()] = sheet


class Project:

    __slots__ = ("_root",)

    def __init__(self, root_path: str):
        self._root: LibraryDir = LibraryDir(root_path, 0)
        self.refresh()

    def get_display_name(self) -> str:
        return self._root.get_display_name()

    def get_root(self) -> LibraryDir:
        return self._root

    def refresh(self) -> None:
        """Re-crawl the project directory"""

        self._root.refresh()

    def get_root_path(self) -> str:
        return self._root.get_path()

    def set_root_path(self, new_root_path: str) -> None:
        self._root = LibraryDir(new_root_path, 0)
        self.refresh()
