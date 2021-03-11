#!/usr/bin/env python3

import setuptools
import grade50

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grade50",
    version=grade50.__version__,
    author="Patrick Totzke",
    author_email="patricktotzke@gmail.com",
    description=grade50.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pazz/grade50",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Jinja2>=2.10.1',
    ],
    entry_points={
        'console_scripts':
            ['grade50 = grade50.main:main'],
    },
    package_data={'grade50': ['templates/*.jinja2']},
)
