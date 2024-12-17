
# check.py
# This script checks the configuration for ID: V-2225
# Description: No description provided
import os
import re

APACHE_CONFIG_PATH = os.getenv('APACHE_CONFIG_PATH', '/etc/apache2/httpd.conf')

def check():
    """Checks if the directive Disable is set correctly."""
    if not os.path.exists(APACHE_CONFIG_PATH):
        print(f"Error: Configuration file not found at {APACHE_CONFIG_PATH}")
        return False

    with open(APACHE_CONFIG_PATH, "r") as file:
        content = file.read()

    match = re.search(r"^\s*CSH_MIME=false\s+(\d+)", content, re.MULTILINE)
    
    if match:
        return True  # The value meets the recommended size
    return False  # Directive not set

if __name__ == "__main__":
    result = check()
    print("Check passed:", result)
