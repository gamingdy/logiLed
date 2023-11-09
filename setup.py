from setuptools import setup

setup(
    name="logiled",
    version="2023.11.9",
    author="Gamingdy",
    description="A simple python wrapper for Logitech G's LED",
    long_description=open("README.rst").read(),
    keywords=[
        "logi",
        "logiled",
        "Logitech",
        "LogitechG",
        "LED",
        "LGS",
        "Logitech Gaming Software",
    ],
    url="https://github.com/gamingdy/logiLed",
    download_url="https://github.com/gamingdy/logiLed",
    packages=["logiled"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
)
