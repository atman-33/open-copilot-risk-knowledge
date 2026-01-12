#!/usr/bin/env python3
"""
Validate risk knowledge base structure and content.

Checks:
- YAML syntax and structure in knowledge-map.yml
- File path existence
- Required fields in spec.md, risks.md, incidents/*.md
- Duplicate domains and keywords
- Bidirectional link consistency
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

import yaml


class ValidationError:
    def __init__(self, severity: str, file: str, message: str):
        self.severity = severity  # "ERROR" or "WARNING"
        self.file = file
        self.message = message

    def __str__(self):
        return f"[{self.severity}] {self.file}: {self.message}"


def validate_knowledge_map(repo_root: Path) -> List[ValidationError]:
    """Validate knowledge-map.yml structure and content."""
    errors = []
    km_path = repo_root / "indexes" / "knowledge-map.yml"

    if not km_path.exists():
        errors.append(ValidationError("ERROR", str(km_path), "knowledge-map.yml not found"))
        return errors

    try:
        with open(km_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(ValidationError("ERROR", str(km_path), f"Invalid YAML: {e}"))
        return errors

    # Support both formats: list at root or definitions key with list
    if isinstance(data, dict) and "definitions" in data:
        data = data["definitions"]
    
    if not isinstance(data, list):
        errors.append(ValidationError("ERROR", str(km_path), "Root must be a list or have 'definitions' key with list"))
        return errors

    # Track domains and keywords for uniqueness
    seen_domains = set()
    seen_keywords = {}

    for idx, entry in enumerate(data):
        entry_ref = f"Entry #{idx + 1}"

        # Required fields
        if "domain_name" not in entry:
            errors.append(ValidationError("ERROR", str(km_path), f"{entry_ref}: Missing 'domain_name'"))
            continue

        domain_name = entry["domain_name"]

        # Check uniqueness
        if domain_name in seen_domains:
            errors.append(ValidationError("ERROR", str(km_path), f"{entry_ref}: Duplicate domain_name '{domain_name}'"))
        seen_domains.add(domain_name)

        # Check required fields
        if "keywords" not in entry:
            errors.append(ValidationError("ERROR", str(km_path), f"{entry_ref}: Missing 'keywords'"))
        else:
            keywords = entry["keywords"]
            if not isinstance(keywords, list):
                errors.append(ValidationError("ERROR", str(km_path), f"{entry_ref}: 'keywords' must be a list"))
            else:
                for kw in keywords:
                    if kw in seen_keywords:
                        errors.append(
                            ValidationError(
                                "WARNING",
                                str(km_path),
                                f"{entry_ref}: Keyword '{kw}' already used in '{seen_keywords[kw]}'"
                            )
                        )
                    seen_keywords[kw] = domain_name

        if "related_files" not in entry:
            errors.append(ValidationError("ERROR", str(km_path), f"{entry_ref}: Missing 'related_files'"))
        else:
            related_files = entry["related_files"]
            
            # Check common_risks paths
            if "common_risks" in related_files:
                for file_path in related_files["common_risks"]:
                    full_path = repo_root / file_path
                    if not full_path.exists():
                        errors.append(
                            ValidationError("ERROR", str(km_path), f"{entry_ref}: File not found: {file_path}")
                        )

            # Check domain_knowledge paths
            if "domain_knowledge" in related_files:
                for file_path in related_files["domain_knowledge"]:
                    full_path = repo_root / file_path
                    if not full_path.exists():
                        errors.append(
                            ValidationError("ERROR", str(km_path), f"{entry_ref}: File not found: {file_path}")
                        )

    return errors


def validate_spec_md(file_path: Path) -> List[ValidationError]:
    """Validate spec.md has required sections."""
    errors = []
    
    if not file_path.exists():
        errors.append(ValidationError("ERROR", str(file_path), "spec.md not found"))
        return errors

    content = file_path.read_text(encoding="utf-8")

    # Required sections (support both English and Japanese)
    required_sections = [
        ("## Overview", "## 概要"),
        ("## Core Components", "## コアコンポーネント")
    ]
    
    for en_section, jp_section in required_sections:
        if en_section not in content and jp_section not in content:
            errors.append(ValidationError("ERROR", str(file_path), f"Missing required section: {en_section} or {jp_section}"))

    return errors


def validate_risks_md(file_path: Path) -> List[ValidationError]:
    """Validate risks.md has proper risk entries."""
    errors = []
    
    if not file_path.exists():
        errors.append(ValidationError("ERROR", str(file_path), "risks.md not found"))
        return errors

    content = file_path.read_text(encoding="utf-8")

    # Check for risk entries (assuming risks start with ### or ##)
    risk_pattern = re.compile(r"^##[#]?\s+(.+)", re.MULTILINE)
    risks = risk_pattern.findall(content)

    if not risks:
        errors.append(ValidationError("WARNING", str(file_path), "No risk entries found (## or ### headings)"))
        return errors

    # For each risk, check required fields
    # Split content by ## or ### to get individual risk sections
    risk_sections = re.split(r"^##[#]?\s+", content, flags=re.MULTILINE)[1:]  # Skip the part before first heading

    for idx, section in enumerate(risk_sections):
        risk_name = risks[idx] if idx < len(risks) else f"Risk #{idx + 1}"
        
        # Check for either English or Japanese field names
        has_details = ("**Details**" in section or "**詳細**" in section or 
                      "詳細:" in section or "Details:" in section)
        has_countermeasures = ("**Countermeasures**" in section or "**対策**" in section or 
                              "対策:" in section or "Countermeasures:" in section)
        
        if not has_details:
            errors.append(ValidationError("WARNING", str(file_path), f"{risk_name}: Missing '**Details**' or '**詳細**' field"))
        
        if not has_countermeasures:
            errors.append(ValidationError("WARNING", str(file_path), f"{risk_name}: Missing '**Countermeasures**' or '**対策**' field"))

    return errors


def validate_incident_md(file_path: Path) -> List[ValidationError]:
    """Validate incident file has required sections."""
    errors = []
    
    content = file_path.read_text(encoding="utf-8")

    # Required sections (support both English and Japanese)
    required_sections = [
        ("## Summary", "## サマリー"),
        ("## Root Cause", "## 根本原因"),
        ("## Related Risks", "## 関連リスク")
    ]
    
    for en_section, jp_section in required_sections:
        if en_section not in content and jp_section not in content:
            errors.append(ValidationError("ERROR", str(file_path), f"Missing required section: {en_section} or {jp_section}"))

    return errors


def validate_bidirectional_links(repo_root: Path) -> List[ValidationError]:
    """Check bidirectional links between incidents and risks."""
    errors = []
    
    incidents_dir = repo_root / "incidents"
    if not incidents_dir.exists():
        return errors

    # Collect all incident files and their referenced risks
    incident_to_risks = {}
    risk_to_incidents = {}

    # Parse incidents
    for incident_file in incidents_dir.glob("*.md"):
        content = incident_file.read_text(encoding="utf-8")
        
        # Find risk file references
        risk_refs = re.findall(r"\[.*?\]\((domains/[^)]+/risks\.md)\)", content)
        incident_to_risks[incident_file.name] = risk_refs

    # Parse risks files
    for risks_file in repo_root.glob("domains/*/risks.md"):
        content = risks_file.read_text(encoding="utf-8")
        
        # Find incident references
        incident_refs = re.findall(r"\[.*?\]\(((?:\.\./\.\./)?incidents/[^)]+\.md)\)", content)
        # Normalize paths
        incident_refs = [ref.replace("../../incidents/", "").replace("incidents/", "") for ref in incident_refs]
        
        relative_path = str(risks_file.relative_to(repo_root))
        risk_to_incidents[relative_path] = incident_refs

    # Check bidirectional consistency
    for incident_name, referenced_risks in incident_to_risks.items():
        for risk_file in referenced_risks:
            if risk_file in risk_to_incidents:
                if incident_name not in risk_to_incidents[risk_file]:
                    errors.append(
                        ValidationError(
                            "WARNING",
                            f"incidents/{incident_name}",
                            f"References {risk_file}, but {risk_file} doesn't reference this incident"
                        )
                    )

    return errors


def validate_domain_folders(repo_root: Path) -> List[ValidationError]:
    """Validate that domain folders have required files."""
    errors = []
    
    domains_dir = repo_root / "domains"
    if not domains_dir.exists():
        errors.append(ValidationError("ERROR", "domains/", "domains/ directory not found"))
        return errors

    for domain_dir in domains_dir.iterdir():
        if not domain_dir.is_dir():
            continue

        spec_path = domain_dir / "spec.md"
        risks_path = domain_dir / "risks.md"

        if not spec_path.exists():
            errors.append(ValidationError("ERROR", str(domain_dir), "Missing spec.md"))
        else:
            errors.extend(validate_spec_md(spec_path))

        if not risks_path.exists():
            errors.append(ValidationError("ERROR", str(domain_dir), "Missing risks.md"))
        else:
            errors.extend(validate_risks_md(risks_path))

    return errors


def validate_all(repo_root: Path) -> Tuple[List[ValidationError], List[ValidationError]]:
    """Run all validations and return errors and warnings."""
    all_errors = []

    # Run all validation checks
    all_errors.extend(validate_knowledge_map(repo_root))
    all_errors.extend(validate_domain_folders(repo_root))
    all_errors.extend(validate_bidirectional_links(repo_root))

    # Validate individual incident files
    incidents_dir = repo_root / "incidents"
    if incidents_dir.exists():
        for incident_file in incidents_dir.glob("*.md"):
            all_errors.extend(validate_incident_md(incident_file))

    # Separate errors and warnings
    errors = [e for e in all_errors if e.severity == "ERROR"]
    warnings = [e for e in all_errors if e.severity == "WARNING"]

    return errors, warnings


def main():
    if len(sys.argv) > 1:
        repo_root = Path(sys.argv[1])
    else:
        # Assume script is in .claude/skills/manage-risk-knowledge/scripts/
        repo_root = Path(__file__).parent.parent.parent.parent.parent

    print(f"Validating knowledge base at: {repo_root}\n")

    errors, warnings = validate_all(repo_root)

    # Print results
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  {error}")
        print()

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
        print()

    if not errors and not warnings:
        print("✓ All validations passed!")
        return 0
    elif not errors:
        print(f"✓ No errors, but {len(warnings)} warning(s) found.")
        return 0
    else:
        print(f"✗ {len(errors)} error(s) and {len(warnings)} warning(s) found.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
