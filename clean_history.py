#!/usr/bin/env python3
"""
Script to remove exposed credentials from git history.
Run: python clean_history.py
"""
import subprocess
import sys

# The exposed password to remove
EXPOSED_PASSWORD = "AVNS_8yo1YBfIXZSH3v1fXIz"

try:
    print("🔄 Cleaning git history of exposed credentials...")
    # Use git filter-repo if available, otherwise filter-branch
    cmd = [
        "git", "filter-repo",
        "--replace-text", f".gitignore::AVNS_8yo1YBfIXZSH3v1fXIz==>",
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
