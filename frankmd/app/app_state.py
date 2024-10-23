import os
from frankmd.app.project import Project, LibraryDir
from frankmd.app.sheet import Sheet


class NotADirError(Exception):
    def __str__(self) -> str:
        return "Path wasn't a valid directory."


class ProjectAlreadyExistsError(Exception):
    def __str__(self) -> str:
        return "This project already exists in the library."


class ProjectDoesntExistError(Exception):
    def __str__(self) -> str:
        return "The library doesn't contain such project."


class NestedProjectsChildError(Exception):
    def __str__(self) -> str:
        return "Can't add a project inside another project."


class NestedProjectsParentError(Exception):
    def __str__(self) -> str:
        return "Can't add a project that contains another project."


class AppState:
    """
    This class is the root of all application logic.
    """

    __slots__ = (
        "_projects",
        "_current_dir",
        "_current_sheet",
    )

    def __init__(self) -> None:
        self._projects: list[Project] = []

        self._projects.append(Project("/home/julius/Documents/Notes/obsidian/Personal"))
        self._projects.append(Project("/home/julius/Documents/Courses/Cyber Security"))

        self._current_dir: LibraryDir | None = self._projects[0].get_root()
        self._current_sheet: Sheet | None

    def get_current_dir(self) -> LibraryDir | None:
        return self._current_dir

    def set_current_dir(self, library_dir: LibraryDir) -> None:
        self._current_dir = library_dir

    def get_current_sheet(self) -> Sheet | None:
        return self._current_sheet

    def set_current_sheet(self, sheet: Sheet) -> None:
        self._current_sheet = sheet

    def get_projects(self) -> list[Project]:
        return self._projects

    def add_project(self, path: str) -> None:
        """May raise exception."""

        new_path = os.path.abspath(path)

        for project in self._projects:
            project_path = os.path.abspath(project.get_root_path())

            if not os.path.isdir(new_path):
                raise NotADirError()

            if new_path == project_path:
                raise ProjectAlreadyExistsError()
            if os.path.commonprefix([new_path, project_path]) == project_path:
                raise NestedProjectsChildError()
            if os.path.commonprefix([project_path, new_path]) == new_path:
                raise NestedProjectsParentError()

        new_project = Project(new_path)
        self._projects.append(new_project)
        self.set_current_dir(new_project.get_root())

    def remove_project(self, path: str) -> None:
        """May raise exception."""

        abs_path = os.path.abspath(path)
        for project in self._projects:
            match_path = os.path.abspath(project.get_root_path())
            if abs_path == match_path:
                self._projects.remove(project)
                return
        raise ProjectDoesntExistError()
