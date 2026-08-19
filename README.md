# AgentForge Shared

`agentforge-shared` is the common foundation repository of **AgentForge**. It contains shared functionality and reusable components used across the AgentForge multi-repository architecture.

> **Project status:** `agentforge-shared` is **COMPLETE and VERIFIED** as of **17 August 2026**.

## Overview

AgentForge is organized as a multi-repository platform:

```text
AgentForge
├── agentforge-backend
├── agentforge-frontend
├── agentforge-agents
├── agentforge-ai-services
├── agentforge-integrations
├── agentforge-docs
├── agentforge-infra
└── agentforge-shared
```

The purpose of the shared repository is to provide common functionality that can be reused by the other AgentForge repositories instead of duplicating the same implementation in each service.

Conceptually:

```text
                    AgentForge Shared
                         / | \
                        /  |  \
                       v   v   v
                 Backend Agents
                    AI Services
                  Integrations
```

## Repository Status

The repository completed its verification cycle successfully.

| Verification | Result |
|---|---|
| Automated tests | ✅ 11/11 passed |
| Editable package installation | ✅ Passed |
| Package/import verification | ✅ Passed |
| Dependency verification | ✅ `pip check` clean |
| Datetime deprecation warnings | ✅ Resolved and verified |
| Repository status | ✅ COMPLETE |

The repository should be treated as a completed foundation component unless a new requirement or regression appears.

## Installation

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the package in editable mode:

```powershell
pip install -e .
```

Editable package installation and import verification were successfully completed during the repository verification.

## Dependency Verification

Check installed dependencies with:

```powershell
pip check
```

Verified result:

```text
No broken requirements found
```

## Testing

Run the complete test suite:

```powershell
pytest -q
```

Verified result:

```text
11 passed
```

The full available automated test suite passed during the completion verification.

## Python Compilation

Where applicable, verify the source tree with:

```powershell
python -m compileall src
```

Use the repository's current source structure as the source of truth for the exact package layout.

## Package and Import Verification

The package and its shared modules were verified after editable installation.

The verification confirmed that the shared package can be imported successfully and that its reusable components are available to the other AgentForge repositories.

## Datetime Deprecation Fixes

The repository previously contained datetime deprecation warnings.

Those warnings were resolved and the updated implementation was verified during the completion cycle.

The repository should therefore not be reverted to the previous deprecated datetime behavior.

## Role in AgentForge

The shared repository provides the common foundation for the wider platform.

The intended separation is:

```text
agentforge-shared
       |
       +--------------------+
       |                    |
       v                    v
agentforge-backend    agentforge-agents
       |
       +--------------------+
       |
       v
Other AgentForge services
```

The shared layer should contain functionality that genuinely belongs across repository boundaries.

Repository-specific business logic should remain in the repository that owns that functionality.

## Development Guidelines

### Reuse shared functionality

Before adding a common utility, schema, helper, or foundation component to another AgentForge repository, check whether an equivalent capability already belongs in `agentforge-shared`.

### Avoid repository-specific business logic

The shared repository should remain broadly reusable.

Avoid adding functionality that is tightly coupled to:

- a single API endpoint,
- one specific agent,
- one frontend screen,
- one external integration,
- or one deployment environment.

### Preserve compatibility

Changes to shared code can affect multiple repositories.

After modifying shared functionality, run the complete test suite and verify downstream imports where applicable.

## Recommended Development Verification

After making a change, use:

```powershell
pip install -e .
pip check
pytest -q
```

Where relevant, also verify compilation:

```powershell
python -m compileall src
```

## Troubleshooting

### Package cannot be imported

Reinstall the repository in editable mode:

```powershell
pip install -e .
```

Then verify:

```powershell
python -c "import agentforge_shared"
```

Use the actual package import name defined by the repository if it differs.

### Dependency errors

Run:

```powershell
pip check
```

If broken requirements are reported, install/update dependencies according to the repository's package configuration.

### Tests fail after a shared change

Run the complete suite:

```powershell
pytest -q
```

Because shared code may be consumed by multiple repositories, avoid validating only a single test unless debugging a specific failure.

## Verification Standard

The shared repository was marked complete after the relevant checks succeeded:

```text
Source
  ↓
Editable installation
  ↓
Package/import verification
  ↓
Dependency verification
  ↓
Automated tests
  ↓
Datetime warning cleanup
  ↓
COMPLETE
```

## Completed Verification Details

### Automated tests

```text
11 / 11 passed
```

### Package installation

Editable installation completed successfully:

```powershell
pip install -e .
```

### Dependency health

```powershell
pip check
```

Result:

```text
No broken requirements found
```

### Import verification

Package and shared component imports were successfully verified.

### Warning cleanup

Previous datetime deprecation warnings were resolved and verified.

## AgentForge Repository Completion Status

As of 19 August 2026:

```text
agentforge-shared          ✅ COMPLETE
agentforge-ai-services    ✅ COMPLETE
agentforge-agents         ✅ COMPLETE
agentforge-integrations   ✅ COMPLETE
agentforge-backend        ✅ COMPLETE
agentforge-frontend       ⏳ PENDING
agentforge-docs           ⏳ PENDING
agentforge-infra          ⏳ PENDING
```

## Completion Record

`agentforge-shared` was completed by **Ajay**.

The completion milestone included:

- 11/11 automated tests passing
- Editable package installation
- Package/import verification
- Dependency verification
- Resolution and verification of datetime deprecation warnings

## Next Work

`agentforge-shared` should now be treated as a verified foundation.

Do not reopen the repository for routine changes unless:

- a regression is discovered,
- a shared requirement changes,
- another AgentForge repository needs a new reusable capability, or
- a compatibility issue is identified.

When shared functionality is changed, rerun the full verification suite because downstream repositories may depend on it.

---

**AgentForge Shared — Completed and verified by Ajay**  
**Status: COMPLETE**  
**Last updated: 19 August 2026**
