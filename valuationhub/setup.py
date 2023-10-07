from setuptools import find_packages, setup

setup(
    name="valuationhub",
    packages=find_packages(exclude=["valuationhub_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
