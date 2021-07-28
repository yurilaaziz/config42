import os

from setuptools import setup, find_packages

try:
    here = os.path.abspath(os.path.dirname(__file__))
    README = open(os.path.join(here, "README.md")).read()
    with open(os.path.join(here, "requirements/base.txt")) as f:
        required = [
            l.strip("\n") for l in f if l.strip("\n") and not l.startswith("#")
        ]
except IOError:
    required = []
    README = ""

setup(
    name="config42",
    packages=find_packages(),
    version="0.4.5",
    license="GPLv3+",
    description=
    "Configuration manager for cloud native application, support configuration "
    " stored in memory, in files, in databases",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Amine Ben Asker",
    author_email="ben.asker.amine@gmail.com",
    url="https://github.com/yurilaaziz/config42",
    download_url="https://github.com/yurilaaziz/config42/releases/tag/0.2",
    keywords=
    "Pretty configuration manager, Key value data store, cloud native configuration",
    install_requires=required,
    entry_points={"console_scripts": ["config42 = config42.__main__:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
