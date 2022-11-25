from setuptools import find_packages, setup


def read(filename: str) -> list[str]:
    return [req.strip() for req in open(filename).readlines()]


setup(
    name="skel",
    version="0.2.0",
    description="skel-description",
    packages=find_packages(where="app"),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    extras_require={"dev": read("requirements-dev.txt")},
)
