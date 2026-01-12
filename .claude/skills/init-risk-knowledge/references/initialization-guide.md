# Repository Initialization Guide

Detailed guide for initializing the risk knowledge base repository for a new project.

## Purpose

This script is designed for **one-time use** when setting up this repository for a new project. It:

1. Preserves sample data as reference material
2. Creates a clean working structure
3. Provides templates for customization
4. Ensures valid initial state

## Pre-Initialization Checklist

Before running the initialization script:

- [ ] Review sample data in `domains/`, `incidents/`, and `common-risks/`
- [ ] Understand the repository structure
- [ ] Read the main README.md
- [ ] Backup if needed (though samples are preserved in `.examples/`)
- [ ] Ensure you have Python 3.8+ and PyYAML installed

## Initialization Process

### Step 1: Review Current Content

```bash
# See what domains exist
ls -la domains/

# See what incidents exist
ls -la incidents/

# See common risks
ls -la common-risks/
```

### Step 2: Run Initialization

**Recommended (with confirmation)**:
```bash
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py
```

**Preview changes first**:
```bash
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py --dry-run
```

**Skip confirmation** (if you're sure):
```bash
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py --force
```

### Step 3: Verify Results

After initialization:

```bash
# Check archived samples
ls -la .examples/domains/
ls -la .examples/incidents/
ls -la .examples/common-risks/

# Verify clean structure
ls -la domains/          # Should be empty
ls -la incidents/        # Should be empty
cat indexes/knowledge-map.yml  # Should have empty definitions: []

# Check templates
cat common-risks/security.md
cat common-risks/performance.md
cat common-risks/availability.md
```

## What Gets Modified

### Archived to .examples/

| Original Location | Archived Location |
|-------------------|-------------------|
| `domains/auth/` | `.examples/domains/auth/` |
| `domains/payment/` | `.examples/domains/payment/` |
| `domains/batch-processing/` | `.examples/domains/batch-processing/` |
| `incidents/2023-login-failure.md` | `.examples/incidents/2023-login-failure.md` |
| `incidents/2024-data-leak-api.md` | `.examples/incidents/2024-data-leak-api.md` |
| `common-risks/*.md` | `.examples/common-risks/*.md` (copy for reference) |

### Cleaned

- `domains/`: All subdirectories removed → empty
- `incidents/`: All .md files removed → empty

### Templated

- `common-risks/security.md`: Replaced with template structure
- `common-risks/performance.md`: Replaced with template structure
- `common-risks/availability.md`: Replaced with template structure

### Reset

- `indexes/knowledge-map.yml`: Reset to empty `definitions: []` with example comment

### Preserved (Unchanged)

- `.claude/skills/`: All skills remain intact
- `.github/`: Copilot configuration unchanged
- `README.md`: Documentation unchanged
- `.gitignore`: Version control settings unchanged

## Post-Initialization Workflow

### 1. Customize Common Risks

Edit the templated files to match your project's risk profile:

```bash
# Edit each file
code common-risks/security.md
code common-risks/performance.md
code common-risks/availability.md
```

Reference `.examples/common-risks/` for ideas.

### 2. Add Your First Domain

Use the interactive script:

```bash
python3 .claude/skills/manage-risk-knowledge/scripts/add_domain.py
```

Or reference `.examples/domains/` for structure.

### 3. Update Knowledge Map

The `add_domain.py` script updates this automatically, but you can also edit manually:

```bash
code indexes/knowledge-map.yml
```

### 4. Add Incidents (As They Occur)

When incidents happen in your project:

```bash
# Create incident file
code incidents/YYYY-description.md

# Link to related risks
code domains/{affected-domain}/risks.md
```

Reference `.examples/incidents/` for format.

## Common Scenarios

### Scenario 1: "I want to keep one sample domain"

Before running init script:

```bash
# Copy the domain you want to keep
cp -r domains/auth domains/my-auth

# Run initialization
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py

# Your copy will be in .examples/, you can reference it
```

### Scenario 2: "I accidentally ran it twice"

The script prevents this by checking for `.examples/` existence. If you see the error:

```
ERROR: .examples/ directory already exists.
```

This is intentional protection. Your repository is already initialized.

### Scenario 3: "I want to completely reset"

**Warning: This is destructive**

```bash
# Backup current work
git commit -am "Backup before reset"

# Remove examples directory
rm -rf .examples/

# Re-run initialization
python3 .claude/skills/init-risk-knowledge/scripts/init_repository.py
```

### Scenario 4: "Validation failed after initialization"

Check the error messages from the validation script:

```bash
# Run validation manually
python3 .claude/skills/manage-risk-knowledge/scripts/validate_knowledge.py

# Common issues:
# - YAML syntax error in knowledge-map.yml
# - File permission issues
# - Disk space issues
```

## Troubleshooting

### Error: "No module named 'yaml'"

Install PyYAML:

```bash
pip install pyyaml
```

Or:

```bash
pip install -r .claude/skills/manage-risk-knowledge/scripts/requirements.txt
```

### Error: "Permission denied"

Ensure you have write permissions:

```bash
ls -la domains/
ls -la incidents/
```

If needed:

```bash
chmod -R u+w domains/ incidents/ common-risks/ indexes/
```

### Error: "Validation failed"

Review validation output:

```bash
python3 .claude/skills/manage-risk-knowledge/scripts/validate_knowledge.py
```

Common fixes:
- Check YAML syntax in knowledge-map.yml
- Ensure all directories exist
- Verify file encodings (should be UTF-8)

## Best Practices

### Before Initialization

1. **Read the documentation**: Understand what the script does
2. **Review samples**: Learn from existing examples
3. **Plan your structure**: Think about your domains and risks
4. **Backup if concerned**: Though samples are preserved

### During Initialization

1. **Use dry-run first**: Preview changes
2. **Review the summary**: Check what will be modified
3. **Proceed with confidence**: Samples are preserved in `.examples/`

### After Initialization

1. **Verify immediately**: Check that structure is as expected
2. **Start small**: Add one domain first
3. **Test validation**: Ensure everything works
4. **Commit to git**: Version control your clean state

## Integration with Other Tools

### Git Workflow

```bash
# After initialization
git status
git add .
git commit -m "Initialize repository for [project-name]"

# Create a clean state branch (optional)
git checkout -b clean-init
```

### CI/CD Integration

Add validation to your CI pipeline:

```yaml
# .github/workflows/validate.yml
- name: Validate Knowledge Base
  run: |
    pip install pyyaml
    python3 .claude/skills/manage-risk-knowledge/scripts/validate_knowledge.py
```

### Documentation

Update your project-specific README sections after initialization:

- Replace generic examples with your domain names
- Update team contacts and maintainers
- Add project-specific best practices

## Reference

- Main skill: `../SKILL.md`
- Management skill: `../../manage-risk-knowledge/SKILL.md`
- Templates: `../../manage-risk-knowledge/references/templates.md`
- Sample domains: `.examples/domains/`
- Sample incidents: `.examples/incidents/`
