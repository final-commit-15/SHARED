# AgentForge Shared

Common language for all AgentForge services.

## Purpose

This repository holds only the **shared, cross‑service** definitions:

- **Schemas** – Pydantic models for agents, executions, users, etc.
- **Enums** – statuses and types used everywhere.
- **Constants** – API version, default limits, timeouts.
- **Exceptions** – standardised error hierarchy.
- **Utilities** – ID generation, datetime helpers, pagination.

**No business logic, no database code, no service‑specific configuration.**

## Installation

```bash
pip install git+https://github.com/final-commit-15/SHARED