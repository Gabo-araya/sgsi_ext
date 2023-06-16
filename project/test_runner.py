class PytestTestRunner:
    """A test runner that delegates its task to pytest."""

    def __init__(  # noqa: PLR0913
        self, verbosity=1, failfast=False, keepdb=False, pdb=False, mark=None, **kwargs
    ):
        self.verbosity = verbosity
        self.failfast = failfast
        self.keepdb = keepdb
        self.pdb = pdb
        self.mark = mark

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument(
            "--keepdb", action="store_true", help="Preserves the test DB between runs."
        )
        parser.add_argument(
            "-m",
            "--mark",
            dest="mark",
            help=(
                "Only run tests matching given mark expression. "
                'For example: --mark "mark1 and not mark2".'
            ),
        )
        parser.add_argument(
            "--pdb",
            action="store_true",
            help="Runs a debugger (pdb, or ipdb if installed) on error or failure.",
        )

    def run_tests(self, test_labels):
        """Apply some parameter translation and invoke pytest."""
        import pytest

        argv = []

        if self.verbosity == 0:
            argv.append("--quiet")
        if self.verbosity == 2:  # noqa: PLR2004
            argv.append("--verbose")
        if self.verbosity == 3:  # noqa: PLR2004
            argv.append("-vv")
        if self.failfast:
            argv.append("--exitfirst")
        if self.keepdb:
            argv.append("--reuse-db")
        if self.pdb:
            argv.append("--pdb")
        if self.mark:
            argv.append("-m")
            argv.append(self.mark)

        argv.extend(test_labels)
        return pytest.main(argv)
