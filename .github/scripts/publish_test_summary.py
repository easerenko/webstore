#!/usr/bin/env python
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_junit(path: Path):
    if not path.is_file():
        print(f"::warning ::JUnit report not found at {path}")
        return None

    tree = ET.parse(path)
    root = tree.getroot()

    total = 0
    failures = 0
    errors = 0
    skipped = 0

    suites = []
    if root.tag == "testsuite":
        suites = [root]
    else:
        suites = root.findall(".//testsuite")

    for suite in suites:
        total += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
        skipped += int(suite.attrib.get("skipped", 0))

    passed = total - failures - errors - skipped
    return {
        "total": total,
        "passed": passed,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
    }

def annotate_failures(root):
    for tc in root.findall(".//testcase"):
        failure = tc.find("failure")
        error = tc.find("error")
        if failure is None and error is None:
            continue

        classname = tc.attrib.get("classname", "")
        name = tc.attrib.get("name", "")
        message = (failure or error).attrib.get("message", "").strip()

        file_hint = classname.replace(".", "/") + ".py" if classname else ""
        title = f"Test failed: {name}"

        print(f"::error title={title} ::{classname}.{name} - {message or 'test failed'}")

def main():
    if len(sys.argv) < 2:
        print("Usage: publish_test_summary.py junit/test-results.xml")
        sys.exit(1)

    report_path = Path(sys.argv[1])
    root = ET.parse(report_path).getroot()
    stats = parse_junit(report_path)
    annotate_failures(root)

    if not stats:
        return

    total = stats["total"]
    passed = stats["passed"]
    failures = stats["failures"]
    errors = stats["errors"]
    skipped = stats["skipped"]

    print()
    print("=== TEST SUMMARY ===")
    print(f"Total:    {total}")
    print(f"Passed:   {passed} ✅")
    print(f"Failed:   {failures} ❌")
    print(f"Errors:   {errors} ❌")
    print(f"Skipped:  {skipped} 💤")
    print("====================")
    print()

    summary = f"""# ✅ Test Summary

- **Total**: `{total}`
- **Passed**: `{passed}`
- **Failed**: `{failures}`
- **Errors**: `{errors}`
- **Skipped**: `{skipped}`
"""

    summary_file = Path.cwd() / os.environ.get("GITHUB_STEP_SUMMARY", "")
    if summary_file.parent.exists():
        summary_file.write_text(summary, encoding="utf-8")
    else:
        print(summary)

if __name__ == "__main__":
    import os
    main()
