from importlib.metadata import version, PackageNotFoundError


# From: https://setuptools-scm.readthedocs.io/en/latest/usage/#version-at-runtime
try:
    __version__ = version("loop-python")
except PackageNotFoundError:
    pass  # package is not installed


from .core import Loop, loop_over, loop_range
