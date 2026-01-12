#!/usr/bin/env python3
"""
Interactive script to add a new domain to the risk knowledge base.

This script guides the user through:
1. Choosing a domain name
2. Specifying keywords
3. Selecting related common risks
4. Creating spec.md and risks.md from templates
5. Updating knowledge-map.yml
"""

import sys
from pathlib import Path
from typing import List

import yaml


def kebab_case(text: str) -> str:
    """Convert text to kebab-case."""
    import re
    # Replace spaces and underscores with hyphens
    text = re.sub(r"[_\s]+", "-", text)
    # Remove non-alphanumeric characters except hyphens
    text = re.sub(r"[^a-zA-Z0-9-]", "", text)
    # Convert to lowercase
    text = text.lower()
    # Remove consecutive hyphens
    text = re.sub(r"-+", "-", text)
    # Remove leading/trailing hyphens
    text = text.strip("-")
    return text


def check_domain_exists(repo_root: Path, domain_name: str) -> bool:
    """Check if domain already exists in filesystem or knowledge-map."""
    # Check filesystem
    domain_dir = repo_root / "domains" / domain_name
    if domain_dir.exists():
        return True
    
    # Check knowledge-map.yml
    km_path = repo_root / "indexes" / "knowledge-map.yml"
    if not km_path.exists():
        return False
    
    try:
        with open(km_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        # Support both formats: list at root or definitions key with list
        if isinstance(data, dict) and "definitions" in data:
            data = data["definitions"]
        
        if isinstance(data, list):
            for entry in data:
                if entry.get("domain_name", "").lower() == domain_name.lower():
                    return True
    except:
        pass
    
    return False


def get_common_risks(repo_root: Path) -> List[str]:
    """Get list of available common risk files."""
    common_risks_dir = repo_root / "common-risks"
    if not common_risks_dir.exists():
        return []
    
    return [f.stem for f in common_risks_dir.glob("*.md")]


def create_spec_md(domain_dir: Path, domain_name: str, description: str):
    """Create spec.md from template."""
    content = f"""# {domain_name.replace('-', ' ').title()} - Feature Specification

## Overview

{description}

## Core Components

### Component 1

Brief description of the component.

**Responsibilities:**
- Responsibility 1
- Responsibility 2

**Technologies:**
- Technology stack used

### Component 2

Brief description of the component.

**Responsibilities:**
- Responsibility 1
- Responsibility 2

**Technologies:**
- Technology stack used

## Data Flow

Describe how data flows through the system.

```
User → Component 1 → Component 2 → Result
```

## External Dependencies

- Dependency 1: Purpose
- Dependency 2: Purpose

## Configuration

Key configuration parameters and environment variables.

## Related Documents

- Link to API docs
- Link to architecture diagrams
"""
    
    spec_path = domain_dir / "spec.md"
    spec_path.write_text(content, encoding="utf-8")
    print(f"Created: {spec_path}")


def create_risks_md(domain_dir: Path, domain_name: str):
    """Create risks.md from template."""
    content = f"""# {domain_name.replace('-', ' ').title()} - Risk Assessment

## Risk 1: Brief Description

**Details**:
Detailed explanation of what can go wrong and under what conditions.

**Countermeasures**:
- Mitigation 1: Description
- Mitigation 2: Description

**Severity**: Medium

**Related Incident**: None

---

## Risk 2: Brief Description

**Details**:
Detailed explanation of what can go wrong and under what conditions.

**Countermeasures**:
- Mitigation 1: Description
- Mitigation 2: Description

**Severity**: Low

**Related Incident**: None

---
"""
    
    risks_path = domain_dir / "risks.md"
    risks_path.write_text(content, encoding="utf-8")
    print(f"Created: {risks_path}")


def update_knowledge_map(repo_root: Path, domain_name: str, display_name: str, 
                        description: str, keywords: List[str], 
                        common_risks: List[str]):
    """Add new entry to knowledge-map.yml."""
    km_path = repo_root / "indexes" / "knowledge-map.yml"
    
    # Load existing data
    use_definitions_key = False
    if km_path.exists():
        with open(km_path, "r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f)
        
        # Support both formats: list at root or definitions key with list
        if isinstance(raw_data, dict) and "definitions" in raw_data:
            data = raw_data["definitions"] or []
            use_definitions_key = True
        elif isinstance(raw_data, list):
            data = raw_data
        else:
            data = []
    else:
        data = []
    
    # Build related_files
    related_files = {
        "domain_knowledge": [
            f"domains/{domain_name}/spec.md",
            f"domains/{domain_name}/risks.md"
        ]
    }
    
    if common_risks:
        related_files["common_risks"] = [f"common-risks/{risk}.md" for risk in common_risks]
    
    # Create new entry
    new_entry = {
        "domain_name": display_name,
        "description": description,
        "keywords": keywords,
        "related_files": related_files
    }
    
    # Append and save
    data.append(new_entry)
    
    # Write back in the same format
    if use_definitions_key:
        output_data = {"definitions": data}
    else:
        output_data = data
    
    with open(km_path, "w", encoding="utf-8") as f:
        yaml.dump(output_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    print(f"Updated: {km_path}")


def main():
    if len(sys.argv) > 1:
        repo_root = Path(sys.argv[1])
    else:
        # Assume script is in .claude/skills/manage-risk-knowledge/scripts/
        repo_root = Path(__file__).parent.parent.parent.parent.parent

    print("=== Add New Domain to Risk Knowledge Base ===\n")
    
    # Get domain name
    while True:
        display_name = input("Domain name (e.g., 'User Authentication'): ").strip()
        if not display_name:
            print("Domain name cannot be empty.")
            continue
        
        domain_name = kebab_case(display_name)
        print(f"Folder name will be: {domain_name}")
        
        if check_domain_exists(repo_root, domain_name):
            print(f"ERROR: Domain '{domain_name}' already exists!")
            continue
        
        confirm = input("OK? (y/n): ").strip().lower()
        if confirm == 'y':
            break
    
    # Get description
    description = input("Brief description: ").strip()
    if not description:
        description = f"Risk assessment for {display_name}"
    
    # Get keywords
    print("\nEnter keywords (comma-separated, e.g., 'auth,login,oauth'):")
    keywords_input = input("Keywords: ").strip()
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    if not keywords:
        keywords = [domain_name.replace("-", " ")]
    
    # Get common risks
    available_risks = get_common_risks(repo_root)
    if available_risks:
        print(f"\nAvailable common risks: {', '.join(available_risks)}")
        print("Select related common risks (comma-separated, or leave empty):")
        common_risks_input = input("Common risks: ").strip()
        common_risks = [r.strip() for r in common_risks_input.split(",") if r.strip()]
        # Validate
        common_risks = [r for r in common_risks if r in available_risks]
    else:
        common_risks = []
    
    # Summary
    print("\n=== Summary ===")
    print(f"Domain name: {display_name}")
    print(f"Folder: domains/{domain_name}/")
    print(f"Keywords: {', '.join(keywords)}")
    print(f"Common risks: {', '.join(common_risks) if common_risks else 'None'}")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return 0
    
    # Create domain directory
    domain_dir = repo_root / "domains" / domain_name
    domain_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nCreated directory: {domain_dir}")
    
    # Create files
    create_spec_md(domain_dir, domain_name, description)
    create_risks_md(domain_dir, domain_name)
    
    # Update knowledge-map
    update_knowledge_map(repo_root, domain_name, display_name, description, 
                        keywords, common_risks)
    
    print("\n✓ Domain added successfully!")
    print("\nNext steps:")
    print(f"1. Edit {domain_dir}/spec.md with actual specification")
    print(f"2. Edit {domain_dir}/risks.md with identified risks")
    print("3. Run validate_knowledge.py to check consistency")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
