---
name: manage-risk-knowledge
description: Manage the risk knowledge base repository for Copilot-driven risk assessment. Use when adding new domains (features), recording incidents, updating risks, or modifying the knowledge-map index. Triggers on requests like "add domain", "record incident", "add risk", "update knowledge-map", or any task involving domains/, incidents/, common-risks/, or indexes/knowledge-map.yml.
---

# Manage Risk Knowledge

Unified skill for maintaining the risk knowledge base. Handles domain creation, incident recording, risk updates, and index synchronization.

## Repository Structure

```
├── indexes/knowledge-map.yml    # Keyword → file routing (MUST update)
├── common-risks/                # Cross-cutting risks (security, performance, availability)
├── domains/{name}/              # Domain-specific knowledge
│   ├── spec.md                  # Feature specification
│   └── risks.md                 # Domain-specific risks
└── incidents/                   # Past incident records
```

## Workflow Decision Tree

```
User Request
    │
    ├─ "Add new domain/feature" ──────► Add Domain Workflow
    │
    ├─ "Record incident" ─────────────► Add Incident Workflow
    │
    ├─ "Add/update risk" ─────────────► Update Risk Workflow
    │
    └─ "Update common risk" ──────────► Update Common Risk Workflow
```

## Add Domain Workflow

When user wants to add a new feature/domain (e.g., "notification", "search"):

1. **Validate uniqueness**
   - Check `domains/` for existing folder
   - Check `indexes/knowledge-map.yml` for duplicate domain_name or keywords

2. **Collect information** (ask if not provided)
   - Domain name (kebab-case for folder, display name for YAML)
   - Keywords (3-5 terms that should trigger this domain)
   - Brief description
   - Related common risks (security? performance? availability?)

3. **Create files** using templates from `references/templates.md`
   - `domains/{name}/spec.md`
   - `domains/{name}/risks.md`

4. **Update index** - Add entry to `indexes/knowledge-map.yml`:
   ```yaml
   - domain_name: "表示名 (English)"
     description: "..."
     keywords: [...]
     related_files:
       common_risks: [...]
       domain_knowledge:
         - "domains/{name}/spec.md"
         - "domains/{name}/risks.md"
   ```

5. **Verify** - Confirm all paths in knowledge-map.yml exist

## Add Incident Workflow

When user reports a past incident:

1. **Collect information**
   - Date, duration, severity
   - What happened (user-facing impact)
   - Root cause (technical)
   - Affected domain(s)

2. **Create incident file**
   - Filename: `incidents/YYYY-short-description.md`
   - Use template from `references/templates.md`

3. **Update related risks**
   - Add `Related Incident` link to relevant `domains/{name}/risks.md`
   - If new risk pattern, add new risk entry

4. **Bidirectional linking**
   - Incident → risks.md (in "Related Risks" section)
   - risks.md → incident (in risk entry)

## Update Risk Workflow

When adding or modifying a risk in existing domain:

1. **Locate target file**
   - Domain-specific: `domains/{name}/risks.md`
   - Cross-cutting: `common-risks/{category}.md`

2. **Check for duplicates**
   - Search existing risks for similar patterns
   - Warn if overlap detected

3. **Add/update risk entry** with required fields:
   - `**Details**`: What can go wrong
   - `**Countermeasures**`: How to prevent/mitigate
   - `**Severity**`: Critical/High/Medium/Low
   - `**Related Incident**`: Link if applicable

4. **Update knowledge-map.yml keywords** if new terms should trigger this domain

## Update Common Risk Workflow

For cross-cutting risks (security, performance, availability):

1. **Identify category** from `common-risks/`:
   - `security.md` - Injection, auth bypass, data exposure
   - `performance.md` - N+1, memory, connection exhaustion
   - `availability.md` - Service outage, login failure

2. **Add/update risk** following existing format

3. **Check domain linkage** - Ensure relevant domains reference this common risk in knowledge-map.yml

## Validation

Before completing any operation, run checks from `references/validation-rules.md`:

- **Block**: Duplicate domain/keyword, broken file paths, missing required fields
- **Warn**: Similar keywords, duplicate risk patterns, missing incident links

## References

- `references/templates.md` - File templates for spec.md, risks.md, incidents/
- `references/validation-rules.md` - Validation rules and checks
