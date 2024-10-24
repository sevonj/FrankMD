# Markdown Editor
[![CI](https://github.com/sevonj/FrankMD/actions/workflows/ci.yml/badge.svg)](https://github.com/sevonj/FrankMD/actions/workflows/ci.yml)

Working title FrankMD, named after Frank the snake, because python.

A description of this project.


## Development
[➜ Project management](https://github.com/users/sevonj/projects/15)

Check out the linked project for an organized overview of issues.

### Requirements
- `PyGObject`
- `PyGObject-stubs`
- Todo...

### Build

### Continuous Integration
Pull requests are gatekept by [this workflow.](https://github.com/sevonj/frankmd/blob/master/.github/workflows/ci.yml) It will check if
- The code passes tests (run `pytest` at project root)
- Linter has complaints (run `ruff check` at project root)
- Is formatted
  - (run `black .` at project root to format)
  - (run `black --check .` at project root to just check)

### Dev FAQ:
#### Pylint no member but code works
https://stackoverflow.com/a/77435230

Adapt to your IDE.
