from setuptools import setup, find_packages

with open('./requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="drag-racing",
    platforms="all",
    packages=find_packages(exclude=["tests"]),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'drag-racing = project.main:main'
        ]
    },
)
