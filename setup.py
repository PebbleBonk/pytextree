import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
with (HERE/"README.md").open(encoding='utf-8') as f:
    README = f.read()

# This call to setup() does all the work
setup(
    name="pytextree",
    version="0.1.1",
    description="Create a tree object from a LaTeX project",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/PebbleBonk/pytextree",
    author="Olli Riikonen",
    author_email="pebblebonk@gmail.com",
    license="MIT",
    python_requires=">=3.7.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pytextree"],
    include_package_data=True,
    install_requires=[
        "anytree==2.8.0",
        "numpy==1.22.0",
        "six==1.14.0",
    ],
)