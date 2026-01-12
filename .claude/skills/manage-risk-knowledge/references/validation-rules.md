# Validation Rules

Apply these checks when adding or updating knowledge files.

## Automatic Checks (Block if violated)

### Domain Name Uniqueness
- Check `domains/` directory for existing folder with same name
- Check `indexes/knowledge-map.yml` for duplicate `domain_name`

### Keyword Uniqueness
- Check `indexes/knowledge-map.yml` for exact duplicate keywords
- Each keyword should map to only one domain

### File Path Integrity
- All paths in `related_files` must exist
- All `Related Incident` references in risks.md must exist
- All `Related Risks` references in incidents/ must exist

### Required Fields
- spec.md: Must have `## Overview` and `## Core Components`
- risks.md: Each risk must have `**Details**` and `**Countermeasures**`
- incidents/: Must have `## Summary`, `## Root Cause`, `## Related Risks`

## Warning Checks (Prompt user for confirmation)

### Similar Keywords
Warn if new keyword is similar to existing:
- "auth" vs "authentication"
- "login" vs "signin"
- "payment" vs "payments"

Prompt: "Similar keyword '[existing]' exists for [domain]. Merge or keep separate?"

### Duplicate Risk Patterns
Warn if new risk description contains 50%+ overlap with existing risk.

Prompt: "Similar risk exists in [file]. Reference it or create new?"

### Missing Incident Link
Warn if risk has `Severity: Critical` but no `Related Incident`.

Prompt: "Critical risk without incident history. Add incident reference?"

### Orphan Incidents
After adding incident, check if any related risks reference it.

Prompt: "Update [risks.md] to reference this incident?"
