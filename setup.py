import os
import subprocess
import sys


def create_project():
    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", "venv"])

    # Activate virtual environment and install requirements
    if os.name == "nt":  # Windows
        subprocess.run(["venv\\Scripts\\pip", "install", "-r", "requirements.txt"])
        subprocess.run(["venv\\Scripts\\django-admin", "startproject", "lms", "."])
    else:  # Unix/Linux/MacOS
        subprocess.run(
            [
                "source",
                "venv/bin/activate",
                "&&",
                "pip",
                "install",
                "-r",
                "requirements.txt",
            ],
            shell=True,
        )
        subprocess.run(
            [
                "source",
                "venv/bin/activate",
                "&&",
                "django-admin",
                "startproject",
                "lms",
                ".",
            ],
            shell=True,
        )

    # Create necessary directories
    directories = [
        "core",
        "courses",
        "users",
        "blog",
        "payments",
        "static",
        "templates",
        "media",
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        if directory not in ["static", "templates", "media"]:
            # Create __init__.py in each app directory
            with open(os.path.join(directory, "__init__.py"), "w") as f:
                pass


if __name__ == "__main__":
    create_project()
