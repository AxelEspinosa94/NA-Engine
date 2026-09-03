import subprocess


def get_git_version():
    try:
        version = (
            subprocess.check_output(
                ["git", "describe", "--tags"], stderr=subprocess.STDOUT
            )
            .decode()
            .strip()
        )

        # cortar todo después del primer "-"
        clean = version.split("-")[0]
        return clean

    except Exception:
        return "dev"
