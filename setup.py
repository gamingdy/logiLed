import os
from setuptools import setup

setup(
    name="logipy",
    version="1.3.1",
    author="Gamingdy",
    description=("A simple python wrapper for Logitech G's LED"),
    long_description=open("README.rst").read(),
    keywords=[
        "logi",
        "logipy",
        "Logitech",
        "LogitechG",
        "LED",
        "LGS",
        "Logitech Gaming Software",
    ],
    url="https://github.com/gamingdy/logiPy",
    download_url="https://github.com/gamingdy/logiPy",
    packages=["logipy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
)
