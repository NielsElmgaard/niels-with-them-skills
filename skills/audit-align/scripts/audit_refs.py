#!/usr/bin/env python3
"""
Repository Reference & Link Auditor (audit_refs.py)

Scans a repository for:
1. Leaked absolute environment paths (file:///, /workspaces/, /Users/, /home/)
2. Broken relative links in Markdown documents
3. Phantom script references in documentation (commands pointing to non-existent scripts)

Usage:
    python3 skills/audit-align/scripts/audit_refs.py [repo_path] [--json]

Exit codes:
    0: Clean, no issues detected
    1: One or more reference or path issues detected
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse

# Directories and patterns to ignore
IGNORED_DIRS = {
    '.git', 'node_modules', 'dist', 'build', '.venv', 'venv',
    '__pycache__', '.pytest_cache', '.next', '.cache', '.turbo',
    'coverage', '.agents', '.claude'
}

IGNORED_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.webp',
    '.pdf', '.zip', '.tar', '.gz', '.tgz', '.exe', '.bin',
    '.pyc', '.pyo', '.so', '.dylib', '.dll', '.woff', '.woff2'
}

# Regex for absolute environment paths
ABSOLUTE_PATH_PATTERNS = [
    (re.compile(r'file:///[a-zA-Z0-9_\-./]+'), "Absolute file:// URI"),
    (re.compile(r'/(?:workspaces|Users|home/[a-zA-Z0-9_\-]+)/[a-zA-Z0-9_\-./]+'), "Host-specific absolute path"),
]

# Regex for markdown links: [label](target) or ![alt](target)
# Excludes image data URIs or empty links
MD_LINK_PATTERN = re.compile(r'!?\[([^\]]*)\]\(([^)]+)\)')

# Regex for script invocations in markdown code blocks / inline code:
# e.g., `python3 scripts/run.py`, `node bin/cli.js`, `./scripts/test.sh`
SCRIPT_CMD_PATTERN = re.compile(r'(?:python3?|node|bash|sh|\./)\s+([a-zA-Z0-9_\-./]+\.(?:py|js|ts|sh|mjs|cjs))')


def should_skip_dir(dir_name):
    return dir_name in IGNORED_DIRS or dir_name.startswith('.git')


def should_skip_file(file_path):
    suffix = file_path.suffix.lower()
    return suffix in IGNORED_EXTENSIONS


def audit_repository(repo_root):
    issues = []
    repo_root = Path(repo_root).resolve()

    for root, dirs, files in os.walk(repo_root):
        # Prune ignored directories in-place
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        for file_name in files:
            file_path = Path(root) / file_name
            if should_skip_file(file_path):
                continue

            rel_path = file_path.relative_to(repo_root)

            # Skip checking this script itself for patterns in strings
            if rel_path.name == 'audit_refs.py':
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            except Exception:
                continue

            is_markdown = file_path.suffix.lower() in ('.md', '.markdown')
            in_code_block = False

            for line_idx, line in enumerate(lines, start=1):
                stripped = line.strip()

                if is_markdown:
                    if stripped.startswith('```') or stripped.startswith('~~~'):
                        in_code_block = not in_code_block
                        continue

                # 1. Check for leaked absolute environment paths
                # Ignore illustrative placeholders or lines containing examples/ellipses
                is_placeholder = any(placeholder in line for placeholder in ('...', '<', '>', 'my-repo', '/home/user/', 'example'))
                if not is_placeholder and not in_code_block:
                    for pattern, desc in ABSOLUTE_PATH_PATTERNS:
                        for match in pattern.finditer(line):
                            matched_str = match.group(0)
                            # Ignore schema references or standard xml namespaces
                            if 'schemas.android.com' in matched_str or 'w3.org' in matched_str:
                                continue
                            issues.append({
                                'file': str(rel_path),
                                'line': line_idx,
                                'type': 'leaked_absolute_path',
                                'severity': 'error',
                                'message': f"{desc}: '{matched_str}'",
                                'snippet': line.strip()
                            })

                # Markdown-specific link and command checks (only outside fenced code blocks)
                if is_markdown and not in_code_block:
                    # Strip inline backtick code spans before checking live markdown links
                    # to avoid matching syntax examples like `[label](path/to/file.md)`
                    line_without_inline_code = re.sub(r'`[^`]+`', '', line)

                    # 2. Check markdown relative links
                    for match in MD_LINK_PATTERN.finditer(line_without_inline_code):
                        raw_target = match.group(2).strip()

                        # Skip empty targets
                        if not raw_target:
                            continue

                        # Clean out title in links like [label](url "title")
                        target_parts = raw_target.split(None, 1)
                        link_target = target_parts[0]

                        # Ignore external links, mailto, anchor-only, or template tags
                        if (link_target.startswith(('http://', 'https://', 'mailto:', 'ftp://', '#', 'javascript:'))
                                or '<' in link_target or '{' in link_target):
                            continue

                        # Strip internal anchors and query parameters
                        target_path_str = link_target.split('#')[0].split('?')[0]
                        if not target_path_str:
                            # It was just an anchor (#something)
                            continue

                        # Resolve target relative to the markdown file's directory
                        resolved_path = (file_path.parent / target_path_str).resolve()

                        if not resolved_path.exists():
                            # Also test if resolved relative to repo root (some projects do /docs/...)
                            repo_relative_target = (repo_root / target_path_str.lstrip('/')).resolve()
                            if not repo_relative_target.exists():
                                issues.append({
                                    'file': str(rel_path),
                                    'line': line_idx,
                                    'type': 'broken_markdown_link',
                                    'severity': 'error',
                                    'message': f"Broken link target '{link_target}' (file does not exist)",
                                    'snippet': line.strip()
                                })

                    # 3. Check for phantom script invocations
                    for match in SCRIPT_CMD_PATTERN.finditer(line):
                        script_ref = match.group(1).strip()
                        # Skip flags or obvious arguments
                        if script_ref.startswith('-'):
                            continue

                        # Try resolving relative to markdown parent or repo root
                        script_local = (file_path.parent / script_ref).resolve()
                        script_root = (repo_root / script_ref.lstrip('/')).resolve()

                        # Only flag if looks like an intended local script reference and doesn't exist
                        if '/' in script_ref and not script_local.exists() and not script_root.exists():
                            # Exclude typical package names or standard examples like 'path/to/script.py'
                            if not ('example' in script_ref or 'path/to' in script_ref or '<' in script_ref or 'my-repo' in script_ref):
                                issues.append({
                                    'file': str(rel_path),
                                    'line': line_idx,
                                    'type': 'phantom_script_reference',
                                    'severity': 'warning',
                                    'message': f"Documented script '{script_ref}' does not exist on disk",
                                    'snippet': line.strip()
                                })

    return issues


def main():
    parser = argparse.ArgumentParser(description="Audit repository for leaked paths, broken links, and phantom scripts.")
    parser.add_argument('path', nargs='?', default='.', help="Repository root path to audit (defaults to current directory)")
    parser.add_argument('--json', action='store_true', help="Output machine-readable JSON")
    args = parser.parse_args()

    repo_path = Path(args.path).resolve()
    if not repo_path.is_dir():
        sys.stderr.write(f"Error: Directory '{repo_path}' does not exist.\n")
        sys.exit(2)

    issues = audit_repository(repo_path)

    if args.json:
        print(json.dumps(issues, indent=2))
    else:
        if not issues:
            print(f"✅ audit_refs: Clean! No leaked paths, broken links, or phantom script references found in '{repo_path.name}'.")
        else:
            print(f"❌ audit_refs: Found {len(issues)} issue(s) in '{repo_path.name}':\n")
            for issue in issues:
                sev_icon = "🔴" if issue['severity'] == 'error' else "🟡"
                print(f"  {sev_icon} [{issue['type']}] {issue['file']}:{issue['line']}")
                print(f"     {issue['message']}")
                print(f"     Line: {issue['snippet']}\n")

    sys.exit(0 if len(issues) == 0 else 1)


if __name__ == '__main__':
    main()
