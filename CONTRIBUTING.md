# Contributing to BloxAPI

Thank you for your interest in contributing to BloxAPI! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)
- [Community](#community)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Add the upstream repository** as a remote:
   ```bash
   git remote add upstream https://github.com/your-username/bloxapi.git
   ```
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip
- git

### Installation

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. **Update your main branch**:
   ```bash
   git checkout main
   git pull upstream main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** and commit them following the [commit message guidelines](#commit-messages)

4. **Test your changes** locally (see [Testing](#testing))

5. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a pull request** from your fork to the upstream repository

## Pull Request Process

1. Ensure your code follows the project's [coding standards](#coding-standards)
2. Update documentation as needed
3. Include tests for new features or bug fixes
4. Ensure the test suite passes
5. Fill out the pull request template with all required information
6. Request a review from maintainers
7. Address any feedback from reviewers

### Commit Messages

We follow conventional commits for our commit messages:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types include:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or correcting tests
- `chore`: Changes to the build process or auxiliary tools

Example:
```
feat(users): add ability to search users by display name

- Added new parameter to search endpoint
- Updated documentation
- Added tests

Closes #123
```

## Coding Standards

We use several tools to enforce coding standards:

- **flake8** for linting
- **black** for code formatting
- **isort** for import sorting
- **mypy** for type checking

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards
- Use type hints for all function parameters and return values
- Document all public functions, classes, and methods with docstrings
- Keep lines under 100 characters
- Use meaningful variable and function names

## Testing

We use pytest for testing. To run the tests:

```bash
pytest
```

For coverage information:

```bash
pytest --cov=bloxapi
```

### Writing Tests

- Write unit tests for all new functionality
- Aim for high test coverage (>90%)
- Use meaningful test names that describe what's being tested
- Structure tests into classes for related functionality
- Use fixtures and parameterized tests where appropriate

## Documentation

- Update documentation for all new features and changes
- Document all public APIs
- Include examples for complex functionality
- Keep the README up to date
- Add/update docstrings for all classes and functions

## Issue Reporting

When reporting issues, please use the issue templates provided and include as much detail as possible:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- System information (OS, Python version, etc.)
- Any relevant logs or error messages

## Feature Requests

Feature requests are welcome. Please use the feature request template and provide:

- A clear description of the feature
- The problem it would solve
- Alternative solutions you've considered
- Any relevant examples

## Community

- Join our [Discord server](https://discord.gg/bloxapi) for real-time discussions
- Follow us on Twitter: [@BloxAPI](https://twitter.com/bloxapi)
- Subscribe to our [mailing list](https://bloxapi.com/mailinglist) for important announcements

---

Thank you for contributing to BloxAPI! Your time and effort help make this project better for everyone.