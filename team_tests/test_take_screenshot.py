"""Team 13 tests for take_screenshot().

Run from the repository folder:
    python3 team_tests/test_take_screenshot.py
"""

import os
import sys

# Let Python find browser_tools.py in the folder above team_tests/.
REPO_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_FOLDER)
os.chdir(REPO_FOLDER)

import browser_tools as tools

SITE_URL = "https://onyourmark.github.io/browser-agent-form/travel/"

# Every real PNG file starts with these 8 bytes.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_png_file(path):
    """Independent check: look at the file itself, not the tool's result.

    Returns (True, reason) if the file is a real, nonempty PNG,
    otherwise (False, reason).
    """
    # Check 1: does the file exist?
    if not os.path.exists(path):
        return False, "file does not exist"

    # Check 2: is the file empty?
    size = os.path.getsize(path)
    if size == 0:
        return False, "file is empty"

    # Check 3: is it really a PNG image?
    with open(path, "rb") as image_file:
        first_bytes = image_file.read(8)
    if first_bytes != PNG_SIGNATURE:
        return False, "file is not a PNG image"

    return True, "real PNG file, " + str(size) + " bytes"


def test_success():
    print("=== Test 1: screenshot of the search page ===")

    # Setup (not the graded tool): open the practice website.
    tools.open_site()

    # Call the tool.
    print("Call: take_screenshot()")
    result = tools.take_screenshot()
    print("Returned observation:", result)

    # Independent check of the real file on disk.
    ok, reason = check_png_file(result["screenshot"])
    print("File evidence:", reason)

    if ok:
        print("PASS: the returned path points to a real, nonempty PNG file")
    else:
        print("FAIL: the screenshot file is not valid")
    print()
    return ok

def test_wrong_path():
    print("=== Test 2: wrong / missing screenshot path ===")

    # Take a real screenshot first, so we know the tool itself works.
    result = tools.take_screenshot()
    real_path = result["screenshot"]

    # Deliberately change the path to one that was never saved.
    wrong_path = real_path.replace(".png", "_missing.png")
    print("Checking deliberately wrong path:", wrong_path)

    # The independent check must NOT report success for this path.
    ok, reason = check_png_file(wrong_path)
    print("File evidence:", reason)

    if ok:
        print("FAIL: the check accepted a file that does not exist")
        print()
        return False

    print("PASS: the check correctly reported the missing file as a failure")
    print()
    return True

def main():
    # Start the browser once, run both tests, then always close it.
    tools.start_browser()
    try:
        passed_1 = test_success()
        passed_2 = test_wrong_path()
    finally:
        tools.close_browser()

    print("=== Summary ===")
    if passed_1:
        print("Test 1 success case: PASS")
    else:
        print("Test 1 success case: FAIL")
    if passed_2:
        print("Test 2 failure case: PASS")
    else:
        print("Test 2 failure case: FAIL")

    # Exit with an error code if any test failed, so automated runs notice.
    if not (passed_1 and passed_2):
        sys.exit(1)


if __name__ == "__main__":
    main()