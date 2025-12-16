#!/usr/bin/env python
import argparse
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional

import requests

CHECKS_API_URL = "https://api.github.com/repos/{owner}/{repo}/check-runs"
ANNOTATIONS_URL = "https://api.github.com/repos/{owner}/{repo}/check-runs/{check_run_id}/annotations"
API_VERSION = "2022-11-28"


def parse_junit(report_path: Path) -> tuple[Optional[dict], List[Dict]]:
    """
    Парсинг JUnit XML
    """
    if not report_path.is_file():
        print(f"::warning ::JUnit report not found at {report_path}")
        return None, []

    tree = ET.parse(report_path)
    root = tree.getroot()

    suites = []
    if root.tag == "testsuite":
        suites = [root]
    else:
        suites = root.findall(".//testsuite")

    total = failures = errors = skipped = 0
    annotations = []

    for suite in suites:
        total += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
        skipped += int(suite.attrib.get("skipped", 0))

        for case in suite.findall("testcase"):
            name = case.attrib.get("name", "unknown")
            classname = case.attrib.get("classname", "")

            failure = case.find("failure")
            error = case.find("error")

            if failure is not None or error is not None:
                file_path = classname.split(".")[-1] + ".py" if classname else "test_file.py"

                message_elem = failure or error
                message = message_elem.attrib.get("message", "").strip()
                if not message and message_elem.text:
                    message = message_elem.text.strip()[:500]

                annotations.append({
                    "path": file_path,
                    "start_line": 1,
                    "end_line": 1,
                    "start_column": 0,
                    "end_column": 80,
                    "annotation_level": "failure",
                    "title": name,
                    "message": message or "Test failed"
                })

            # message = "Test failed"
            # if failure is not None:
            #     message = failure.attrib.get("message", "").strip()
            #     if not message and failure.text:
            #         message = failure.text.strip()[:1000]
            # elif error is not None:
            #     message = error.attrib.get("message", "").strip()
            #     if not message and error.text:
            #         message = error.text.strip()[:1000]
            #
            # if failure is not None or error is not None:
            #     file_path = classname.split(".")[-1] + ".py" if classname else "test_file.py"
            #
            #     annotations.append({
            #         "path": file_path,
            #         "start_line": 1,
            #         "end_line": 1,
            #         "start_column": 0,
            #         "end_column": 0,
            #         "annotation_level": "failure",
            #         "title": name,
            #         "message": message,
            #         "raw_details": f"{classname}.{name}"
            #     })

    passed = total - failures - errors - skipped
    stats = {
        "total": total,
        "passed": passed,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
    }
    return stats, annotations


def create_check_run_step1(name: str, head_sha: str, owner: str, repo: str) -> int:
    """
    Создание Check Run со статусом in_progress и возвращает ID
    """
    token = os.environ.get("GITHUB_TOKEN")
    url = CHECKS_API_URL.format(owner=owner, repo=repo)

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
    }

    payload = {
        "name": name,
        "head_sha": head_sha,
        "status": "in_progress",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    data = resp.json()
    print(f"✅ Created check run: {data['html_url']} (ID: {data['id']})")
    return data["id"]


# def add_annotations(check_run_id: int, annotations: List[Dict], owner: str, repo: str):
#     """
#     Добавление annotations к Check Run
#     """
#     if not annotations:
#         return
#
#     token = os.environ.get("GITHUB_TOKEN")
#     url = ANNOTATIONS_URL.format(owner=owner, repo=repo, check_run_id=check_run_id)
#
#     headers = {
#         "Accept": "application/vnd.github+json",
#         "Authorization": f"Bearer {token}",
#         "X-GitHub-Api-Version": API_VERSION,
#     }
#
#     for i in range(0, len(annotations), 50):
#         batch = annotations[i:i + 50]
#         resp = requests.post(url, headers=headers, json=batch)
#         if resp.status_code >= 300:
#             print(f"::warning ::Failed to add annotations batch: {resp.status_code}")
#         else:
#             print(f"✅ Added {len(batch)} annotations")

def add_annotations(check_id, annotations, owner, repo, max_retries=3):
    """Add annotations с retry"""
    url = f"https://api.github.com/repos/{owner}/{repo}/check-runs/{check_id}/annotations"
    token = os.environ.get("GITHUB_TOKEN")

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=annotations[:10], headers={"Authorization": f"token {token}"})

            if response.status_code == 201:
                print(f"✅ Added {len(annotations)} annotations")
                return
            else:
                print(f"⚠️ Attempt {attempt + 1}: {response.status_code}")
                time.sleep(2 ** attempt)  # exponential backoff

        except Exception as e:
            print(f"❌ Annotation error: {e}")
            time.sleep(2)

    print("⚠️ Failed to add annotations after retries")


def update_check_run(check_run_id: int, output: dict, conclusion: str, owner: str, repo: str):
    """
    Завершение Check Run
    """
    token = os.environ.get("GITHUB_TOKEN")
    url = f"{CHECKS_API_URL.format(owner=owner, repo=repo)}/{check_run_id}"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
    }

    payload = {
        "status": "completed",
        "conclusion": conclusion,
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "output": output,
    }

    resp = requests.patch(url, headers=headers, json=payload)
    resp.raise_for_status()
    print(f"✅ Check run completed: {conclusion}")


def build_output(stats: dict, failed_count: int, check_name: str) -> tuple[dict, str]:
    total = stats["total"]
    passed = stats["passed"]
    failures = stats["failures"]
    errors = stats["errors"]
    skipped = stats["skipped"]

    title = f"{check_name}: {passed}/{total}"
    summary = f"""**Results**: {passed}/{total} passed
        **Failed**: {failures} | **Errors**: {errors} | **Skipped**: {skipped}"""

    conclusion = "success" if failures == 0 and errors == 0 else "failure"

    output = {
        "title": title,
        "summary": summary,
        "text": f"See annotations for detailed failures ({failed_count} failed tests)."
    }
    return output, conclusion


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, help="Path to JUnit XML")
    parser.add_argument("--name", default="Tests", help="Check run name")
    args = parser.parse_args()

    owner, repo = os.environ["GITHUB_REPOSITORY"].split("/")
    head_sha = os.environ["GITHUB_SHA"]

    check_id = create_check_run_step1(args.name, head_sha, owner, repo)

    report_path = Path(args.report)
    stats, annotations = parse_junit(report_path)

    if not stats:
        output = {"title": f"{args.name}: no report", "summary": "No JUnit report found"}
        update_check_run(check_id, output, "neutral", owner, repo)
        return

    time.sleep(2)
    add_annotations(check_id, annotations, owner, repo)
    output, conclusion = build_output(stats, len(annotations), args.name)
    update_check_run(check_id, output, conclusion, owner, repo)


if __name__ == "__main__":
    main()
