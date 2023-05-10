import project


def build_info(request):
    """
    Context processor that provides Git commit and build time into the context.
    """

    return {
        "build_info": {
            "git_commit": project._GIT_COMMIT,
            "build_time": project._BUILD_TIME,
        }
    }
