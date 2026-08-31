import subprocess
import sys
import time
import re


def run_tests():

    start_time = time.time()

    try:

        process = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_sample.py",
                "-v",
                "--tb=short"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = process.stdout + "\n" + process.stderr

        # Extract passed tests
        passed_match = re.search(
            r"(\d+)\s+passed",
            output
        )

        # Extract failed tests
        failed_match = re.search(
            r"(\d+)\s+failed",
            output
        )

        # Extract errors
        error_match = re.search(
            r"(\d+)\s+error",
            output
        )

        passed = int(passed_match.group(1)) if passed_match else 0

        failed = int(failed_match.group(1)) if failed_match else 0

        errors = int(error_match.group(1)) if error_match else 0

        total = passed + failed + errors

        execution_time = round(
            time.time() - start_time,
            3
        )

        status = "PASSED"

        if failed > 0 or errors > 0:
            status = "FAILED"

        return {
            "status": status,
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "execution_time": execution_time,
            "output": output
        }

    except subprocess.TimeoutExpired:

        return {
            "status": "ERROR",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "execution_time": round(
                time.time() - start_time,
                3
            ),
            "output": "Test execution timed out."
        }

    except Exception as error:

        return {
            "status": "ERROR",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "execution_time": round(
                time.time() - start_time,
                3
            ),
            "output": str(error)
        }
