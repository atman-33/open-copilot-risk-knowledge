#!/usr/bin/env python3
"""
Initialize risk knowledge base repository for a new project.

This script:
1. Archives sample data to .examples/
2. Cleans domains/ and incidents/
3. Templates common-risks/ files
4. Resets knowledge-map.yml
5. Runs validation

This is a ONE-TIME operation for initial project setup.
"""

import argparse
import shutil
import sys
from pathlib import Path

import yaml


COMMON_RISKS_TEMPLATES = {
    "security.md": """# Security Risks

Cross-cutting security risk patterns applicable to all domains.

## 1. SQL Injection

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## 2. Cross-Site Scripting (XSS)

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## 3. Information Disclosure

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## (Add More Risks)

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)
""",
    "performance.md": """# Performance Risks

Cross-cutting performance degradation patterns.

## 1. N+1 Query Problem

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## 2. Memory Leak

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## 3. Connection Exhaustion

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## (Add More Risks)

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)
""",
    "availability.md": """# Availability Risks

Cross-cutting service availability and outage patterns.

## 1. Service Outage

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## 2. Login Failure

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## 3. Database Connection Failure

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)

---

## (Add More Risks)

**Risk**:
(Add description here)

**Causes**:
- (Add causes here)

**Severity**: 
(Critical/High/Medium/Low)
"""
}

KNOWLEDGE_MAP_TEMPLATE = """# Copilot Knowledge Map
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
"""


def get_repo_root():
    """Get repository root (assuming script is in .claude/skills/init-risk-knowledge/scripts/)."""
    return Path(__file__).parent.parent.parent.parent.parent


def check_already_initialized(repo_root: Path) -> bool:
    """Check if .examples/ already exists."""
    return (repo_root / ".examples").exists()


def inventory_files(repo_root: Path):
    """List all files that will be archived."""
    print("\n=== Current Content to Archive ===\n")
    
    # Count domains
    domains_dir = repo_root / "domains"
    if domains_dir.exists():
        domains = [d for d in domains_dir.iterdir() if d.is_dir()]
        print(f"  domains/: {len(domains)} domains")
        for domain in domains:
            print(f"    - {domain.name}/")
    
    # Count incidents
    incidents_dir = repo_root / "incidents"
    if incidents_dir.exists():
        incidents = list(incidents_dir.glob("*.md"))
        print(f"  incidents/: {len(incidents)} incidents")
        for incident in incidents:
            print(f"    - {incident.name}")
    
    # Common risks
    common_risks_dir = repo_root / "common-risks"
    if common_risks_dir.exists():
        risks = list(common_risks_dir.glob("*.md"))
        print(f"  common-risks/: {len(risks)} files (will be templated)")
        for risk in risks:
            print(f"    - {risk.name}")
    
    print()


def confirm_proceed() -> bool:
    """Ask user to confirm."""
    print("This will:")
    print("  ✓ Move samples to .examples/ directory")
    print("  ✓ Clean domains/ and incidents/ directories")
    print("  ✓ Template common-risks/ files")
    print("  ✓ Reset knowledge-map.yml")
    print()
    
    response = input("Proceed? (yes/no): ").strip().lower()
    return response in ["yes", "y"]


def archive_samples(repo_root: Path, dry_run: bool = False):
    """Move sample files to .examples/."""
    examples_dir = repo_root / ".examples"
    
    if not dry_run:
        examples_dir.mkdir(exist_ok=True)
    
    print("\n=== Archiving Samples ===\n")
    
    # Archive domains
    domains_dir = repo_root / "domains"
    if domains_dir.exists():
        for domain in domains_dir.iterdir():
            if domain.is_dir():
                dest = examples_dir / "domains" / domain.name
                if dry_run:
                    print(f"[DRY RUN] Would move: {domain} → {dest}")
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(domain), str(dest))
                    print(f"✓ Moved: {domain.name}/ → .examples/domains/")
    
    # Archive incidents
    incidents_dir = repo_root / "incidents"
    if incidents_dir.exists():
        for incident in incidents_dir.glob("*.md"):
            dest = examples_dir / "incidents" / incident.name
            if dry_run:
                print(f"[DRY RUN] Would move: {incident} → {dest}")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(incident), str(dest))
                print(f"✓ Moved: {incident.name} → .examples/incidents/")
    
    # Archive original common-risks (for reference)
    common_risks_dir = repo_root / "common-risks"
    if common_risks_dir.exists():
        dest_dir = examples_dir / "common-risks"
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
        for risk_file in common_risks_dir.glob("*.md"):
            dest = dest_dir / risk_file.name
            if dry_run:
                print(f"[DRY RUN] Would copy: {risk_file.name} → .examples/common-risks/")
            else:
                shutil.copy2(str(risk_file), str(dest))
                print(f"✓ Archived: {risk_file.name} → .examples/common-risks/")


