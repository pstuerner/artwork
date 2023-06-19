from setuptools import setup, find_packages

setup(
    name='artwork',
    version='1.0.0',
    author='Philipp Stuerner',
    description='Create an artwork a day using gpt3.5 and lexica.art',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "artwork = artwork.__main__:main",
        ],
    },
)