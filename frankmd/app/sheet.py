import os
from typing import Self


class Sheet:
    """A markdown file"""

    __slots__ = ("_path",)

    def __init__(self, file_path: str):
        self._path: str = file_path

    def __lt__(self, other: Self) -> bool:
        return self._path < other._path

    def get_path(self) -> str:
        return self._path

    def get_display_name(self) -> str:
        return os.path.basename(self._path)

    def get_display_stub(self) -> str:
        """Get a short excerpt from the beginning."""

        max_w = 30  # + ellipsis ("...")

        try:
            with open(self._path, "r", encoding="utf-8") as f:
                lines = []
                line = ""
                for _ in range(100):
                    c = f.read(1)

                    if not c:
                        line = line.strip()
                        lines.append(line)
                        break

                    if c == "\n" or len(line) == max_w:
                        line = line.strip()
                        if line:
                            lines.append(line)
                        if len(lines) == 3:
                            break
                        line = ""
                        if c.strip():
                            line += c
                    else:
                        line += c

                if f.read(1):
                    lines[-1] += "..."

            return "\n".join(lines)

        except:  # pylint: disable=bare-except
            return "(Couldn't open file)"

    def load(self) -> str:
        return "TODO"

    def save(self, _content: str) -> None:
        return
