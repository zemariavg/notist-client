from setuptools import setup, find_packages

setup(
    name="cryptolib",
    version="0.1.0",
    description="A cryptography library for the Notist project",
    packages=find_packages(),
    install_requires=[
        "cryptography >= 3.4.7",
    ],
    python_requires=">=3.6",
)
