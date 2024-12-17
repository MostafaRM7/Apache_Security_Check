import os
import subprocess
import pandas as pd
from tqdm import tqdm


def run_checks_and_fixes(csv_file_path):
    # Base directory where the checks and fixes are located
    base_directory = "scripts/"

    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Ensure result columns exist in the DataFrame
    if "status" not in df.columns:
        df["status"] = None
    if "fix run status" not in df.columns:
        df["fix run status"] = None

    # Iterate through all subdirectories in the base directory
    for subdir in tqdm(os.listdir(base_directory), desc="Checking and fixing...", colour="blue", unit="script"):
        check_path = os.path.join(base_directory, subdir, "check.py")
        fix_path = os.path.join(base_directory, subdir, "fix.py")

        # Find the row in the DataFrame that matches the folder name (e.g., V-XXXX)
        issue_row = df[df['id'] == subdir]

        if not issue_row.empty:
            idx = issue_row.index[0]  # Get the index of the matching row

            if os.path.exists(check_path):
                # Run the check script
                check_result = subprocess.run(["python3", check_path], capture_output=True, text=True)
                if "Check passed: True" in check_result.stdout:
                    df.at[idx, "status"] = "pass"
                    df.at[idx, "fix run status"] = None
                else:
                    # Run the fix script if the check failed
                    if os.path.exists(fix_path):
                        subprocess.run(["python3", fix_path], capture_output=True, text=True)
                        df.at[idx, "status"] = "fail"
                        df.at[idx, "fix run status"] = "ran"
                    else:
                        df.at[idx, "status"] = "fail"
                        df.at[idx, "fix run status"] = "fix script missing"
            else:
                df.at[idx, "status"] = "missing check script"
                df.at[idx, "fix run status"] = None

    # Save the updated CSV file
    output_csv_path = "updated_results.csv"
    df.to_csv(output_csv_path, index=False)
    print(f"Results saved to {output_csv_path}")


if __name__ == "__main__":
    csv_file_path = "APACHE_2_2_Server_for_UNIX_Security_Technical_Implementation_Guide (2).csv"
    run_checks_and_fixes(csv_file_path)