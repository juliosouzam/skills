#!/usr/bin/env python3
"""Fail-closed approval verifier for a completed Deep Review round.

This is the only machine-readable source of a strict Deep Review approval. It
checks the frozen checkout, current policy version, all job outputs, canonical
ledger, rendered verdict, state entry, and reviewed HEAD. A caller must not
derive approval from review.md or state.yaml alone.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

from _common import (
    POLICY_VERSION,
    check_freeze,
    load_jobs,
    read_json,
    repo_root,
    validate_job_output,
    write_json,
)


def git_head(repo: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True
    )
    if result.returncode:
        raise RuntimeError(f"git rev-parse HEAD failed: {result.stderr.strip()}")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    repo = repo_root()
    out = Path(args.out).resolve()

    try:
        manifest = read_json(out / "manifest.json")
        ledger = read_json(out / "findings.json")
        state = read_json(out / "state.json")
        jobs = load_jobs(out / "jobs.json")
        review = (out / "review.md").read_text(encoding="utf-8")
    except (OSError, RuntimeError) as error:
        sys.stderr.write(f"approval refused: {error}\n")
        return 1

    errors: list[str] = []
    try:
        errors.extend(check_freeze(repo, out, "approval"))
        current_head = git_head(repo)
    except RuntimeError as error:
        errors.append(str(error))
        current_head = None

    if manifest.get("policy_version") != POLICY_VERSION:
        errors.append(
            f"manifest policy_version={manifest.get('policy_version')!r}; expected {POLICY_VERSION}"
        )
    if state.get("policy_version") != POLICY_VERSION:
        errors.append(
            f"state policy_version={state.get('policy_version')!r}; expected {POLICY_VERSION}"
        )
    if current_head and manifest.get("head") != current_head:
        errors.append(f"reviewed HEAD {manifest.get('head')} != current HEAD {current_head}")
    if ledger.get("source_snapshot") != manifest.get("worktree_snapshot"):
        errors.append("findings ledger source snapshot differs from manifest freeze")
    if not re.search(r"^\*\*Verdict: SHIP\*\*", review, re.M):
        errors.append("review.md does not render the strict SHIP verdict")

    current_round = next(
        (row for row in state.get("rounds", []) if row.get("n") == manifest.get("round")), None
    )
    if current_round is None:
        errors.append("state.json has no entry for the current review round")
    else:
        if current_round.get("verdict") != "SHIP":
            errors.append(f"state round verdict is {current_round.get('verdict')!r}, not SHIP")
        if current_round.get("head") != manifest.get("head"):
            errors.append("state round HEAD differs from manifest reviewed HEAD")

    active_defects = [
        finding for finding in ledger.get("findings", [])
        if finding.get("round_status") in {"new", "duplicate"}
    ]
    if active_defects:
        errors.append(f"{len(active_defects)} open defect(s) remain in findings.json")
    lingering = [
        fingerprint for fingerprint, row in state.get("ledger", {}).items()
        if row.get("result_kind") == "defect" and row.get("status") == "open"
    ]
    if lingering:
        errors.append(f"{len(lingering)} defect(s) remain open in state.json")
    reconciliation = ledger.get("reconciliation", {})
    if reconciliation.get("unconfirmed_defects"):
        errors.append("prior defects lack explicit independent resolution certification")
    if reconciliation.get("still_open_unreviewed"):
        errors.append("prior findings remain unreviewed")

    for job in jobs:
        try:
            validate_job_output(repo, out, job)
        except ValueError as error:
            errors.append(str(error))
    if manifest.get("counts", {}).get("selected", 0) and not any(
        job.get("label") == "sweep-verdict-audit" for job in jobs
    ):
        errors.append("mandatory sweep-verdict-audit job is missing")

    coverage = ledger.get("review_stats", {}).get("coverage", {}).get("lanes", {})
    for lane in ("defect", "polish"):
        if not coverage.get(lane, {}).get("complete"):
            errors.append(f"{lane} hunk coverage is incomplete")

    if errors:
        for error in errors:
            sys.stderr.write(f"approval refused: {error}\n")
        return 1

    approval = {
        "policy_version": POLICY_VERSION,
        "target": manifest["target"],
        "round": manifest["round"],
        "base": manifest["base"],
        "head": manifest["head"],
        "worktree_snapshot": manifest["worktree_snapshot"],
        "verdict": "SHIP",
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "freeze": "pass",
            "jobs": "pass",
            "coverage": "pass",
            "open_defects": 0,
            "prior_defects": "explicitly reconciled",
        },
    }
    write_json(out / "approval.json", approval)
    print(f"approval -> {out / 'approval.json'}")
    print(f"verdict=SHIP policy={POLICY_VERSION} head={manifest['head']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
