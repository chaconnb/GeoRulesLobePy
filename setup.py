from setuptools import find_packages, setup

PACKAGE_NAME = "georules"
PACKAGE_DIRS = [PACKAGE_NAME]
VERSION = None
# RUNTIME_DEPS = None


def main():
    """Run setup."""
    print("\nRunning `setup.py`...")
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        # install_requires=RUNTIME_DEPS,
        packages=find_packages(where=PACKAGE_DIRS),
    )


if __name__ == "__main__":
    main()