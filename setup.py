# setup.py
from setuptools import setup, find_packages

setup(
    name="snail-unrolling",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'snail-unroll = cli:main',
        ]
    },
)

