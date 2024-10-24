import os
import pytest

from frankmd.app import app_state
from frankmd.app.app_state import AppState
from frankmd.app.project import LibraryDir, Project
from frankmd.app.sheet import Sheet

ROOT = os.path.join("tests", "example_content")


def test_add_project():
    app = AppState()

    path_a = os.path.join(ROOT, "project_a")
    path_b = os.path.join(ROOT, "project_b")
    app.add_project(path_a)
    app.add_project(path_b)
    assert len(app.get_projects()) == 2
    assert isinstance(app.get_projects()[0], Project)
    assert isinstance(app.get_projects()[1], Project)


def test_cant_add_nonexistent_project_dir():
    app = AppState()

    path_a = os.path.join(ROOT, "nonexist")
    try:
        app.add_project(path_a)
        assert False
    except FileNotFoundError:
        pass


def test_cant_add_file_as_project():
    app = AppState()

    path_a = os.path.join(ROOT, "a_file.md")
    try:
        app.add_project(path_a)
        assert False
    except NotADirectoryError:
        pass


def test_cant_add_existing_project():
    app = AppState()

    path_a = os.path.join(ROOT, "project_a")
    app.add_project(path_a)
    try:
        app.add_project(path_a)
        assert False
    except app_state.ProjectAlreadyExistsError:
        pass

    assert len(app.get_projects()) == 1
    assert isinstance(app.get_projects()[0], Project)


def test_cant_add_nested_child_project():
    app = AppState()

    path_a = os.path.join(ROOT, "project_a")
    path_b = os.path.join(ROOT, "project_a", "subdir")
    app.add_project(path_a)
    try:
        app.add_project(path_b)
        assert False
    except app_state.NestedProjectsChildError:
        pass

    assert len(app.get_projects()) == 1
    assert isinstance(app.get_projects()[0], Project)
    assert app.get_projects()[0].get_root_path() == os.path.realpath(path_a)


def test_cant_add_nested_parent_project():
    app = AppState()

    path_a = os.path.join(ROOT, "project_a", "subdir")
    path_b = os.path.join(ROOT, "project_a")
    app.add_project(path_a)
    try:
        app.add_project(path_b)
        assert False
    except app_state.NestedProjectsParentError:
        pass

    assert len(app.get_projects()) == 1
    assert isinstance(app.get_projects()[0], Project)
    assert app.get_projects()[0].get_root_path() == os.path.realpath(path_a)


def test_remove_project_relpath():
    app = AppState()

    path_a = os.path.join(ROOT, "project_a")
    path_b = os.path.join(ROOT, "project_b")
    app.add_project(path_a)
    app.add_project(path_b)
    app.remove_project(path_a)
    assert len(app.get_projects()) == 1
    app.get_projects()[0].get_root_path(), os.path.realpath(path_b)


def test_remove_project_realpath():
    app = AppState()

    path_a = os.path.realpath(os.path.join(ROOT, "project_a"))
    path_b = os.path.realpath(os.path.join(ROOT, "project_b"))
    app.add_project(path_a)
    app.add_project(path_b)
    app.remove_project(path_a)
    assert len(app.get_projects()) == 1
    app.get_projects()[0].get_root_path(), os.path.realpath(path_b)


def test_remove_project_no_such():
    app = AppState()

    path_a = os.path.realpath(os.path.join(ROOT, "project_a"))
    path_b = os.path.realpath(os.path.join(ROOT, "project_b"))
    app.add_project(path_a)
    try:
        app.remove_project(path_b)
        assert False
    except app_state.ProjectDoesntExistError:
        pass
    assert len(app.get_projects()) == 1
    app.get_projects()[0].get_root_path(), os.path.realpath(path_b)