def clean_directories(repo_root: Path, dry_run: bool = False):
    """Ensure domains/ and incidents/ are empty."""
    print("\n=== Cleaning Directories ===\n")
    
    domains_dir = repo_root / "domains"
    incidents_dir = repo_root / "incidents"
    
    # Domains should be empty after archiving
    if domains_dir.exists() and list(domains_dir.iterdir()):
        if dry_run:
            print(f"[DRY RUN] Would clean: domains/")
        else:
            # Remove any remaining files
            for item in domains_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            print("✓ Cleaned: domains/")
    else:
        print("✓ domains/ already clean")
    
    # Incidents should be empty after archiving
    if incidents_dir.exists() and list(incidents_dir.glob("*.md")):
        if dry_run:
            print(f"[DRY RUN] Would clean: incidents/")
        else:
            for item in incidents_dir.glob("*.md"):
                item.unlink()
            print("✓ Cleaned: incidents/")
    else:
        print("✓ incidents/ already clean")


def template_common_risks(repo_root: Path, dry_run: bool = False):
    """Replace common-risks files with templates."""
    print("\n=== Templating Common Risks ===\n")
    
    common_risks_dir = repo_root / "common-risks"
    common_risks_dir.mkdir(exist_ok=True)
    
    for filename, content in COMMON_RISKS_TEMPLATES.items():
        file_path = common_risks_dir / filename
        if dry_run:
            print(f"[DRY RUN] Would template: {filename}")
        else:
            file_path.write_text(content, encoding="utf-8")
            print(f"✓ Templated: {filename}")


def reset_knowledge_map(repo_root: Path, dry_run: bool = False):
    """Reset knowledge-map.yml to empty state."""
    print("\n=== Resetting Knowledge Map ===\n")
    
    km_path = repo_root / "indexes" / "knowledge-map.yml"
    km_path.parent.mkdir(parents=True, exist_ok=True)
    
    if dry_run:
        print(f"[DRY RUN] Would reset: knowledge-map.yml")
    else:
        km_path.write_text(KNOWLEDGE_MAP_TEMPLATE, encoding="utf-8")
        print("✓ Reset: knowledge-map.yml")


def run_validation(repo_root: Path):
    """Run validation script."""
    print("\n=== Running Validation ===\n")
    
    validate_script = repo_root / ".claude/skills/manage-risk-knowledge/scripts/validate_knowledge.py"
    
    if not validate_script.exists():
        print("⚠ Validation script not found, skipping...")
        return True
    
    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, str(validate_script), str(repo_root)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✓ Validation passed")
            return True
        else:
            print(f"✗ Validation failed:\n{result.stdout}")
            return False
    except Exception as e:
        print(f"⚠ Validation error: {e}")
        return False


def show_next_steps():
    """Display next steps guidance."""
    print("\n" + "="*60)
    print("✓ Repository initialized successfully!")
    print("="*60)
    print("\nSamples archived to .examples/ directory.\n")
    print("Next steps:")
    print("  1. Review examples: ls -la .examples/")
    print("  2. Add your first domain:")
    print("     python3 .claude/skills/manage-risk-knowledge/scripts/add_domain.py")
    print("  3. Customize common-risks/ for your project")
    print("  4. Update README.md with project-specific information")
    print("\nResources:")
    print("  - Templates: .claude/skills/manage-risk-knowledge/references/templates.md")
    print("  - Examples: .examples/")
    print("  - Management: .claude/skills/manage-risk-knowledge/SKILL.md")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Initialize risk knowledge repository (one-time operation)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without making changes"
    )
    
    args = parser.parse_args()
    
    repo_root = get_repo_root()
    
    print("=== Repository Initialization ===")
    
    # Check if already initialized
    if check_already_initialized(repo_root):
        print("\nERROR: .examples/ directory already exists.")
        print("This script is for initial setup only and has already been run.\n")
        print("If you want to reset completely, delete .examples/ first (NOT recommended).")
        print("For ongoing maintenance, use git or manual file management.")
        return 1
    
    # Show inventory
    inventory_files(repo_root)
    
    # Confirm (unless --force or --dry-run)
    if not args.force and not args.dry_run:
        if not confirm_proceed():
            print("\nCancelled.")
            return 0
    
    if args.dry_run:
        print("\n[DRY RUN MODE - No changes will be made]\n")
    
    # Execute
    archive_samples(repo_root, args.dry_run)
    clean_directories(repo_root, args.dry_run)
    template_common_risks(repo_root, args.dry_run)
    reset_knowledge_map(repo_root, args.dry_run)
    
    if args.dry_run:
        print("\n[DRY RUN COMPLETE - No changes were made]")
        return 0
    
    # Validate
    validation_ok = run_validation(repo_root)
    
    if not validation_ok:
        print("\n⚠ Warning: Validation failed. Please check the output above.")
        return 1
    
    # Show guidance
    show_next_steps()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
