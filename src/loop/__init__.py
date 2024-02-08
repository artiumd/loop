from importlib.metadata import version, PackageNotFoundError


# From: https://setuptools-scm.readthedocs.io/en/latest/usage/#version-at-runtime
try:
    __version__ = version("package-name")
except PackageNotFoundError:
    pass  # package is not installed


from .core import Loop, loop_over
