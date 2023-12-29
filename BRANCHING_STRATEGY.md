# Solo Git Branching Strategy

## Branches Overview

- `main`: The branch that reflects the stable, production-ready state of your project.
- `dev`: A branch for testing and finalizing before merging into `main`.
- `feature`: A dedicated, long-lived branch for ongoing development.

## Workflow Details

### Ongoing Development:
- All development work happens in the `feature` branch. Commit all changes to this branch as you work.

### Integration and Testing:
- Periodically merge `feature` into `dev` to prepare for a stable release. This is where you'll test everything together.

### Releasing:
- Once you're satisfied with the stability and performance in the `dev` branch, merge `dev` into `main` for a new release.

### Maintenance:
- If you need to make critical hotfixes directly to production, commit these to `main` and then merge `main` back into both `dev` and `feature` to keep everything in sync.

## Simplified Instructions

1. Perform all new development in the `feature` branch.
2. Merge `feature` into `dev` for combined testing when approaching a release.
3. After testing in `dev`, merge into `main` for a stable release version.
4. Optionally, tag your releases on `main` for historical reference (e.g., `git tag v1.0.1`).
