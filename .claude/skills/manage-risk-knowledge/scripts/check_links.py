#!/usr/bin/env python3
"""
Check bidirectional link consistency between incidents and risks.

This script specifically focuses on link validation:
- Incident → Risk references
- Risk → Incident references
- Broken file links
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set


def find_markdown_links(content: str, base_path: Path) -> List[str]:
    """Extract all markdown file links from content."""
    # Match [text](path.md) pattern
    pattern = r"\[.*?\]\(([^)]+\.md)\)"
    links = re.findall(pattern, content)
    
    # Normalize paths
    normalized = []
    for link in links:
        # Remove anchors
        link = link.split("#")[0]
        # Convert relative to absolute
        if link.startswith("http"):
            continue  # Skip external links
        normalized.append(link)
    
    return normalized


def check_incident_risk_links(repo_root: Path) -> Dict[str, List[str]]:
    """Check links from incidents to risks."""
    results = {
        "broken_links": [],
        "missing_backlinks": [],
    }
    
    incidents_dir = repo_root / "incidents"
    if not incidents_dir.exists():
        return results

    for incident_file in incidents_dir.glob("*.md"):
        content = incident_file.read_text(encoding="utf-8")
        
        # Find risk file references
        links = find_markdown_links(content, incident_file)
        risk_links = [l for l in links if "risks.md" in l]
        
        for risk_link in risk_links:
            # Resolve path
            if risk_link.startswith("../"):
                # Relative from incident file
                risk_path = (incident_file.parent / risk_link).resolve()
            else:
                # Relative from repo root
                risk_path = (repo_root / risk_link).resolve()
            
            # Check if file exists
            if not risk_path.exists():
                results["broken_links"].append({
                    "from": str(incident_file.relative_to(repo_root)),
                    "to": risk_link,
                    "reason": "File not found"
                })
                continue
            
            # Check if risk file references this incident back
            risk_content = risk_path.read_text(encoding="utf-8")
            incident_name = incident_file.name
            
            if incident_name not in risk_content:
                results["missing_backlinks"].append({
                    "incident": str(incident_file.relative_to(repo_root)),
                    "risk": str(risk_path.relative_to(repo_root)),
                    "reason": "Risk doesn't reference incident back"
                })

    return results


def check_risk_incident_links(repo_root: Path) -> Dict[str, List[str]]:
    """Check links from risks to incidents."""
    results = {
        "broken_links": [],
        "missing_backlinks": [],
    }
    
    for risks_file in repo_root.glob("domains/*/risks.md"):
        content = risks_file.read_text(encoding="utf-8")
        
        # Find incident file references
        links = find_markdown_links(content, risks_file)
        incident_links = [l for l in links if "incidents/" in l]
        
        for incident_link in incident_links:
            # Resolve path
            if incident_link.startswith("../"):
                # Relative from risks file
                incident_path = (risks_file.parent / incident_link).resolve()
            else:
                # Relative from repo root
                incident_path = (repo_root / incident_link).resolve()
            
            # Check if file exists
            if not incident_path.exists():
                results["broken_links"].append({
                    "from": str(risks_file.relative_to(repo_root)),
                    "to": incident_link,
                    "reason": "File not found"
                })
                continue
            
            # Check if incident file references this risk back
            incident_content = incident_path.read_text(encoding="utf-8")
            risks_filename = risks_file.name
            risks_domain = risks_file.parent.name
            
            # Check for various reference formats
            if (risks_filename not in incident_content and 
                risks_domain not in incident_content and
                str(risks_file.relative_to(repo_root)) not in incident_content):
                results["missing_backlinks"].append({
                    "risk": str(risks_file.relative_to(repo_root)),
                    "incident": str(incident_path.relative_to(repo_root)),
                    "reason": "Incident doesn't reference risk back"
                })

    return results


def check_knowledge_map_links(repo_root: Path) -> List[Dict]:
    """Check that all files referenced in knowledge-map.yml exist."""
    import yaml
    
    broken_links = []
    
    km_path = repo_root / "indexes" / "knowledge-map.yml"
    if not km_path.exists():
        return [{"error": "knowledge-map.yml not found"}]
    
    try:
        with open(km_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [{"error": f"Invalid YAML: {e}"}]
    
    # Support both formats: list at root or definitions key with list
    if isinstance(data, dict) and "definitions" in data:
        data = data["definitions"]
    
    if not isinstance(data, list):
        return [{"error": "knowledge-map.yml root must be a list or have 'definitions' key with list"}]
    
    for idx, entry in enumerate(data):
        domain_name = entry.get("domain_name", f"Entry #{idx + 1}")
        
        if "related_files" not in entry:
            continue
        
        related_files = entry["related_files"]
        
        # Check common_risks
        if "common_risks" in related_files:
            for file_path in related_files["common_risks"]:
                full_path = repo_root / file_path
                if not full_path.exists():
                    broken_links.append({
                        "domain": domain_name,
                        "file": file_path,
                        "reason": "File not found"
                    })
        
        # Check domain_knowledge
        if "domain_knowledge" in related_files:
            for file_path in related_files["domain_knowledge"]:
                full_path = repo_root / file_path
                if not full_path.exists():
                    broken_links.append({
                        "domain": domain_name,
                        "file": file_path,
                        "reason": "File not found"
                    })
    
    return broken_links


def main():
    if len(sys.argv) > 1:
        repo_root = Path(sys.argv[1])
    else:
        # Assume script is in .claude/skills/manage-risk-knowledge/scripts/
        repo_root = Path(__file__).parent.parent.parent.parent.parent

    print(f"Checking links in: {repo_root}\n")

    # Check knowledge-map links
    print("=== Knowledge Map Links ===")
    km_broken = check_knowledge_map_links(repo_root)
    if km_broken:
        for issue in km_broken:
            if "error" in issue:
                print(f"ERROR: {issue['error']}")
            else:
                print(f"✗ [{issue['domain']}] {issue['file']}: {issue['reason']}")
    else:
        print("✓ All knowledge-map.yml references are valid")
    print()

    # Check incident → risk links
    print("=== Incident → Risk Links ===")
    incident_results = check_incident_risk_links(repo_root)
    
    if incident_results["broken_links"]:
        print("Broken links:")
        for issue in incident_results["broken_links"]:
            print(f"✗ {issue['from']} → {issue['to']}: {issue['reason']}")
    
    if incident_results["missing_backlinks"]:
        print("Missing backlinks:")
        for issue in incident_results["missing_backlinks"]:
            print(f"⚠ {issue['incident']} references {issue['risk']}, but risk doesn't link back")
    
    if not incident_results["broken_links"] and not incident_results["missing_backlinks"]:
        print("✓ All incident → risk links are valid")
    print()

    # Check risk → incident links
    print("=== Risk → Incident Links ===")
    risk_results = check_risk_incident_links(repo_root)
    
    if risk_results["broken_links"]:
        print("Broken links:")
        for issue in risk_results["broken_links"]:
            print(f"✗ {issue['from']} → {issue['to']}: {issue['reason']}")
    
    if risk_results["missing_backlinks"]:
        print("Missing backlinks:")
        for issue in risk_results["missing_backlinks"]:
            print(f"⚠ {issue['risk']} references {issue['incident']}, but incident doesn't link back")
    
    if not risk_results["broken_links"] and not risk_results["missing_backlinks"]:
        print("✓ All risk → incident links are valid")
    print()

    # Summary
    total_issues = (
        len(km_broken) +
        len(incident_results["broken_links"]) +
        len(incident_results["missing_backlinks"]) +
        len(risk_results["broken_links"]) +
        len(risk_results["missing_backlinks"])
    )

    if total_issues == 0:
        print("✓ All link checks passed!")
        return 0
    else:
        print(f"✗ Found {total_issues} link issue(s)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
