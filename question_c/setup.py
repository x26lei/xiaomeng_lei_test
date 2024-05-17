from setuptools import setup, find_packages

setup(
    name='geo_distributed_cache',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [],
    },
    author='Xiaomeng Lei',
    author_email='xmlei001@gmail.com',
    description='A geographically distributed caching library with LRU eviction and TTL expiration mechanisms',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/x26lei/xiaomeng_lei_test/tree/main/question_c',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
