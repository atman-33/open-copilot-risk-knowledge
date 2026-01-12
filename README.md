# Open Copilot Risk Knowledge

AI-driven risk assessment knowledge base for web application development. This repository enables GitHub Copilot to identify potential high-risk issues by referencing past incidents, domain-specific risks, and common security vulnerabilities.

## Overview

This repository serves as a structured knowledge base for proactive risk assessment in software development. By maintaining domain specifications, risk catalogs, and incident histories, development teams can leverage AI agents (GitHub Copilot) to:

- Identify overlooked high-risk items before implementation
- Reference past incidents during code review
- Apply domain-specific best practices
- Prevent recurring security and availability issues

## Repository Structure

```
├── .claude/
│   └── skills/
│       └── manage-risk-knowledge/    # Skill for managing this repository
│           ├── SKILL.md              # Main skill documentation
│           ├── scripts/              # Validation and utility scripts
│           └── references/           # Templates and validation rules
├── .github/
│   ├── copilot-instructions.md       # Copilot agent configuration
│   └── prompts/
│       └── risk-assessment.prompt.md # Agent behavior definition
├── common-risks/                     # Cross-cutting risk patterns
│   ├── availability.md               # Service outage risks
│   ├── performance.md                # Performance degradation risks
│   └── security.md                   # Security vulnerability patterns
├── domains/                          # Domain-specific knowledge
│   ├── auth/                         # Authentication domain
│   │   ├── spec.md                   # Feature specification
│   │   └── risks.md                  # Domain-specific risks
│   ├── payment/                      # Payment processing domain
│   │   ├── spec.md
│   │   └── risks.md
│   └── batch-processing/             # Batch job domain
│       ├── spec.md
│       └── risks.md
├── incidents/                        # Past incident records
│   ├── 2023-login-failure.md         # Login outage incident
│   └── 2024-data-leak-api.md         # Data leak incident
└── indexes/
    └── knowledge-map.yml             # Keyword-based routing configuration
```

## How It Works

### 1. Knowledge Map

The `indexes/knowledge-map.yml` file defines keyword-based routing that helps Copilot identify which knowledge files to reference based on user input.

**Example entry:**

```yaml
definitions:
  - domain_name: "認証・ログイン (Auth)"
    description: "Login, logout, session management, password handling"
    keywords:
      - "login"
      - "authentication"
      - "session"
      - "token"
    related_files:
      common_risks:
        - "common-risks/availability.md"
        - "common-risks/security.md"
      domain_knowledge:
        - "domains/auth/spec.md"
        - "domains/auth/risks.md"
```

### 2. Domain Knowledge

Each domain contains:
- **spec.md**: Feature specification and architecture overview
- **risks.md**: Domain-specific risk catalog with countermeasures

### 3. Incident Records

Past incidents are documented with:
- Summary (date, duration, severity, impact)
- Root cause analysis
- Timeline
- Related risks (bidirectional links to `domains/*/risks.md`)

### 4. Common Risks

Cross-cutting risk patterns applicable to all domains:
- **security.md**: SQL injection, XSS, authentication bypass, etc.
- **performance.md**: N+1 queries, memory leaks, connection exhaustion
- **availability.md**: Service outages, login failures

## Usage

### For Developers

When starting a new feature or refactoring existing code:

1. **Describe your work** to GitHub Copilot Chat:
   ```
   "I'm implementing a password reset feature for the login system"
   ```

2. **Receive risk assessment** based on:
   - Past incidents (e.g., `2023-login-failure.md`)
   - Domain-specific risks (e.g., `auth/risks.md`)
   - Common security patterns (e.g., `security.md`)

3. **Review recommendations** and apply countermeasures proactively

### For Knowledge Maintainers

#### Adding a New Domain

Use the interactive script:

```bash
python3 .claude/skills/manage-risk-knowledge/scripts/add_domain.py
```

Or manually:
1. Create `domains/{name}/` directory
2. Add `spec.md` and `risks.md` using templates
3. Update `indexes/knowledge-map.yml`
4. Run validation: `python3 scripts/validate_knowledge.py`

#### Recording an Incident

1. Create `incidents/YYYY-description.md` using the template
2. Add bidirectional links to related `domains/*/risks.md`
3. Update relevant risk entries with incident references
4. Validate links: `python3 scripts/check_links.py`

