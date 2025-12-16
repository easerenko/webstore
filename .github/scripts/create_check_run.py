#!/usr/bin/env python
import argparse
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests


CHECKS_API_URL = "https://api.github.com/repos/{owner}/{repo}/check-runs"
API_VERSION = "2022-11-28"


def parse_junit(report_path: Path):
    if not report_path.is_file():
        print(f"::warning ::JUnit report not found at {report_path}")
        return None, None

    tree = ET.parse(report_path)
    root = tree.getroot()

    suites = []
    if root.tag == "testsuite":
        suites = [root]
    else:
        suites = root.findall(".//testsuite")

    total = failures = errors = skipped = 0
    failed_tests = []

    for suite in suites:
        total += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
        skipped += int(suite.attrib.get("skipped", 0))

        for case in suite.findall("testcase"):
            name = case.attrib.get("name", "")
            classname = case.attrib.get("classname", "")
            failure = case.find("failure")
            error = case.find("error")
            if failure is not None or error is not None:
                msg = ""
                node = failure or error
                if node is not None:
                    msg = (node.attrib.get("message", "") or "").strip()
                    if not msg and node.text:
                        msg = node.text.strip()
                failed_tests.append(
                    {
                        "name": name,
                        "classname": classname,
                        "message": msg or "Test failed",
                    }
                )

    passed = total - failures - errors - skipped
    stats = {
        "total": total,
        "passed": passed,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
    }
    return stats, failed_tests


def build_output(stats, failed_tests, check_name: str):
    total = stats["total"]
    passed = stats["passed"]
    failures = stats["failures"]
    errors = stats["errors"]
    skipped = stats["skipped"]

    title = f"{check_name}: {passed}/{total} passed"
    summary_lines = [
        f"**Total**: {total}",
        f"**Passed**: {passed}",
        f"**Failed**: {failures}",
        f"**Errors**: {errors}",
        f"**Skipped**: {skipped}",
    ]

    details_lines = []
    if failed_tests:
        details_lines.append("\n### Failed tests:\n")
        for t in failed_tests[:20]:
            details_lines.append(
                f"- `{t['classname']}.{t['name']}` – {t['message']}"
            )
        if len(failed_tests) > 20:
            details_lines.append(
                f"\n… и ещё {len(failed_tests) - 20} падений."
            )

    output = {
        "title": title,
        "summary": "\n".join(summary_lines),
        "text": "\n".join(details_lines) if details_lines else "",
    }

    conclusion = "success"
    if failures or errors:
        conclusion = "failure"

    return output, conclusion


def create_check_run(name: str, output: dict, conclusion: str):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("::error ::GITHUB_TOKEN is not set")
        sys.exit(1)

    repo_full = os.environ.get("GITHUB_REPOSITORY")
    if not repo_full:
        print("::error ::GITHUB_REPOSITORY is not set")
        sys.exit(1)
    owner, repo = repo_full.split("/")

    head_sha = os.environ.get("GITHUB_SHA")
    if not head_sha:
        print("::error ::GITHUB_SHA is not set")
        sys.exit(1)

    url = CHECKS_API_URL.format(owner=owner, repo=repo)

    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    payload = {
        "name": name,
        "head_sha": head_sha,
        "status": "completed",
        "conclusion": conclusion,
        "completed_at": now_iso,
        "output": output,
    }

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
    }

    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    if resp.status_code >= 300:
        print(f"::error ::Failed to create check run: {resp.status_code} {resp.text}")
        sys.exit(1)
    else:
        data = resp.json()
        html_url = data.get("html_url")
        print(f"Created check run: {html_url}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, help="Path to JUnit XML report")
    parser.add_argument("--name", default="Tests", help="Check run name")
    args = parser.parse_args()

    report_path = Path(args.report)
    stats, failed_tests = parse_junit(report_path)
    if not stats:
        output = {
            "title": f"{args.name}: no report",
            "summary": "JUnit report not found.",
            "text": "",
        }
        create_check_run(args.name, output, "neutral")
        return

    output, conclusion = build_output(stats, failed_tests, args.name)
    create_check_run(args.name, output, conclusion)


if __name__ == "__main__":
    main()
