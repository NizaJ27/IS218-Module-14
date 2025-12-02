# Reflection

This reflection documents the key experiences and challenges encountered during the development and deployment of Module 11, focusing on calculation modeling, validation, and testing.

## Module 10 Foundation: User Model and CI Pipeline

- Implemented SQLAlchemy `User` model with unique constraints and `created_at` timestamp.
- Added Pydantic schemas `UserCreate` and `UserRead` to validate input and hide password details.
- Used `passlib` (bcrypt) to hash passwords and verify them.
- Wrote unit tests for hashing and schema validation and integration tests that exercise the `/users` endpoint.
- Added a GitHub Actions workflow that runs tests against Postgres and pushes a Docker image to Docker Hub (requires repository secrets to be configured).

## Module 11: Calculation Model and Factory Pattern

### Implementation Overview

This module introduced calculation modeling with SQLAlchemy and robust validation using Pydantic v2:

- **Calculation Model**: Created `Calculation` SQLAlchemy model with fields `id`, `a`, `b`, `type`, `result`, and optional `user_id` foreign key to the `users` table.
- **Enum Type**: Defined `CalculationType` enum (Add, Sub, Multiply, Divide) to enforce calculation type constraints at the database and application layers.
- **Pydantic Schemas**: Implemented `CalculationCreate` for input validation and `CalculationRead` for serializing output, ensuring type safety and preventing division by zero.
- **Factory Pattern**: Built a calculation factory in `app/operations/calculations.py` that dynamically routes to the appropriate arithmetic operation based on the calculation type.

### Key Experiences

1. **Pydantic v2 Migration**: Working with Pydantic v2 required understanding the new validation decorators (`@field_validator`, `@model_validator`) and the `mode="after"` pattern for cross-field validation. The initial attempt used `@field_validator` alone, but division-by-zero validation needed `@model_validator` to access both `type` and `b` fields after model instantiation.

2. **SQLAlchemy Enum Integration**: Using SQLAlchemy's `Enum` column type with Python's native `Enum` class required importing both `from sqlalchemy import Enum as SQLEnum` and `from enum import Enum` to avoid naming conflicts. The `CalculationType` enum inherits from both `str` and `Enum` to ensure proper JSON serialization in FastAPI responses.

3. **Factory Pattern Application**: The factory pattern (`compute_result` function) demonstrates how design patterns can simplify data layer operations. By centralizing operation routing, we reduced code duplication and made it easier to add new calculation types in the future.

4. **Foreign Key Relationships**: Adding the optional `user_id` foreign key with SQLAlchemy's `relationship` and `backref` enables future features where users can track their calculation history without breaking existing functionality.

### Challenges Faced

1. **Test Environment Setup**: Running tests locally required careful management of dependencies. The initial test runs failed because:
   - Playwright and requests were imported at the module level in `conftest.py`, causing `ModuleNotFoundError` when these packages weren't installed.
   - **Solution**: Implemented lazy imports inside fixtures to allow unit and integration tests to run without e2e dependencies.

2. **Cross-Field Validation in Pydantic v2**: Validating division by zero required checking both `type` and `b` fields together. The initial `@field_validator("b")` approach couldn't reliably access the `type` field due to field processing order.
   - **Solution**: Added a `@model_validator(mode="after")` that runs after the model is fully constructed, ensuring both fields are available for validation.

3. **Database Initialization**: Integration tests needed a clean database state between runs. The tests use SQLite by default but should work with Postgres in CI.
   - **Solution**: The `setup_db` fixture removes the SQLite file before each test run and calls `init_db()` to recreate tables, ensuring test isolation.

4. **Config Deprecation Warning**: Pydantic v2 warned that `orm_mode` should be renamed to `from_attributes` in the `Config` class.
   - **Impact**: Tests still pass but produce warnings. This should be addressed in future updates by migrating all schemas to use `from_attributes=True` in the model config.

### CI/CD Pipeline

- The existing GitHub Actions workflow from Module 10 continues to run all tests (user + calculation) against a PostgreSQL container.
- On successful test completion, the workflow builds a Docker image and pushes it to Docker Hub.
- **Configuration Required**: Ensure `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repository secrets are configured in GitHub Settings for automated deployments.

### Testing Strategy

- **Unit Tests** (`tests/unit/test_calculation.py`): Validate each arithmetic operation (Add, Sub, Multiply, Divide) through the factory pattern and verify schema validation catches invalid inputs (e.g., division by zero).
- **Integration Tests** (`tests/integration/test_calculations_integration.py`): Test database operations by creating calculation records, verifying stored results, and ensuring error handling for invalid calculation types.

### Lessons Learned

1. **Design Patterns Matter**: The factory pattern made the code more maintainable and testable. By separating operation selection from execution, we can easily mock or extend operations.

2. **Validation Layers**: Using both Pydantic validation (application layer) and SQLAlchemy enum constraints (database layer) provides defense in depth against invalid data.

3. **Test Compatibility**: Writing tests that work in multiple environments (local SQLite, CI Postgres) requires careful fixture design and environment variable handling.

4. **Dependency Management**: Properly managing test dependencies with lazy imports prevents test collection failures and makes the test suite more portable.

### Next Steps

The following improvements could be made in future modules:

- Add authentication endpoints (login, logout) with JWT token-based auth.
- Implement BREAD (Browse, Read, Edit, Add, Delete) endpoints for calculations in Module 12.
- Migrate Pydantic schemas to use `from_attributes=True` instead of deprecated `orm_mode`.
- Add database migration tooling (Alembic) for production-grade schema management.
- Implement pagination for calculation history queries.
- Add user-scoped calculation filtering so users only see their own calculations.

