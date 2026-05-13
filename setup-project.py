import os

folders = [
    "app/core",
    "app/services",
    "app/api",
    "app/models",
    "tests",
    "data/raw",
    "data/processed",
    "scripts"
]

files = [
    "app/main.py",
    "app/core/config.py",
    ".env",
    ".gitignore",
    "README.md",
    "requirements.txt"
]

def create_structure():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        # Create an __init__.py to make it a package
        with open(os.path.join(folder, "__init__.py"), "w") as f:
            pass
            
    for file in files:
        if not os.path.exists(file):
            with open(file, "w") as f:
                if file == ".gitignore":
                    f.write(".env\n__pycache__/\ndata/\n.venv/\n")
                elif file == "README.md":
                    f.write("# Legal Intelligence Engine\n\n2026 Production-grade Contract Auditor.")

    print("✅ Project structure created successfully!")

if __name__ == "__main__":
    create_structure()