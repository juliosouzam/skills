"""Regression tests for the strict Deep Review approval policy."""

from __future__ import annotations

import sys
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from _common import POLICY_VERSION, findings_contract_errors, freeze_snapshot  # noqa: E402
from merge_findings import reconcile  # noqa: E402


def payload(*, suppressions=None, resolutions=None):
    return {
        "defects": [],
        "advisories": [],
        "suppressions": suppressions or [],
        "resolutions": resolutions or [],
        "coverage": {"hunks": [], "rules": []},
    }


class StrictPolicyTests(unittest.TestCase):
    def test_policy_version_is_bumped_for_strict_artifacts(self):
        self.assertEqual(POLICY_VERSION, 2)

    def test_suppression_requires_a_causal_refutation_and_corroboration(self):
        invalid = payload(suppressions=[{
            "file": "src/example.py",
            "line": 3,
            "hunk": "new:1-4",
            "candidate": "might fail",
            "reason": "speculative",
            "rule_ids": [],
            "note": "This does not include a sufficiently specific explanation.",
            "evidence": ["it seemed fine"],
        }])
        errors = findings_contract_errors(invalid)
        self.assertTrue(errors)
        self.assertIn("evidence", "; ".join(errors))

    def test_prior_defect_is_not_resolved_merely_because_its_file_is_selected(self):
        fingerprint = "a" * 16
        prior = {
            "ledger": {
                fingerprint: {
                    "file": "src/example.py",
                    "title": "Preserve caller failure",
                    "severity": "minor",
                    "result_kind": "defect",
                    "status": "open",
                    "round": 1,
                }
            }
        }
        result = reconcile([], set(), prior, [], {"src/example.py"}, {"src/example.py"})
        self.assertEqual(result["resolved"], [])
        self.assertEqual(result["unconfirmed_defects"], [fingerprint])

    def test_prior_defect_requires_explicit_resolution_certificate_row(self):
        fingerprint = "b" * 16
        prior = {
            "ledger": {
                fingerprint: {
                    "file": "src/example.py",
                    "title": "Preserve caller failure",
                    "severity": "minor",
                    "result_kind": "defect",
                    "status": "open",
                    "round": 1,
                }
            }
        }
        result = reconcile(
            [], set(), prior,
            [{"fingerprint": fingerprint, "status": "resolved", "evidence": ["x", "y"]}],
            {"src/example.py"}, {"src/example.py"},
        )
        self.assertEqual(result["resolved"], [fingerprint])
        self.assertEqual(result["unconfirmed_defects"], [])

    def test_approval_verifier_accepts_only_a_clean_frozen_round(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "review@example.test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Deep Review Test"], cwd=repo, check=True)
            (repo / "example.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "example.py"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()

            out = repo / ".deep-review" / "fixture"
            agents = out / "agents"
            agents.mkdir(parents=True)
            snapshot = freeze_snapshot(repo, out)
            manifest = {
                "policy_version": POLICY_VERSION,
                "target": "fixture",
                "round": 1,
                "base": head,
                "head": head,
                "worktree_snapshot": snapshot,
                "counts": {"selected": 1},
                "files": [{"path": "example.py", "disposition": "selected", "hunks": [{"start": 1, "lines": 1, "side": "new"}]}],
            }
            hunk = {"file": "example.py", "hunk": "new:1-1"}
            jobs = []
            for label, lane, check in (("cohort-fixture", "defect", "defect"), ("polish-fixture", "polish", "polish"), ("sweep-verdict-audit", "audit", "audit")):
                output = f".deep-review/fixture/agents/{label}.json"
                jobs.append({
                    "label": label, "kind": "sweep" if lane == "audit" else "cohort",
                    "lane": lane, "coverage_check": check, "required_hunks": [hunk],
                    "rule_ids": [], "required_resolutions": [], "prompt": "unused", "output": output,
                })
                (repo / output).write_text(json.dumps(payload() | {
                    "coverage": {"hunks": [{**hunk, "checks": [check], "outcome": "clear"}], "rules": []},
                }), encoding="utf-8")
            (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (out / "jobs.json").write_text(json.dumps({"jobs": jobs}), encoding="utf-8")
            (out / "findings.json").write_text(json.dumps({
                "source_snapshot": snapshot, "findings": [], "advisories": [], "suppressions": [],
                "resolutions": [], "reconciliation": {"resolved": [], "still_open_unreviewed": [], "unconfirmed_defects": []},
                "review_stats": {"coverage": {"lanes": {"defect": {"complete": True}, "polish": {"complete": True}}}},
            }), encoding="utf-8")
            (out / "state.json").write_text(json.dumps({
                "policy_version": POLICY_VERSION, "target": "fixture", "ledger": {},
                "rounds": [{"n": 1, "head": head, "verdict": "SHIP"}],
            }), encoding="utf-8")
            (out / "review.md").write_text("**Verdict: SHIP** — clean\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "verify_approval.py"), "--out", str(out)],
                cwd=repo, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((out / "approval.json").is_file())

            ledger = json.loads((out / "findings.json").read_text(encoding="utf-8"))
            ledger["findings"] = [{"round_status": "new"}]
            (out / "findings.json").write_text(json.dumps(ledger), encoding="utf-8")
            rejected = subprocess.run(
                [sys.executable, str(SCRIPTS / "verify_approval.py"), "--out", str(out)],
                cwd=repo, text=True, capture_output=True,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("open defect", rejected.stderr)

    def test_job_builder_injects_an_adversarial_full_hunk_audit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "review@example.test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Deep Review Test"], cwd=repo, check=True)
            (repo / "example.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "example.py"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()

            out = repo / ".deep-review" / "fixture"
            out.mkdir(parents=True)
            manifest = {
                "policy_version": POLICY_VERSION, "target": "fixture", "base": head,
                "head": head, "diff_command": "git diff", "counts": {"selected": 1},
                "files": [{"path": "example.py", "disposition": "selected", "status": "M", "adds": 1, "dels": 0,
                           "hunks": [{"start": 1, "lines": 1, "side": "new"}]}],
            }
            (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (out / "knowledge.json").write_text(json.dumps({"selected_paths": ["example.py"], "sources": []}), encoding="utf-8")
            (out / "rules.json").write_text(json.dumps({"sources": [], "rules": []}), encoding="utf-8")
            (out / "plan.json").write_text(json.dumps({"cohorts": [{"id": "unit", "name": "Unit", "risk": "normal", "files": ["example.py"]}], "sweeps": []}), encoding="utf-8")
            (out / "context-pack.md").write_text("# Context\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_jobs.py"), "--out", str(out)],
                cwd=repo, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            jobs = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"]
            audit = next(job for job in jobs if job["label"] == "sweep-verdict-audit")
            self.assertEqual(audit["lane"], "audit")
            self.assertEqual(audit["coverage_check"], "audit")
            self.assertEqual(audit["required_hunks"], [{"file": "example.py", "hunk": "new:1-1"}])
            self.assertEqual(audit["depends_on"], ["cohort-unit", "polish-unit-p01"])

    def test_renderer_refuses_ship_when_only_a_minor_defect_is_open(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "review@example.test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Deep Review Test"], cwd=repo, check=True)
            (repo / "example.py").write_text("pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "example.py"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()

            out = repo / ".deep-review" / "fixture"
            agents = out / "agents"
            agents.mkdir(parents=True)
            snapshot = freeze_snapshot(repo, out)
            hunk = {"file": "example.py", "hunk": "new:1-1"}
            manifest = {
                "policy_version": POLICY_VERSION, "target": "fixture", "round": 1,
                "base": head, "head": head, "worktree_snapshot": snapshot,
                "counts": {"selected": 1}, "files": [{"path": "example.py", "disposition": "selected", "hunks": [{"start": 1, "lines": 1, "side": "new"}]}],
            }
            jobs = []
            for label, lane, check in (("cohort-fixture", "defect", "defect"), ("polish-fixture", "polish", "polish"), ("sweep-verdict-audit", "audit", "audit")):
                output = f".deep-review/fixture/agents/{label}.json"
                jobs.append({
                    "label": label, "kind": "sweep" if lane == "audit" else "cohort",
                    "lane": lane, "coverage_check": check, "required_hunks": [hunk],
                    "rule_ids": [], "required_resolutions": [], "prompt": "unused", "output": output,
                })
                (repo / output).write_text(json.dumps(payload() | {
                    "coverage": {"hunks": [{**hunk, "checks": [check], "outcome": "clear"}], "rules": []},
                }), encoding="utf-8")
            minor = {
                "result_kind": "defect", "round_status": "new", "severity": "minor",
                "category": "potential-issue", "file": "example.py", "line": 1,
                "in_diff": True, "hunk": "new:1-1", "quick_win": False,
                "title": "Minor defect", "body": "A concrete narrow defect remains.",
                "rule_ids": [], "evidence": ["Premise: example.py:1 is wrong → Path: caller reaches it → Verdict: narrow failure"],
                "fingerprint": "c" * 16, "source_jobs": ["cohort-fixture"], "raw_ids": ["RD0001"],
            }
            (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (out / "jobs.json").write_text(json.dumps({"jobs": jobs}), encoding="utf-8")
            (out / "rules.json").write_text(json.dumps({"rules": []}), encoding="utf-8")
            (out / "context-pack.md").write_text("# Context\n", encoding="utf-8")
            (out / "walkthrough.md").write_text(
                "<!-- deep-review:walkthrough -->\n## Walkthrough\n## Changes\n## Estimated code review effort\n## Review details\n",
                encoding="utf-8",
            )
            (out / "findings.json").write_text(json.dumps({
                "source_snapshot": snapshot, "findings": [minor], "advisories": [], "suppressions": [], "resolutions": [],
                "summary": {"merged_raw": 0}, "reconciliation": {"resolved": [], "still_open_unreviewed": [], "unconfirmed_defects": []},
                "review_stats": {"candidates": 1, "reported": 1, "suppressed": 0, "coverage": {"selected_hunk_lines": 1}},
            }), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "render_review.py"), "--out", str(out)],
                cwd=repo, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            review = (out / "review.md").read_text(encoding="utf-8")
            self.assertIn("**Verdict: FIX_BEFORE_SHIP**", review)
            self.assertNotIn("**Verdict: SHIP**", review)


if __name__ == "__main__":
    unittest.main()
