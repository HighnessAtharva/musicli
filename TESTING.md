# Testing musicli

## Running All Tests

To run all tests:

    pytest tests/

## Test Coverage

- Core logic (file creation, album list, image generation)
- CLI help/usage output
- User experience improvements (album count, output messages)
- Album list and tier list logic
- Output directory and file creation

## Useful Commands

- Run all tests:

      pytest tests/

- Run a specific test file:

      pytest tests/test_musicli_core.py

- Show test summary:

      pytest --maxfail=1 --disable-warnings -v

- Run tests and show coverage (if coverage is installed):

      pytest --cov=src/musicli

## Adding More Tests

- Add new test files in the tests/ directory.
- Use pytest fixtures for setup/teardown.
- Test CLI flows, error handling, and edge cases.

## Notes

- All tests are written using pytest.
- Test output is shown in the terminal.
- See tests/README.md for more info.
