import subprocess

def get_git_version():
    try:
        version = subprocess.check_output(
            ["git", "describe", "--tags"],
            stderr=subprocess.STDOUT
        ).decode().strip()
        return version
    except Exception:
        return "dev"
