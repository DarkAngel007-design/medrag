# Development Guide

**Project:** MedRAG
**Version:** 1.0
**Status:** Sprint 0 – Complete

---

# 1. Purpose

This document describes the development workflow, coding standards, tooling, and best practices for contributing to MedRAG.

The primary goals are:

* Consistent development practices
* High code quality
* Reproducible environments
* Efficient onboarding
* Maintainable codebase

---

# 2. Development Philosophy

MedRAG follows these engineering principles:

* Build incrementally.
* Keep architecture modular.
* Write code that is easy to replace.
* Optimize only after measuring.
* Document important decisions.
* Favor readability over cleverness.

---

# 3. Prerequisites

Required software:

* Python 3.12+
* `uv`
* Git
* Docker
* Docker Compose
* Node.js (LTS)
* VS Code (recommended)

---

# 4. Initial Setup

```bash
git clone <repository-url>

cd medrag

uv sync
```

Create environment variables:

```bash
cp .env.example .env
```

---

# 5. Repository Structure

```text
docs/
src/
tests/
configs/
scripts/
docker/
data/
```

Only add new top-level directories when justified.

---

# 6. Coding Standards

## Formatting

* Black

## Linting

* Ruff

## Type Checking

* mypy

## Documentation

* Google-style docstrings
* Type hints on all public APIs

---

# 7. Naming Conventions

Files

```text
snake_case.py
```

Classes

```text
PascalCase
```

Functions

```text
snake_case()
```

Constants

```text
UPPER_CASE
```

Private methods

```text
_private_method()
```

---

# 8. Git Workflow

Branches:

```text
main
develop
feature/*
bugfix/*
docs/*
experiment/*
```

---

# 9. Commit Convention

Use Conventional Commits.

Examples:

```text
feat(retrieval): add hybrid retriever

fix(chunking): handle empty documents

docs(api): update endpoint specification

test(reranker): add latency benchmark
```

---

# 10. Development Workflow

Every feature should follow:

```text
Plan
↓

Implement
↓

Unit Tests
↓

Integration Tests
↓

Run Locally
↓

Lint
↓

Type Check
↓

Commit
```

---

# 11. Testing

Before every commit:

* Unit tests pass
* Integration tests pass (if affected)
* No lint errors
* No type errors

---

# 12. Pull Requests

Every PR should include:

* Description
* Motivation
* Test summary
* Documentation updates
* Related issue (if any)

---

# 13. Error Handling

* Never silently ignore exceptions.
* Use meaningful custom exceptions.
* Log unexpected failures.
* Return consistent API errors.

---

# 14. Logging

Use structured logging.

Every request should include:

* Request ID
* Timestamp
* Latency
* Service name
* Log level

---

# 15. Configuration

Configuration must come from:

* Environment variables
* Configuration files

Never hardcode:

* Secrets
* API keys
* Paths
* URLs

---

# 16. Code Review Checklist

Before merging:

* Code is readable.
* Architecture respected.
* Tests added.
* Documentation updated.
* No duplicated logic.
* Public interfaces typed.
* Error handling included.

---

# 17. Definition of Ready

A task is ready when:

* Requirements are understood.
* Dependencies are identified.
* Acceptance criteria are defined.

---

# 18. Definition of Done

A task is complete when:

* Implementation finished
* Tests passing
* Lint passing
* Type checks passing
* Documentation updated
* Code reviewed

---

# 19. Continuous Improvement

Refactoring is encouraged when it improves:

* Readability
* Maintainability
* Testability
* Performance (when measured)

Avoid unnecessary abstraction.

---

# 20. Summary

The development process emphasizes quality, consistency, and incremental improvement. Every contribution should leave the codebase cleaner, more maintainable, and better documented than before.
