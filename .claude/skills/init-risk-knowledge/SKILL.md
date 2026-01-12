---
name: init-risk-knowledge
description: Initialize the risk knowledge base repository by removing sample data and creating a clean structure. Use when setting up this repository for a new project. Creates .examples/ directory with sample files for reference while cleaning the main structure. This is a one-time operation for initial project setup.
---

# Initialize Risk Knowledge Repository

One-time initialization script to prepare the risk knowledge base for a new project by archiving sample data and creating a clean structure.

## When to Use

- **Initial project setup**: When forking or cloning this repository for a new project
- **Starting fresh**: When you want to replace all sample data with your own content
- **Clean slate**: After reviewing examples and ready to build your own knowledge base

**NOT for**:
- Cleaning up test data in an active project (use git/manual deletion)
- Resetting after adding your own content (not reversible)
- Multiple executions (runs only once)

## What It Does

### Archives Sample Data

Moves sample content to `.examples/` directory for reference:

```
domains/auth/               → .examples/domains/auth/
domains/payment/            → .examples/domains/payment/
domains/batch-processing/   → .examples/domains/batch-processing/
incidents/*.md              → .examples/incidents/*.md
```

### Cleans Main Structure

- **domains/**: Becomes empty directory
- **incidents/**: Becomes empty directory
- **common-risks/*.md**: Templates with headings only
- **indexes/knowledge-map.yml**: Reset to empty definitions list

### Preserves

- `.claude/skills/`: All management skills
- `.github/`: Copilot configuration
- `README.md`: Documentation
- `.examples/`: Created with archived samples

## Usage

### Basic Usage

```bash
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py
```

Interactive mode with confirmation prompt.

### Advanced Options

```bash
# Skip confirmation prompt
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py --force

# Dry run (show what would happen)
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py --dry-run
```

## Script Workflow

1. **Pre-check**: Verify `.examples/` doesn't exist (prevent multiple runs)
2. **Inventory**: List all files to be archived
3. **Confirmation**: Ask user to proceed (unless `--force`)
4. **Archive**: Move samples to `.examples/`
5. **Clean**: Empty `domains/` and `incidents/`
6. **Template**: Replace `common-risks/` content with structure only
7. **Reset**: Initialize `knowledge-map.yml` with empty list
8. **Validate**: Run validation to ensure clean state
9. **Guide**: Display next steps

## After Initialization

The script displays guidance for next steps:

```
✓ Repository initialized successfully!

Samples archived to .examples/ directory.

Next steps:
1. Review examples: ls -la .examples/
2. Add your first domain: python3 .claude/skills/manage-risk-knowledge/scripts/add_domain.py
3. Customize common-risks/ for your project
4. Update README.md with project-specific information

Resources:
- Templates: .claude/skills/manage-risk-knowledge/references/templates.md
- Examples: .examples/
- Management: .claude/skills/manage-risk-knowledge/SKILL.md
```

## Safety Features

### Single Execution

Script exits with error if `.examples/` already exists:

```
ERROR: .examples/ directory already exists.
This script is for initial setup only and has already been run.

If you want to reset completely, delete .examples/ first (NOT recommended).
For ongoing maintenance, use git or manual file management.
```

### Validation

Runs `validate_knowledge.py` after initialization to ensure clean state.

### Dry Run

Use `--dry-run` to preview changes without modifying files.

## Common-Risks Templates

Each common risk file is templated with this structure:

```markdown
# Security Risks

Cross-cutting security risk patterns applicable to all domains.

## 1. SQL Injection

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## 2. (Add Risk Name)

**Risk**:
(Add description here)
...
```

Users can edit these templates directly or reference `.examples/common-risks/` for ideas.

## Knowledge Map Reset

`indexes/knowledge-map.yml` is reset to:

```yaml
# Copilot Knowledge Map
# Define keyword-based routing for domains

definitions: []

# Example entry:
# - domain_name: "Your Domain Name"
#   description: "Brief description"
#   keywords:
#     - "keyword1"
#     - "keyword2"
#   related_files:
#     common_risks:
#       - "common-risks/security.md"
#     domain_knowledge:
#       - "domains/your-domain/spec.md"
#       - "domains/your-domain/risks.md"
```

## Troubleshooting

### Already Initialized

If you see the error about `.examples/` existing:

**Option 1 (Recommended)**: Keep current state and manage with git
```bash
# Add your content normally
python3 .claude/skills/manage-risk-knowledge/scripts/add_domain.py
```

**Option 2 (Destructive)**: Complete reset
```bash
# Backup if needed
cp -r .examples .examples.backup
# Remove and re-run
rm -rf .examples
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py
```

### Validation Errors

If validation fails after initialization, check:
- File permissions
- Disk space
- YAML syntax in knowledge-map.yml

Run validation manually:
```bash
python3 .claude/skills/manage-risk-knowledge/scripts/validate_knowledge.py
```

## References

- Detailed guide: `references/initialization-guide.md`
- Management skill: `../manage-risk-knowledge/SKILL.md`
- Templates: `../manage-risk-knowledge/references/templates.md`