#### Updating Risks

1. Edit `domains/{name}/risks.md` or `common-risks/{category}.md`
2. Ensure required fields: **Details**, **Countermeasures**, **Severity**
3. Add **Related Incident** links where applicable
4. Update keywords in `knowledge-map.yml` if needed

## Scripts

The repository includes validation and utility scripts in `.claude/skills/manage-risk-knowledge/scripts/`:

### validate_knowledge.py

Comprehensive validation of the entire knowledge base.

```bash
python3 .claude/skills/manage-risk-knowledge/scripts/validate_knowledge.py
```

**Checks:**
- YAML syntax in knowledge-map.yml
- File path existence
- Required fields in all documents
- Duplicate domains and keywords
- Bidirectional link consistency

### check_links.py

Focused validation of cross-references.

```bash
python3 .claude/skills/manage-risk-knowledge/scripts/check_links.py
```

**Checks:**
- Incident → Risk references
- Risk → Incident references
- Knowledge-map.yml file paths
- Broken markdown links

### add_domain.py

Interactive wizard for creating new domains.

```bash
python3 .claude/skills/manage-risk-knowledge/scripts/add_domain.py
```

**Features:**
- Validates domain uniqueness
- Creates spec.md and risks.md from templates
- Updates knowledge-map.yml automatically
- Guides keyword selection

### Installation

Scripts require PyYAML:

```bash
pip install -r .claude/skills/manage-risk-knowledge/scripts/requirements.txt
```

## Templates

Templates and validation rules are available in `.claude/skills/manage-risk-knowledge/references/`:

- **templates.md**: File templates for spec.md, risks.md, incidents/*.md
- **validation-rules.md**: Validation rules and checks

## Integration with GitHub Copilot

This repository is designed to work seamlessly with GitHub Copilot:

### Agent Configuration

The `.github/copilot-instructions.md` file configures Copilot to act as a **Risk Assessment AI Agent** that:

1. Greets users and explains how to use the knowledge base
2. Asks clarifying questions about implementation details
3. Searches `knowledge-map.yml` for relevant domains
4. Analyzes user input against known risks and incidents
5. Returns high-risk warnings with countermeasures

### Claude Skill Integration

The `.claude/skills/manage-risk-knowledge/` skill enables AI assistants to:

- Maintain the knowledge base structure
- Add new domains systematically
- Record incidents with proper linking
- Validate data integrity
- Update risk catalogs

## Validation Rules

Before committing changes, ensure:

### Blocking Errors
- ✗ Duplicate domain names
- ✗ Duplicate keywords across domains
- ✗ Broken file paths in knowledge-map.yml
- ✗ Missing required sections in spec.md/risks.md/incidents

### Warnings
- ⚠ Similar keywords (e.g., "auth" vs "authentication")
- ⚠ Duplicate risk patterns
- ⚠ Critical risks without incident references
- ⚠ Missing bidirectional links

## Contributing

### Prerequisites

- Python 3.8+
- PyYAML 6.0+
- GitHub Copilot (for agent features)

### Workflow

1. **Add/Update Knowledge**: Use provided scripts or edit files manually
2. **Validate Changes**: Run `validate_knowledge.py` and `check_links.py`
3. **Test with Copilot**: Verify agent behavior with sample queries
4. **Commit**: Push changes after validation passes

### Best Practices

- **Be specific**: Use concrete examples in risk descriptions
- **Link incidents**: Always reference past incidents in risk entries
- **Keep it concise**: Focus on high-severity issues only
- **Maintain bidirectional links**: Ensure incidents ↔ risks are cross-referenced
- **Use keywords wisely**: Choose search terms developers would naturally use

## License

See individual skill licenses in `.claude/skills/*/license.txt`.

## Support

For issues with:
- **Knowledge content**: Open an issue describing the missing/incorrect information
- **Scripts**: Check `.tmp/outputs/script-validation-results.md` for debug info
- **Copilot agent**: Review `.github/prompts/risk-assessment.prompt.md` configuration

## Related Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Claude Skills Framework](https://docs.anthropic.com/)

---

**Maintained by**: Risk Assessment Team  
**Last Updated**: 2026-01-12
