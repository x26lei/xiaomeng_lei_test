# setup.py
from setuptools import setup, find_packages

setup(
    name='version_compare',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [],
    },
    author='Xiaomeng Lei',
    author_email='xmlei001@gmail.com',
    description='A library to compare version strings',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/x26lei/tree/main/question_b',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
