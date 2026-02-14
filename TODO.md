# Project Improvement To-Do List

This document tracks all planned improvements for the `musicli` project, focusing on code quality, UI/UX, documentation, output management, and testing. Each item is actionable and will be checked off as completed.

---

## 1. Code & Structure

- [x] Refactor code for clarity, modularity, and maintainability
- [x] Move all output (e.g., tier list files) to a dedicated `output/` directory
- [x] Improve error handling and user feedback
- [x] Ensure all functions and classes are well-documented (docstrings, comments)
- [x] Remove or refactor any unused or unclear features

## 2. UI/UX (Terminal)

- [x] Enhance terminal output: use colors, tables, and clear prompts
- [x] Explore and utilize features in packages like `rich`, `click`, or `prompt_toolkit` for better CLI design
- [x] Add progress bars, spinners, or interactive elements where appropriate
- [x] Make prompts and outputs more user-friendly and visually appealing

## 3. Testing

- [x] Add comprehensive unit tests for all modules and functions
- [x] Ensure tests cover edge cases and error handling
- [x] Use `pytest` for test discovery and reporting
- [x] Add test cases for CLI interactions (if possible)

## 4. Documentation & Marketing

- [x] Rewrite `README.md` to:
  - [x] Clearly explain features, usage, and installation
  - [x] Add usage examples, screenshots, and badges
  - [x] Highlight unique selling points and marketing copy
  - [x] Document all commands, options, and configuration
- [x] Add or update docstrings and inline comments throughout the codebase
- [x] Create or update API documentation in `docs/`

## 5. Project Management

- [x] Create this `to-do.md` with a prioritized list of improvements
- [x] Track progress and future ideas in this file

## 6. Output Management

- [x] Ensure all generated files (e.g., tier lists) are saved in an `output/` directory
- [x] Create the `output/` directory if it doesn’t exist

## 7. Package & Dependency Review

- [x] Review `requirements.txt` and `pyproject.toml` for outdated or unused packages
- [x] Check for new features in terminal UI packages and suggest upgrades

---

### Notes

- This list will be updated as improvements are made or new ideas arise.
- Focus is on code quality, usability, and maintainability—no new features unless they improve existing functionality or user experience.
