# standard library
import subprocess
import traceback


def print_TODOs():
    try:
        common_args = (
            "rg",
            "--word-regexp",
            "--pretty",
        )
        pattern = "T" + "ODO|FIXM" + "E"  # Prevent searching itself
        subprocess.run((*common_args, "--ignore-file=project/.todoignore", pattern))
        subprocess.run((*common_args, "--glob=*.env*", pattern))
        # Run twice because of unoverridable precedences  https://github.com/BurntSushi/ripgrep/issues/1734#issuecomment-730769439
    except Exception:
        # Continue instead of breaking runserver
        print(traceback.format_exc())
