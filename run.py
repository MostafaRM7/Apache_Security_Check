import os
import subprocess

from openpyxl import Workbook


def run_checks_and_fixes():
    # Base directory where the checks and fixes are located
    base_directory = "scripts/"

    # Prepare a workbook for storing results
    wb = Workbook()
    ws = wb.active
    ws.title = "Check and Fix Results"
    ws.append(["id", "status", "fix run status"])

    # Iterate through all subdirectories in the base directory
    for subdir in os.listdir(base_directory):
        check_path = os.path.join(base_directory, subdir, "check.py")
        fix_path = os.path.join(base_directory, subdir, "fix.py")
        # print(f"Checking {subdir}...")
        # Run the check script
        if os.path.exists(check_path):
            check_result = subprocess.run(["python3", check_path], capture_output=True, text=True)
            print(check_result.stdout)
            if "Check passed: True" in check_result.stdout:
                ws.append([subdir, "pass", None])
            else:
                # If check fails, run the fix script
                if os.path.exists(fix_path):
                    fix_result = subprocess.run(["python3", fix_path], capture_output=True, text=True)
                    ws.append([subdir, "fail", "ran"])
                else:
                    ws.append([subdir, "fail", "fix script missing"])
        else:
            ws.append([subdir, "missing check script", None])

    # Save the results to an Excel file
    output_excel_path = "check_and_fix_results.xlsx"
    wb.save(output_excel_path)
    print(f"Results saved to {output_excel_path}")


if __name__ == "__main__":
    run_checks_and_fixes()