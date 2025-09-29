# AGENT.md

## Architectural Overview

This project is a Django-based web application, organized for clarity, modularity, and maintainability. The architecture follows Django best practices, with each app encapsulating a distinct domain of functionality. The `politics` app is a prime example, providing a self-contained quiz and scoring system with clear separation of models, views, utilities, and tests.

**Django apps, when created, should be placed in the `prodigius/apps` folder.** This keeps the project organized and makes it easy to locate all feature-specific Django apps in one place.

### Key Architectural Guidelines

- **App Modularity:**
  - Each Django app (e.g., `politics`) is responsible for a single domain or feature set.
  - Apps contain their own models, views, templates, admin, tests, and utility logic.

- **Separation of Concerns:**
  - Business logic (e.g., scoring algorithms) is placed in `utils.py` or similar utility modules, not in views or models.
  - Views are kept thin, delegating computation and data manipulation to utilities or models.

- **Data Modeling:**
  - Models are designed to be explicit and normalized, with clear relationships and constraints (e.g., `unique_together`).
  - Use of Django's built-in field types and features (e.g., `JSONField`, `ForeignKey`, `Meta.ordering`).

- **Admin Customization:**
  - The Django admin is configured for each model to improve usability for content managers (e.g., list display, ordering, search fields).

- **URL Routing:**
  - Each app defines its own `urls.py` for encapsulated routing.
  - Use of class-based views for clarity and reusability.

- **Templates:**
  - Templates are organized by app and view, with partials for reusable components.
  - Context data is passed explicitly from views.

- **Fixtures:**
  - Initial data (e.g., questions, choices) is provided via JSON fixtures for easy loading and reproducibility.

- **Static Assets:**
  - Static files (CSS, JS, images) are organized under `static/` and `staticfiles/` for development and production use.
  - Tailwind CSS is used for styling, with a build process managed via npm scripts.

- **Configuration:**
  - Project configuration is managed via `pyproject.toml` (for dependencies and tooling) and Django settings modules.
  - Environment variables are handled with `django-environ`.

- **Code Quality:**
  - Formatting is enforced with Black (`pyproject.toml` config).
  - Linting is performed with Flake8.
  - Pre-commit hooks are set up for consistent code style and quality.

## Unit Testing

- **Test Structure:**
  - Each app contains a `tests/` directory with test modules for views, utilities, and models.
  - Tests use Django's `TestCase` and `RequestFactory` for database and view testing.
  - In-memory templates are used in tests to avoid filesystem dependencies and speed up test runs.

- **Coverage:**
  - Views, utility functions, and model logic are all covered by unit tests.
  - Edge cases, empty states, and error handling are explicitly tested.

- **Tools:**
  - Test discovery and execution is handled by Django's test runner.
  - Coverage measurement is available via the `coverage` package (see `pyproject.toml`).

- **Best Practices:**
  - Tests are isolated, repeatable, and do not depend on external state.
  - Test data is created in `setUpTestData` or within individual tests.
  - Clean-up is handled automatically by Django's test framework.

## Adding Features, Fixes, or Enhancements

- **Follow the App Structure:**
  - Place new models, views, and logic in the appropriate app.
  - Add or update tests in the app's `tests/` directory.

- **Write and Run Tests:**
  - Ensure all new code is covered by unit tests.
  - Run the full test suite before committing changes.

- **Maintain Code Quality:**
  - Format code with Black and check with Flake8 before submitting changes.
  - Use pre-commit hooks to automate checks.

- **Document Changes:**
  - Update or add docstrings and comments as needed.
  - If architectural changes are made, update this `AGENT.md` file.

- **Respect Existing Patterns:**
  - Reuse existing utilities and patterns where possible.
  - Keep views thin and business logic in utilities or models.

## Environment & Tooling

- **Python 3.12+**
- **Django 5.2+**
- **Poetry** for dependency management
- **Black** for formatting
- **Flake8** for linting
- **Pre-commit** for code quality automation
- **Tailwind CSS** for styling (managed via npm)
- **htmx** for modern, dynamic HTML interactions (progressive enhancement)
- **Alpine.js** for lightweight frontend reactivity
- **PostgreSQL** as the primary database backend

This file is intended for future AI agents and developers to understand the architectural intent, best practices, and testing philosophy of this project. Always strive for clarity, modularity, and testability in all changes.
