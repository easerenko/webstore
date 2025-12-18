#!/usr/bin/env python
import sys
import xml.etree.ElementTree as ET
import re

from pathlib import Path


def parse_junit(path: Path):
    """
    Парсинг JUnit XML файла и возврат статистики по тестам
    """
    if not path.is_file():
        print(f"::warning ::JUnit report not found at {path}")
        return None

    tree = ET.parse(path)
    root = tree.getroot()
    test_details = []

    total = 0
    failures = 0
    errors = 0
    skipped = 0

    suites = []
    if root.tag == "testsuite":
        suites = [root]
    else:
        suites = root.findall(".//testsuite")

    total_time = 0.0

    for suite in suites:
        total += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
        skipped += int(suite.attrib.get("skipped", 0))
        total_time += float(suite.attrib.get("time", 0))

        for tc in suite.findall(".//testcase"):
            name = tc.attrib.get("name", "unknown")
            classname = tc.attrib.get("classname", "unknown")
            time = float(tc.attrib.get("time", 0))

            status = "passed"
            if tc.find("failure") is not None:
                status = "failed"
            elif tc.find("error") is not None:
                status = "error"
            elif tc.find("skipped") is not None:
                status = "skipped"

            test_details.append({
                "name": name,
                "classname": classname,
                "time": time,
                "status": status
            })

    passed = total - failures - errors - skipped
    return {
        "total": total,
        "passed": passed,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "test_details": test_details,
        "total_time": total_time
    }


def parse_traceback_line(failure_text: str, filename: str) -> int:
    """
    Извлечение номера строки из traceback в failure
    """
    simple_pattern = rf'{re.escape(filename)}:(\d+):'
    match = re.search(simple_pattern, failure_text)
    if match:
        return int(match.group(1))

    line_pattern = r'line\s+(\d+),'
    match = re.search(line_pattern, failure_text)
    if match:
        return int(match.group(1))

    pattern = rf'File\s+"{re.escape(filename)}",\s*line\s+(\d+),'
    match = re.search(pattern, failure_text)
    if match:
        return int(match.group(1))

    return 1


def normalize_filename(classname: str) -> str:
    """
    Приведение наименования файла к корректному виду, если в наименовании указан тестовый класс
    """
    if not classname or '.' not in classname:
        return "unknown.py"

    parts = classname.split('.')

    i = len(parts) - 1
    while i >= 0:
        if not parts[i].startswith('Test'):
            break
        i -= 1

    if i >= 0:
        base_path = '.'.join(parts[:i + 1])
    else:
        base_path = '.'.join(parts)

    return base_path.replace(".", "/") + ".py"


def annotate_failures(root):
    """
    Публикация аннотации по упавшим тестам
    """
    failure_count = 0
    for tc in root.findall(".//testcase"):
        failure = tc.find("failure")
        error = tc.find("error")

        if failure is None and error is None:
            continue

        if failure is not None:
            failed_element = failure
        elif error is not None:
            failed_element = error
        else:
            print("⚠️ Unexpected: both failure and error are None!")
            continue

        classname = tc.attrib.get("classname", "")
        name = tc.attrib.get("name", "")
        failure_text = ET.tostring(failed_element, encoding='unicode')
        message = failed_element.attrib.get("message", "Test failed").strip()

        raw_time = tc.attrib.get("time", "0")
        try:
            time = float(raw_time)
        except ValueError:
            time = 0.0

        file_hint = normalize_filename(classname)
        time_str = f" ({time:.2f}s)" if time > 0 else ""

        print(f"🔍 DEBUG: parsing '{file_hint}' in '{failure_text[:100]}...'") # DEBUG
        error_line = parse_traceback_line(failure_text, file_hint)
        print(f"   -> found line={error_line}") # DEBUG

        title = f"Test failed: {name}{time_str}"
        print(f"::error title={title} file={file_hint} line={error_line} ::{message}")
        failure_count += 1

    print(f"✅ Annotated {failure_count} failures")


def publication_summary():
    """
    Подготовка отчета о результате выполнения тестов и публикация в summary
    """
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
    test_details = stats["test_details"]
    total_time = stats["total_time"]

    print()
    print("=== TEST SUMMARY ===")
    print(f"Total:    {total}")
    print(f"Passed:   {passed} ✅")
    print(f"Failed:   {failures} ❌")
    print(f"Errors:   {errors} 💥")
    print(f"Skipped:  {skipped} 💤")
    print(f"Duration: {total_time:.2f}s ⏱️")
    print("====================")
    print()

    summary = f"""# ✅ Test Summary

| Metric     | Count | Duration   |
|------------|-------|------------|
| **Total**  | `{total}` **Σ**| `{total_time:.2f}s` ⏱️ |
| **Passed** | `{passed}` ✅|         |
| **Failed** | `{failures}` ❌|       |
| **Errors** | `{errors}` 💥|       |
| **Skipped**| `{skipped}` 💤|      |

**Top 10 slowest tests:**
"""

    slow_tests = sorted(test_details, key=lambda x: x["time"], reverse=True)[:10]
    for test in slow_tests:
        status_emoji = {"passed": "✅", "failed": "❌", "error": "💥", "skipped": "💤"}.get(test["status"], "⚪")
        summary += f"- `{test['classname']}.{test['name']}` **{test['time']:.2f}s** {status_emoji}\n"

    if failures + errors > 0:
        summary += f"\n**Failed tests ({failures + errors}):**\n"
        failed_tests = [t for t in test_details if t["status"] in ["failed", "error"]]
        for test in failed_tests:
            summary += f"- `{test['classname']}.{test['name']}` **{test['time']:.2f}s** ❌\n"

    summary_file = Path.cwd() / os.environ.get("GITHUB_STEP_SUMMARY", "")
    if summary_file.parent.exists():
        summary_file.write_text(summary, encoding="utf-8")
    else:
        print(summary)


if __name__ == "__main__":
    import os
    publication_summary()
