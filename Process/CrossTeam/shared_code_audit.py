#!/usr/bin/env python3
"""Advisory audit of cross-team code-sharing channels (read-only).

Reports places where one team consumes another team's code through a
channel that bypasses a sharing policy: writable imports, imports pinned in
a way that may not be overridable downstream, and imports of moving
branches. It changes nothing, so it needs no one's permission, and its
counts are the evidence for enforcing the rules above documentation.

Usage:
  shared_code_audit.py p4-specs DIR     DIR holds stream specs saved with
                                        `p4 stream -o <stream>` (one per file)
  shared_code_audit.py p4-live DEPOT    fetch specs from a server using
                                        read-only p4 commands, e.g. //Game
  shared_code_audit.py git REPO         inspect .gitmodules in REPO

Options (given after the subcommand and its argument):
  --release-pattern REGEX   sources matching this count as release references
  --consumers-of TEXT       (Perforce modes) provider-side view: list the streams
                            that import from a source containing TEXT, and how,
                            instead of auditing against the rules
  --json                    machine-readable output

Exit status: 0 no findings, 1 findings, 2 usage or tool error.
"""
import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_RELEASE_PATTERN = r"(release|rel|rc|stable|v\d)"


@dataclass
class Finding:
    consumer: str
    rule: str
    detail: str
    severity: str  # "high" or "medium"


# ---------------------------------------------------------------- Perforce

def parse_stream_spec(text):
    """Return (stream_name, [(path_type, target, source), ...]).

    Only import and import+ lines of the Paths field are returned.
    """
    name = None
    section = None
    entries = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw[0].isspace():
            field, _, rest = raw.partition(":")
            section = field.strip()
            if section == "Stream":
                name = rest.strip()
            continue
        if section == "Paths":
            tokens = raw.split()
            if tokens and tokens[0] in ("import", "import+"):
                target = tokens[1] if len(tokens) > 1 else ""
                source = tokens[2] if len(tokens) > 2 else ""
                entries.append((tokens[0], target, source))
    return name, entries


def audit_stream(name, entries, release_re):
    findings = []
    for path_type, target, source in entries:
        where = f"{target} <- {source or '(parent path)'}"
        if path_type == "import+":
            findings.append(Finding(name, "writable-import", where, "high"))
        if "@" in source:
            findings.append(Finding(name, "pinned-import", where, "medium"))
        if source and not release_re.search(source):
            findings.append(Finding(name, "moving-branch", where, "medium"))
    return findings


def consumers_of(name, entries, text):
    """Provider-side view: imports in this stream whose source contains `text`."""
    return [(name, source, path_type)
            for path_type, _target, source in entries
            if source and text in source]


def print_consumers(rows, as_json):
    if as_json:
        print(json.dumps([{"stream": s, "source": src, "link": link}
                          for s, src, link in rows], indent=2))
        return
    if not rows:
        print("No streams import from that source.")
        return
    print(f"{'Stream':<40} {'Source':<50} Link")
    for stream, source, link in sorted(rows):
        print(f"{stream:<40} {source:<50} {link}")


def run_p4(*args):
    result = subprocess.run(["p4", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "p4 command failed")
    return result.stdout


def live_specs(depot):
    names = run_p4("-ztag", "-F", "%Stream%", "streams", f"{depot}/...").split()
    return [run_p4("stream", "-o", name) for name in names]


# --------------------------------------------------------------------- Git

def audit_git(repo, release_re):
    gitmodules = Path(repo) / ".gitmodules"
    if not gitmodules.exists():
        return []
    result = subprocess.run(
        ["git", "config", "-f", str(gitmodules), "--list"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git config failed")
    submodules = {}
    for line in result.stdout.splitlines():
        key, _, value = line.partition("=")
        match = re.match(r"submodule\.(.+)\.(path|url|branch)$", key)
        if match:
            submodules.setdefault(match.group(1), {})[match.group(2)] = value
    findings = []
    for name, info in submodules.items():
        branch = info.get("branch")
        if branch and not release_re.search(branch):
            findings.append(Finding(
                info.get("path", name), "moving-branch",
                f"tracks branch '{branch}' ({info.get('url', 'unknown url')})",
                "medium",
            ))
    return findings


# ------------------------------------------------------------------ Report

def report(findings, as_json):
    if as_json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
        return
    if not findings:
        print("No findings.")
        return
    ordered = sorted(findings, key=lambda f: (f.severity != "high", f.consumer))
    for f in ordered:
        print(f"[{f.severity:<6}] {f.consumer}: {f.rule}: {f.detail}")
    counts = {}
    for f in findings:
        counts[f.rule] = counts.get(f.rule, 0) + 1
    print("\nSummary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--release-pattern", default=DEFAULT_RELEASE_PATTERN)
    common.add_argument("--consumers-of", metavar="TEXT")
    common.add_argument("--json", action="store_true")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="mode", required=True)
    sub.add_parser("p4-specs", parents=[common]).add_argument("directory")
    sub.add_parser("p4-live", parents=[common]).add_argument("depot")
    sub.add_parser("git", parents=[common]).add_argument("repo")
    args = parser.parse_args(argv)
    if args.consumers_of and args.mode == "git":
        parser.error("--consumers-of is only available in the Perforce modes")

    release_re = re.compile(args.release_pattern, re.IGNORECASE)
    findings = []
    try:
        if args.mode == "git":
            findings = audit_git(args.repo, release_re)
        else:
            if args.mode == "p4-specs":
                specs = [p.read_text() for p in sorted(Path(args.directory).iterdir())
                         if p.is_file()]
            else:
                specs = live_specs(args.depot)
            rows = []
            for text in specs:
                name, entries = parse_stream_spec(text)
                name = name or "(unnamed stream)"
                if args.consumers_of:
                    rows += consumers_of(name, entries, args.consumers_of)
                else:
                    findings += audit_stream(name, entries, release_re)
            if args.consumers_of:
                print_consumers(rows, args.json)
                return 0
    except (OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    report(findings, args.json)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())