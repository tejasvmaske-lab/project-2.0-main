#!/usr/bin/env python3
"""
Script to remove exposed credentials from git history.
Run: python clean_history.py
"""
import subprocess
import sys
import os

# Load the password from environment variable (set in .env)
EXPOSED_PASSWORD = os.getenv('DB_PASSWORD', '')

if not EXPOSED_PASSWORD:
    print("Error: DB_PASSWORD environment variable not set. Please set it in your .env file.")
    sys.exit(1)

try:
    print("🔄 Cleaning git history of exposed credentials...")
    # Use git filter-repo if available, otherwise filter-branch
    cmd = [
        "git", "filter-repo",
        "--replace-text", f".gitignore::{EXPOSED_PASSWORD}==>",
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Git history cleaned successfully!")
        print("✓ Run: git push --force-with-lease")
    else:
        # Fallback to filter-branch
        print("⚠ git filter-repo not found, using filter-branch...")
        cmd = [
            "git", "filter-branch", "-f",
            "--tree-filter",
            f'python -c "import sys; content = open(\'init_db.py\').read(); open(\'init_db.py\', \'w\').write(content.replace(\'{EXPOSED_PASSWORD}\', \'os.getenv(\\\"DB_PASSWORD\\\")\'))"',
            "--all"
        ]
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
