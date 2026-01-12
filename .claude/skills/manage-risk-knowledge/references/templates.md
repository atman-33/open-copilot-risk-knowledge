# Templates for Risk Knowledge Files

Use these templates when creating new files. Follow the structure exactly.

## spec.md Template

```markdown
# [Domain Name] Domain Specification

## Overview

[1-2 sentences describing this domain's purpose and scope]

## Core Components

### 1. [Component Name]

- [Key point about the component]
- [Another key point]

### 2. [Component Name]

- [Key point about the component]

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/... | POST | ... |
| /api/... | GET | ... |

## Dependencies

- [External service or system]
- [Database or storage]
```

## risks.md Template

```markdown
# [Domain Name] Domain Risks

Risks specific to the [domain name] system's architecture and implementation.

## 1. [Risk Name]

- **Details**: [What can go wrong and why]
- **Countermeasures**:
  - [Mitigation step 1]
  - [Mitigation step 2]
- **Severity**: [Critical/High/Medium/Low]
- **Related Incident**: `incidents/YYYY-incident-name.md` (if applicable)

## 2. [Risk Name]

- **Details**: [What can go wrong and why]
- **Countermeasures**:
  - [Mitigation step 1]
- **Severity**: [Critical/High/Medium/Low]
```

## incidents/ File Template

```markdown
# Incident: [Short Descriptive Title]

## Summary

- **Date**: YYYY-MM-DD
- **Duration**: X hours (HH:MM - HH:MM TZ)
- **Severity**: [Critical/High/Medium/Low]
- **Affected Users**: [Number or percentage]

## Incident Description

[2-3 sentences describing what happened from user perspective]

## Root Cause

[Technical explanation of why this happened]

## Timeline

| Time | Event |
|------|-------|
| HH:MM | [Event description] |
| HH:MM | [Event description] |

## Impact

- [Business impact 1]
- [Business impact 2]

## Lessons Learned

1. [Key takeaway 1]
2. [Key takeaway 2]

## Related Risks

- `domains/[domain]/risks.md` - [Risk name]
- `common-risks/[category].md` - [Risk name]

## Action Items

- [ ] [Action 1]
- [ ] [Action 2]
```

## knowledge-map.yml Entry Template

```yaml
  - domain_name: "[Domain Name in Japanese] ([English Name])"
    description: "[What this domain covers]"
    keywords:
      - "keyword1"
      - "keyword2"
      - "keyword3"
    related_files:
      common_risks:
        - "common-risks/[relevant].md"
      domain_knowledge:
        - "domains/[domain-name]/spec.md"
        - "domains/[domain-name]/risks.md"
```
