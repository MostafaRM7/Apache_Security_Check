import os

# Root directory containing the scripts
root_dir = "../scripts"

# Output file to combine all functions
output_file = "../combined_scripts.py"


def merge_scripts(root_dir, output_file):
    with open(output_file, "w", encoding="utf-8") as outfile:
        for folder_name in sorted(os.listdir(root_dir)):
            folder_path = os.path.join(root_dir, folder_name)

            # Check if the item is a directory
            if os.path.isdir(folder_path):
                for script_name in ["check.py", "fix.py"]:
                    script_path = os.path.join(folder_path, script_name)

                    # Check if the script file exists
                    if os.path.isfile(script_path):
                        # Write folder and file name as a comment
                        outfile.write(f"\n# --- {folder_name}/{script_name} ---\n")

                        # Read and append the file content
                        with open(script_path, "r", encoding="utf-8") as infile:
                            for line in infile:
                                outfile.write(line)
                        outfile.write("\n")


if __name__ == "__main__":
    merge_scripts(root_dir, output_file)
    print(f"All scripts have been combined into {output_file}")
