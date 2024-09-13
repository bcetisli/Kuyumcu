import requests
import os
import subprocess

# Local file and version
local_version = "2.1"
local_file = "github_update.py"
github_url = "https://github.com/bcetisli/Kuyumcu/main/update.json"  # GitHub raw file URL


# Fetch the latest version from GitHub
response = requests.get(github_url)
if response.status_code == 200:
    latest_code = response.text
    # Extract version from the GitHub file (assuming it's at the top)
    latest_version = latest_code.split('\n')[0].replace("# Version:", "").strip()

    # Compare versions
    if latest_version > local_version:
        # Save the new version
        with open(local_file, "w") as f:
            f.write(latest_code)
        print(f"Updated to version {latest_version}")
        
        # Restart the script
        subprocess.run(["python3", local_file])
    else:
        print("Already up-to-date.")
else:
    print("Failed to fetch the latest version.")
