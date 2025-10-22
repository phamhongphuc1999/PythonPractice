import os
import subprocess
from pathlib import Path

# Define source and destination directories
src_root = Path("games")
dst_root = Path("games_cython")

# Folders to ignore during traversal
IGNORED_DIRS = {"venv", "__pycache__", ".git", ".idea", ".vscode"}

dst_root.mkdir(parents=True, exist_ok=True)

for root, dirs, files in os.walk(src_root):
    # Remove ignored dirs from the walk
    dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

    rel_dir = Path(root).relative_to(src_root)
    target_dir = dst_root / rel_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        if not file.endswith(".py"):
            continue

        py_path = Path(root) / file
        c_path = target_dir / file.replace(".py", ".pyx")

        # Skip up-to-date files
        if c_path.exists() and c_path.stat().st_mtime >= py_path.stat().st_mtime:
            print(f"⏩ Skipping {py_path} (up-to-date)")
            continue

        print(f"⚙️ Compiling {py_path} → {c_path}")
        try:
            subprocess.run(
                ["cython", "-3", str(py_path), "-o", str(c_path)],
                check=True,
            )
        except subprocess.CalledProcessError:
            print(f"❌ Failed to compile {py_path}, skipping.")
