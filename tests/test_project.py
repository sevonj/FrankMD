import os
import pytest

from frankmd.app.project import LibraryDir, Project
from frankmd.app.sheet import Sheet

ROOT = os.path.join("tests", "example_content")


def print_dir_tree(dir: LibraryDir, depth: int = 0):
    print("  " * depth, dir.get_display_name() + "/")
    for child in dir._subdirs.items():
        print_dir_tree(child[1], depth + 1)

    for sheet in dir._sheets.items():
        print("  " * (depth + 1), sheet[1].get_display_name())


def test_open_project():
    path = os.path.join(ROOT, "project_a")
    project = Project(path)
    assert isinstance(project, Project)


def test_open_project_has_correct_path():
    path = os.path.join(ROOT, "project_a")
    project = Project(path)
    assert project.get_root_path() == path
    assert project.get_root_path() == project.get_root().get_path()


def test_cant_open_nonexistent_project():
    path = os.path.join(ROOT, "nonexist")
    try:
        project = Project(path)
        assert False
    except:
        pass


def test_open_project_finds_subdirs():
    path = os.path.join(ROOT, "project_a")
    project = Project(path)

    print_dir_tree(project.get_root())

    root = project.get_root()
    assert isinstance(root, LibraryDir)
    assert len(root.get_subdirs()) == 2

    subdir = root.get_subdirs()[0]
    assert isinstance(subdir, LibraryDir)
    assert subdir.get_path() == os.path.join(path, "subdir")
    assert len(subdir.get_subdirs()) == 1

    subsubdir = subdir.get_subdirs()[0]
    assert isinstance(subsubdir, LibraryDir)
    assert subsubdir.get_path() == os.path.join(path, "subdir", "subsubdir")
    assert len(subsubdir.get_subdirs()) == 0

    subdir2 = root.get_subdirs()[1]
    assert isinstance(subdir2, LibraryDir)
    assert subdir2.get_path() == os.path.join(path, "subdir2")
    assert len(subdir2.get_subdirs()) == 0


def test_open_project_finds_all_sheets():
    path = os.path.join(ROOT, "project_a")
    project = Project(path)

    print_dir_tree(project.get_root())

    root = project.get_root()
    subdir = root.get_subdirs()[0]
    subdir2 = root.get_subdirs()[1]
    subsubdir = subdir.get_subdirs()[0]

    assert len(root.get_sheets()) == 3
    assert len(subdir.get_sheets()) == 1
    assert len(subsubdir.get_sheets()) == 1
    assert len(subdir2.get_sheets()) == 0

    sheet_0 = root.get_sheets()[0]
    sheet_1 = root.get_sheets()[1]
    sheet_2 = root.get_sheets()[2]
    sheet_sub = subdir.get_sheets()[0]
    sheet_subsub = subsubdir.get_sheets()[0]

    assert isinstance(sheet_0, Sheet)
    assert isinstance(sheet_1, Sheet)
    assert isinstance(sheet_2, Sheet)
    assert isinstance(sheet_sub, Sheet)
    assert isinstance(sheet_subsub, Sheet)
    assert sheet_0.get_path() == os.path.join(path, "sheet1.md")
    assert sheet_1.get_path() == os.path.join(path, "sheet2.md")
    assert sheet_2.get_path() == os.path.join(path, "sheet3.md")
    assert sheet_sub.get_path() == os.path.join(path, "subdir", "subsheet.md")
    assert sheet_subsub.get_path() == os.path.join(
        path, "subdir", "subsubdir", "subsubsheet.md"
    )
